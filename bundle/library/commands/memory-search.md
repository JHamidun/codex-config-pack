---
name: "memory-search"
description: "Поиск по памяти: заметки (memory_find.py) + чаты + знания (search_chats.py knowledge). Триггеры: «поищи в памяти», «найди в базе знаний». Чистый поиск чатов → /search-chats."
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


# Search Memory

> **Алиас `/search-chats`.** Обе команды используют один движок — `${CODEX_PACK_ROOT}/library/tools/search_chats.py` (SQLite FTS5, `${CODEX_PACK_ROOT}/library/chats.db`).
> `/memory-search` дополнительно ищет по извлечённым знаниям (knowledge base); `/search-chats` — базовый полнотекстовый поиск + управление индексом/архивом.

**Arguments:** $ARGUMENTS (search query [--type code|error|learning|decision])

## Task

Search across all chat history and accumulated knowledge using SQLite FTS5.

## Actions

1. **Search chats (full history):**

```bash
python ${CODEX_PACK_ROOT}/library/tools/search_chats.py search "$ARGUMENTS"
```

2. **Search knowledge base (extracted learnings, code, errors):**

```bash
python ${CODEX_PACK_ROOT}/library/tools/search_chats.py knowledge "$ARGUMENTS"
```

3. **Search only code snippets:**

```bash
python ${CODEX_PACK_ROOT}/library/tools/search_chats.py knowledge "$ARGUMENTS" --type code
```

4. **Search only errors:**

```bash
python ${CODEX_PACK_ROOT}/library/tools/search_chats.py knowledge "$ARGUMENTS" --type error
```

## Content Types

| Type | Description |
|------|-------------|
| `code` | Code, functions, configs |
| `error` | Errors and solutions |
| `learning` | Extracted knowledge |
| `decision` | Architectural decisions |
| `discussion` | Discussions |
| `question` | Questions |

## Examples

```
/memory-search FastAPI streaming
/memory-search telegram bot errors --type error
/memory-search ChromaDB vector --type code
```
