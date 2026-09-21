---
name: "kb"
description: "Поиск по локальной KB kb.py: встречи tl;dv/Spark, письма Gmail/Outlook, Telegram; + ingest. Триггеры: «база знаний», «найди в встречах». История чатов → /search-chats."
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


# Knowledge Base Search

**Arguments:** $ARGUMENTS

## Task

Search the local knowledge base (meetings, emails, chats) using SQLite FTS5 with BM25 ranking.

## Actions

### Search all sources

```bash
python ${CODEX_PACK_ROOT}/library/tools/kb.py search "$ARGUMENTS"
```

### Search specific source

```bash
python ${CODEX_PACK_ROOT}/library/tools/kb.py search "$ARGUMENTS" --source tldv
```

### Search with date filter

```bash
python ${CODEX_PACK_ROOT}/library/tools/kb.py search "$ARGUMENTS" --after 2025-01-01
```

### Search by speaker

```bash
python ${CODEX_PACK_ROOT}/library/tools/kb.py search "$ARGUMENTS" --speaker "Name"
```

### Show stats

```bash
python ${CODEX_PACK_ROOT}/library/tools/kb.py stats
```

### Show sources

```bash
python ${CODEX_PACK_ROOT}/library/tools/kb.py sources
```

### Ingest new data

```bash
python ${CODEX_PACK_ROOT}/library/tools/kb.py ingest tldv                # tl;dv transcripts
python ${CODEX_PACK_ROOT}/library/tools/kb.py ingest spark                # Spark Mail transcripts
python ${CODEX_PACK_ROOT}/library/tools/kb.py ingest telegram <file.json> # Telegram export
python ${CODEX_PACK_ROOT}/library/tools/kb.py ingest gmail [days]         # Gmail emails (default: 90)
python ${CODEX_PACK_ROOT}/library/tools/kb.py ingest gcalendar [days]     # Google Calendar (default: 365)
python ${CODEX_PACK_ROOT}/library/tools/kb.py ingest outlook [days]       # Outlook/Exchange (default: 90)
```

### Show full document

```bash
python ${CODEX_PACK_ROOT}/library/tools/kb.py doc <id>
```

## Search tips

| Syntax | Example | Description |
|--------|---------|-------------|
| Simple words | `спринт планирование` | Match both words |
| Quoted phrase | `"example-query"` | Exact phrase match |
| Prefix | `react*` | Words starting with react |
| OR | `zoom OR meet` | Either word |

## Sources

| Source | Description | Documents |
|--------|-------------|-----------|
| tldv | tl;dv meeting transcripts | XXX |
| gmail | Gmail emails | XXX |
| spark | Spark Mail AI meeting summaries | XXX |
| gcalendar | Google Calendar events | XXX |
| telegram | Telegram chat exports | (on demand) |
| outlook | Outlook/Exchange emails | XXX |

## Examples

```
/kb example-query
/kb спринт --source tldv --after 2025-01-01
/kb "YourProduct" --source spark
/kb stats
/kb sources
```
