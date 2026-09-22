import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('memory', REPO / 'scripts/memory.py')
memory = importlib.util.module_from_spec(spec)
spec.loader.exec_module(memory)


class MemoryTests(unittest.TestCase):
    def test_duplicate_note_is_idempotent_at_capacity(self):
        with tempfile.TemporaryDirectory() as d, patch.object(memory, 'MAX_NOTES', 1):
            root = Path(d)
            (root / 'note.md').write_text('Selected decision', encoding='utf-8')
            first = memory.add(root, 'note.md', 'Decision')
            self.assertFalse(memory.add(root, 'note.md', 'Decision')['created'])
            self.assertEqual(len(memory.load_notes(root)), 1)
            self.assertEqual(memory.load_notes(root)[0]['id'], first['id'])
            with self.assertRaises(ValueError):
                memory.add(root, 'note.md', 'Different topic')

    def test_no_memory_exists_until_explicit_add(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            self.assertEqual(memory.query(root, 'nothing'), [])
            self.assertEqual(list(root.iterdir()), [])

    def test_curated_note_roundtrip_provenance_and_idempotency(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / 'decision.md').write_text('Используем локальную очередь задач.', encoding='utf-8')
            first = memory.add(root, 'decision.md', 'Архитектура')
            second = memory.add(root, 'decision.md', 'Архитектура')
            self.assertEqual(first['id'], second['id'])
            self.assertFalse(second['created'])
            result = memory.query(root, 'очередь')
            self.assertEqual(result[0]['source'], 'decision.md')
            self.assertIn('локальную', result[0]['excerpt'])
            self.assertEqual((root / '.codex-context/.gitignore').read_text(), '*\n')

    def test_graph_has_only_explicit_links_and_depth(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / 'note.md').write_text('A decision')
            first = memory.add(root, 'note.md', 'First')['id']
            (root / 'note.md').write_text('A related decision')
            second = memory.add(root, 'note.md', 'Second', [first])['id']
            self.assertEqual(len(memory.graph(root, first, 0)['nodes']), 1)
            result = memory.graph(root, first)
            self.assertEqual({x['id'] for x in result['nodes']}, {first, second})
            self.assertEqual(result['edges'], [{'from': second, 'to': first}])
            with self.assertRaises(ValueError):
                memory.add(root, 'note.md', 'Third', ['f' * 32])

    def test_private_roots_raw_sessions_and_secrets_are_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            for relative in ['../note.md', '.claude/note.md', 'session.jsonl', '.env']:
                with self.subTest(relative=relative), self.assertRaises(ValueError):
                    memory.add(root, relative, 'private')
            (root / 'note.md').write_text('api_key=' + 'x' * 50)
            with self.assertRaises(ValueError):
                memory.add(root, 'note.md', 'credentials')
            self.assertFalse((root / '.codex-context').exists())


if __name__ == '__main__':
    unittest.main()
