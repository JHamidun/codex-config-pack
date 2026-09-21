"""Reviewed offline workflow helpers. No provider calls or legacy script execution."""
import argparse
import csv
from decimal import Decimal, InvalidOperation
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile
import uuid
from typing import Any

PROTECTED = {'.claude', '.agents', '.brain', '_casebook', '.git', '.snapshots'}
PRIVATE_FILES = {'.env', 'auth.json', 'credentials.json', '.credentials.master.env'}
MAX_BYTES = 20_000_000


def no_links(path):
    for part in (path, *path.parents):
        if part.is_symlink() or (hasattr(part, 'is_junction') and part.is_junction()):
            raise ValueError('Refusing a link or junction')


def workspace_root(value):
    path = Path(value).absolute()
    no_links(path)
    path = path.resolve()
    if not path.is_dir() or path == Path(path.anchor) or path == Path.home().resolve():
        raise ValueError('Use an existing project workspace, not a home or filesystem root')
    if any(p.casefold() in PROTECTED - {'.snapshots'} for p in path.parts):
        raise ValueError('Protected source cannot be a workspace')
    return path


def artifact_path(root, relative):
    rel = PurePosixPath(relative)
    if not relative or rel.is_absolute() or '..' in rel.parts or '\\' in relative or ':' in relative:
        raise ValueError('Use a relative artifact path inside the workspace')
    if any(p != p.rstrip(' .') for p in rel.parts):
        raise ValueError('Ambiguous Windows path component')
    if any(p.casefold() in PROTECTED or p.casefold() in PRIVATE_FILES for p in rel.parts):
        raise ValueError('Refusing protected or private files')
    if any(p.casefold().startswith('.env.') for p in rel.parts) or rel.suffix in {'.source', '.session', '.db'}:
        raise ValueError('Refusing source or private-state files')
    path = root / Path(*rel.parts)
    no_links(path)
    if not path.resolve().is_relative_to(root):
        raise ValueError('Artifact escapes workspace')
    return path


def read_limited(path):
    no_links(path)
    with path.open('rb') as handle:
        data = handle.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ValueError('File exceeds the 20 MB offline helper limit')
    return data


def git_status(root):
    root = workspace_root(root)
    result = subprocess.run(
        ['git', '--no-optional-locks', '-C', str(root), 'status', '--porcelain=v2', '-z', '--branch'],
        capture_output=True, timeout=30,
    )
    if result.returncode:
        raise ValueError('Git status failed; check repository and Git access')
    report: dict[str, Any] = {'branch': None, 'head': None, 'tracking': None, 'ahead': 0, 'behind': 0,
              'staged': [], 'modified': [], 'deleted': [], 'renamed': [], 'untracked': [], 'unmerged': []}
    records = iter(result.stdout.decode('utf-8', errors='surrogateescape').split('\0'))
    for record in records:
        if not record:
            continue
        if record.startswith('# branch.head '):
            report['branch'] = record.removeprefix('# branch.head ')
        elif record.startswith('# branch.oid '):
            report['head'] = record.removeprefix('# branch.oid ')
        elif record.startswith('# branch.upstream '):
            report['tracking'] = record.removeprefix('# branch.upstream ')
        elif record.startswith('# branch.ab '):
            ahead, behind = record.removeprefix('# branch.ab ').split()
            report['ahead'], report['behind'] = int(ahead[1:]), int(behind[1:])
        elif record.startswith('? '):
            report['untracked'].append(record[2:])
        elif record.startswith('u '):
            report['unmerged'].append(record.split(' ', 10)[10])
        elif record.startswith(('1 ', '2 ')):
            fields = record.split(' ', 9 if record.startswith('2 ') else 8)
            xy, path = fields[1], fields[-1]
            if xy[0] != '.':
                report['staged'].append(path)
            if xy[1] != '.' or fields[2] not in {'N...', 'S...'}:
                report['modified'].append(path)
            if 'D' in xy:
                report['deleted'].append(path)
            if record.startswith('2 '):
                original = next(records, None)
                if original is None:
                    raise ValueError('Incomplete Git rename record')
                report['renamed'].append({'from': original, 'to': path})
        elif not record.startswith(('# ', '! ')):
            raise ValueError('Unsupported Git status record')
    report['clean'] = not any(report[key] for key in ('staged', 'modified', 'untracked', 'unmerged'))
    return report


def csv_profile(path, numeric=None, keys=None, delimiter=None, max_rows=100_000):
    numeric, keys = numeric or [], keys or []
    if not 1 <= max_rows <= 100_000:
        raise ValueError('max_rows must be between 1 and 100000')
    data = read_limited(Path(path)).decode('utf-8-sig')
    if delimiter is None:
        try:
            delimiter = csv.Sniffer().sniff(data[:8192], delimiters=',;\t|').delimiter
        except csv.Error:
            delimiter = ','
    if delimiter not in {',', ';', '\t', '|'}:
        raise ValueError('Unsupported delimiter')
    import io
    reader = csv.reader(io.StringIO(data, newline=''), delimiter=delimiter, strict=True)
    header = next(reader, None)
    if not header or any(not h.strip() for h in header) or len(set(header)) != len(header):
        raise ValueError('CSV needs nonempty, unique column headers')
    if set(numeric + keys) - set(header):
        raise ValueError('Requested columns are absent from the CSV header')
    columns: list[dict[str, Any]] = [{'name': h, 'missing': 0, 'distinct': 0} for h in header]
    distinct: list[set[str]] = [set() for h in header]
    metrics: dict[str, dict[str, Any]] = {h: {'valid': 0, 'invalid': 0, 'sum': Decimal(0), 'min': None, 'max': None} for h in numeric}
    key_indices = [header.index(k) for k in keys]
    seen_keys = set()
    duplicates, rows = 0, 0
    for row in reader:
        if len(row) != len(header):
            raise ValueError('CSV row width differs from header')
        rows += 1
        if rows > max_rows:
            raise ValueError('CSV exceeds max_rows; use an explicitly reviewed larger-data workflow')
        if keys:
            key = tuple(row[i] for i in key_indices)
            duplicates += key in seen_keys
            seen_keys.add(key)
        for i, raw in enumerate(row):
            value = raw.strip()
            if not value:
                columns[i]['missing'] += 1
                continue
            distinct[i].add(raw)
            if header[i] in metrics:
                metric = metrics[header[i]]
                try:
                    number = Decimal(value)
                    if not number.is_finite() or abs(number.adjusted()) > 100:
                        raise InvalidOperation
                except InvalidOperation:
                    metric['invalid'] += 1
                    continue
                metric['valid'] += 1
                metric['sum'] += number
                metric['min'] = number if metric['min'] is None else min(number, metric['min'])
                metric['max'] = number if metric['max'] is None else max(number, metric['max'])
    for i, column in enumerate(columns):
        column['distinct'] = len(distinct[i])
        if column['name'] in metrics:
            metric = metrics[column['name']]
            metric['mean'] = metric['sum'] / metric['valid'] if metric['valid'] else None
            column['numeric'] = {k: str(v) if isinstance(v, Decimal) else v for k, v in metric.items()}
    return {'rows': rows, 'delimiter': delimiter, 'columns': columns, 'key_columns': keys,
            'duplicate_key_rows': duplicates if keys else None, 'numeric_scope': 'explicit columns; valid finite cells only'}


def snapshot_create(workspace, relative):
    root = workspace_root(workspace)
    source = artifact_path(root, relative)
    content = read_limited(source)
    base = root / '.snapshots'
    no_links(base)
    base.mkdir(exist_ok=True)
    ident = uuid.uuid4().hex
    folder = base / ident
    folder.mkdir()
    no_links(folder)
    metadata = {'schema': 1, 'id': ident, 'path': relative, 'sha256': hashlib.sha256(content).hexdigest()}
    with (folder/'content').open('xb') as handle:
        handle.write(content)
    with (folder/'metadata.json').open('x', encoding='utf-8') as handle:
        json.dump(metadata, handle, indent=2)
    return metadata


def snapshot_restore(workspace, ident):
    root = workspace_root(workspace)
    if not re.fullmatch('[a-f0-9]{32}', ident):
        raise ValueError('Invalid snapshot identifier')
    folder = root / '.snapshots' / ident
    metadata = json.loads(read_limited(folder/'metadata.json'))
    if metadata.get('schema') != 1 or metadata.get('id') != ident:
        raise ValueError('Invalid snapshot metadata')
    target = artifact_path(root, metadata['path'])
    content = read_limited(folder/'content')
    if hashlib.sha256(content).hexdigest() != metadata.get('sha256'):
        raise ValueError('Snapshot checksum mismatch')
    before = snapshot_create(root, metadata['path']) if target.exists() else None
    target.parent.mkdir(parents=True, exist_ok=True)
    no_links(target)
    descriptor, temporary = tempfile.mkstemp(prefix='.snapshot-', dir=target.parent)
    try:
        with os.fdopen(descriptor, 'wb') as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        no_links(target)
        if before and hashlib.sha256(read_limited(target)).hexdigest() != before['sha256']:
            raise ValueError('Target changed during restore')
        if not before and target.exists():
            raise ValueError('Target appeared during restore')
        os.replace(temporary, target)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    return {'restored': metadata['path'], 'snapshot_id': ident, 'before_restore_id': before['id'] if before else None}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    status = commands.add_parser('git-status')
    status.add_argument('--workspace', type=Path, required=True)
    profile = commands.add_parser('csv-profile')
    profile.add_argument('file', type=Path)
    profile.add_argument('--numeric', action='append', default=[])
    profile.add_argument('--key', action='append', default=[])
    profile.add_argument('--delimiter')
    profile.add_argument('--max-rows', type=int, default=100_000)
    snapshot = commands.add_parser('snapshot')
    snapshot.add_argument('--workspace', type=Path, required=True)
    operation = snapshot.add_mutually_exclusive_group(required=True)
    operation.add_argument('--file')
    operation.add_argument('--restore')
    args = parser.parse_args()
    try:
        if args.command == 'git-status':
            result = git_status(args.workspace)
        elif args.command == 'csv-profile':
            result = csv_profile(args.file, args.numeric, args.key, args.delimiter, args.max_rows)
        elif args.restore:
            result = snapshot_restore(args.workspace, args.restore)
        else:
            result = snapshot_create(args.workspace, args.file)
        print(json.dumps({'status': 'ok', 'result': result}, ensure_ascii=True, indent=2))
    except (OSError, ValueError, csv.Error, subprocess.SubprocessError):
        print(json.dumps({'status': 'error', 'code': 'workflow_failed',
                          'message': 'Check input format, paths, permissions and helper limits. No raw input or exception payload is logged.'}))
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
