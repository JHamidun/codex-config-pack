"""Execute planning/memory CLIs after isolated installation, without an LLM or account."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('state_installer', REPO / 'install.py')
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstalledStateTests(unittest.TestCase):
    def test_planning_and_curated_memory_execute_from_installed_routes(self):
        entries = json.loads((REPO / 'bundle/catalog.json').read_text(encoding='utf-8'))['entries']
        selected = [e for e in entries if e['source'].endswith('/commands/gsd/new-project.md')
                    or (e['kind'] == 'skill' and e['name'] == 'graph-memory')]
        self.assertEqual(len(selected), 2)
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            bundle = base / 'bundle'
            files = {'catalog.json': json.dumps({'entries': selected}).encode(),
                     'router/SKILL.md': b'Use ${CODEX_PACK_ROOT}/scripts/catalog.py'}
            needed = {'scripts/catalog.py'}
            for entry in selected:
                route = entry['execution']
                needed.update([route['recipe'], route['domain_reference'], *route['helpers']])
            for name in needed:
                files[name] = (REPO / 'bundle' / name).read_bytes()
            for name, data in files.items():
                path = bundle / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
            manifest = {'schema': 1, 'source_commit': 'b' * 40,
                        'files': {name: hashlib.sha256(data).hexdigest() for name, data in files.items()}}
            (bundle / 'manifest.json').write_text(json.dumps(manifest), encoding='utf-8')
            target = base / 'codex-home'
            installed = Path(installer.install(bundle, target)['pack_root'])
            workspace = base / 'project'
            workspace.mkdir()

            def run(script, *args):
                result = subprocess.run([sys.executable, '-B', str(installed / script), *args],
                                        check=True, capture_output=True, timeout=30)
                return json.loads(result.stdout)

            for entry in selected:
                prepared = run('scripts/catalog.py', '--prepare', entry['id'], '--workspace', str(workspace))
                self.assertEqual(prepared['mode'], 'native-procedure')
                self.assertFalse(prepared['executed'])

            brief = '# Fixture project\n\nBuild a local task list without a cloud account.\n'
            (workspace / 'brief.md').write_text(brief, encoding='utf-8')
            run('scripts/planning.py', '--workspace', str(workspace), 'init', '--spec', 'brief.md')
            self.assertEqual((workspace / '.planning/PROJECT.md').read_text(encoding='utf-8'), brief)
            state = run('scripts/planning.py', '--workspace', str(workspace), 'inspect')
            self.assertTrue(state['initialized'])
            self.assertFalse(state['ready_to_execute'])
            note = 'Decision: use a local queue; resume with persistence tests.'
            (workspace / 'decision.md').write_text(note, encoding='utf-8')
            checkpoint = run('scripts/planning.py', '--workspace', str(workspace),
                             'checkpoint', '--note', 'decision.md')
            self.assertEqual((workspace / checkpoint['path']).read_text(encoding='utf-8'), note)
            saved = run('scripts/memory.py', '--workspace', str(workspace), 'add',
                        '--note', 'decision.md', '--topic', 'Architecture')
            hits = run('scripts/memory.py', '--workspace', str(workspace), 'query', 'queue')
            self.assertEqual(hits[0]['id'], saved['id'])
            self.assertEqual(hits[0]['source'], 'decision.md')
            graph = run('scripts/memory.py', '--workspace', str(workspace), 'graph', saved['id'])
            self.assertEqual(len(graph['nodes']), 1)
            self.assertEqual(graph['edges'], [])
            stats = run('scripts/memory.py', '--workspace', str(workspace), 'stats')
            self.assertEqual(stats['notes'], 1)
            self.assertEqual(stats['semantic_index'], 'not-configured')
            self.assertFalse(stats['background_jobs'])
            for name, expected in installer.read_state(target)['files'].items():
                self.assertEqual(installer.sha((target / name).read_bytes()), expected)
            self.assertFalse((target / 'config.toml').exists())


if __name__ == '__main__':
    unittest.main()
