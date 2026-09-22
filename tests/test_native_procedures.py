import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('catalog_procedures', REPO / 'scripts/catalog.py')
catalog = importlib.util.module_from_spec(spec)
spec.loader.exec_module(catalog)


class NativeProcedureTests(unittest.TestCase):
    def test_unlisted_reference_is_rejected_before_file_read(self):
        with tempfile.TemporaryDirectory() as d, patch.object(Path, 'read_bytes') as read:
            with self.assertRaises(ValueError):
                catalog.verified_text(Path(d), 'unlisted.md', {'files': {}})
            read.assert_not_called()

    def test_connection_contract_members_exist_and_are_unique(self):
        entries = json.loads((REPO / 'bundle/catalog.json').read_text(encoding='utf-8'))['entries']
        contracts = json.loads((REPO / 'native/connection-contracts.json').read_text(encoding='utf-8'))
        seen = set()
        for service, contract in contracts.items():
            self.assertTrue(contract['required'], service)
            for kind in ('skills', 'commands', 'agents'):
                known = {e['name'] for e in entries if e['kind'] + 's' == kind}
                self.assertFalse(set(contract[kind]) - known, service)
                for name in contract[kind]:
                    self.assertNotIn((kind, name), seen)
                    seen.add((kind, name))

    def test_every_declared_group_member_exists_and_is_unambiguous(self):
        entries = json.loads((REPO / 'bundle/catalog.json').read_text(encoding='utf-8'))['entries']
        groups = json.loads((REPO / 'native/procedure-groups.json').read_text(encoding='utf-8'))
        seen = set()
        for group, kinds in groups.items():
            self.assertTrue((REPO / 'native/recipes' / (group + '.md')).is_file())
            for kind, names in kinds.items():
                known = {e['name'] for e in entries if e['kind'] + 's' == kind}
                self.assertFalse(set(names) - known, (group, set(names) - known))
                for name in names:
                    self.assertNotIn((kind, name), seen)
                    seen.add((kind, name))

    def test_every_gsd_command_has_an_explicit_native_operation(self):
        entries = json.loads((REPO / 'bundle/catalog.json').read_text(encoding='utf-8'))['entries']
        for entry in entries:
            if '/commands/gsd/' in entry['source']:
                with self.subTest(entry=entry['id']):
                    result = catalog.prepare(REPO / 'bundle', entry['id'])
                    self.assertEqual(result['mode'], 'native-procedure')
                    self.assertTrue(result['operation'])
                    self.assertFalse(result['executed'])

    def test_all_native_procedures_resolve_and_do_not_claim_live_execution(self):
        entries = json.loads((REPO / 'bundle/catalog.json').read_text(encoding='utf-8'))['entries']
        for entry in entries:
            if entry['execution']['mode'] == 'native-procedure':
                with self.subTest(entry=entry['id']):
                    result = catalog.prepare(REPO / 'bundle', entry['id'])
                    self.assertTrue(result['instructions'])
                    self.assertIn('not-live-tested', result['verification'])
                    self.assertEqual(result['domain_reference'], entry['path'])
                    self.assertFalse(result['executed'])

    def test_business_context_is_workspace_owned_not_a_pack_write(self):
        root = REPO / 'bundle'
        manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
        with tempfile.TemporaryDirectory() as d:
            result = catalog.verified_text(root, 'library/skills/campaign-planning/SKILL.md', manifest, Path(d))
            self.assertIn(Path(d).resolve().as_posix() + '/.codex-context/business-context.md', result)
            self.assertNotIn(root.as_posix() + '/library/business-context.md', result)
            self.assertEqual(list(Path(d).iterdir()), [])

    def test_source_execution_and_root_escape_stay_blocked(self):
        root = REPO / 'bundle'
        manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
        for relative in ['../README.md', 'library/get-shit-done/bin/gsd-tools.cjs.source']:
            with self.subTest(relative=relative), self.assertRaises(ValueError):
                catalog.verified_text(root, relative, manifest)

    def test_connections_are_not_reported_as_available_or_tested(self):
        root = REPO / 'bundle'
        entries = json.loads((root / 'catalog.json').read_text(encoding='utf-8'))['entries']
        for entry in entries:
            if entry['execution']['mode'] == 'connection-required':
                with self.subTest(entry=entry['id']):
                    result = catalog.prepare(root, entry['id'])
                    self.assertIsNone(result['connected'])
                    self.assertIn('blocker', result)
                    self.assertTrue(result['required'])
                    self.assertFalse(result['executed'])

    def test_every_catalog_entry_has_explicit_route_without_legacy_fallback(self):
        entries = json.loads((REPO / 'bundle/catalog.json').read_text(encoding='utf-8'))['entries']
        self.assertEqual(len(entries), 573)
        for entry in entries:
            self.assertIn(entry['execution']['mode'], {'native-helper', 'native-procedure', 'connection-required'})


if __name__ == '__main__':
    unittest.main()
