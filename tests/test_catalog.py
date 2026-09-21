import json
import hashlib
import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('catalog', REPO/'scripts/catalog.py')
catalog = importlib.util.module_from_spec(spec)
spec.loader.exec_module(catalog)


class CatalogTests(unittest.TestCase):
    def fixture(self, root):
        entry = {'id':'skill:skills/demo/SKILL.md', 'name':'demo', 'description':'Artifact snapshots',
                 'path':'library/skills/demo/SKILL.md', 'dependencies':['old-runtime'],
                 'execution': {'mode':'native-helper', 'recipe':'native/recipe.md', 'helper':'scripts/runtime.py',
                               'verification':'offline-integration-tested', 'aliases':['сохрани версию файла']}}
        contents = {'catalog.json': json.dumps({'entries':[entry]}),
                    'native/recipe.md':'Run ${CODEX_PACK_ROOT}/scripts/runtime.py snapshot.',
                    'scripts/runtime.py': (REPO/'scripts/runtime.py').read_text(encoding='utf-8')}
        for name, text in contents.items():
            path = root/name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding='utf-8')
        manifest = {'schema':1, 'files': {name:hashlib.sha256((root/name).read_bytes()).hexdigest() for name in contents}}
        (root/'manifest.json').write_text(json.dumps(manifest), encoding='utf-8')
        return entry

    def test_prompt_selects_native_recipe_and_prepares_resolved_path(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            entry = self.fixture(root)
            results = catalog.search(root, 'сохрани версию файла')
            self.assertEqual(results[0]['id'], entry['id'])
            result = catalog.prepare(root, results[0]['id'])
            self.assertEqual(result['mode'], 'native-helper')
            self.assertFalse(result['executed'])
            self.assertNotIn('${CODEX_PACK_ROOT}', result['instructions'])
            self.assertIn(root.resolve().as_posix(), result['instructions'])

    def test_tampered_helper_is_rejected_before_preparation(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            entry = self.fixture(root)
            (root/'scripts/runtime.py').write_text('raise RuntimeError("unreviewed")')
            with self.assertRaisesRegex(ValueError, 'checksum'):
                catalog.prepare(root, entry['id'])

    def test_unreviewed_entry_is_not_claimed_executable(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            self.fixture(root)
            path = root/'catalog.json'
            entries = json.loads(path.read_text())
            entries['entries'][0]['execution'] = {'mode':'needs-adapter'}
            path.write_text(json.dumps(entries))
            manifest = json.loads((root/'manifest.json').read_text())
            manifest['files']['catalog.json'] = hashlib.sha256(path.read_bytes()).hexdigest()
            (root/'manifest.json').write_text(json.dumps(manifest))
            result = catalog.prepare(root, 'demo')
            self.assertIn('blocker', result)
            self.assertNotIn('instructions', result)

    def test_cli_emits_utf8_with_legacy_stdout_encoding(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            entry = {'id': 'demo', 'name': 'demo', 'description': '\u041f\u0440\u0438\u043c\u0435\u0440'}
            (root / 'catalog.json').write_text(json.dumps({'entries': [entry]}), encoding='utf-8')
            for script in ('scripts/catalog.py', 'bundle/scripts/catalog.py'):
                with self.subTest(script=script):
                    result = subprocess.run(
                        [sys.executable, '-B', str(REPO / script), 'demo', '--root', str(root)],
                        env={**os.environ, 'PYTHONIOENCODING': 'cp1252'},
                        capture_output=True,
                    )
                    self.assertEqual(result.returncode, 0, result.stderr.decode('utf-8', errors='replace'))
                    self.assertEqual(json.loads(result.stdout.decode('utf-8')), [entry])
