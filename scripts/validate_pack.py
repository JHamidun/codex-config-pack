"""Validate bundle hashes, native schemas, paths and publication hygiene."""
import argparse
import ast
import importlib.util
import json
from pathlib import Path
import re
import sys
import tomllib

REPO = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location('pack_installer', REPO / 'install.py')
assert spec is not None and spec.loader is not None
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)

PATTERNS = {
    'private-key': r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
    'github-token': r'\bgh[pousr]_[A-Za-z0-9]{30,}\b',
    'openai-token': r'\bsk-(?:proj-|svcacct-)[A-Za-z0-9_-]{30,}',
    'slack-token': r'\bxox[baprs]-[A-Za-z0-9-]{20,}',
    'personal-windows-path': r'(?i)[A-Z]:[/\\]Users[/\\][a-z0-9_.-]+(?:[/\\]|\b)',
    'personal-unix-path': r'/(?:home|Users)/[a-zA-Z0-9_.-]+(?:/|\b)',
}


def validate(root):
    bundle = root / 'bundle'
    manifest = installer.validate_bundle(bundle)
    catalog = json.loads((bundle / 'catalog.json').read_text(encoding='utf-8'))
    ids = [e['id'] for e in catalog['entries']]
    audit = json.loads((bundle / 'dependency-audit.json').read_text(encoding='utf-8'))
    if {e['id'] for e in audit['entries']} != set(ids):
        raise ValueError('Dependency audit does not cover the full catalog')
    audited = {e['id']:e for e in audit['entries']}
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate catalog IDs')
    for entry in catalog['entries']:
        if entry['path'] not in manifest['files']:
            raise ValueError('Missing catalog target: ' + entry['id'])
        if entry['live_verified'] is not False:
            raise ValueError('Unsupported live-verification claim')
        if entry['dependencies'] != audited[entry['id']]['flags']:
            raise ValueError('Catalog/audit dependency mismatch')
    agents = []
    for path in sorted((bundle / 'agents').glob('*.toml')):
        data = tomllib.loads(path.read_text(encoding='utf-8'))
        if not all(isinstance(data.get(k), str) and data[k] for k in ('name', 'description', 'developer_instructions')):
            raise ValueError('Invalid agent: ' + path.name)
        if 'model' in data or 'model_reasoning_effort' in data:
            raise ValueError('Agents must inherit configured models')
        agents.append(data['name'])
    if len(agents) != len(set(agents)):
        raise ValueError('Duplicate agent names')
    findings = []
    files_checked = 0
    for path in root.rglob('*'):
        if not path.is_file() or any(p in {'.git', '__pycache__', 'dist', '.venv'} for p in path.relative_to(root).parts):
            continue
        if path.is_symlink():
            raise ValueError('Publication contains a symlink')
        if path.suffix in {'.db', '.session', '.env'} or path.name in {'auth.json', '.credentials.master.env'}:
            findings.append({'path': path.relative_to(root).as_posix(), 'rule': 'private-state-file'})
        try:
            text = path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            raise ValueError('Opaque binary requires explicit release review: ' + path.relative_to(root).as_posix())
        files_checked += 1
        if path.suffix == '.py' and 'library' not in path.parts:
            ast.parse(text, filename=str(path))
        for label, pattern in PATTERNS.items():
            if re.search(pattern, text):
                findings.append({'path': path.relative_to(root).as_posix(), 'rule': label})
    if findings:
        # Never print matched values, even on failure.
        print(json.dumps({'hygiene_findings': findings}, ensure_ascii=False, indent=2))
        raise ValueError('Publication hygiene failed')
    return {'manifest_files': len(manifest['files']), 'catalog_entries': len(ids), 'agent_profiles': len(agents), 'text_files_scanned': files_checked, 'hygiene_findings': 0, 'live_workflows_tested': 0}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=REPO)
    args = parser.parse_args()
    print(json.dumps(validate(args.root), indent=2))
