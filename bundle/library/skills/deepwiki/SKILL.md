---
name: "deepwiki"
description: "Доки любого GitHub-репо через DeepWiki/gitmcp.io и llms.txt. Триггеры: «как устроен этот репозиторий»."
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


# DeepWiki: GitHub Repository Documentation

Fetch and analyze documentation for any GitHub repository.

## When to Use

- **DeepWiki**: Any GitHub repository documentation
- **Context7** (separate skill): npm/pypi packages with published docs

## Method 0 — llms.txt preflight (ВСЕГДА первым, до любого краулинга)

Многие проекты уже отдают готовый срез доков для LLM. Спросить — секунда, краулить — минуты.

```bash
python ${CODEX_PACK_ROOT}/library/tools/llms_txt.py https://docs.example.com          # или сразу несколько доменов
python ${CODEX_PACK_ROOT}/library/tools/llms_txt.py https://svelte.dev --full --save ./llms   # llms-full.txt целиком
```

- `[FOUND]` → бери этот текст как источник, дальше по Methods 1-3 идти не нужно.
- `[NONE ]` → llms.txt нет, спокойно переходи к Method 1 (корректная деградация, не ошибка).

Проверяется `/llms.txt` и `/llms-full.txt` рядом с путём и в корне домена.
**Валидация по телу, а не по коду ответа:** SPA-сайты отдают 200 + HTML на любой
несуществующий путь (проверено: `your-domain.com/llms.txt` → 200 `text/html`), поэтому
скрипт режет HTML-заглушки и отдаёт `found=false` вместо вёрстки под видом доков.

Из Python: `from llms_txt import discover, parse` (`sys.path` → `${CODEX_PACK_ROOT}/library/tools`).

## Methods

### Method 1: gitmcp.io (preferred)
Convert any GitHub URL to gitmcp.io format:
```
https://github.com/{owner}/{repo} -> https://gitmcp.io/{owner}/{repo}
```

Fetch via WebFetch:
```
WebFetch: https://gitmcp.io/{owner}/{repo}
Prompt: "Get the main documentation, API reference, and getting started guide"
```

### Method 2: Raw GitHub README
```
WebFetch: https://raw.githubusercontent.com/{owner}/{repo}/main/README.md
```

### Method 3: GitHub API
```bash
gh api repos/{owner}/{repo}/readme --jq '.content' | base64 -d
```

## Process

1. User provides GitHub repo URL or name
2. Fetch documentation using Method 1 (gitmcp.io)
3. If fails, fallback to Method 2 or 3
4. Summarize key sections: setup, API, examples
5. Answer user's specific questions about the repo

## Examples

```
User: "документация для langchain"
-> WebFetch https://gitmcp.io/langchain-ai/langchain

User: "как использовать playwright python"
-> WebFetch https://gitmcp.io/microsoft/playwright-python
```

## Notes
- For npm packages, use Context7 MCP instead
- For private repos, use `gh` CLI with authenticated access
- Cache results in memory for repeated queries
