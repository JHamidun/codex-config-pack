"""Bounded project-state operations for native Codex planning procedures.

No Git commits, provider calls, source-home discovery, or legacy script execution.
Markdown remains the source of truth; inventory is not a claim of task completion.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import time
import uuid

_spec = importlib.util.spec_from_file_location('pack_runtime', Path(__file__).with_name('runtime.py'))
assert _spec is not None and _spec.loader is not None
runtime = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(runtime)

REQUIRED = ('PROJECT.md', 'REQUIREMENTS.md', 'ROADMAP.md', 'STATE.md')
MAX_FILES = 2000


def planning_path(root, relative=''):
    return runtime.artifact_path(root, '.planning' + ('/' + relative if relative else ''))


def text_file(root, relative):
    return runtime.read_limited(runtime.artifact_path(root, relative)).decode('utf-8-sig')


def inspect(workspace):
    root = runtime.workspace_root(workspace)
    base = planning_path(root)
    result = {'initialized': (base / 'PROJECT.md').is_file(), 'missing': [], 'files': [],
              'phases': [], 'checkpoints': [], 'ready_to_execute': False,
              'verification': 'inventory-only; inspect task evidence before reporting completion'}
    if not base.exists():
        result['missing'] = list(REQUIRED)
        return result
    result['missing'] = [name for name in REQUIRED if not planning_path(root, name).is_file()]
    # Walk explicitly so no junction or symlink can silently redirect discovery.
    pending = [base]
    paths: list[Path] = []
    while pending:
        directory = pending.pop()
        for path in sorted(directory.iterdir()):
            runtime.no_links(path)
            if len(paths) + len(pending) >= MAX_FILES:
                raise ValueError('Planning tree exceeds the bounded inventory limit')
            if path.is_dir():
                pending.append(path)
            elif path.is_file():
                paths.append(path)
    for path in sorted(paths):
        relative = path.relative_to(root).as_posix()
        data = runtime.read_limited(runtime.artifact_path(root, relative))
        result['files'].append({'path': relative, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
        if path.parent == base / 'checkpoints' and path.suffix == '.md':
            result['checkpoints'].append(relative)
    phases = sorted({p.parent for p in paths if p.parent.parent == base / 'phases'})
    executable_plans = 0
    for phase in phases:
        plans = sorted(p for p in paths if p.parent == phase and p.name.endswith('PLAN.md'))
        summaries = sorted(p for p in paths if p.parent == phase and p.name.endswith('SUMMARY.md'))
        verifications = sorted(p for p in paths if p.parent == phase and p.name.endswith('VERIFICATION.md'))
        for plan in plans:
            body = runtime.read_limited(plan).decode('utf-8-sig')
            if re.search(r'<task(?:\s|>)', body) and re.search(r'<verify(?:\s|>)', body):
                executable_plans += 1
        result['phases'].append({
            'path': phase.relative_to(root).as_posix(), 'plan_count': len(plans),
            'summary_count': len(summaries), 'verification_files': [p.name for p in verifications],
            'verified': False, 'evidence_review_required': True,
            'plans_without_summary': [p.name for p in plans if p.with_name(p.name.replace('PLAN.md', 'SUMMARY.md')) not in summaries],
        })
    result['ready_to_execute'] = not result['missing'] and executable_plans > 0
    return result


def initialize(workspace, spec_relative):
    root = runtime.workspace_root(workspace)
    spec_text = text_file(root, spec_relative)
    if not spec_text.strip():
        raise ValueError('Project brief must not be empty')
    base = planning_path(root)
    if base.exists():
        raise ValueError('Planning already exists; inspect and update explicitly without resetting it')
    files = {
        'PROJECT.md': spec_text,
        'STATE.md': '# Project state\n\nStatus: initialized; requirements and roadmap pending.\n\n## Next action\n\nReview the brief, define requirements, then create a roadmap.\n',
        'config.json': json.dumps({'runtime': 'codex', 'model_profile': 'inherit',
                                  'commit_docs': False, 'parallelization': False}, indent=2) + '\n',
    }
    stage = runtime.artifact_path(root, '.planning-init-' + uuid.uuid4().hex)
    stage.mkdir()
    try:
        for name, content in files.items():
            with (stage / name).open('x', encoding='utf-8', newline='\n') as handle:
                handle.write(content)
        for attempt in range(6):
            runtime.no_links(base)
            if base.exists():
                raise ValueError('Planning appeared during initialization; preserving it')
            try:
                stage.rename(base)
                break
            except PermissionError:
                if attempt == 5:
                    raise
                time.sleep(0.05 * (2 ** attempt))
    except BaseException:
        # Remove only files created by this invocation, never a pre-existing tree.
        if stage.exists():
            runtime.no_links(stage)
            for name in files:
                target = stage / name
                runtime.no_links(target)
                if target.is_file():
                    target.unlink()
            stage.rmdir()
        raise
    return {'created': ['.planning/' + name for name in files],
            'next': 'Create REQUIREMENTS.md and ROADMAP.md from real scope; do not fabricate implementation evidence.'}


def checkpoint(workspace, note_relative):
    root = runtime.workspace_root(workspace)
    base = planning_path(root)
    if not base.is_dir():
        raise ValueError('No planning directory; inspect the selected workspace')
    note = text_file(root, note_relative)
    if not note.strip():
        raise ValueError('Checkpoint must contain actual continuation context')
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    relative = 'checkpoints/' + stamp + '-' + uuid.uuid4().hex[:12] + '.md'
    target = planning_path(root, relative)
    target.parent.mkdir(exist_ok=True)
    with target.open('x', encoding='utf-8', newline='\n') as handle:
        handle.write(note)
    return {'path': target.relative_to(root).as_posix(), 'sha256': hashlib.sha256(target.read_bytes()).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', type=Path, required=True)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('inspect')
    init = sub.add_parser('init')
    init.add_argument('--spec', required=True, help='Workspace-relative Markdown brief')
    pause = sub.add_parser('checkpoint')
    pause.add_argument('--note', required=True, help='Workspace-relative continuation note')
    args = parser.parse_args()
    try:
        if args.command == 'inspect':
            result = inspect(args.workspace)
        elif args.command == 'init':
            result = initialize(args.workspace, args.spec)
        else:
            result = checkpoint(args.workspace, args.note)
    except (OSError, ValueError, UnicodeError):
        parser.exit(2, 'Planning operation failed: check workspace, safe relative input, existing state and file limits. No source fallback was attempted.\n')
    print(json.dumps(result, ensure_ascii=True, indent=2))


if __name__ == '__main__':
    main()
