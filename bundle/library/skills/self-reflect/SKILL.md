---
name: "self-reflect"
description: "Разбор недавних ошибок и паттернов, генерация правок для rules/skills. Триггеры: «проанализируй себя», «какие ошибки повторяются»."
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


# Self-Reflect: Continuous Improvement

Analyze past sessions and errors to generate actionable improvements.

## Process

### Phase 1: Gather Data

1. **Recent errors from memory**:
```bash
python ${CODEX_PACK_ROOT}/library/tools/vector_memory.py search "ошибка error fix bug" --limit 10
```

2. **Recent decisions**:
```bash
python ${CODEX_PACK_ROOT}/library/tools/vector_memory.py search "решение выбрали decided" --limit 10
```

3. **Recent learnings**:
```bash
python ${CODEX_PACK_ROOT}/library/tools/vector_memory.py search "learned паттерн pattern" --limit 10
```

4. **Subagent usage patterns**:
```bash
powershell -c "Get-Content $env:USERPROFILE\.claude\logs\subagents.log -Tail 50"
```

### Phase 2: Analyze Patterns

For each error/issue found:
1. Has this type of error occurred before?
2. What was the root cause?
3. Could a rule/skill/hook have prevented it?
4. What's the fix pattern?

### Phase 3: Generate Improvements

Categories:
- **New rule** -> add to `${CODEX_PACK_ROOT}/library/rules/`
- **Updated routing** -> modify `routing.md`
- **New skill** -> add to `${CODEX_PACK_ROOT}/library/skills/`
- **Hook adjustment** -> modify `settings.json`
- **Memory entry** -> save via vector_memory

### Phase 4: Apply & Save

For each improvement:
```bash
python ${CODEX_PACK_ROOT}/library/tools/vector_memory.py learn "[improvement description]" "self-improvement"
```

## Report Format

```markdown
# Self-Reflection Report

## Errors Analyzed
1. [Error] -> [Root cause] -> [Fix applied]

## Recurring Patterns
- Pattern: [description]
  - Frequency: N times
  - Improvement: [what to change]

## Improvements Generated
- [ ] [Rule/skill/hook change description]

## Metrics
- Errors analyzed: N
- Patterns found: N
- Improvements proposed: N
```

## Rules
- Be honest about mistakes
- Focus on systemic fixes, not one-off patches
- Prioritize by frequency x impact
- Always save findings to vector memory
