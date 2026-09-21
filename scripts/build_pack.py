"""Build a deterministic documentation-first Codex pack from a pinned public checkout."""
import argparse
import collections
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

import yaml  # type: ignore[import-untyped]
import importlib.util

_spec = importlib.util.spec_from_file_location('dependency_audit', Path(__file__).with_name('dependency_audit.py'))
assert _spec is not None and _spec.loader is not None
dependency_audit = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(dependency_audit)

REPO = Path(__file__).resolve().parent.parent
SOURCE_URL = 'https://github.com/JHamidun/claude-code-config-pack'
PIN = 'e9f5f9e019d3c6dc9fe83b00499f223b5f9e6d32'
TEXT = {'.md', '.txt', '.rst', '.csv', '.json', '.yaml', '.yml', '.toml', '.html', '.css', '.svg', '.xml'}
CODE = {'.py', '.js', '.mjs', '.cjs', '.ts', '.tsx', '.jsx', '.sh', '.ps1', '.bat', '.cmd', '.sql'}
SENSITIVE_NAMES = {'.env', '.credentials.master.env', 'auth.json', 'credentials.json'}
DEPENDENCIES = {
    'upstream_home': r'(?:~|\$\{HOME\}|\$HOME)/\.claude|\.claude[/\\]',
    'legacy_tool': r'mcp__|\b(?:Task|Agent|Workflow)\s*\(',
    'runtime_script': r'(?:scripts/|tools/|\b[\w-]+\.(?:py|ps1|sh|mjs)\b)',
    'credential_or_session': r'credentials|api[_ -]?key|oauth|\.session\b',
    'claude_runtime': r'claude\s+(?:-p|--|plugin|mcp)|CLAUDE_CODE_',
}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def frontmatter(text):
    match = re.match(r'\A---\s*\n(.*?)\n---\s*\n?', text, re.S)
    if not match:
        return {}, text
    try:
        meta = yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        return {}, text
    return (meta if isinstance(meta, dict) else {}), text[match.end():]


def slug(value):
    return re.sub(r'[^a-z0-9-]+', '-', value.lower()).strip('-')[:80]


def sanitize(text):
    """Remove literal contacts and workstation identifiers from reference material too."""
    text = re.sub(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', 'user@example.com', text)
    text = re.sub(r'(?i)[A-Z]:[/\\]Users[/\\][^/\\\s`"<>]+', '<UPSTREAM_HOME>', text)
    text = re.sub(r'(?i)[A-Z]:[/\\]Vibecode', '<PROJECT_ROOT>', text)
    text = re.sub(r'/(?:Users|home)/[^/\s`"<>]+', '<UPSTREAM_HOME>', text)
    text = re.sub(r'\b(?:10|172|192)\.(?:\d{1,3}\.){2}\d{1,3}\b', '192.0.2.1', text)
    text = re.sub(r'(?i)(["\'](?:access_token|refresh_token|token|api_key|apiKey)["\']\s*:\s*["\'])[^"\'\n]{20,}(["\'])', r'\1EXAMPLE_TOKEN\2', text)
    text = re.sub(r'(?i)(x-publora-key:\s*)[^"\'\n]+', r'\1$PUBLORA_API_KEY', text)
    text = re.sub(r'(?i)(Authorization:\s*Bearer\s+)[^"\'\n]+', r'\1$API_KEY', text)
    return text


def adapt(text):
    text = sanitize(text)
    text = re.sub(r'(?:~|\$\{HOME\}|\$HOME)/\.claude', '${CODEX_PACK_ROOT}/library', text)
    text = re.sub(r'(?i)[A-Z]:[/\\]Users[/\\][^/\\\s`"<>]+', '<UPSTREAM_HOME>', text)
    text = re.sub(r'(?i)[A-Z]:[/\\]Vibecode', '<PROJECT_ROOT>', text)
    text = re.sub(r'/(?:Users|home)/[^/\s`"<>]+', '<UPSTREAM_HOME>', text)
    text = re.sub(r'\bmodel\s*[:=]\s*["\']?(?:opus|sonnet|haiku|fable)[\w.-]*["\']?', 'model: inherit-current-codex-model', text)
    return text


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding='utf-8', newline='\n')


def build(source, output):
    source = source.resolve()
    output = output.absolute()
    for part in (output, *output.parents):
        if part.is_symlink() or (hasattr(part, 'is_junction') and part.is_junction()):
            raise ValueError('Output cannot contain a link')
    if output.exists():
        raise ValueError('Output must not exist; build into a fresh directory')
    output = output.resolve()
    if source == output or source in output.parents:
        raise ValueError('Never build into the source checkout')
    commit = subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True).strip()
    if commit != PIN:
        raise ValueError('Unexpected source revision; review and update the pin explicitly')
    if subprocess.check_output(['git', '-C', str(source), 'status', '--porcelain', '--untracked-files=no'], text=True).strip():
        raise ValueError('Source tracked files must be clean')
    output.mkdir(parents=True)
    contract = (REPO / 'templates/ADAPTATION.md').read_text(encoding='utf-8')
    entries, omissions, copied = [], [], []
    tracked = subprocess.check_output(['git', '-C', str(source), 'ls-files', '-z'], text=True).split('\0')
    selected = ('skills/', 'commands/', 'agents/', 'rules/', 'config/',
                'get-shit-done/', 'schemas/', 'templates/', 'workflows/')
    for relative in sorted(filter(None, tracked)):
        if not relative.startswith('.claude/') or not relative[len('.claude/'):].startswith(selected):
            continue
        src = source / relative
        rel = Path(relative[len('.claude/'):])
        if any(rel.as_posix().startswith('skills/' + name + '/') for name in ('doc-coauthoring', 'building-an-exo')):
            omissions.append({'path': relative, 'reason': 'upstream-license-not-established'})
            continue
        if rel.as_posix().startswith('skills/n8n/catalog/workflows/'):
            omissions.append({'path': relative, 'reason': 'raw-workflow-export-privacy-boundary'})
            continue
        if src.is_symlink() or any(p.is_symlink() or (hasattr(p, 'is_junction') and p.is_junction()) for p in src.parents if p != source.parent):
            omissions.append({'path': relative, 'reason': 'link'})
            continue
        if src.name in SENSITIVE_NAMES or src.suffix in {'.db', '.session', '.env'}:
            omissions.append({'path': relative, 'reason': 'state-or-secret-file'})
            continue
        is_license = src.name.upper() in {'LICENSE', 'NOTICE', 'COPYING', 'LICENSE-MIT', 'LICENSE-APACHE'}
        if (src.suffix.lower() not in TEXT | CODE and not is_license) or src.stat().st_size > 2_000_000:
            omissions.append({'path': relative, 'reason': 'binary-or-large-asset-not-runtime-validated'})
            continue
        raw = src.read_bytes()
        try:
            text = raw.decode('utf-8-sig').replace('\r\n', '\n')
        except UnicodeDecodeError:
            omissions.append({'path': relative, 'reason': 'non-utf8'})
            continue
        dst = output / 'library' / rel
        if src.suffix.lower() in CODE:
            dst = dst.with_name(dst.name + '.source')
            write(dst, sanitize(text))
            copied.append({'source': relative, 'path': dst.relative_to(output).as_posix(), 'source_sha256': digest(raw), 'status': 'quarantined-source-not-executable'})
            continue
        meta, body = frontmatter(text)
        is_skill = src.name == 'SKILL.md' and rel.parts[0] == 'skills'
        is_command = rel.parts[0] == 'commands' and src.suffix == '.md'
        is_agent = rel.parts[0] == 'agents' and src.suffix == '.md' and bool(meta.get('name'))
        if is_skill or is_command or is_agent:
            kind = 'skill' if is_skill else 'command' if is_command else 'agent'
            name = str(meta.get('name') or (rel.parent.name if is_skill else src.stem))
            description = adapt(str(meta.get('description') or next((s.lstrip('# ').strip() for s in body.splitlines() if s.strip()), name))).replace('\n', ' ')[:700]
            reasons = [label for label, pattern in DEPENDENCIES.items() if re.search(pattern, text, re.I)]
            if is_skill and any(p.suffix.lower() in CODE for p in src.parent.rglob('*') if p.is_file()):
                reasons.append('bundled-reference-code')
            status = 'requires-runtime-review' if reasons else 'instructions-adapted'
            entry = {'id': kind + ':' + rel.as_posix(), 'kind': kind, 'name': name, 'description': description, 'path': dst.relative_to(output).as_posix(), 'source': relative, 'source_sha256': digest(raw), 'status': status, 'dependencies': sorted(set(reasons)), 'live_verified': False}
            entries.append(entry)
            header = '---\nname: ' + json.dumps(name, ensure_ascii=False) + '\ndescription: ' + json.dumps(description, ensure_ascii=False) + '\n---\n\n'
            write(dst, header + contract + '\n\n' + adapt(body))
            if is_agent:
                agent_name = 'pack-' + slug(rel.with_suffix('').as_posix().removeprefix('agents/'))
                agent = {'name': agent_name, 'description': description, 'developer_instructions': contract + '\n\n' + adapt(body)}
                if any(word in name for word in ('reviewer', 'fact-checker', 'security-engineer', 'explore')):
                    agent['sandbox_mode'] = 'read-only'
                toml = '\n'.join(key + ' = ' + json.dumps(value, ensure_ascii=False) for key, value in agent.items()) + '\n'
                write(output / 'agents' / (agent_name + '.toml'), toml)
                entry['agent_file'] = 'agents/' + agent_name + '.toml'
        else:
            write(dst, text if is_license else adapt(text))
        copied.append({'source': relative, 'path': dst.relative_to(output).as_posix(), 'source_sha256': digest(raw), 'status': 'adapted-reference'})
    audit = dependency_audit.audit(output, entries)
    native = json.loads((REPO / 'native/registry.json').read_text(encoding='utf-8'))
    for entry in entries:
        entry['execution'] = native['entries'].get(entry['id'], {
            'mode': 'instructions' if entry['status'] == 'instructions-adapted' else 'needs-adapter',
            'verification': 'not-executed',
        })
    for path in sorted((REPO / 'native').rglob('*')):
        if path.is_file():
            write(output / path.relative_to(REPO), path.read_text(encoding='utf-8'))
    write(output / 'scripts/runtime.py', (REPO / 'scripts/runtime.py').read_text(encoding='utf-8'))
    write(output / 'dependency-audit.json', json.dumps(audit, ensure_ascii=False, indent=2) + '\n')
    # Upstream MCP/hooks are indexed, not activated or silently translated.
    mcp = json.loads((source / '.claude/mcp.json').read_text(encoding='utf-8'))
    integrations = [{'name': name, 'status': 'not-installed', 'reason': 'Requires native connector or individually reviewed Codex MCP configuration and authentication'} for name in sorted(mcp.get('servers', mcp.get('mcpServers', {})))]
    settings = json.loads((source / '.claude/settings.json').read_text(encoding='utf-8'))
    hooks = [{'event': name, 'status': 'not-installed', 'reason': 'Claude event/tool payloads are not a Codex compatibility guarantee'} for name in sorted(settings.get('hooks', {}))]
    write(output / 'catalog.json', json.dumps({'source_url': SOURCE_URL, 'source_commit': commit, 'entries': entries}, ensure_ascii=False, indent=2) + '\n')
    write(output / 'CORE.md', (REPO / 'templates/CORE.md').read_text(encoding='utf-8'))
    write(output / 'ADAPTATION.md', contract)
    write(output / 'scripts/catalog.py', (REPO / 'scripts/catalog.py').read_text(encoding='utf-8'))
    write(output / 'LICENSE', (source / 'LICENSE').read_text(encoding='utf-8'))
    router = '''---
name: hamidun-pack
description: "Use the portable Hamidun workflows for development, research, writing, media and design requests, including Russian prompts. Select one matching recipe and execute its reviewed Codex procedure; distinguish unavailable integrations."
---

# Hamidun Codex pack

Pack root: `${CODEX_PACK_ROOT}`

Search metadata only:

```text
python "${CODEX_PACK_ROOT}/scripts/catalog.py" "task keywords"
```

Search using the user's actual task keywords. Prefer an exact workflow name when
provided. Inspect the few highest-ranked descriptions; keyword ranking alone does
not establish intent. Ask only when the remaining ambiguity matters to execution.

Prepare the selected catalog ID:

```text
python "${CODEX_PACK_ROOT}/scripts/catalog.py" --prepare "<catalog-id>"
```

Read `${CODEX_PACK_ROOT}/CORE.md` and the prepared instructions, then carry out the
requested task with available Codex tools. `--prepare` does not itself perform the
user task. Do not stop at printing the catalog entry or ask the user to run Python.
For `native-helper`, run the reviewed helper exactly as the prepared recipe says,
using task-specific inputs and an explicit workspace. Verify the actual result.
For `instructions`, use native tools and the selected domain guidance.
For `needs-adapter`, report the concrete missing adapter; do not claim completion.
If preparation fails, stop and repair installation integrity instead of executing
an unverified historical fallback. Read only the selected recipe and needed references.
Do not read the full catalog or all recipes into the conversation.
`requires-runtime-review` entries are NOT working script/connector integrations.
Never execute `.source` files or run legacy source-default commands. Resolve native tools first.
`instructions-adapted` means structural conversion, not an end-to-end workflow test.
Optional custom agents have the `pack-` prefix; they inherit the current model and permissions,
except explicitly read-only reviewers. Claude commands are recipes, not installed slash commands.
'''
    write(output / 'router/SKILL.md', router)
    summary = {'entries': dict(collections.Counter(e['kind'] for e in entries)), 'status': dict(collections.Counter(e['status'] for e in entries)), 'reference_files': len(copied), 'quarantined_code_files': sum(e['status'].startswith('quarantined') for e in copied), 'omitted_files': len(omissions), 'mcp_not_activated': len(integrations), 'hook_events_not_activated': len(hooks)}
    report = {'source_url': SOURCE_URL, 'source_commit': commit, 'summary': summary, 'entries': entries, 'integrations': integrations, 'hooks': hooks, 'omissions': omissions, 'source_files': copied}
    write(output / 'compatibility.json', json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    rows = ['# Compatibility matrix', '', 'Structural conversion only. No provider, source script or hook was executed.', '', '| Kind | Name | Status | Dependencies |', '|---|---|---|---|']
    rows += ['| ' + e['kind'] + ' | ' + e['name'].replace('|', '/') + ' | ' + e['status'] + ' | ' + ', '.join(e['dependencies']) + ' |' for e in entries]
    write(output / 'COMPATIBILITY.md', '\n'.join(rows) + '\n')
    manifest = {'schema': 1, 'source_url': SOURCE_URL, 'source_commit': commit, 'files': {p.relative_to(output).as_posix(): digest(p.read_bytes()) for p in sorted(output.rglob('*')) if p.is_file()}}
    write(output / 'manifest.json', json.dumps(manifest, indent=2) + '\n')
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--output', type=Path, default=REPO / 'bundle')
    args = parser.parse_args()
    print(json.dumps(build(args.source, args.output), indent=2))


if __name__ == '__main__':
    main()
