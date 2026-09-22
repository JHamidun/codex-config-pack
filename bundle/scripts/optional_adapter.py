"""Execute one explicit optional-engine request. Check mode never imports an engine."""
import argparse
import contextlib
import importlib.util
import json
import os
from pathlib import Path
import sys

from adapter_io import runtime, source, staged_output, manifest, write_json

DEPENDENCIES = {
    'enhance': ['PIL'], 'upscale': ['PIL'], 'web-assets': ['PIL'], 'gif': ['PIL'],
    'sticker-static': ['PIL'], 'sticker-video': ['PIL'], 'ocr-restore': [], 'ocr-extract': ['PIL'],
    'segment': ['PIL', 'rembg'],
    'ace-submit': [], 'ace-fetch': [], 'privacy-redact': ['opf'], 'privacy-restore': [],
    'edit-banana': ['PIL'], 'cad-inspect': ['pythoncom', 'win32com'], 'cad-create': ['pythoncom', 'win32com'],
}


def check(operation):
    if operation not in DEPENDENCIES:
        raise ValueError('Unknown operation')
    return {'operation': operation, 'modules': {name: importlib.util.find_spec(name) is not None
            for name in DEPENDENCIES[operation]}, 'engine_live_tested': False,
            'engine_paths_and_models': 'Validate the explicit request at run time; check does not download or connect'}


def execute(root, job):
    import media_adapter
    import engine_adapter
    root = runtime.workspace_root(root)
    operation = job['operation']
    operations = dict(media_adapter.OPERATIONS, **engine_adapter.OPERATIONS)
    if operation not in operations:
        raise ValueError('Unknown adapter operation')
    dependencies = check(operation)
    if not all(dependencies['modules'].values()):
        raise ValueError('Missing optional module; run check and follow OPTIONAL-ADAPTERS.md')
    with staged_output(root, job['output']) as out:
        result = operations[operation](root, job, out)
        write_json(out / 'adapter-result.json', {'operation': operation, 'result': result})
        files = manifest(out)
    return {'operation': operation, 'output': job['output'], 'result': result, 'artifacts': files}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    inspect = sub.add_parser('check')
    inspect.add_argument('operation', choices=sorted(DEPENDENCIES))
    run = sub.add_parser('run')
    run.add_argument('--workspace', required=True)
    run.add_argument('--request', required=True, help='Workspace-relative UTF-8 JSON request')
    args = parser.parse_args()
    try:
        if args.action == 'check':
            result = check(args.operation)
        else:
            root = runtime.workspace_root(args.workspace)
            request = json.loads(runtime.read_limited(source(root, args.request)))
            with open(os.devnull, 'w') as sink, contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
                result = execute(root, request)
        print(json.dumps({'status': 'ok', 'result': result}, ensure_ascii=True))
    except Exception as exc:
        # Engine exceptions may contain input text, access tokens or private paths.
        print(json.dumps({'status': 'error', 'error_type': type(exc).__name__,
                          'message': 'Adapter failed. Check request, optional dependencies and synthetic engine smoke test; no output was committed.'}))
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
