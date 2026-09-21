---
name: "verifier"
description: "Открыть готовый HTML в headless-браузере перед сдачей: console-ошибки + скриншот. Триггеры: «проверь артефакт», «screenshot verify». НЕ WCAG→a11y-audit."
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


# Verifier

Sub-роль для Claude Code. Открывает результат в Playwright headless, проверяет:
- console errors / warnings
- невыполнившиеся network requests
- наличие ключевых элементов (опционально через селектор)
- размер документа (не пусто ли)

И сохраняет один скриншот для визуальной самопроверки.

## Скрипт

`templates/verify.mjs`:

```bash
node verify.mjs deck.html
# → verify-out/console.log + verify-out/screenshot.png
# Exit code: 0 если всё чисто, 1 если есть ошибки.
```

Опции:
- `--require-selector ".some-class"` — упасть, если элемента нет
- `--width 1920 --height 1080` — viewport
- `--wait 1000` — дополнительная задержка перед снимком
- `--out verify-out/` — куда писать

## Когда главный агент должен дёргать verifier

1. Прототип / дек / макет готов.
2. Перед тем как писать «готово» в чат.
3. Если получит exit 1 — прочитать `console.log`, исправить, повторить.

Это **не** замена ручному просмотру пользователем — это санитарный фильтр, чтобы пользователь не открывал заведомо сломанное.

## Анти-анкоринг (проверка чужой работы)

Когда verifier зовут проверять результат другого агента/воркера (кросс-чек, ревью артефакта):

1. Сначала сформируй **свой** вердикт: прогони verify.mjs, собери свой список проблем по артефакту.
2. Только потом читай отчёт/самооценку автора и сверяй.

Чтение чужих выводов до собственной проверки анкерит на их версии — получаются «подтверждающие» проверки вместо независимых. Драфт своего вердикта ДО чтения чужого — обязательный порядок.

## Выбор лучшего из вариантов + GAN-паттерн

Когда verifier сравнивает 2+ результата воркеров (или adversarial-review решает «оставить/откатить»):
LLM-судья предпочитает первый вариант — прогоняй ОБА порядка A-vs-B и B-vs-A, оставляй кандидата
только при перевесе голосов, а не по самоотчётной цифре. Генератор не оценивает свою работу.
Полный паттерн (двусторонний pairwise против position bias, скептик-оценщик, crash-proof apply ladder) —
`references/gan-adversarial-improve.md`.

## Проверка аналитики (второй режим)

Когда на проверку приходит не HTML, а **выводы по данным** (отчёт, дашборд, набор SQL, слайд
с цифрами), console-ошибок не будет — сломанный анализ выглядит нормально и просто врёт.
Порядок тот же: свой вердикт до чужого отчёта. Чек-лист перед отдачей, каталог ловушек
(размножение строк на JOIN, неполный период, сдвиг знаменателя, среднее от средних, часовые
пояса, отбор по результату, черри-пикинг окна), способы независимого пересчёта, красные флаги
и трёхуровневый вердикт — `references/data-analysis-qa.md`.

## Legacy reference

Прежняя расширенная версия скилла (дерево @2026-04-30) сохранена целиком в `references/legacy-verifier.md`. Секции там: Зависимости, Базовый verifier, Что проверяет, Скриншот для review, Multi-viewport проверка, Custom assertions, Когда запускать, Не путать с, Антипаттерны.
