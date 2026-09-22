"""Shared boundaries for optional adapters; no imports of optional engines."""
import contextlib
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import subprocess
import tempfile

_spec = importlib.util.spec_from_file_location('pack_runtime_io', Path(__file__).with_name('runtime.py'))
assert _spec and _spec.loader
runtime = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(runtime)


def source(root, name):
    path = runtime.artifact_path(root, name)
    if not path.is_file():
        raise ValueError('Input artifact is missing')
    return path


def number(value, minimum, maximum):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError('Expected a finite number')
    if not minimum <= value <= maximum:
        raise ValueError('Numeric option is outside the documented bounds')
    return value


def integer(value, minimum, maximum):
    number(value, minimum, maximum)
    if not isinstance(value, int):
        raise ValueError('Expected an integer')
    return value


def installed_path(value, directory=False):
    path = Path(value)
    if not path.is_absolute():
        raise ValueError('Use an explicit absolute engine/checkpoint path')
    runtime.no_links(path)
    if any(p.casefold() in runtime.PROTECTED for p in path.parts):
        raise ValueError('An engine cannot reside in a protected source tree')
    if not (path.is_dir() if directory else path.is_file()):
        raise ValueError('Explicit engine/checkpoint path is missing')
    return path.resolve()


def process(argv, *, cwd=None, timeout=300, data=None, capture=False):
    """Fixed argument lists only; never expose engine logs or exception payloads."""
    result = subprocess.run([str(a) for a in argv], cwd=cwd, input=data,
                            stdout=subprocess.PIPE if capture else subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL, timeout=timeout, check=False)
    if result.returncode:
        raise ValueError('Engine failed; verify its isolated setup with synthetic input')
    return result.stdout


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=True, indent=2) + '\n', encoding='utf-8')


@contextlib.contextmanager
def staged_output(root, relative):
    target = runtime.artifact_path(root, relative)
    if target.exists():
        raise ValueError('Output already exists; choose a new run directory')
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.pack-run-', dir=target.parent) as temporary:
        stage = Path(temporary) / 'result'
        stage.mkdir(mode=0o700)
        yield stage
        runtime.no_links(target)
        if target.exists():
            raise ValueError('Output appeared during execution; refusing to replace it')
        os.rename(stage, target)


def manifest(directory):
    result = []
    for path in sorted(directory.rglob('*')):
        runtime.no_links(path)
        if path.is_file():
            with path.open('rb') as handle:
                digest = hashlib.file_digest(handle, 'sha256').hexdigest()
            result.append({'file': path.relative_to(directory).as_posix(),
                           'bytes': path.stat().st_size, 'sha256': digest})
    return result
