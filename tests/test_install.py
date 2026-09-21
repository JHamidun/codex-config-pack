import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('installer', REPO / 'install.py')
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.bundle = self.base / 'bundle'
        self.bundle.mkdir()
        self.target = self.base / 'codex-home'
        self.files = {
            'router/SKILL.md': b'root=${CODEX_PACK_ROOT}',
            'CORE.md': b'core rules',
            'agents/pack-reviewer.toml': b'name = "pack-reviewer"\n',
        }
        for name, data in self.files.items():
            path = self.bundle / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        self.manifest = {'schema': 1, 'source_commit': 'a' * 40, 'files': {name: installer.sha(data) for name, data in self.files.items()}}
        self.save_manifest()

    def tearDown(self):
        self.temp.cleanup()

    def save_manifest(self):
        (self.bundle / 'manifest.json').write_text(json.dumps(self.manifest), encoding='utf-8')

    def test_dry_run_has_no_writes(self):
        result = installer.install(self.bundle, self.target, dry_run=True)
        self.assertEqual(result['new_or_updated'], 5)
        self.assertFalse(self.target.exists())

    def test_install_is_idempotent(self):
        installer.install(self.bundle, self.target)
        result = installer.install(self.bundle, self.target)
        self.assertEqual(result['new_or_updated'], 0)
        self.assertFalse((self.target / 'config.toml').exists())
        self.assertNotIn('${CODEX_PACK_ROOT}', (self.target / 'skills/hamidun-pack/SKILL.md').read_text())
        installed_manifest = self.target / 'packs/hamidun-pack' / self.manifest['source_commit'] / 'manifest.json'
        self.assertEqual(json.loads(installed_manifest.read_text()), self.manifest)

    def test_agents_are_opt_in(self):
        installer.install(self.bundle, self.target)
        self.assertFalse((self.target / 'agents').exists())
        installer.install(self.bundle, self.target, with_agents=True)
        self.assertTrue((self.target / 'agents/pack-reviewer.toml').exists())

    def test_conflict_aborts_before_any_install(self):
        router = self.target / 'skills/hamidun-pack/SKILL.md'
        router.parent.mkdir(parents=True)
        router.write_text('user content')
        with self.assertRaisesRegex(ValueError, 'conflicts'):
            installer.install(self.bundle, self.target)
        self.assertEqual(router.read_text(), 'user content')
        self.assertFalse((self.target / 'packs').exists())

    def test_modified_files_survive_uninstall(self):
        installer.install(self.bundle, self.target)
        router = self.target / 'skills/hamidun-pack/SKILL.md'
        router.write_text('user modification')
        result = installer.uninstall(self.target)
        self.assertEqual(result['modified_files_preserved'], ['skills/hamidun-pack/SKILL.md'])
        self.assertEqual(router.read_text(), 'user modification')

    def test_uninstall_dry_run_preserves_files(self):
        installer.install(self.bundle, self.target)
        installer.uninstall(self.target, dry_run=True)
        self.assertTrue((self.target / 'skills/hamidun-pack/SKILL.md').exists())

    def test_uninstall_preserves_unrelated_files(self):
        installer.install(self.bundle, self.target)
        keep = self.target / 'config.toml'
        keep.write_text('[agents]\nmax_threads = 9\n')
        installer.uninstall(self.target)
        self.assertIn('9', keep.read_text())

    def test_existing_identical_file_is_not_owned(self):
        path = self.target / 'packs/hamidun-pack' / ('a' * 40) / 'CORE.md'
        path.parent.mkdir(parents=True)
        path.write_bytes(self.files['CORE.md'])
        result = installer.install(self.bundle, self.target)
        self.assertEqual(result['foreign_identical_not_owned'], 1)
        installer.uninstall(self.target)
        self.assertTrue(path.exists())

    def test_checksum_tampering_is_rejected(self):
        (self.bundle / 'CORE.md').write_text('tampered')
        with self.assertRaisesRegex(ValueError, 'checksum'):
            installer.install(self.bundle, self.target)
        self.assertFalse(self.target.exists())

    def test_unlisted_files_are_rejected(self):
        (self.bundle / 'unexpected.py').write_text('raise Exception()')
        with self.assertRaisesRegex(ValueError, 'Unexpected'):
            installer.install(self.bundle, self.target)

    def test_manifest_traversal_is_rejected(self):
        self.manifest['files']['../outside'] = '0' * 64
        self.save_manifest()
        with self.assertRaisesRegex(ValueError, 'Unsafe'):
            installer.install(self.bundle, self.target)

    def test_protected_target_is_rejected(self):
        for folder in ('.claude', '.agents', '.brain', '_casebook'):
            with self.assertRaisesRegex(ValueError, 'protected'):
                installer.install(self.bundle, self.base / folder / 'nested')

    def test_symlink_target_is_rejected(self):
        actual = self.base / 'actual'
        actual.mkdir()
        try:
            self.target.symlink_to(actual, target_is_directory=True)
        except OSError:
            self.skipTest('Creating symlinks is not permitted by this OS')
        with self.assertRaisesRegex(ValueError, 'Links'):
            installer.install(self.bundle, self.target)
        self.assertEqual(list(actual.iterdir()), [])

    def test_malicious_installed_manifest_is_rejected(self):
        installer.install(self.bundle, self.target)
        path = installer.state_path(self.target)
        data = json.loads(path.read_text())
        data['files']['config.toml'] = '0' * 64
        path.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, 'unowned'):
            installer.uninstall(self.target)

    def test_journal_allows_recovery_after_interruption(self):
        original = installer.atomic_write
        def interrupt(path, data):
            if path.name == 'CORE.md':
                raise OSError('Simulated interruption')
            return original(path, data)
        installer.atomic_write = interrupt
        try:
            with self.assertRaises(OSError):
                installer.install(self.bundle, self.target)
        finally:
            installer.atomic_write = original
        installer.uninstall(self.target)
        self.assertFalse((self.target / 'skills/hamidun-pack/SKILL.md').exists())

    def test_atomic_write_retries_transient_sharing_lock(self):
        original = installer.os.replace
        calls = []
        def transient(source, destination):
            calls.append(1)
            if len(calls) < 3:
                raise PermissionError('Simulated transient sharing violation')
            return original(source, destination)
        path = self.base / 'atomic.txt'
        with patch.object(installer.os, 'replace', side_effect=transient):
            installer.atomic_write(path, b'verified')
        self.assertEqual(path.read_bytes(), b'verified')
        self.assertEqual(len(calls), 3)


if __name__ == '__main__':
    unittest.main()
