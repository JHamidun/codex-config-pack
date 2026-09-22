"""Explicit project-owned notes, lexical retrieval and provenance graph. Offline only."""
import argparse
from collections import deque
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import re

_spec = importlib.util.spec_from_file_location('pack_runtime', Path(__file__).with_name('runtime.py'))
assert _spec is not None and _spec.loader is not None
runtime = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(runtime)

MAX_NOTES = 2000
MAX_NOTE_BYTES = 40_000
IDENTIFIER = re.compile(r'[a-f0-9]{32}')
SECRET = re.compile(r'-----BEGIN .{0,20}PRIVATE KEY-----|\b(?:gh[pousr]_|xox[baprs]-|sk-proj-)[\w-]{20,}|(?im:^\s*(?:password|api[_-]?key|access[_-]?token)\s*[:=]\s*[^\s<]{8,})')


def notes_root(workspace):
    root = runtime.workspace_root(workspace)
    return root, runtime.artifact_path(root, '.codex-context/memory/notes')


def load_notes(workspace):
    root, notes = notes_root(workspace)
    if not notes.exists():
        return []
    paths = sorted(notes.iterdir())
    if len(paths) > MAX_NOTES:
        raise ValueError('Memory exceeds the local helper limit; select a narrower workspace')
    records = []
    for path in paths:
        runtime.no_links(path)
        if path.suffix != '.json' or not IDENTIFIER.fullmatch(path.stem):
            raise ValueError('Unexpected memory record; inspect rather than silently skipping')
        raw = runtime.read_limited(path)
        if len(raw) > MAX_NOTE_BYTES * 2:
            raise ValueError('Oversized memory record')
        row = json.loads(raw)
        if not isinstance(row, dict) or row.get('id') != path.stem or row.get('schema') != 1:
            raise ValueError('Invalid memory record schema')
        if not isinstance(row.get('topic'), str) or not isinstance(row.get('content'), str):
            raise ValueError('Invalid memory record contents')
        if SECRET.search(row['content']) or SECRET.search(row['topic']):
            raise ValueError('Potential secret in note; refusing to display it')
        if not isinstance(row.get('links'), list) or any(not isinstance(x, str) or not IDENTIFIER.fullmatch(x) for x in row['links']):
            raise ValueError('Invalid note graph')
        if not isinstance(row.get('source'), str) or not isinstance(row.get('created_at'), str):
            raise ValueError('Invalid note provenance')
        runtime.artifact_path(root, row['source'])
        identity = json.dumps([row['topic'], row['content'], row['links']], ensure_ascii=True).encode('utf-8')
        if hashlib.sha256(identity).hexdigest()[:32] != row['id']:
            raise ValueError('Note identity does not match its contents')
        records.append(row)
    return records


def add(workspace, note_relative, topic, links=None):
    root, notes = notes_root(workspace)
    source = runtime.artifact_path(root, note_relative)
    if source.suffix.casefold() not in {'.md', '.txt'}:
        raise ValueError('Supply a curated Markdown/text note, not a raw session or database')
    raw = runtime.read_limited(source)
    if len(raw) > MAX_NOTE_BYTES:
        raise ValueError('Curate a note of at most 40 KB')
    content = raw.decode('utf-8-sig').strip()
    if not content or not topic.strip() or len(topic) > 160 or SECRET.search(content) or SECRET.search(topic):
        raise ValueError('Empty/invalid note or potential credential; secret values are never reported')
    existing = load_notes(root)
    links = sorted(set(links or []))
    known = {n['id'] for n in existing}
    if any(link not in known for link in links):
        raise ValueError('Link must reference an existing local note ID')
    identity = json.dumps([topic.strip(), content, links], ensure_ascii=True).encode('utf-8')
    note_id = hashlib.sha256(identity).hexdigest()[:32]
    if note_id in known:
        return {'id': note_id, 'created': False, 'semantic_index': 'not-configured'}
    if len(existing) >= MAX_NOTES:
        raise ValueError('Note limit reached')
    notes.mkdir(parents=True, exist_ok=True)
    ignored = runtime.artifact_path(root, '.codex-context/.gitignore')
    if not ignored.exists():
        with ignored.open('x', encoding='utf-8', newline='\n') as handle:
            handle.write('*\n')
    row = {'schema': 1, 'id': note_id, 'topic': topic.strip(), 'content': content,
           'links': links, 'created_at': datetime.now(timezone.utc).isoformat(),
           'source': source.relative_to(root).as_posix(), 'source_sha256': hashlib.sha256(raw).hexdigest()}
    target = runtime.artifact_path(root, '.codex-context/memory/notes/' + note_id + '.json')
    with target.open('x', encoding='utf-8', newline='\n') as handle:
        json.dump(row, handle, ensure_ascii=True, indent=2)
        handle.write('\n')
    return {'id': note_id, 'created': True, 'semantic_index': 'not-configured',
            'privacy': 'Local notes only. Git ignore does not untrack files already committed.'}


def query(workspace, text, limit=8):
    if not 1 <= limit <= 50:
        raise ValueError('Limit must be 1..50')
    words = set(re.findall(r'[\w-]+', text.casefold()))
    if not words:
        raise ValueError('Query must not be empty')
    ranked = []
    for note in load_notes(workspace):
        topic = note['topic'].casefold()
        body = note['content'].casefold()
        score = sum(3 if w in topic else 1 for w in words if w in topic or w in body)
        if score:
            start = min((body.index(w) for w in words if w in body), default=0)
            ranked.append((score, {'id': note['id'], 'topic': note['topic'],
                                  'excerpt': note['content'][max(0, start - 100):start + 1100],
                                  'source': note['source'], 'created_at': note['created_at'], 'links': note['links']}))
    return [item for _, item in sorted(ranked, key=lambda item: (-item[0], item[1]['id']))[:limit]]


def graph(workspace, note_id, depth=2):
    if not 0 <= depth <= 6:
        raise ValueError('Depth must be 0..6')
    rows = {n['id']: n for n in load_notes(workspace)}
    if note_id not in rows:
        raise ValueError('Unknown note ID')
    adjacent = {key: set(row['links']) for key, row in rows.items()}
    for key, row in rows.items():
        for linked in row['links']:
            if linked not in rows:
                raise ValueError('Dangling graph link; inspect memory integrity')
            adjacent[linked].add(key)
    queue = deque([(note_id, 0)])
    visited = {note_id}
    nodes = []
    while queue:
        key, distance = queue.popleft()
        nodes.append({'id': key, 'topic': rows[key]['topic'], 'distance': distance})
        if distance < depth:
            for linked in sorted(adjacent[key] - visited):
                visited.add(linked)
                queue.append((linked, distance + 1))
    return {'nodes': nodes, 'edges': [{'from': key, 'to': linked} for key in sorted(visited)
                                   for linked in rows[key]['links'] if linked in visited]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', type=Path, required=True)
    sub = parser.add_subparsers(dest='command', required=True)
    add_cmd = sub.add_parser('add')
    add_cmd.add_argument('--note', required=True)
    add_cmd.add_argument('--topic', required=True)
    add_cmd.add_argument('--link', action='append', default=[])
    search = sub.add_parser('query')
    search.add_argument('text')
    search.add_argument('--limit', type=int, default=8)
    edges = sub.add_parser('graph')
    edges.add_argument('id')
    edges.add_argument('--depth', type=int, default=2)
    sub.add_parser('stats')
    args = parser.parse_args()
    try:
        if args.command == 'add':
            result = add(args.workspace, args.note, args.topic, args.link)
        elif args.command == 'query':
            result = query(args.workspace, args.text, args.limit)
        elif args.command == 'graph':
            result = graph(args.workspace, args.id, args.depth)
        else:
            notes = load_notes(args.workspace)
            result = {'notes': len(notes), 'links': sum(len(n['links']) for n in notes),
                      'semantic_index': 'not-configured', 'background_jobs': False}
    except (OSError, ValueError, KeyError, TypeError, UnicodeError):
        parser.exit(2, 'Memory operation failed: check curated input, workspace, record integrity and limits. No private source was scanned.\n')
    print(json.dumps(result, ensure_ascii=True, indent=2))


if __name__ == '__main__':
    main()
