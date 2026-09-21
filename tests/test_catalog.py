import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[1]


class CatalogTests(unittest.TestCase):
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
