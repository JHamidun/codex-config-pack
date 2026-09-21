---
name: "run-quality-gate"
description: "Прогон quality gate: type-check, build, tests, lint со структурным отчётом. Служебный. Триггеры: «прогони проверки», «проверь перед мержем»."
---

# Codex execution contract

This recipe was adapted from a pinned public source. Its domain guidance is reusable;
its historical provider examples are not a live capability registry.

1. Resolve `${CODEX_PACK_ROOT}` from the installed `hamidun-pack` entrypoint. It is a documentation root, not an environment variable automatically created by Codex.
2. Native tool mapping: Claude `Read/Glob/Grep` means available file/search tools; `Bash` means the current shell; `Write/Edit/MultiEdit` means the supported patch/file tool. Claude `Task/Agent` means native collaboration with a concrete bounded subtask, only when delegation is authorized. Tool names inside old examples are illustrative, not callable API schemas.
3. Claude slash commands become catalog recipes. They are not automatically registered as Codex slash commands. Pass arguments explicitly in the task.
4. Do not execute files ending in `.source`, upstream hook examples, or paths containing `UPSTREAM_HOME`. They are quarantined reference code, NOT a validated runtime. A dependent workflow must first receive a reviewed Codex-owned adapter with explicit state/output roots and tests, or use an available native capability.
5. Do not load secrets, session databases, private memory, or Claude model/provider defaults. Resolve integrations and named environment variables only when required and authorized.
6. Model IDs, MCP names, permission snippets and scheduled-job examples in the source are historical. Check current supported equivalents. Never activate them just because a recipe mentions them.
7. Prefer native image generation, documents and browser tooling where available. Do not install dependencies or authorize a third party as a side effect of reading this recipe.
8. Preserve scope and output requirements. Mark unavailable dependencies clearly; do not claim a recipe passed a live test from a syntax/manifest check.

## Adapted domain recipe


# Run Quality Gate

Execute validation commands as quality gates with structured error reporting.

## When to Use

- Type-check, build, test, lint validation
- Orchestrator phase validation
- Worker self-validation

## Input

```json
{
  "gate": "type-check|build|tests|lint|custom",
  "blocking": true,
  "custom_command": "pnpm custom-validate"
}
```

## Gate Commands

| Gate | Command |
|------|---------|
| type-check | `pnpm type-check` |
| build | `pnpm build` |
| tests | `pnpm test` |
| lint | `pnpm lint` |
| custom | `custom_command` value |

## Process

1. **Map gate to command** - Validate custom_command if gate="custom"
2. **Execute via Bash** - Timeout: 5 minutes, capture stdout/stderr
3. **Parse result** - Exit code 0 = passed, non-zero = failed
4. **Extract errors** - Lines with "error", "failed", TS#### codes
5. **Determine action**:
   - Passed → action="continue"
   - Failed + blocking → action="stop"
   - Failed + non-blocking → action="warn"

## Output

```json
{
  "gate": "type-check",
  "passed": true,
  "blocking": true,
  "action": "continue",
  "errors": [],
  "exit_code": 0,
  "duration_ms": 2345,
  "command": "pnpm type-check",
  "timestamp": "2025-10-18T14:30:00Z"
}
```

## Examples

**Blocking gate passes**:
```json
{ "gate": "type-check", "blocking": true }
→ { "passed": true, "action": "continue", "errors": [] }
```

**Blocking gate fails** (stops workflow):
```json
{ "gate": "build", "blocking": true }
→ { "passed": false, "action": "stop", "errors": ["Module not found: missing-module"] }
```

**Non-blocking gate fails** (warns only):
```json
{ "gate": "lint", "blocking": false }
→ { "passed": false, "action": "warn", "errors": ["Missing semicolon"] }
```

## Error Handling

- **Timeout (5 min)**: Return failed with timeout error
- **Missing custom_command**: Return error
- **Command not found**: Return failed with exit_code=127

## Notes

- Exit code 0 always = success regardless of output
- Blocking flag only affects action, not passed status
- Error extraction is best-effort
