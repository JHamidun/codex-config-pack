import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('deps', Path(__file__).resolve().parents[1] / 'scripts/dependency_audit.py')
deps = importlib.util.module_from_spec(spec)
spec.loader.exec_module(deps)

class DependencyTests(unittest.TestCase):
    def test_quarantined_code_is_not_reported_runnable(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            origin = root / 'SKILL.md'
            (root / 'scripts').mkdir()
            (root / 'scripts/a.py.source').write_text('raise RuntimeError("must not execute")')
            self.assertEqual(deps.resolve(root, origin, 'scripts/a.py')['status'], 'reference-code-only')
    def test_missing_and_external_are_distinct(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            self.assertEqual(deps.resolve(root, root/'SKILL.md', 'missing.md')['status'], 'missing-or-illustrative')
            self.assertEqual(deps.resolve(root, root/'SKILL.md', '../outside.md')['status'], 'external-local-reference')
    def test_transitive_missing_dependency_downgrades_entry(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            folder = root/'library/skills/demo'
            folder.mkdir(parents=True)
            (folder/'SKILL.md').write_text('[Details](../../shared.md)')
            (root/'library/shared.md').write_text('[Missing](not-shipped.md)')
            entries=[{'id':'demo','kind':'skill','path':'library/skills/demo/SKILL.md','dependencies':[]}]
            report=deps.audit(root, entries)
            self.assertEqual(entries[0]['status'],'requires-runtime-review')
            self.assertEqual(report['entries'][0]['closure_files'],2)
    def test_python_inspection_never_executes(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            path=root/'a.py.source'
            path.write_text('import os\nimport requests\nraise RuntimeError("not executed")\nx=os.getenv("DEMO_KEY")')
            result=deps.inspect_file(root,path)
            self.assertEqual(result['python_imports'],['requests'])
            self.assertEqual(result['environment_names'],['DEMO_KEY'])
