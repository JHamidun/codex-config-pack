---
name: "memory-extract"
description: "Пакетное извлечение знаний из чатов по топикам (легаси chat_ingester_v2.py). Триггеры: «извлеки знания из чатов». Повседневный поиск → /search-chats."
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


# Извлечь знания из памяти

> **Канон поиска/индексации — `${CODEX_PACK_ROOT}/library/tools/search_chats.py`** (SQLite FTS5, `${CODEX_PACK_ROOT}/library/chats.db`).
> Эта команда использует легаси-скрипт `chat_ingester_v2.py` для пакетного извлечения знаний по топикам.
> Для повседневного поиска и обновления индекса используй `/search-chats` (canonical).

## Задача

Автоматически извлечь и сгруппировать ключевые знания из всей истории чатов.

## Действия

1. **Извлечь знания по топикам:**
```bash
python ${CODEX_PACK_ROOT}/library/tools/chat_ingester_v2.py extract-knowledge
```

2. **Удалить дубликаты:**
```bash
python ${CODEX_PACK_ROOT}/library/tools/chat_ingester_v2.py dedupe
```

3. **Показать статистику:**
```bash
python ${CODEX_PACK_ROOT}/library/tools/chat_ingester_v2.py scan
```

## Что извлекается

- **Ошибки и их решения** (type: error)
- **Код и паттерны** (type: code)
- **Архитектурные решения** (type: decision)
- **Извлечённые знания** (type: learning)

## Автоматическая категоризация

Система автоматически определяет топики:
- `python`, `fastapi`, `django`
- `telegram`, `bot`
- `react`, `typescript`, `javascript`
- `postgresql`, `mongodb`, `redis`
- `docker`, `kubernetes`
- `heygen`, `elevenlabs`, `deepgram`
- и другие...

## Формат вывода

```markdown
## 📚 Extracted Knowledge by Topic:

### TELEGRAM (15 items)
  - [error] Webhook не работал из-за...
  - [code] async def handler(update)...
  - [decision] Выбрал aiogram вместо...

### FASTAPI (10 items)
  - [error] Streaming response зависал...
  - [code] @app.get("/stream")...
```
