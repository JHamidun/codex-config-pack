---
name: "tool-search-protocol"
description: "До отказа «нет интеграции» с Slack/Drive/Linear — сначала поиск инструмента через tool_search. Триггеры: «есть ли коннектор», «найди инструмент»."
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


# Tool search protocol

Claude Code (и Claude в целом) видит **частичный** список инструментов. MCP-коннекторы могут быть подключены, но не появиться в видимом списке до явного поиска.

## Правило

Если юзер просит сделать что-то с внешним сервисом (Slack, Google Drive, Linear, Notion, Jira, GitHub Issues, Asana и т.д.) — **до того как сказать "не могу"**, проверь:

1. Доступен ли `tool_search` или эквивалент в среде. (В Claude Code это может быть `mcp` команда или `tool_search_tool_bm25`.)
2. Поищи по ключевым словам сервиса.
3. Если нашёлся — используй.
4. Если нет — теперь можно отказаться, но конкретно: «Я не вижу инструмента для X. Если у тебя установлен MCP-сервер для X, проверь, что он подключён».

## Антипаттерн

```
Юзер: "Запости в наш Slack #design"
Я:    "Извини, не могу — нет интеграции со Slack."
```

Это **до того**, как проверил.

## Правильный flow

```
Юзер: "Запости в наш Slack #design"
Я:    *проверяю tool_search "slack"*
       1) если найден slack_post — использую
       2) если не найден — "не вижу Slack-интеграции; добавь её в MCP и перезапусти, или вкинь сообщение сам"
```

## Команды поиска

- В Claude Code (с MCP) — `mcp list` или `mcp tools`.
- Внутри агентного контекста — функция `tool_search_tool_bm25` или `tool_search` по имени.
- Документации MCP-серверов — `${CODEX_PACK_ROOT}/library/mcp.json` или `.claude/mcp.json` в проекте.

## Что искать по ключевым словам

| Запрос упоминает | Поиск по |
|---|---|
| Slack | `slack`, `chat`, `message` |
| Notion | `notion`, `page`, `database` |
| Linear / Jira | `linear`, `jira`, `issue`, `ticket` |
| Google Drive | `drive`, `gdrive`, `gdocs` |
| Figma | `figma`, `design`, `frame` |
| GitHub | `github`, `repo`, `pr`, `pull request` |
| Email | `email`, `mail`, `smtp` |
| Calendar | `calendar`, `event` |
| Filesystem outside project | `file`, `bash`, `shell` |

## Не повторяй ошибку дважды

Если в одном чате уже искал и не нашёл — не зацикливайся: «не нашёл» один раз достаточно. Не делай tool_search на каждом сообщении.

## Когда никакого MCP нет

Спроси юзера: «Хочешь подключить MCP-сервер для X? Минимальный путь: <ссылка/команда>». Это полезнее, чем отказ.

## Что MCP **обычно умеет**

- Чтение содержимого (страницы, тикеты, файлы).
- Создание/обновление сущностей.
- Поиск.

И **обычно не** умеет:
- Долгоживущие подписки на события.
- Сложные UI-актиш с кликами по конкретным кнопкам.
- Что-то требующее пользовательского OAuth-flow в моменте.
