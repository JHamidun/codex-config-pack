"""Search the cold skill/command catalog without loading recipe bodies."""
import argparse
import json
import hashlib
from pathlib import Path
import re


def search(root, query, limit=12):
    entries = json.loads((root / 'catalog.json').read_text(encoding='utf-8'))['entries']
    words = re.findall(r'[\w-]+', query.casefold())
    ranked = []
    for entry in entries:
        name = entry['name'].casefold()
        haystack = (name + ' ' + entry['description']).casefold()
        score = sum(3 if word in name else 1 for word in words if word in haystack)
        normalized = query.casefold().strip().removeprefix('$').removeprefix('/')
        if normalized in (entry['id'].casefold(), name):
            score += 100
        if normalized in [alias.casefold() for alias in entry.get('execution', {}).get('aliases', [])]:
            score += 100
        if score or not words:
            ranked.append((score, entry))
    return [entry for _, entry in sorted(ranked, key=lambda item: (-item[0], item[1]['id']))[:limit]]


def verified_text(root, relative, manifest, workspace=None):
    path = root / relative
    if not path.resolve().is_relative_to(root.resolve()) or path.name.endswith('.source'):
        raise ValueError('Unsafe execution document path')
    for part in (path, *path.parents):
        if part.is_symlink() or (hasattr(part, 'is_junction') and part.is_junction()):
            raise ValueError('Execution documents cannot use links')
    expected = manifest['files'].get(relative)
    if not isinstance(expected, str) or not re.fullmatch(r'[a-f0-9]{64}', expected):
        raise ValueError('Execution document is not listed in the manifest')
    raw = path.read_bytes()
    if expected != hashlib.sha256(raw).hexdigest():
        raise ValueError('Execution document checksum mismatch')
    text = raw.decode('utf-8').replace('${CODEX_PACK_ROOT}', root.resolve().as_posix())
    if workspace is not None:
        text = text.replace('${CODEX_WORKSPACE}', Path(workspace).resolve().as_posix())
    return text


def prepare(root, selector, workspace=None):
    manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
    catalog = json.loads(verified_text(root, 'catalog.json', manifest))
    selected = [e for e in catalog['entries'] if selector in {e['id'], e['name']}]
    if len(selected) != 1:
        raise ValueError('Select exactly one catalog ID; missing or ambiguous name')
    entry = selected[0]
    execution = entry.get('execution', {'mode': 'needs-adapter'})
    result = {'id': entry['id'], 'mode': execution['mode'], 'executed': False,
              'legacy_dependencies': entry.get('dependencies', [])}
    if execution['mode'] == 'native-helper':
        verified_text(root, execution['helper'], manifest)
        for helper in execution.get('helpers', []):
            verified_text(root, helper, manifest)
        result['instructions'] = verified_text(root, execution['recipe'], manifest)
        result['verification'] = execution['verification']
    elif execution['mode'] == 'instructions':
        result['instructions'] = verified_text(root, entry['path'], manifest)
        result['verification'] = 'not-executed'
    elif execution['mode'] in {'native-procedure', 'connection-required'}:
        for helper in execution.get('helpers', []):
            verified_text(root, helper, manifest)
        result['instructions'] = verified_text(root, execution['recipe'], manifest, workspace)
        result['verification'] = execution['verification']
        result['domain_reference'] = execution['domain_reference']
        verified_text(root, execution['domain_reference'], manifest, workspace)
        if 'operation' in execution:
            result['operation'] = execution['operation']
        if execution['mode'] == 'connection-required':
            result['service'] = execution['service']
            result['required'] = execution['required']
            result['connected'] = None
            result['blocker'] = 'Verify an actual authorized capability for the required action. This pack does not supply or prove the connection.'
    else:
        result['reference_path'] = entry['path']
        result['blocker'] = 'No reviewed executable adapter is registered. Do not execute historical commands or .source files.'
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('query', nargs='?')
    parser.add_argument('--prepare', metavar='CATALOG_ID')
    parser.add_argument('--read-reference', metavar='PACK_RELATIVE_PATH')
    parser.add_argument('--workspace', type=Path)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument('--limit', type=int, default=12)
    args = parser.parse_args()
    if not 1 <= args.limit <= 100:
        parser.error('--limit must be between 1 and 100')
    if args.prepare and args.read_reference:
        parser.error('Choose --prepare or --read-reference')
    if args.prepare or args.read_reference:
        try:
            if args.prepare:
                result = prepare(args.root, args.prepare, args.workspace)
            else:
                manifest = json.loads((args.root / 'manifest.json').read_text(encoding='utf-8'))
                result = {'reference': args.read_reference, 'executable': False,
                          'content': verified_text(args.root, args.read_reference, manifest, args.workspace)}
        except (OSError, ValueError, KeyError):
            parser.exit(2, 'Recipe preparation failed: check selector, manifest integrity and installation.\n')
    elif args.query is not None:
        result = search(args.root, args.query, args.limit)
    else:
        parser.error('Provide a query or --prepare CATALOG_ID')
    print(json.dumps(result, ensure_ascii=True, indent=2))


if __name__ == '__main__':
    main()
