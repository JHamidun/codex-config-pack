"""Test installed routing, preparation and real offline helpers, not LLM selection."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('installer', REPO/'install.py')
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstalledWorkflowTests(unittest.TestCase):
    def test_prompt_to_installed_helper_with_real_artifacts(self):
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            bundle = base/'bundle'
            bundle.mkdir()
            native = json.loads((REPO/'native/registry.json').read_text(encoding='utf-8'))['entries']
            entries = [{'id': ident, 'name': ident.split('/')[1], 'description': 'Fixture',
                        'execution': route, 'dependencies': [], 'path':'unused-reference.md'}
                       for ident, route in native.items()]
            files = {'catalog.json':json.dumps({'entries':entries}).encode(),
                     'router/SKILL.md':b'Use ${CODEX_PACK_ROOT}/scripts/catalog.py'}
            helpers = {r['helper'] for r in native.values()}
            helpers.update(h for r in native.values() for h in r.get('helpers', []))
            for name in ('scripts/catalog.py', *sorted(helpers), *(r['recipe'] for r in native.values())):
                files[name] = (REPO/name).read_bytes()
            for name, data in files.items():
                path = bundle/name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
            manifest = {'schema':1, 'source_commit':'a'*40,
                        'files':{name:hashlib.sha256(data).hexdigest() for name,data in files.items()}}
            (bundle/'manifest.json').write_text(json.dumps(manifest))
            target = base/'codex-home'
            installed = installer.install(bundle, target)
            root = Path(installed['pack_root'])
            workspace = base/'project'
            workspace.mkdir()
            (workspace/'index.html').write_bytes(b'original')
            (workspace/'data.csv').write_text('id,amount\n001,2\n002,4\n')
            subprocess.run(['git','-C',str(workspace),'init','-b','main'], check=True, capture_output=True)

            def run(script, *arguments):
                result = subprocess.run([sys.executable, '-B', str(root/script), *arguments], capture_output=True, check=True)
                return json.loads(result.stdout)

            cases = [
                ('покажи изменения в репозитории', 'git-status', ['--workspace',str(workspace)]),
                ('проанализируй csv', 'csv-profile', [str(workspace/'data.csv'),'--numeric','amount']),
                ('сохрани версию файла', 'snapshot', ['--workspace',str(workspace),'--file','index.html']),
            ]
            for prompt, command, arguments in cases:
                with self.subTest(command=command):
                    choices = run('scripts/catalog.py', prompt)
                    prepared = run('scripts/catalog.py','--prepare',choices[0]['id'])
                    self.assertEqual(prepared['mode'],'native-helper')
                    self.assertIn(str(root).replace('\\','/'), prepared['instructions'])
                    result = run('scripts/runtime.py', command, *arguments)
                    self.assertEqual(result['status'], 'ok')
                    if command == 'csv-profile':
                        self.assertEqual(result['result']['columns'][1]['numeric']['mean'], '3')
                    elif command == 'git-status':
                        self.assertIn('index.html',result['result']['untracked'])
                    else:
                        self.assertEqual((workspace/'.snapshots'/result['result']['id']/'content').read_bytes(), b'original')
            self.assertFalse((target/'config.toml').exists())
            choices = run('scripts/catalog.py', 'проверь пак на утечки')
            prepared = run('scripts/catalog.py', '--prepare', choices[0]['id'])
            self.assertEqual(prepared['mode'], 'native-helper')
            clean = run('scripts/hygiene.py', '--workspace', str(workspace))
            self.assertEqual(clean['findings'], [])
            self.assertFalse(clean['security_certified'])
            for ident in native:
                prepared = run('scripts/catalog.py', '--prepare', ident, '--workspace', str(workspace))
                self.assertEqual(prepared['mode'], 'native-helper')
                self.assertFalse(prepared['executed'])
            request = {'operation': 'ocr-restore', 'input': 'scan.txt', 'output': 'ocr-result'}
            (workspace / 'scan.txt').write_bytes('syn\u00adthetic'.encode('utf-8'))
            (workspace / 'job.json').write_text(json.dumps(request), encoding='utf-8')
            adapted = run('scripts/optional_adapter.py', 'run', '--workspace', str(workspace), '--request', 'job.json')
            self.assertEqual(adapted['status'], 'ok')
            self.assertEqual((workspace / 'ocr-result/restored.txt').read_text(), 'synthetic')
