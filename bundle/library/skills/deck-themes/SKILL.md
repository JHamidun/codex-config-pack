---
name: "deck-themes"
description: "Готовые CSS-темы для slides без бренда: минимал, editorial, dark, data, brutalist. Триггеры: «тема презентации», «оформление дека». Любой артефакт → theme-factory."
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


# Deck themes

Готовые CSS-темы для `<deck-stage>`. Каждая — один CSS-файл, который подключается рядом с `deck-stage.js`. Конкретный набор шрифтов, цветов, размеров.

## Файлы

- `templates/theme-minimal.css` — спокойный, для B2B и продуктовых ревью.
- `templates/theme-editorial.css` — антиква + воздух, для лонгридов и питчей.
- `templates/theme-dark.css` — тёмный фон, для конференций и кинематографичности.
- `templates/theme-data.css` — для отчётов с цифрами и таблицами.
- `templates/theme-brutalist.css` — моноширинная утилитарность, для девелопер-брендов.

## Использование

```html
<link rel="stylesheet" href="theme-editorial.css" />
<script src="deck-stage.js"></script>
<deck-stage width="1920" height="1080">
  <section>
    <h1>Заголовок</h1>
    <p>Текст</p>
  </section>
</deck-stage>
```

Темы не используют !important — переопределяй конкретные слайды inline-стилями.

## Что общего у всех тем

Каждая тема задаёт:
- `--bg`, `--fg`, `--muted`, `--accent`
- `--font-display`, `--font-body`, `--font-mono`
- размеры `h1`, `h2`, `h3`, `p`, `.eyebrow`
- `.statement`, `.two-col`, `.title-stack`, `.dark` (инвертированный режим)
- `.placeholder`

Слайды переносимы между темами — поменяй `<link>`, и тот же HTML выглядит иначе.

## Правила выбора

| Тема | Подходит | Не подходит |
|---|---|---|
| minimal | внутренние ревью, продукт | креатив-агентства |
| editorial | питчи, манифесты, бренды | data-репорты |
| dark | конференции, AI/tech | финансы, образование |
| data | отчёты, KPI, аналитика | креатив, маркетинг |
| brutalist | dev-tools, опен-сорс | продажи b2c |
