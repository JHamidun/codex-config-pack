import importlib.util
import json
from pathlib import Path
import tempfile
import tomllib
import unittest
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('builder', REPO / 'scripts/build_pack.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class BuildTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.source = self.base / 'upstream'
        self.source.mkdir()
        self.output = self.base / 'built'
        self.files = {
            '.claude/skills/demo/SKILL.md': '---\nname: demo\ndescription: Documentation example\n---\n# Demo\nWrite docs.\n',
            '.claude/skills/runtime/SKILL.md': '---\nname: runtime\ndescription: Integration example\n---\nRun scripts/run.py\n',
            '.claude/skills/runtime/scripts/run.py': 'raise RuntimeError("Never execute during conversion")\n',
            '.claude/skills/runtime/NOTICE': 'Third-party attribution fixture\n',
            '.claude/agents/reviewer.md': '---\nname: reviewer\ndescription: Review only\nmodel: opus\n---\nRead and review.\n',
            '.claude/commands/check.md': '# Check\nReview the requested changes.\n',
            '.claude/mcp.json': '{"servers":{"example":{"command":"never-run"}}}',
            '.claude/settings.json': '{"hooks":{"PreToolUse":[]}}',
            'LICENSE': 'MIT fixture\n',
        }
        for name, text in self.files.items():
            path = self.source / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding='utf-8')

    def tearDown(self):
        self.temp.cleanup()

    def git(self, args, **kwargs):
        if 'rev-parse' in args:
            return builder.PIN + '\n'
        if 'status' in args:
            return ''
        if 'ls-files' in args:
            return '\0'.join(self.files) + '\0'
        raise AssertionError('Unexpected subprocess')

    def build(self, output=None):
        with patch.object(builder.subprocess, 'check_output', side_effect=self.git):
            return builder.build(self.source, output or self.output)

    def test_source_is_unchanged(self):
        before = {name: (self.source / name).read_bytes() for name in self.files}
        self.build()
        self.assertEqual(before, {name: (self.source / name).read_bytes() for name in self.files})

    def test_shared_workflow_dependencies_are_shipped_without_execution(self):
        additions = {
            '.claude/get-shit-done/workflows/new-project.md': '# Project workflow\n',
            '.claude/get-shit-done/LICENSE': 'MIT fixture\n',
            '.claude/get-shit-done/bin/gsd-tools.cjs': 'throw Error("never execute");\n',
            '.claude/schemas/bug-plan.schema.json': '{"type":"object"}\n',
            '.claude/templates/plan.md': '# Plan template\n',
            '.claude/workflows/review.md': '# Review workflow\n',
            '.claude/docs/architecture.md': '# Shared architecture reference\n',
            '.claude/prompts/example.json': '{"prompt":"public example"}\n',
            '.claude/scripts/check.py': 'raise RuntimeError("never execute");\n',
            '.claude/tools/client.py': 'raise RuntimeError("never execute");\n',
            '.claude/hooks/guard.js': 'throw Error("never execute");\n',
            '.claude/mcps/example/server.py': 'raise RuntimeError("never execute");\n',
        }
        for name, text in additions.items():
            path = self.source / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding='utf-8')
        self.files.update(additions)
        self.build()
        for name in additions:
            relative = name.removeprefix('.claude/')
            if Path(relative).suffix in builder.CODE:
                relative += '.source'
            self.assertTrue((self.output / 'library' / relative).is_file(), relative)

    def test_every_tracked_configuration_file_is_accounted_for(self):
        self.files['.claude/.refcheck-coverage'] = 'not-runtime-data'
        (self.source / '.claude/.refcheck-coverage').write_text('not-runtime-data', encoding='utf-8')
        self.build()
        report = json.loads((self.output / 'compatibility.json').read_text(encoding='utf-8'))
        expected = {name for name in self.files if name.startswith('.claude/')}
        observed = {row['source'] for row in report['source_files']}
        observed.update(row['path'] for row in report['omissions'])
        self.assertEqual(observed, expected)

    def test_model_inherited_and_reviewer_read_only(self):
        self.build()
        agent = tomllib.loads((self.output / 'agents/pack-reviewer.toml').read_text(encoding='utf-8'))
        self.assertNotIn('model', agent)
        self.assertEqual(agent['sandbox_mode'], 'read-only')

    def test_source_code_is_quarantined(self):
        self.build()
        root = self.output / 'library/skills/runtime/scripts'
        self.assertTrue((root / 'run.py.source').exists())
        self.assertFalse((root / 'run.py').exists())

    def test_third_party_notice_is_preserved(self):
        self.build()
        self.assertEqual((self.output / 'library/skills/runtime/NOTICE').read_text(), 'Third-party attribution fixture\n')

    def test_runtime_dependency_is_explicit(self):
        self.build()
        entries = json.loads((self.output / 'catalog.json').read_text(encoding='utf-8'))['entries']
        entry = next(e for e in entries if e['name'] == 'runtime')
        self.assertEqual(entry['status'], 'requires-runtime-review')
        self.assertFalse(entry['live_verified'])

    def test_mcp_and_hooks_not_activated(self):
        self.build()
        report = json.loads((self.output / 'compatibility.json').read_text(encoding='utf-8'))
        self.assertEqual(report['integrations'][0]['status'], 'not-installed')
        self.assertEqual(report['hooks'][0]['status'], 'not-installed')
        self.assertFalse((self.output / 'config.toml').exists())

    def test_build_is_deterministic(self):
        self.build()
        second = self.base / 'second'
        self.build(second)
        self.assertEqual((self.output / 'manifest.json').read_bytes(), (second / 'manifest.json').read_bytes())

    def test_unknown_revision_is_rejected(self):
        with patch.object(builder.subprocess, 'check_output', return_value='b' * 40):
            with self.assertRaisesRegex(ValueError, 'revision'):
                builder.build(self.source, self.output)
        self.assertFalse(self.output.exists())

    def test_output_inside_source_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'source checkout'):
            builder.build(self.source, self.source / 'generated')

    def test_output_alias_inside_source_is_rejected_before_git(self):
        alias = self.base / 'short-name-alias' / 'generated'
        canonical_output = self.source.resolve() / 'generated'
        original_resolve = Path.resolve

        def resolve(path, *args, **kwargs):
            if path == alias:
                return canonical_output
            return original_resolve(path, *args, **kwargs)

        with patch.object(Path, 'resolve', resolve):
            with patch.object(builder.subprocess, 'check_output') as git:
                with self.assertRaisesRegex(ValueError, 'source checkout'):
                    builder.build(self.source, alias)
                git.assert_not_called()

    def test_output_through_link_is_rejected(self):
        link = self.base / 'link'
        try:
            link.symlink_to(self.source, target_is_directory=True)
        except OSError:
            self.skipTest('Creating symlinks is not permitted by this OS')
        with self.assertRaisesRegex(ValueError, 'link'):
            builder.build(self.source, link / 'generated')

    def test_full_bundle_native_agent_schemas(self):
        for path in (REPO / 'bundle/agents').glob('*.toml'):
            agent = tomllib.loads(path.read_text(encoding='utf-8'))
            self.assertTrue(agent['name'].startswith('pack-'))
            self.assertNotIn('model', agent)
            self.assertIsInstance(agent['developer_instructions'], str)

    def test_reference_source_is_sanitized_too(self):
        name = '.claude/skills/runtime/scripts/run.py'
        fixture_home = '/'.join(('', 'home', 'demo_owner'))
        (self.source/name).write_text('CONTACT = "someone@private.invalid"\nHOME = "' + fixture_home + '/data"\n')
        self.build()
        text = (self.output/'library/skills/runtime/scripts/run.py.source').read_text()
        self.assertNotIn('someone@private.invalid', text)
        self.assertNotIn(fixture_home, text)

    def test_raw_workflow_exports_are_not_redistributed(self):
        name = '.claude/skills/n8n/catalog/workflows/Example/export.json'
        self.files[name] = '{"pinData":{"contact":"private"}}'
        path = self.source/name
        path.parent.mkdir(parents=True)
        path.write_text(self.files[name])
        self.build()
        self.assertFalse((self.output/'library/skills/n8n/catalog/workflows/Example/export.json').exists())
        report = json.loads((self.output/'compatibility.json').read_text())
        self.assertTrue(any(x['path']==name and x['reason']=='raw-workflow-export-privacy-boundary' for x in report['omissions']))

    def test_unestablished_license_is_excluded(self):
        name = '.claude/skills/doc-coauthoring/SKILL.md'
        self.files[name] = '---\nname: restricted\ndescription: fixture\n---\nNot licensed for this test.'
        path = self.source/name
        path.parent.mkdir(parents=True)
        path.write_text(self.files[name])
        self.build()
        self.assertFalse((self.output/'library/skills/doc-coauthoring/SKILL.md').exists())
        report = json.loads((self.output/'compatibility.json').read_text())
        self.assertTrue(any(x['reason']=='upstream-license-not-established' for x in report['omissions']))


if __name__ == '__main__':
    unittest.main()
