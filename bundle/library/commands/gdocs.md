---
name: "gdocs"
description: "Google Docs (gdocs_client.py): прочитать документ, найти по названию, дописать. Триггеры: «гугл документ», «саммари документа». Хаб → skill google-workspace."
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


# /gdocs

Рабочий код — в навыке `google-workspace`, скрипт
`${CODEX_PACK_ROOT}/library/skills/google-workspace/scripts/gdocs_client.py`.

```bash
python ${CODEX_PACK_ROOT}/library/skills/google-workspace/scripts/gdocs_client.py read <id_или_ссылка>
python ${CODEX_PACK_ROOT}/library/skills/google-workspace/scripts/gdocs_client.py read <id> --limit 2000
python ${CODEX_PACK_ROOT}/library/skills/google-workspace/scripts/gdocs_client.py search "резюме встреч"
python ${CODEX_PACK_ROOT}/library/skills/google-workspace/scripts/gdocs_client.py append <id> --text "строка" --yes
```

Принимает ссылку целиком. Права берутся из `${CODEX_PACK_ROOT}/library/google_oauth_token.json`:
у токена единственный скоуп `drive`, и Docs API на нём работает — проверено.

За подробностями (таблицы в документах, разграничение токенов, что делать при 404)
— Skill `google-workspace`.

> Раньше здесь лежал inline-код работы с Docs API. Он был рабочим, но не проверялся
> ничем: тела команд линтер связности не покрывает. Код перенесён в скрипт навыка и
> прогнан на живом документе.
