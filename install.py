"""Install the portable pack additively. Python 3.11+, standard library only."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import tempfile
import time

REPO = Path(__file__).resolve().parent
PACK_ID = 'hamidun-pack'
PROTECTED = {'.claude', '.agents', '.brain', '_casebook'}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def safe_relative(value):
    path = PurePosixPath(value)
    if not value or path.is_absolute() or '..' in path.parts or '\\' in value or ':' in value:
        raise ValueError('Unsafe manifest path')
    return Path(*path.parts)


def no_links(path):
    for part in (path, *path.parents):
        if part.is_symlink() or (hasattr(part, 'is_junction') and part.is_junction()):
            raise ValueError('Links/reparse points are not supported: ' + str(part))


def target_root(path):
    root = path.absolute()
    no_links(root)
    if any(part.casefold() in PROTECTED for part in root.parts):
        raise ValueError('Refusing a protected source/shared configuration path')
    if root == Path(root.anchor) or root == Path.home():
        raise ValueError('Use a dedicated Codex home, not a home or filesystem root')
    return root


def atomic_write(path, data):
    no_links(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    no_links(path)
    descriptor, temporary = tempfile.mkstemp(prefix='.pack-', dir=path.parent)
    try:
        with os.fdopen(descriptor, 'wb') as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        for attempt in range(6):
            no_links(path)
            try:
                os.replace(temporary, path)
                break
            except PermissionError:
                if attempt == 5:
                    raise
                time.sleep(0.05 * (2 ** attempt))
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def validate_bundle(bundle):
    no_links(bundle)
    manifest = json.loads((bundle / 'manifest.json').read_text(encoding='utf-8'))
    if manifest.get('schema') != 1:
        raise ValueError('Unsupported bundle schema')
    for name, expected in manifest['files'].items():
        file = bundle / safe_relative(name)
        no_links(file)
        if sha(file.read_bytes()) != expected:
            raise ValueError('Bundle checksum mismatch: ' + name)
    actual = {p.relative_to(bundle).as_posix() for p in bundle.rglob('*') if p.is_file()}
    if actual != set(manifest['files']) | {'manifest.json'}:
        raise ValueError('Unexpected or missing bundle files')
    return manifest


def state_path(root):
    return root / 'pack-manifests' / (PACK_ID + '.json')


def read_state(root):
    path = state_path(root)
    no_links(path)
    if not path.exists():
        return {'schema': 1, 'files': {}}
    state = json.loads(path.read_text(encoding='utf-8'))
    if state.get('schema') != 1:
        raise ValueError('Unsupported installed manifest schema')
    for name, expected in state['files'].items():
        relative = safe_relative(name)
        allowed = name.startswith('packs/' + PACK_ID + '/') or name == 'skills/hamidun-pack/SKILL.md' or (name.startswith('agents/pack-') and len(relative.parts) == 2 and name.endswith('.toml'))
        if not allowed or not isinstance(expected, str) or len(expected) != 64:
            raise ValueError('Installed manifest contains an unowned path')
    return state


def install(bundle, target, dry_run=False, with_agents=False):
    root = target_root(target)
    manifest = validate_bundle(bundle)
    commit = manifest['source_commit']
    if len(commit) != 40 or any(c not in '0123456789abcdef' for c in commit):
        raise ValueError('Invalid source commit')
    pack_root = root / 'packs' / PACK_ID / commit
    state = read_state(root)
    planned = {}
    for name in manifest['files']:
        planned[(pack_root / safe_relative(name)).relative_to(root).as_posix()] = (bundle / safe_relative(name)).read_bytes()
    router = (bundle / 'router/SKILL.md').read_text(encoding='utf-8').replace('${CODEX_PACK_ROOT}', pack_root.as_posix()).encode('utf-8')
    planned['skills/hamidun-pack/SKILL.md'] = router
    if with_agents:
        for file in sorted((bundle / 'agents').glob('*.toml')):
            planned['agents/' + file.name] = file.read_text(encoding='utf-8').replace('${CODEX_PACK_ROOT}', pack_root.as_posix()).encode('utf-8')
    changes, unchanged, foreign_identical = [], [], []
    owned = dict(state['files'])
    for relative, data in planned.items():
        destination = root / safe_relative(relative)
        no_links(destination)
        if destination.exists():
            current = sha(destination.read_bytes())
            if current == sha(data):
                unchanged.append(relative)
                if relative not in owned:
                    foreign_identical.append(relative)
                continue
            if owned.get(relative) != current:
                raise ValueError('Existing user file conflicts; nothing changed: ' + relative)
        changes.append(relative)
    result = {'action': 'install', 'dry_run': dry_run, 'new_or_updated': len(changes), 'unchanged': len(unchanged), 'foreign_identical_not_owned': len(foreign_identical), 'agents_enabled': with_agents, 'config_changed': False}
    if dry_run:
        return result
    # Journal progress after every write so an interrupted install remains removable.
    for relative in changes:
        destination = root / safe_relative(relative)
        no_links(destination)
        if destination.exists() and sha(destination.read_bytes()) != owned.get(relative):
            raise ValueError('Destination changed after preflight: ' + relative)
        owned[relative] = sha(planned[relative])
        atomic_write(state_path(root), (json.dumps({'schema': 1, 'source_commit': commit, 'files': owned}, indent=2) + '\n').encode())
        atomic_write(destination, planned[relative])
    if not state_path(root).exists():
        atomic_write(state_path(root), (json.dumps({'schema': 1, 'source_commit': commit, 'files': owned}, indent=2) + '\n').encode())
    result['pack_root'] = str(pack_root)
    return result


def uninstall(target, dry_run=False):
    root = target_root(target)
    state = read_state(root)
    removed, preserved = [], []
    for relative, expected in state['files'].items():
        file = root / safe_relative(relative)
        no_links(file)
        if not file.exists():
            continue
        if sha(file.read_bytes()) != expected:
            preserved.append(relative)
            continue
        removed.append(relative)
        if not dry_run:
            no_links(file)
            if sha(file.read_bytes()) != expected:
                raise ValueError('File changed during uninstall: ' + relative)
            file.unlink()
    if not dry_run and state_path(root).exists():
        remaining = {name: state['files'][name] for name in preserved}
        atomic_write(state_path(root), (json.dumps({'schema': 1, 'files': remaining}, indent=2) + '\n').encode())
    return {'action': 'uninstall', 'dry_run': dry_run, 'removed': len(removed), 'modified_files_preserved': preserved, 'config_changed': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', type=Path, default=Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex'))))
    parser.add_argument('--bundle', type=Path, default=REPO / 'bundle')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--with-agents', action='store_true')
    parser.add_argument('--uninstall', action='store_true')
    args = parser.parse_args()
    try:
        result = uninstall(args.target, args.dry_run) if args.uninstall else install(args.bundle, args.target, args.dry_run, args.with_agents)
    except (ValueError, OSError, KeyError, json.JSONDecodeError) as exc:
        parser.exit(1, type(exc).__name__ + ': ' + str(exc) + '\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
