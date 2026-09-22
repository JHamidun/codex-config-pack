"""Read-only, redacted release/skill hygiene scan. Findings are candidates, not verdicts."""
import argparse
import importlib.util
import json
from pathlib import Path
import re

_spec = importlib.util.spec_from_file_location('pack_runtime', Path(__file__).with_name('runtime.py'))
assert _spec is not None and _spec.loader is not None
runtime = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(runtime)

GENERIC = {
    'private-key': r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
    'github-token': r'\bgh[pousr]_[A-Za-z0-9]{30,}\b',
    'provider-token': r'\bsk-(?:proj-|svcacct-|ant-)[A-Za-z0-9_-]{25,}',
    'slack-token': r'\bxox[baprs]-[A-Za-z0-9-]{20,}',
    'google-api-key': r'\bAIza[A-Za-z0-9_-]{30,}',
    'telegram-token': r'\b\d{7,12}:[A-Za-z0-9_-]{30,}',
    'jwt-candidate': r'\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}',
    'credential-assignment': r'(?im)^\s*(?:password|api[_-]?key|access[_-]?token|refresh[_-]?token)\s*[:=]\s*["\']?[A-Za-z0-9_/-]{16,}',
    'personal-windows-path': r'(?i)[A-Z]:[/\\]Users[/\\][A-Za-z0-9_.-]+[/\\]',
    'personal-unix-path': r'/(?:Users|home)/[A-Za-z0-9_.-]+/',
    'email-candidate': r'[A-Za-z0-9._%+-]+@(?!example\.(?:com|org|net)\b)[A-Za-z0-9.-]+\.[A-Za-z]{2,}',
}
INJECTION = {
    'override-instructions': r'(?i)(?:ignore|disregard|override)\s+(?:all\s+)?(?:previous|system|developer)\s+instructions',
    'secret-exfiltration-candidate': r'(?is)(?:curl|fetch|requests\.post).{0,200}(?:credentials|process\.env|os\.environ)',
    'encoded-execution-candidate': r'(?is)(?:base64|b64decode).{0,120}(?:exec|eval|invoke-expression)',
}
SKIP_DIRS = {'.git', '.venv', 'node_modules', '__pycache__'}
PRIVATE = {'.env', 'auth.json', 'credentials.json', '.credentials.master.env'}


def scan(workspace, identity_relative=None, include_injection=False):
    root = runtime.workspace_root(workspace)
    patterns = dict(GENERIC)
    identity_path = None
    if include_injection:
        patterns.update(INJECTION)
    if identity_relative:
        identity_path = runtime.artifact_path(root, identity_relative)
        raw = runtime.read_limited(identity_path)
        if len(raw) > 100_000:
            raise ValueError('Identity rule file is too large')
        identity = json.loads(raw)
        if not isinstance(identity, list) or len(identity) > 100:
            raise ValueError('Identity rules must be a bounded list of label/pattern pairs')
        for index, pair in enumerate(identity):
            if not isinstance(pair, list) or len(pair) != 2 or any(not isinstance(x, str) for x in pair):
                raise ValueError('Invalid identity rule')
            # Literal matching avoids regex denial-of-service and keeps private values out of labels.
            if not pair[1] or len(pair[1]) > 500:
                raise ValueError('Invalid identity literal')
            patterns['identity-' + str(index + 1)] = re.escape(pair[1])
    compiled = [(label, re.compile(pattern)) for label, pattern in patterns.items()]
    findings = []
    skipped = []
    checked = 0
    pending = [root]
    visited = 0
    while pending:
        directory = pending.pop()
        for path in sorted(directory.iterdir()):
            visited += 1
            if visited > 30_000:
                raise ValueError('Tree exceeds the 30000-entry scan limit')
            relative = path.relative_to(root).as_posix()
            if path == identity_path:
                skipped.append({'path': relative, 'reason': 'private-identity-dictionary'})
                continue
            if path.is_symlink() or (hasattr(path, 'is_junction') and path.is_junction()):
                findings.append({'path': relative, 'rule': 'link-not-followed', 'line': None})
                continue
            if path.is_dir():
                if path.name in SKIP_DIRS:
                    continue
                if path.name.casefold() in {'.claude', '.agents', '.brain', '_casebook'}:
                    findings.append({'path': relative, 'rule': 'protected-source-not-read', 'line': None})
                    continue
                pending.append(path)
                continue
            if path.name.casefold() in PRIVATE or path.name.casefold().startswith('.env.') or path.suffix.casefold() in {'.db', '.sqlite', '.session'}:
                findings.append({'path': relative, 'rule': 'private-state-file-not-read', 'line': None})
                continue
            if path.stat().st_size > 2_000_000:
                skipped.append({'path': relative, 'reason': 'large-file-needs-separate-review'})
                continue
            try:
                text = path.read_text(encoding='utf-8-sig')
            except UnicodeError:
                skipped.append({'path': relative, 'reason': 'binary-needs-separate-review'})
                continue
            checked += 1
            for label, pattern in compiled:
                for match in pattern.finditer(text):
                    findings.append({'path': relative, 'rule': label,
                                     'line': text.count('\n', 0, match.start()) + 1})
                    if len(findings) > 10_000:
                        raise ValueError('Finding limit reached; narrow the scan')
    return {'text_files_checked': checked, 'findings': findings, 'skipped': skipped,
            'matched_values_included': False, 'security_certified': False,
            'limitation': 'Heuristics only. Review candidates, skipped assets, Git history and provenance before publication.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', type=Path, required=True)
    parser.add_argument('--identity-file', help='Explicit private workspace-relative JSON label/literal pairs; never auto-discovered')
    parser.add_argument('--injection', action='store_true')
    args = parser.parse_args()
    try:
        result = scan(args.workspace, args.identity_file, args.injection)
    except (OSError, ValueError, re.error, TypeError):
        parser.exit(2, 'Hygiene scan failed: inspect safe paths, bounded inputs and identity rule format. No matched values are logged.\n')
    print(json.dumps(result, ensure_ascii=True, indent=2))
    if result['findings'] or result['skipped']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
