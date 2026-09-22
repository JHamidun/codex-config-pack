import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import wave

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / 'scripts'))
import optional_adapter as adapter
import engine_adapter as engines
import media_adapter as media
from adapter_io import installed_path, staged_output, runtime
try:
    from PIL import Image, ImageDraw
except ImportError:
    Image = None


class AdapterTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def run_job(self, operation, **kwargs):
        return adapter.execute(self.root, dict(operation=operation, output='result', **kwargs))

    def test_check_does_not_import_connect_install_or_create_files(self):
        before = list(self.root.iterdir())
        with patch.object(engines, 'ace_request') as request, patch.object(subprocess, 'run') as process:
            for operation in adapter.DEPENDENCIES:
                result = adapter.check(operation)
                self.assertFalse(result['engine_live_tested'])
            request.assert_not_called()
            process.assert_not_called()
        self.assertEqual(list(self.root.iterdir()), before)

    def test_path_escape_and_existing_output_are_rejected(self):
        for name in ['../escape', '.claude/out', '.agents/out', 'C:/absolute', 'bad\\path']:
            with self.subTest(name=name), self.assertRaises(ValueError):
                with staged_output(self.root, name):
                    self.fail('Must reject before yielding')
        (self.root / 'result').mkdir()
        (self.root / 'result/valuable').write_text('keep')
        with self.assertRaises(ValueError):
            with staged_output(self.root, 'result'):
                pass
        self.assertEqual((self.root / 'result/valuable').read_text(), 'keep')

    def test_failed_job_commits_no_output(self):
        with self.assertRaises(ValueError):
            with staged_output(self.root, 'failed') as out:
                (out / 'partial').write_text('partial')
                raise ValueError('synthetic')
        self.assertEqual(list(self.root.iterdir()), [])

    def test_cli_does_not_leak_exception_or_document_content(self):
        (self.root / 'input.txt').write_text('SYNTHETIC_PRIVATE_PAYLOAD')
        (self.root / 'job.json').write_text(json.dumps({'operation': 'ocr-restore', 'input': 'input.txt',
           'output': 'result', 'corrections': [{'old': 'SYNTHETIC_PRIVATE_PAYLOAD', 'new': 'x', 'count': 2}]}))
        process = subprocess.run([sys.executable, '-B', str(REPO / 'scripts/optional_adapter.py'),
                  'run', '--workspace', str(self.root), '--request', 'job.json'], capture_output=True)
        self.assertEqual(process.returncode, 2)
        self.assertNotIn(b'SYNTHETIC_PRIVATE_PAYLOAD', process.stdout + process.stderr)
        self.assertFalse((self.root / 'result').exists())

    def test_ocr_conservative_cleanup_and_explicit_correction(self):
        (self.root / 'ocr.txt').write_bytes('one\u00ad\x00 two\nthree'.encode())
        result = self.run_job('ocr-restore', input='ocr.txt', corrections=[{'old': 'two', 'new': 'TWO'}])
        self.assertEqual((self.root / 'result/restored.txt').read_bytes(), b'one TWO\nthree')
        self.assertFalse(result['result']['factual_accuracy_verified'])
        self.assertIn('restored.txt', [f['file'] for f in result['artifacts']])

    def test_ocr_correction_count_prevents_global_unreviewed_replacement(self):
        (self.root / 'ocr.txt').write_text('same same')
        with self.assertRaises(ValueError):
            self.run_job('ocr-restore', input='ocr.txt', corrections=[{'old': 'same', 'new': 'X'}])
        self.assertFalse((self.root / 'result').exists())

    def test_privacy_tokens_preserve_coreference_and_roundtrip_unicode(self):
        text = 'Zoë, Zoë.'
        spans = [SimpleNamespace(start=0, end=3, label='private_person', text='Zoë'),
                 SimpleNamespace(start=5, end=8, label='private_person', text='Zoë')]
        clean, mapping = engines.privacy_tokens(text, spans)
        self.assertEqual(clean, '[PRIVATE_PERSON_1], [PRIVATE_PERSON_1].')
        (self.root / 'clean.txt').write_bytes(clean.encode())
        (self.root / 'map.json').write_text(json.dumps({'placeholders': mapping}))
        self.run_job('privacy-restore', input='clean.txt', map='map.json')
        self.assertEqual((self.root / 'result/restored.txt').read_bytes(), text.encode())

    def test_privacy_invalid_offsets_collision_and_overlap_fail_closed(self):
        cases = [('text', [SimpleNamespace(start=0, end=4, text='wrong', label='private_person')]),
                 ('[PRIVATE_PERSON_1]', []),
                 ('abc', [SimpleNamespace(start=0, end=2, text='ab', label='private_person'),
                          SimpleNamespace(start=1, end=3, text='bc', label='private_person')])]
        for text, spans in cases:
            with self.subTest(text=text), self.assertRaises(ValueError):
                engines.privacy_tokens(text, spans)

    def test_privacy_opf_contract_uses_explicit_model_and_private_map(self):
        (self.root / 'model').mkdir()
        (self.root / 'doc.txt').write_text('Alice!', encoding='utf-8')
        redaction = SimpleNamespace(text='Alice!', warning=None, detected_spans=[
            SimpleNamespace(start=0, end=5, text='Alice', label='private_person')])
        model = unittest.mock.Mock()
        model.return_value.redact.return_value = redaction
        with patch.dict(sys.modules, {'opf': SimpleNamespace(OPF=model)}), \
             patch.object(adapter, 'check', return_value={'modules': {'opf': True}}):
            result = self.run_job('privacy-redact', input='doc.txt', checkpoint=str(self.root / 'model'))
        self.assertEqual(model.call_args.kwargs['model'], str(self.root / 'model'))
        self.assertEqual((self.root / 'result/redacted.txt').read_text(), '[PRIVATE_PERSON_1]!')
        self.assertTrue((self.root / 'result/private/.gitignore').exists())
        self.assertNotIn('Alice', json.dumps(result))

    def test_privacy_tokenizer_mismatch_does_not_emit_unsafe_result(self):
        (self.root / 'model').mkdir()
        (self.root / 'doc.txt').write_text('one')
        model = unittest.mock.Mock()
        model.return_value.redact.return_value = SimpleNamespace(text='different', warning='mismatch')
        with patch.dict(sys.modules, {'opf': SimpleNamespace(OPF=model)}), \
             patch.object(adapter, 'check', return_value={'modules': {'opf': True}}), self.assertRaises(ValueError):
            self.run_job('privacy-redact', input='doc.txt', checkpoint=str(self.root / 'model'))
        self.assertFalse((self.root / 'result').exists())

    def test_ace_rejects_credentials_cross_origin_and_implicit_remote(self):
        for url in ['https://user:pass@example.com', 'http://example.com', 'https://example.com',
                    'http://localhost:8001/path', 'file:///tmp']:
            with self.subTest(url=url), self.assertRaises(ValueError):
                engines.endpoint(url)
        self.assertEqual(engines.endpoint('https://example.com', True), 'https://example.com')
        with self.assertRaises(ValueError):
            engines.ace_request('http://localhost:8001', '//example.com/file')

    def test_ace_submit_receipt_is_resumable_without_storing_prompt(self):
        with patch.object(engines, 'ace_request', return_value={'task_id': 'synthetic-job'}) as request:
            result = self.run_job('ace-submit', endpoint='http://localhost:8001', parameters={'prompt': 'SYNTHETIC_PROMPT'})
        self.assertFalse(result['result']['complete'])
        self.assertEqual(request.call_args.args[2]['audio_format'], 'wav')
        self.assertNotIn('SYNTHETIC_PROMPT', (self.root / 'result/task.json').read_text())

    def test_ace_poll_pending_never_submits_again(self):
        (self.root / 'task.json').write_text(json.dumps({'endpoint': 'http://localhost:8001', 'task_id': 'job'}))
        with patch.object(engines, 'ace_request', return_value=[{'task_id': 'job', 'status': 0}]) as request:
            result = self.run_job('ace-fetch', input='task.json')
        self.assertFalse(result['result']['complete'])
        self.assertEqual(request.call_args.args[1], '/query_result')
        self.assertEqual(request.call_count, 1)

    def test_ace_completed_download_validates_actual_wav_bytes(self):
        data = io.BytesIO()
        with wave.open(data, 'wb') as audio:
            audio.setparams((1, 2, 8000, 0, 'NONE', 'not compressed'))
            audio.writeframes(b'\x00\x00' * 800)
        (self.root / 'task.json').write_text(json.dumps({'endpoint': 'http://localhost:8001', 'task_id': 'job'}))
        status = [{'task_id': 'job', 'status': 1, 'result': json.dumps([{'file': '/v1/audio?path=example.wav'}])}]
        with patch.object(engines, 'ace_request', side_effect=[status, data.getvalue()]):
            self.run_job('ace-fetch', input='task.json')
        self.assertEqual((self.root / 'result/audio-1.wav').read_bytes(), data.getvalue())

    def test_cad_contract_uses_geometry_and_entity_readback(self):
        msp = unittest.mock.Mock()
        msp.Count = 2
        msp.AddLine.return_value.Handle = '1'
        msp.AddDimAligned.return_value.Handle = '2'
        document = SimpleNamespace(ModelSpace=msp, Regen=unittest.mock.Mock())
        result = engines.cad_entities(document, [
            {'type': 'line', 'start': [0, 0, 0], 'end': [10, 0, 0]},
            {'type': 'dimension', 'start': [0, 0, 0], 'end': [10, 0, 0], 'location': [0, 2, 0], 'scale': 5}], tuple)
        self.assertEqual(len(result), 2)
        self.assertEqual(msp.AddDimAligned.return_value.ScaleFactor, 5)
        msp.AddLine.assert_called_once_with((0, 0, 0), (10, 0, 0))
        document.Regen.assert_called_once_with(1)


@unittest.skipIf(Image is None, 'Install requirements-test-media.txt for artifact tests')
class MediaTests(unittest.TestCase):
    setUp = AdapterTests.setUp
    tearDown = AdapterTests.tearDown
    run_job = AdapterTests.run_job
    def picture(self, name, offset=0):
        image = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
        ImageDraw.Draw(image).rectangle((12 + offset, 12, 40 + offset, 40), fill=(255, 30, 20, 255))
        image.save(self.root / name)

    def test_web_icons_and_ico_have_real_dimensions_and_magic(self):
        self.picture('logo.png')
        self.run_job('web-assets', input='logo.png', social_input='logo.png')
        for path in (self.root / 'result').glob('icon-*.png'):
            size = int(path.stem.split('-')[1].split('x')[0])
            with Image.open(path) as result:
                self.assertEqual(result.size, (size, size))
                self.assertEqual(result.format, 'PNG')
        with Image.open(self.root / 'result/favicon.ico') as ico:
            self.assertEqual(ico.ico.sizes(), {(16, 16), (32, 32)})
        with Image.open(self.root / 'result/og-image.png') as result:
            self.assertEqual(result.size, (1200, 630))

    def test_enhance_deterministically_preserves_alpha(self):
        self.picture('in.png')
        self.run_job('enhance', input='in.png', scale=2, contrast=1.1)
        with Image.open(self.root / 'result/image.png') as image:
            self.assertEqual(image.size, (128, 128))
            self.assertEqual(image.getchannel('A').getextrema(), (0, 255))

    def test_gif_has_multiple_frames_correct_timing_and_limit(self):
        self.picture('a.png')
        self.picture('b.png', 8)
        self.run_job('gif', frames=['a.png', 'b.png'], fps=10)
        path = self.root / 'result/animation.gif'
        with Image.open(path) as gif:
            self.assertEqual(gif.n_frames, 2)
            self.assertEqual(gif.info['duration'], 100)
            self.assertEqual(gif.info['loop'], 0)
        self.assertLess(path.stat().st_size, 65536)

    def test_sticker_static_requires_transparency(self):
        Image.new('RGB', (64, 64), 'red').save(self.root / 'opaque.png')
        with self.assertRaises(ValueError):
            self.run_job('sticker-static', input='opaque.png')

    def test_sticker_static_has_valid_webp_and_dimensions(self):
        self.picture('sticker.png')
        self.run_job('sticker-static', input='sticker.png')
        with Image.open(self.root / 'result/sticker.webp') as image:
            self.assertEqual(image.size, (512, 512))
            self.assertEqual(image.format, 'WEBP')
            self.assertEqual(image.getchannel('A').getextrema(), (0, 255))

    @unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'), 'Optional FFmpeg live artifact test')
    def test_video_alpha_survives_real_encode_decode(self):
        self.picture('a.png')
        self.picture('b.png', 8)
        result = self.run_job('sticker-video', frames=['a.png', 'b.png'], fps=10,
              ffmpeg=str(Path(shutil.which('ffmpeg')).resolve()), ffprobe=str(Path(shutil.which('ffprobe')).resolve()))
        self.assertTrue(result['result']['alpha_decode_verified'])
        self.assertLess((self.root / 'result/sticker.webm').stat().st_size, 262144)

    def test_banana_requires_actual_editable_xml_and_text(self):
        self.picture('input.png')
        engine = self.root / 'engine'
        (engine / 'config').mkdir(parents=True)
        (engine / 'config/config.yaml').write_text('synthetic: true')
        (engine / 'main.py').write_text('pass')
        def fake_process(argv, **kwargs):
            output = Path(argv[-1]) / 'input'
            output.mkdir()
            (output / 'text_only.drawio').write_text('<mxGraphModel><root><mxCell/><mxCell/>'
                '<mxCell value="Synthetic text"/></root></mxGraphModel>')
        with patch.object(engines, 'process', side_effect=fake_process) as run:
            result = self.run_job('edit-banana', input='input.png', engine=str(engine),
                                 python=str(Path(sys.executable).resolve()), engine_config_reviewed=True)
        self.assertTrue(result['result']['text_layer'])
        self.assertEqual(run.call_args.args[0][-2], '-o')

    def test_banana_success_exit_without_artifacts_is_failure(self):
        self.picture('input.png')
        engine = self.root / 'engine'
        (engine / 'config').mkdir(parents=True)
        (engine / 'config/config.yaml').write_text('synthetic: true')
        (engine / 'main.py').write_text('pass')
        with patch.object(engines, 'process'), self.assertRaises(ValueError):
            self.run_job('edit-banana', input='input.png', engine=str(engine),
                         python=str(Path(sys.executable).resolve()), engine_config_reviewed=True)
        self.assertFalse((self.root / 'result').exists())

    def test_segmentation_uses_explicit_custom_model_without_fallback(self):
        self.picture('input.png')
        (self.root / 'weights.onnx').write_bytes(b'synthetic-contract-fixture')
        cut = media.load_image(self.root / 'input.png')
        session = unittest.mock.Mock(return_value='session')
        remove = unittest.mock.Mock(return_value=cut)
        with patch.dict(sys.modules, {'rembg': SimpleNamespace(new_session=session, remove=remove)}), \
             patch.object(adapter, 'check', return_value={'modules': {'rembg': True}}):
            self.run_job('segment', input='input.png', rembg_checkpoint=str(self.root / 'weights.onnx'))
        session.assert_called_once_with('u2net_custom', model_path=str(self.root / 'weights.onnx'),
                                        providers=['CPUExecutionProvider'])
        with Image.open(self.root / 'result/frame-0000.png') as image:
            self.assertEqual(image.getchannel('A').getextrema(), (0, 255))

    def test_union_mask_retains_white_seed_and_flying_colored_prop(self):
        image = Image.new('RGBA', (64, 64), 'white')
        ImageDraw.Draw(image).rectangle((45, 20, 50, 25), fill='red')
        seed = Image.new('L', (64, 64), 0)
        ImageDraw.Draw(seed).rectangle((10, 10, 30, 40), fill=255)
        mask = media.union_mask(image, seed, 215)
        self.assertEqual(mask.getpixel((20, 20)), 255)
        self.assertEqual(mask.getpixel((47, 22)), 255)
        self.assertEqual(mask.getpixel((60, 60)), 0)

    def test_upscale_contract_requires_local_model_and_checks_output_dimensions(self):
        self.picture('input.png')
        models = self.root / 'models'
        models.mkdir()
        for suffix in ('.bin', '.param'):
            (models / ('fixture' + suffix)).write_bytes(b'synthetic')
        def fake_process(argv, **kwargs):
            media.load_image(self.root / 'input.png').resize((128, 128)).save(argv[4])
        with patch.object(media, 'process', side_effect=fake_process) as run:
            self.run_job('upscale', input='input.png', scale=2, model='fixture', models=str(models),
                         executable=str(Path(sys.executable).resolve()))
        self.assertEqual(run.call_args.args[0][3], '-o')
        with Image.open(self.root / 'result/image.png') as image:
            self.assertEqual(image.size, (128, 128))

    def test_tesseract_contract_requires_both_text_and_coordinates(self):
        self.picture('scan.png')
        def fake_process(argv, **kwargs):
            base = Path(argv[2])
            base.with_suffix('.txt').write_text('synthetic')
            base.with_suffix('.tsv').write_text('level\ttext\n1\tsynthetic')
        with patch.object(media, 'process', side_effect=fake_process) as run:
            self.run_job('ocr-extract', input='scan.png', executable=str(Path(sys.executable).resolve()))
        self.assertEqual(run.call_args.args[0][-2:], ['txt', 'tsv'])
        self.assertTrue((self.root / 'result/ocr.tsv').exists())


if __name__ == '__main__':
    unittest.main()
