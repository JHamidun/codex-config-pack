---
name: "gdrive"
description: "Google Drive (gdrive_client.py): что в папке, поиск, скачать файл/папку, залить. Триггеры: «гугл диск», «скачай с диска», «расшаренная папка». НЕ Яндекс.Диск → skill yandex."
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


# /gdrive

Рабочий клиент — `${CODEX_PACK_ROOT}/library/tools/gdrive_client.py`.

```bash
python ${CODEX_PACK_ROOT}/library/tools/gdrive_client.py ls <id_или_ссылка> [--recursive]
python ${CODEX_PACK_ROOT}/library/tools/gdrive_client.py find "вебинар"
python ${CODEX_PACK_ROOT}/library/tools/gdrive_client.py get <id_файла> -o ./куда/
python ${CODEX_PACK_ROOT}/library/tools/gdrive_client.py pull <id_папки> -o ./куда/ --ext mp4,m4a --min-mb 5
python ${CODEX_PACK_ROOT}/library/tools/gdrive_upload.py upload <локальная_папка> <имя_на_диске>
```

Принимает ссылку целиком — идентификатор вынимается сам. Права — из
`${CODEX_PACK_ROOT}/library/google_oauth_token.json` (скоуп `drive`, чтение и запись).

За подробностями — Skill `google-workspace`.

> Здесь лежал inline-код `files().list()` БЕЗ `supportsAllDrives` и
> `includeItemsFromAllDrives`. Без этих двух флагов API молча скрывает всё, что
> лежит на общих дисках: папка выглядит пустой, хотя файлы в ней есть. В клиенте
> флаги проставлены — и в списке, и при скачивании. Код удалён.
