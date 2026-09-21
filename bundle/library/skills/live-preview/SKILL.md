---
name: "live-preview"
description: "Локальный сервер с auto-reload для итеративной работы над HTML/CSS — браузер обновляется при сохранении. Триггеры: «live reload», «browser-sync»."
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


# Live preview

Запусти `live.mjs <path>` — он поднимет http-сервер на 5173, откроет браузер и будет реактивно перезагружать страницу при изменении файлов.

```bash
node ./skills/live-preview/templates/live.mjs index.html
# → открыто http://localhost:5173/
# редактируй файлы — браузер обновится сам
```

Зависимости: `npm i -D chokidar ws`.

## Как работает

1. Простейший HTTP-сервер отдаёт файлы из текущей директории.
2. WebSocket-канал на `/_lp` — клиент в каждой странице слушает.
3. При сохранении файла chokidar шлёт `reload` всем клиентам.
4. В страницы инжектится 6-строчный snippet перед `</body>`.

## Когда не использовать

- Если артефакт уже использует свой dev-server (Vite, Next).
- Если работаешь с production-сборкой без перезагрузок.

## Legacy reference

Прежняя расширенная версия скилла (дерево @2026-04-30) сохранена целиком в `references/legacy-live-preview.md`. Секции там: Самый простой: livereload, Альтернатива: live-server, Альтернатива 3: vite (если артефакт уже React), Альтернатива 4: Python http.server + auto-reload, Custom auto-reload через WebSocket (если хочется без deps), Browser-sync features, Best practices, Tunneling для шеринга, Когда НЕ использовать, Stack, Антипаттерны.
