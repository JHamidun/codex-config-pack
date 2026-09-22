import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('planning', REPO / 'scripts/planning.py')
planning = importlib.util.module_from_spec(spec)
spec.loader.exec_module(planning)


class PlanningTests(unittest.TestCase):
    def test_initialization_retries_transient_directory_lock(self):
        original = Path.rename
        attempts = []

        def rename(path, target):
            attempts.append(target)
            if len(attempts) == 1:
                raise PermissionError('Transient directory lock')
            return original(path, target)

        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / 'brief.md').write_text('# Demo', encoding='utf-8')
            with patch.object(Path, 'rename', rename):
                planning.initialize(root, 'brief.md')
            self.assertGreaterEqual(len(attempts), 2)
            self.assertTrue((root / '.planning/PROJECT.md').is_file())
            self.assertEqual(list(root.glob('.planning-init-*')), [])

    def test_initialization_does_not_hide_permanent_denial(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / 'brief.md').write_text('# Demo', encoding='utf-8')
            with patch.object(Path, 'rename', side_effect=PermissionError('Denied')):
                with self.assertRaises(PermissionError):
                    planning.initialize(root, 'brief.md')
            self.assertFalse((root / '.planning').exists())
            self.assertEqual(list(root.glob('.planning-init-*')), [])

    def test_missing_project_is_not_initialized_by_inspection(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            result = planning.inspect(root)
            self.assertFalse(result['initialized'])
            self.assertEqual(list(root.iterdir()), [])

    def test_initialize_preserves_spec_and_can_resume_without_provider(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            specfile = root / 'brief.md'
            specfile.write_text('# Demo\n\nBuild a local task list.\n', encoding='utf-8')
            planning.initialize(root, 'brief.md')
            self.assertEqual((root / '.planning/PROJECT.md').read_text(encoding='utf-8'), specfile.read_text(encoding='utf-8'))
            result = planning.inspect(root)
            self.assertTrue(result['initialized'])
            self.assertFalse(result['ready_to_execute'])
            self.assertIn('REQUIREMENTS.md', result['missing'])
            with self.assertRaises(ValueError):
                planning.initialize(root, 'brief.md')

    def test_plan_summary_is_not_proof_of_verification(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            planningdir = root / '.planning'
            phase = planningdir / 'phases/01-local'
            phase.mkdir(parents=True)
            for filename in ('PROJECT.md', 'REQUIREMENTS.md', 'ROADMAP.md', 'STATE.md'):
                (planningdir / filename).write_text('# Draft', encoding='utf-8')
            (phase / '01-01-PLAN.md').write_text('---\nphase: 01-local\nplan: 01\n---\n<tasks>Implement</tasks>', encoding='utf-8')
            (phase / '01-01-SUMMARY.md').write_text('# Claimed done', encoding='utf-8')
            report = planning.inspect(root)
            self.assertEqual(report['phases'][0]['plan_count'], 1)
            self.assertEqual(report['phases'][0]['summary_count'], 1)
            self.assertFalse(report['phases'][0]['verified'])
            self.assertFalse(report['ready_to_execute'])

    def test_checkpoint_is_explicit_and_unique(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / 'note.md').write_text('Next: reproduce the parser failure.', encoding='utf-8')
            planningdir = root / '.planning'
            planningdir.mkdir()
            first = planning.checkpoint(root, 'note.md')
            second = planning.checkpoint(root, 'note.md')
            self.assertNotEqual(first['path'], second['path'])
            self.assertTrue((root / first['path']).is_file())
            self.assertEqual(len(planning.inspect(root)['checkpoints']), 2)

    def test_rejects_escape_private_source_and_links(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            for source in ('../outside.md', '.claude/notes.md', '.env', 'nested/.brain/key.md'):
                with self.subTest(source=source), self.assertRaises(ValueError):
                    planning.initialize(root, source)
            (root / 'note.md').write_text('safe')
            outside = root / 'outside'
            outside.mkdir()
            try:
                (root / '.planning').symlink_to(outside, target_is_directory=True)
            except OSError:
                return
            with self.assertRaises(ValueError):
                planning.inspect(root)

    def test_limit_and_config_models_are_not_silently_changed(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / '.planning').mkdir()
            config = root / '.planning/config.json'
            raw = json.dumps({'model_profile': 'custom', 'parallelization': False})
            config.write_text(raw)
            planning.inspect(root)
            self.assertEqual(config.read_text(), raw)


if __name__ == '__main__':
    unittest.main()
