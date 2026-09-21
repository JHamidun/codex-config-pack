---
name: "github-import"
description: "Импорт файлов GitHub-репо как контекст: токены, компоненты, стили. Триггеры: «сделай в стиле этого репо», «из репо токены», «воссоздай UI»."
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


# GitHub import

Без авторизации можно тянуть публичные репы через raw.githubusercontent.com и API. Для приватных нужен токен.

## Парсинг URL

```
https://github.com/OWNER/REPO                          → весь реп, default branch
https://github.com/OWNER/REPO/tree/REF/PATH            → папка
https://github.com/OWNER/REPO/blob/REF/PATH/file.ext   → один файл
```

```js
function parseGithubUrl(url) {
  const u = new URL(url);
  const [, owner, repo, type, ref, ...path] = u.pathname.split('/');
  return { owner, repo, type, ref: ref || 'HEAD', path: path.join('/') };
}
```

## Получение

**Один файл (raw):**
```
https://raw.githubusercontent.com/OWNER/REPO/REF/PATH
```

**Список папки (API):**
```
https://api.github.com/repos/OWNER/REPO/contents/PATH?ref=REF
```

**Дерево целиком (API, может быть большим):**
```
https://api.github.com/repos/OWNER/REPO/git/trees/REF?recursive=1
```

Без токена rate-limit 60 запросов/час с IP. С токеном — 5000. Токен передаётся как `Authorization: Bearer $API_KEY

## Стратегия импорта

Дерево — это меню, не еда. Не клади себе в контекст рекурсивный листинг на 5000 файлов. Вместо этого:

1. **Не-рекурсивный листинг корня.** Понять, какой это стек (есть ли `package.json`, `tailwind.config`, `theme.ts`, `_variables.scss`).
2. **Прицельные файлы.** Скачивай только то, что точно нужно:
   - **Тема/токены:** `theme.ts`, `colors.ts`, `tokens.css`, `_variables.scss`, `tailwind.config.{js,ts}`, `globals.css`.
   - **Конкретные компоненты, упомянутые пользователем.**
   - **Глобальные стили.**
3. **Прочитай эти файлы.** Не строй UI по «памяти, как этот сайт примерно выглядит» — это даёт generic look-alike. Бери hex-коды, шрифты, скейлы отступов, радиусы прямо оттуда.

## Скрипт

`templates/gh-pull.sh` — bash-скрипт-обёртка:

```bash
templates/gh-pull.sh https://github.com/owner/repo/tree/main/src/theme
# → выкачает все файлы из этой папки в ./gh-import/owner-repo/src/theme/
```

Использует `curl` и `jq`. **`jq` не входит ни в macOS, ни в Windows, ни в базовый
Debian** — скрипт проверяет его первым делом и печатает команду установки под твою
систему (`brew install jq` · `sudo apt install -y jq` · `winget install jqlang.jq`).
Без этой проверки обход дерева заканчивался пустыми папками и словом «Готово».

Приватная репа или упор в лимит запросов (60/час без токена) — задай
`GITHUB_TOKEN`; скрипт сам подскажет это по коду ответа. Скачано 0 файлов —
это ошибка и ненулевой код возврата, а не успех.

## После импорта

В корне импорта оставь `_INDEX.md` с:
- Что это за реп.
- Какие файлы импортированы и зачем.
- Какие ключевые значения (палитра, шрифт, радиусы) уже извлечены.

Потом на это ссылайся при дизайне: «использую палитру из gh-import/owner-repo/src/theme/colors.ts».

## Важно

Не воспроизводи защищённые товарным знаком интерфейсы 1:1, даже если код открыт. Бери токены и принципы, но делай **оригинальный** дизайн. Особенно если репо принадлежит крупному продукту (мессенджеры, соцсети, известные SaaS) — повторение их UI попадает под претензии по интеллектуальной собственности.

## Legacy reference

Прежняя расширенная версия скилла сохранена целиком в `references/legacy-github-import.md`. Секции там: Использование, Что искать в существующем проекте, Output: project-context.md, Stack, Tokens (use these names), Components (use these instead of building new), Conventions, Routes, Что НЕ копировать, Multi-repo контекст, Антипаттерны.
