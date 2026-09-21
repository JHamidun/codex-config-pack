---
name: "memory-learn"
description: "Сохранить знание в память (search_chats.py learn); без аргументов — разбор сессии. Триггеры: «запиши знание», «сохрани в базу знаний». Пайплайн 4 уровней → save-knowledge-base."
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


# Save to Memory

**Arguments:** $ARGUMENTS (what to remember)

## Task

Save new knowledge to long-term memory (SQLite FTS5).

## Format

```
/memory-learn [category]: [content]
```

## Categories

- `technical` - technical knowledge (code, patterns, debugging)
- `tools` - tools and usage
- `workflow` - work processes
- `preference` - user preferences
- `project` - project info

## Actions

1. **Parse arguments:**
   - If contains ":" - first part = category
   - Otherwise category = "general"

2. **Save:**
```bash
python ${CODEX_PACK_ROOT}/library/tools/search_chats.py learn "$CONTENT" "$CATEGORY"
```

3. **Confirm:**
   - Show what was saved
   - Category
   - Timestamp

## Examples

```
/memory-learn technical: ChromaDB crashes Extension Host on Windows
/memory-learn preference: User prefers TypeScript for frontend
/memory-learn Always use uv instead of pip for Python projects
```

## Auto-Learning Prompt

If just `/memory-learn` without arguments:
1. Analyze current session
2. Suggest what to save
3. Ask for confirmation
