"""Static dependency closure audit; never import or execute library code."""
import ast
import collections
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote

LINK = re.compile(r'\[[^\]\n]*\]\(([^)\n]+)\)')
PACK_PATH = re.compile(r'(\$\{CODEX_PACK_ROOT\}/[^\s`\"\'<>\[\]()]*)')
SCRIPT = re.compile(r'(?<![\w/])((?:\.?\.?/)?(?:scripts|references|assets|tools)/[\w./-]+\.(?:py|ps1|sh|mjs|js|md|json|yaml|yml|png|svg|pdf|pptx|xlsx|docx))\b')

def references(text):
    results = set()
    for pattern in (LINK, SCRIPT, PACK_PATH):
        for match in pattern.finditer(text):
            target = match.group(1).split(' "', 1)[0].strip('<> ').split('#', 1)[0]
            if not target or re.match(r'[a-z]+:', target, re.I) or target.startswith('//'):
                continue
            results.add((text.count('\n', 0, match.start()) + 1, unquote(target)))
    return sorted(results)

def resolve(root, origin, target):
    base = origin.parent
    if target.startswith('${CODEX_PACK_ROOT}/'):
        target = target.removeprefix('${CODEX_PACK_ROOT}/')
        base = root
    if any(c in target for c in ('$', '<', '>', '{', '}', '*')):
        return {'status': 'parameterized-reference'}
    candidate = (base / target).resolve()
    if not candidate.is_relative_to(root.resolve()):
        return {'status': 'external-local-reference'}
    if candidate.is_file():
        return {'status': 'present', 'path': candidate.relative_to(root.resolve()).as_posix()}
    quarantined = candidate.with_name(candidate.name + '.source')
    if quarantined.is_file():
        return {'status': 'reference-code-only', 'path': quarantined.relative_to(root.resolve()).as_posix()}
    return {'status': 'missing-or-illustrative'}

def inspect_file(root, path):
    text = path.read_text(encoding='utf-8', errors='replace')
    row = {'path': path.relative_to(root).as_posix(), 'references': [], 'python_imports': [], 'environment_names': [], 'syntax': 'not-applicable'}
    if path.suffix == '.md':
        row['references'] = [{'line': line, 'target': target, **resolve(root, path, target)} for line, target in references(text)]
    if path.name.endswith('.py.source'):
        try:
            tree = ast.parse(text)
            row['syntax'] = 'parsed-not-executed'
            imports: set[str] = set()
            env = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imports.update(n.name.split('.')[0] for n in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module and not node.level:
                    imports.add(node.module.split('.')[0])
                elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr in {'getenv', 'get'} and node.args and isinstance(node.args[0], ast.Constant):
                    name = node.args[0].value
                    if isinstance(name, str) and re.fullmatch('[A-Z][A-Z0-9_]{2,}', name):
                        env.add(name)
            row['python_imports'] = sorted(imports - sys.stdlib_module_names - {'__future__'})
            row['environment_names'] = sorted(env)
        except SyntaxError:
            row['syntax'] = 'parse-failed-reference-only'
    if path.name in {'package.json', 'requirements.txt'}:
        row['dependency_manifest'] = True
        if path.name == 'package.json':
            try:
                data = json.loads(text)
                row['npm_packages'] = sorted(set(data.get('dependencies', {})) | set(data.get('devDependencies', {})))
            except (ValueError, TypeError):
                row['syntax'] = 'manifest-parse-failed'
    return row

def audit(root, entries):
    root = root.resolve()
    files = {}
    for p in sorted((root / 'library').rglob('*')):
        if p.is_file() and (p.suffix == '.md' or p.name.endswith('.py.source') or p.name in {'package.json', 'requirements.txt'}):
            files[p.relative_to(root).as_posix()] = inspect_file(root, p)
    audited = []
    for entry in entries:
        origin = root / entry['path']
        scope = origin.parent if entry['kind'] == 'skill' else None
        closure = {entry['path']}
        if scope:
            closure.update(p.relative_to(root).as_posix() for p in scope.rglob('*') if p.is_file())
        pending = list(closure)
        while pending:
            current = files.get(pending.pop(), {})
            for ref in current.get('references', []):
                target = ref.get('path')
                if target and target not in closure:
                    closure.add(target)
                    pending.append(target)
        members = [files[p] for p in sorted(closure) if p in files]
        flags = set(entry['dependencies'])
        refs = [r for m in members for r in m['references']]
        if any(r['status'] == 'missing-or-illustrative' for r in refs):
            flags.add('unresolved-or-illustrative-local-reference')
        if any(r['status'] in {'parameterized-reference', 'external-local-reference'} for r in refs):
            flags.add('parameterized-or-external-local-reference')
        code_count = sum(p.endswith('.source') for p in closure)
        if code_count:
            flags.add('reference-code-not-adapted')
        if any(m['syntax'] == 'parse-failed-reference-only' for m in members):
            flags.add('reference-python-parse-failure')
        if any(m.get('dependency_manifest') for m in members):
            flags.add('dependency-manifest-not-installed')
        entry['dependencies'] = sorted(flags)
        entry['status'] = 'requires-runtime-review' if flags else 'instructions-adapted'
        audited.append({'id': entry['id'], 'closure_files': len(closure), 'quarantined_code_files': code_count, 'reference_counts': dict(collections.Counter(r['status'] for r in refs)), 'python_import_candidates': sorted({v for m in members for v in m['python_imports']}), 'environment_name_candidates': sorted({v for m in members for v in m['environment_names']}), 'flags': sorted(flags), 'live_verified': False})
    all_refs = [r for m in files.values() for r in m['references']]
    return {'schema': 1, 'method': 'Static whole-skill tree plus transitive local Markdown links; illustrative references can be false positives. Python imports are names, not verified PyPI packages. No provider calls or dependency installation.', 'summary': {'entries': len(audited), 'analyzed_files': len(files), 'reference_counts': dict(collections.Counter(r['status'] for r in all_refs)), 'python_sources': sum(p.endswith('.py.source') for p in files), 'python_parse_failures': sum(m['syntax'] == 'parse-failed-reference-only' for m in files.values()), 'live_workflows_tested': 0}, 'entries': audited, 'files': list(files.values())}

if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1] / 'bundle'
    entries = json.loads((root / 'catalog.json').read_text(encoding='utf-8'))['entries']
    print(json.dumps(audit(root, entries)['summary'], indent=2))
