"""Optional local engine contracts; no implicit setup, credentials or downloads."""
import contextlib
import io
import json
import os
import re
import sys
import urllib.parse
import urllib.request
import wave
import xml.etree.ElementTree as ET

from adapter_io import integer, number, source, installed_path, process, runtime, write_json


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError('Engine redirects are disabled')


def endpoint(value, allow_remote=False):
    parsed = urllib.parse.urlsplit(value)
    if not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment or parsed.path not in ('', '/'):
        raise ValueError('Endpoint must be an origin without credentials or path')
    local = parsed.hostname in ('localhost', '127.0.0.1', '::1')
    if parsed.scheme not in ('http', 'https') or (not local and (not allow_remote or parsed.scheme != 'https')):
        raise ValueError('Use loopback or explicitly authorized remote HTTPS')
    return value.rstrip('/')


def ace_request(origin, path, payload=None, binary=False):
    parsed = urllib.parse.urlsplit(path)
    if parsed.scheme or parsed.netloc or not path.startswith('/') or path.startswith('//'):
        raise ValueError('Engine returned a cross-origin URL')
    headers = {}
    token = os.environ.get('ACESTEP_API_KEY')
    if token:
        headers['Authorization'] = 'Bearer ' + token
    data = None if payload is None else json.dumps(payload).encode('utf-8')
    if data is not None:
        headers['Content-Type'] = 'application/json'
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
    with opener.open(urllib.request.Request(origin + path, data=data, headers=headers), timeout=30) as response:
        limit = 100_000_000 if binary else 2_000_000
        raw = response.read(limit + 1)
    if len(raw) > limit:
        raise ValueError('Engine response exceeds budget')
    if binary:
        return raw
    result = json.loads(raw)
    if result.get('code') != 200 or result.get('error'):
        raise ValueError('ACE-Step rejected the request')
    return result['data']


def ace_submit(root, job, out):
    origin = endpoint(job['endpoint'], job.get('allow_remote', False))
    params = job['parameters']
    allowed = {'prompt', 'lyrics', 'thinking', 'vocal_language', 'sample_query', 'use_format',
               'model', 'bpm', 'key_scale', 'time_signature', 'audio_duration', 'inference_steps',
               'seed', 'use_random_seed', 'batch_size'}
    if not isinstance(params, dict) or set(params) - allowed:
        raise ValueError('Unsupported ACE-Step parameter; use the documented text-to-music contract')
    if not params.get('prompt') and not params.get('sample_query'):
        raise ValueError('Music generation needs a prompt or sample_query')
    number(params.get('audio_duration', 30), 10, 600)
    integer(params.get('batch_size', 1), 1, 8)
    integer(params.get('inference_steps', 8), 1, 200)
    number(params.get('bpm', 120), 30, 300)
    data = dict(params, audio_format='wav')
    data.setdefault('audio_duration', 30)
    data.setdefault('batch_size', 1)
    result = ace_request(origin, '/release_task', data)
    ident = result['task_id']
    if not isinstance(ident, str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,100}', ident):
        raise ValueError('Invalid task receipt')
    write_json(out / 'task.json', {'endpoint': origin, 'task_id': ident})
    return {'submitted': True, 'task_id': ident, 'complete': False,
            'next': 'Use ace-fetch with task.json; never resubmit to poll'}


def ace_fetch(root, job, out):
    receipt = json.loads(runtime.read_limited(source(root, job['input'])))
    origin = endpoint(receipt['endpoint'], job.get('allow_remote', False))
    result = ace_request(origin, '/query_result', {'task_id_list': [receipt['task_id']]})
    matching = [r for r in result if r.get('task_id') == receipt['task_id']]
    if len(matching) != 1:
        raise ValueError('Task status response does not match the receipt')
    status = matching[0]['status']
    if status == 0:
        write_json(out / 'status.json', {'complete': False, 'task_id': receipt['task_id']})
        return {'complete': False, 'resubmit': False}
    if status != 1:
        raise ValueError('ACE-Step task failed')
    files = matching[0]['result']
    files = json.loads(files) if isinstance(files, str) else files
    if not isinstance(files, list) or not 1 <= len(files) <= 8:
        raise ValueError('Unexpected music result count')
    for index, item in enumerate(files):
        url = item['file']
        if urllib.parse.urlsplit(url).path != '/v1/audio':
            raise ValueError('Unexpected audio download route')
        raw = ace_request(origin, url, binary=True)
        if not (raw[:4] == b'RIFF' and raw[8:12] == b'WAVE'):
            raise ValueError('Engine did not return WAV bytes')
        with wave.open(io.BytesIO(raw)) as audio:
            if audio.getnframes() == 0 or audio.getframerate() <= 0:
                raise ValueError('Empty audio result')
            duration = audio.getnframes() / audio.getframerate()
            if duration > 610:
                raise ValueError('Audio duration exceeds request budget')
        (out / f'audio-{index + 1}.wav').write_bytes(raw)
    return {'complete': True, 'audio_files': len(files)}


def privacy_tokens(text, spans):
    if re.search(r'\[PRIVATE_[A-Z_]+_\d+\]', text):
        raise ValueError('Input contains reserved placeholders; choose a separate document')
    mapping, reuse = {}, {}
    counts: dict[str, int] = {}
    pieces: list[str] = []
    cursor = 0
    for span in sorted(spans, key=lambda s: s.start):
        if not 0 <= cursor <= span.start < span.end <= len(text) or text[span.start:span.end] != span.text:
            raise ValueError('Privacy spans overlap or do not match the original text')
        label = span.label.upper().removeprefix('PRIVATE_')
        if not re.fullmatch(r'[A-Z_]{1,40}', label):
            raise ValueError('Unexpected privacy label')
        key = (label, span.text)
        if key not in reuse:
            counts[label] = counts.get(label, 0) + 1
            token = f'[PRIVATE_{label}_{counts[label]}]'
            reuse[key] = token
            mapping[token] = span.text
        pieces.extend((text[cursor:span.start], reuse[key]))
        cursor = span.end
    pieces.append(text[cursor:])
    return ''.join(pieces), mapping


def privacy(root, job, out):
    text = runtime.read_limited(source(root, job['input'])).decode('utf-8')
    if len(text) > 1_000_000:
        raise ValueError('Privacy document exceeds character budget')
    if job['operation'] == 'privacy-restore':
        mapping = json.loads(runtime.read_limited(source(root, job['map'])))['placeholders']
        if not isinstance(mapping, dict) or not all(
                re.fullmatch(r'\[PRIVATE_[A-Z_]+_\d+\]', k) and isinstance(v, str) for k,v in mapping.items()):
            raise ValueError('Invalid local restore map')
        tokens = set(re.findall(r'\[PRIVATE_[A-Z_]+_\d+\]', text))
        if tokens - mapping.keys():
            raise ValueError('Response contains unknown placeholders')
        result = re.sub(r'\[PRIVATE_[A-Z_]+_\d+\]', lambda m: mapping[m.group(0)], text)
        (out / 'restored.txt').write_bytes(result.encode('utf-8'))
        return {'restored': True, 'contains_private_data': True}
    checkpoint = installed_path(job['checkpoint'], directory=True)
    device = job.get('device', 'cpu')
    if device not in ('cpu', 'cuda'):
        raise ValueError('Select cpu or cuda explicitly')
    os.environ.setdefault('HF_HUB_OFFLINE', '1')
    if sys.platform == 'win32':
        os.environ.setdefault('OPF_MOE_TRITON', '0')
    with open(os.devnull, 'w') as sink, contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
        from opf import OPF
        model = OPF(model=str(checkpoint), device=device, output_mode='typed', decode_mode='viterbi')
        result = model.redact(text)
    if result.warning or result.text != text:
        raise ValueError('Tokenizer changed input; reversible redaction refused')
    clean, mapping = privacy_tokens(text, result.detected_spans)
    private = out / 'private'
    private.mkdir(mode=0o700)
    (private / '.gitignore').write_text('*\n', encoding='utf-8')
    write_json(private / 'restore-map.json', {'schema': 1, 'placeholders': mapping})
    os.chmod(private / 'restore-map.json', 0o600)
    (out / 'redacted.txt').write_bytes(clean.encode('utf-8'))
    return {'detected_values': len(mapping), 'human_review_required': True,
            'upload_only_after_review': 'redacted.txt', 'private_map': 'private/restore-map.json'}


def banana(root, job, out):
    if job.get('engine_config_reviewed') is not True:
        raise ValueError('Review the engine configuration, model setup and external providers first')
    engine = installed_path(job['engine'], directory=True)
    python = installed_path(job['python'])
    main = installed_path(engine / 'main.py')
    installed_path(engine / 'config/config.yaml')
    image = source(root, job['input'])
    from media_adapter import load_image
    load_image(image)
    process([python, '-B', main, '-i', image, '-o', out], cwd=engine, timeout=1800)
    drawings = list(out.rglob('*.drawio')) + list(out.rglob('*.xml'))
    valid, text_layer = [], False
    for path in drawings:
        raw = runtime.read_limited(path)
        if b'<!DOCTYPE' in raw.upper() or b'<!ENTITY' in raw.upper():
            raise ValueError('Unexpected XML declarations')
        xml = ET.fromstring(raw)
        cells = list(xml.iter('mxCell'))
        if len(cells) > 2:
            valid.append(path.relative_to(out).as_posix())
        if 'text' in path.stem and any(c.get('value') for c in cells):
            text_layer = True
    if not valid or (job.get('require_text', True) and not text_layer):
        raise ValueError('Engine produced no editable diagram or omitted required OCR text')
    return {'editable_drawings': valid, 'text_layer': text_layer, 'visual_review_required': True}


def cad_entities(document, items, point):
    msp = document.ModelSpace
    if not isinstance(items, list) or not 1 <= len(items) <= 1000:
        raise ValueError('CAD entity list must contain 1..1000 items')
    created = []
    def pos(values):
        if len(values) != 3:
            raise ValueError('CAD points need x, y, z')
        return point([number(v, -1e9, 1e9) for v in values])
    for item in items:
        kind = item['type']
        if kind == 'line':
            entity = msp.AddLine(pos(item['start']), pos(item['end']))
        elif kind == 'circle':
            entity = msp.AddCircle(pos(item['center']), number(item['radius'], 1e-9, 1e9))
        elif kind == 'arc':
            entity = msp.AddArc(pos(item['center']), number(item['radius'], 1e-9, 1e9),
                                number(item['start_angle'], -100, 100), number(item['end_angle'], -100, 100))
        elif kind == 'text':
            entity = msp.AddText(str(item['text'])[:10000], pos(item['point']), number(item['height'], 1e-9, 1e9))
        elif kind == 'box':
            entity = msp.AddBox(pos(item['center']), *[number(item[k], 1e-9, 1e9) for k in ('length', 'width', 'height')])
        elif kind == 'cylinder':
            entity = msp.AddCylinder(pos(item['center']), number(item['radius'], 1e-9, 1e9), number(item['height'], 1e-9, 1e9))
        elif kind == 'dimension':
            entity = msp.AddDimAligned(pos(item['start']), pos(item['end']), pos(item['location']))
            entity.ScaleFactor = number(item.get('scale', 1), 1e-6, 1e6)
        else:
            raise ValueError('Unsupported CAD entity type')
        created.append({'type': kind, 'handle': str(entity.Handle)})
    document.Regen(1)
    if int(msp.Count) != len(created):
        raise ValueError('CAD entity readback count differs from the requested drawing')
    return created


def cad(root, job, out):
    if sys.platform != 'win32':
        raise ValueError('CAD COM requires Windows and an already running compatible application')
    import pythoncom
    import win32com.client
    progid = job.get('progid', 'AutoCAD.Application')
    if not re.fullmatch(r'(AutoCAD\.Application|GstarCAD\.Application|ZWCAD\.Application|BricscadApp\.AcadApplication|nanoCAD\.Application)(\.\d+)?', progid):
        raise ValueError('Unsupported CAD ProgID')
    pythoncom.CoInitialize()
    try:
        app = win32com.client.GetActiveObject(progid)
        if job['operation'] == 'cad-inspect':
            return {'running': True, 'open_documents': int(app.Documents.Count)}
        document = app.Documents.Add()
        try:
            document.SetVariable('INSUNITS', integer(job['units'], 0, 24))
            entities = cad_entities(document, job['entities'],
                                    lambda values: win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, values))
            document.SaveAs(str(out / 'drawing.dwg'))
            if not (out / 'drawing.dwg').is_file():
                raise ValueError('CAD did not save the requested drawing')
            write_json(out / 'entities.json', entities)
        finally:
            document.Close(False)
        return {'entities': len(entities), 'saved': True, 'visual_review_required': True}
    finally:
        pythoncom.CoUninitialize()


OPERATIONS = {'ace-submit': ace_submit, 'ace-fetch': ace_fetch, 'privacy-redact': privacy,
              'privacy-restore': privacy, 'edit-banana': banana, 'cad-inspect': cad, 'cad-create': cad}
