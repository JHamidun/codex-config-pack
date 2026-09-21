---
name: "outlook"
description: "Рабочая почта компании (user@example.com) через локальный Outlook по COM — пароль не нужен. Триггеры: «рабочая почта», «exchange». Личная → /gmail."
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


# /outlook

Рабочий путь — локальный Outlook через COM, скрипт
`${CODEX_PACK_ROOT}/library/skills/google-workspace/scripts/outlook_local.py`. Приложение стоит на
машине, учётная запись настроена, пароль не нужен. Проверено на рабочем ящике.

```bash
python ${CODEX_PACK_ROOT}/library/skills/google-workspace/scripts/outlook_local.py inbox --limit 10
python ${CODEX_PACK_ROOT}/library/skills/google-workspace/scripts/outlook_local.py unread
python ${CODEX_PACK_ROOT}/library/skills/google-workspace/scripts/outlook_local.py search "конференция" --days 60
python ${CODEX_PACK_ROOT}/library/skills/google-workspace/scripts/outlook_local.py search "лендинг" --field body
python ${CODEX_PACK_ROOT}/library/skills/google-workspace/scripts/outlook_local.py read 2 --full
python ${CODEX_PACK_ROOT}/library/skills/google-workspace/scripts/outlook_local.py folders
python ${CODEX_PACK_ROOT}/library/skills/google-workspace/scripts/outlook_local.py send --to кому@x.ru --subject "Тема" --body "Текст" --yes
```

Отправка требует `--yes` — без него письмо собирается и показывается, но не уходит.

За граблями (DASL-поиск, поиск по имени вместо адреса) — Skill `google-workspace`.

> **Сетевой путь `exchangelib` на mail.company.example НЕ РАБОТАЕТ — не пробовать.**
> Падает `RecursionError` в urllib3 ещё до авторизации, воспроизводится стабильно,
> пароль ни при чём. Здесь лежало 150 строк такого кода — удалены.
>
> Оттуда же был удалён пример поиска `items.Restrict("[Subject] like '%счёт%'")`:
> Outlook отвергает его («Условие неверно»). Рабочий вариант — DASL
> `@SQL="urn:schemas:httpmail:subject" like '%…%'`, он зашит в скрипт.
