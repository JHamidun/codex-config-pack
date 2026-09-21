import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('runtime', REPO / 'scripts/runtime.py')
runtime = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runtime)


class RuntimeTests(unittest.TestCase):
    def test_git_status_real_repository_handles_rename_and_unicode(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            def git(*args):
                return subprocess.run(['git', '-C', str(root), *args], check=True, capture_output=True)
            git('init', '-b', 'main')
            (root/'before name.txt').write_text('first')
            git('add', '.')
            git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.com', 'commit', '-m', 'fixture')
            git('mv', 'before name.txt', 'after name.txt')
            (root/'after name.txt').write_text('changed')
            (root/'\u0442\u0435\u0441\u0442.txt').write_text('new')
            result = runtime.git_status(root)
            self.assertEqual(result['branch'], 'main')
            self.assertEqual(result['renamed'], [{'from': 'before name.txt', 'to': 'after name.txt'}])
            self.assertIn('after name.txt', result['staged'])
            self.assertIn('after name.txt', result['modified'])
            self.assertIn('\u0442\u0435\u0441\u0442.txt', result['untracked'])
            self.assertFalse(result['clean'])

    def test_git_status_rejects_non_repository(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaisesRegex(ValueError, 'Git status failed'):
                runtime.git_status(Path(d))

    def test_csv_profile_does_not_treat_identifiers_as_metrics(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d)/'data.csv'
            path.write_text('id;amount;label\n001;10;A\n002;20;B\n002;;B\n', encoding='utf-8-sig')
            result = runtime.csv_profile(path, numeric=['amount'], keys=['id'])
            self.assertEqual(result['rows'], 3)
            self.assertEqual(result['duplicate_key_rows'], 1)
            cols = {c['name']: c for c in result['columns']}
            self.assertNotIn('numeric', cols['id'])
            self.assertEqual(cols['amount']['missing'], 1)
            self.assertEqual(cols['amount']['numeric']['mean'], '15')

    def test_csv_reports_invalid_nonfinite_values(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d)/'data.csv'
            path.write_text('amount,label\nNaN,a\nInfinity,b\nno,c\n4,d\n')
            result = runtime.csv_profile(path, numeric=['amount'])
            numeric = result['columns'][0]['numeric']
            self.assertEqual(numeric['invalid'], 3)
            self.assertEqual(numeric['valid'], 1)
            self.assertEqual(numeric['mean'], '4')

    def test_csv_rejects_duplicate_headers_bad_rows_and_unknown_columns(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d)/'data.csv'
            for text, kwargs in [('a,a\n1,2\n', {}), ('a,b\n1,2,3\n', {}), ('a,b\n1,2\n', {'keys':['missing']})]:
                with self.subTest(text=text):
                    path.write_text(text)
                    with self.assertRaises(ValueError):
                        runtime.csv_profile(path, delimiter=',', **kwargs)

    def test_snapshot_roundtrip_preserves_pre_restore_version(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            target = root/'index.html'
            target.write_bytes(b'original')
            snapshot = runtime.snapshot_create(root, 'index.html')
            target.write_bytes(b'changed')
            result = runtime.snapshot_restore(root, snapshot['id'])
            self.assertEqual(target.read_bytes(), b'original')
            backup = runtime.snapshot_restore(root, result['before_restore_id'])
            self.assertEqual(target.read_bytes(), b'changed')
            self.assertIn('before_restore_id', backup)

    def test_snapshot_rejects_escape_protected_and_source_files(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            for name in ('../escape', '.claude/config.json', '.env', 'run.py.source', '.claude./config.json'):
                with self.subTest(name=name), self.assertRaises(ValueError):
                    runtime.snapshot_create(root, name)

    def test_tampered_snapshot_never_overwrites_target(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            target = root/'index.html'
            target.write_bytes(b'original')
            result = runtime.snapshot_create(root, 'index.html')
            (root/'.snapshots'/result['id']/'content').write_bytes(b'tampered')
            target.write_bytes(b'current')
            with self.assertRaisesRegex(ValueError, 'checksum'):
                runtime.snapshot_restore(root, result['id'])
            self.assertEqual(target.read_bytes(), b'current')

    def test_snapshot_does_not_follow_link(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            target = root/'index.html'
            target.write_bytes(b'original')
            link = root/'linked.html'
            try:
                link.symlink_to(target)
            except OSError:
                self.skipTest('Symlinks unavailable')
            with self.assertRaisesRegex(ValueError, 'link'):
                runtime.snapshot_create(root, 'linked.html')

    def test_cli_is_encoding_safe_and_errors_do_not_dump_file_contents(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d)/'data.csv'
            path.write_text('a,b\n1,2,not-to-be-printed\n')
            result = subprocess.run([sys.executable, '-B', str(REPO/'scripts/runtime.py'), 'csv-profile', str(path), '--delimiter', ','], env={**os.environ, 'PYTHONIOENCODING':'cp1252'}, capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertNotIn(b'not-to-be-printed', result.stdout + result.stderr)
            self.assertEqual(json.loads(result.stdout)['status'], 'error')
