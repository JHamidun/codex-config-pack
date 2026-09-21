---
name: "print-styles"
description: "Print stylesheet, чтобы Cmd+P давал приличный результат. Триггеры: «стили для печати», «@media print», «page-break»."
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


# Print styles

90% сайтов при печати выдают мусор: огромные иконки, обрезанная навигация, пустые страницы. Хороший print stylesheet — это уважение.

## Минимум

```css
@media print {
  /* Сброс */
  * { background: transparent !important; color: #000 !important; box-shadow: none !important; text-shadow: none !important; }
  body { font: 11pt/1.4 Georgia, serif; margin: 0; }

  /* Скрыть навигацию, sticky-элементы, кнопки */
  nav, header.sticky, footer, .no-print, [data-no-print] { display: none !important; }

  /* URL у ссылок — раскрыть */
  a:not(.no-href)::after { content: " (" attr(href) ")"; font-size: 9pt; color: #666; }
  a[href^="#"]::after, a[href^="javascript:"]::after { content: ""; }

  /* Не разрезать заголовки и блоки */
  h1, h2, h3, h4 { page-break-after: avoid; break-after: avoid; }
  blockquote, pre, table, figure, ul, ol { page-break-inside: avoid; break-inside: avoid; }

  /* Картинки — в рамках страницы */
  img { max-width: 100%; height: auto; page-break-inside: avoid; break-inside: avoid; }

  /* Размер бумаги */
  @page { size: A4; margin: 20mm 18mm; }

  /* Колонки в одну */
  .grid, .columns, [data-cols] { display: block !important; }
}
```

## A4 vs Letter

```css
@page { size: A4; }            /* Европа, Азия */
@page { size: letter; }        /* США, Канада */
```

Если не уверен — `auto` (берёт из настроек браузера).

## Pagination

Принудительный разрыв перед заголовком уровня h1 / h2:

```css
@media print {
  h1 { page-break-before: always; break-before: page; }
  h1:first-of-type { page-break-before: auto; break-before: auto; }
}
```

## Таблицы

```css
@media print {
  table { width: 100%; border-collapse: collapse; }
  thead { display: table-header-group; }   /* Повторять header на каждой странице */
  tfoot { display: table-footer-group; }
  tr { page-break-inside: avoid; }
}
```

## Цвет в печати

По умолчанию браузеры **отключают** background-printing. Чтобы остался:

```css
@media print {
  .keep-bg { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
}
```

Используй экономно — расход чернил.

## Header / footer

В CSS Print можно задать колонтитулы:

```css
@page {
  margin: 20mm 18mm;
  @top-center { content: "Договор № 42"; font: 9pt sans-serif; color: #666; }
  @bottom-right { content: counter(page) " / " counter(pages); font: 9pt monospace; }
}
```

Поддержка частичная — Chromium ✓, Firefox частично, Safari нет. Для надёжности используй `@page` блок и не полагайся на `@top-*`.

## Тестирование

```bash
# Через DevTools: Cmd+Shift+P → "Show rendering" → Emulate CSS media: print
# Или сразу:
chrome --headless --print-to-pdf=out.pdf file.html
```

Скрипт:

```bash
#!/bin/bash
chrome --headless --disable-gpu --print-to-pdf="$2" "$1"
```

## Антипаттерны

- ❌ Ничего не делать — браузер напечатает navbar и подвал.
- ❌ `display: none` на всех `<a>` — пользователь не увидит ссылок.
- ❌ Полностью «свой» дизайн в print — он должен быть **спокойнее** и **читабельнее** экранного, не другим.

## Чек-лист

- ✅ Cmd+P даёт читаемую первую страницу.
- ✅ Нет пустой первой страницы.
- ✅ Картинки помещаются.
- ✅ Таблицы не обрезаны.
- ✅ Шрифт ≥10pt в основном тексте.
- ✅ Ссылки с раскрытым URL.

## Legacy reference

Прежняя расширенная версия скилла (дерево @2026-04-30) сохранена целиком в `references/legacy-print-styles.md`. Секции там: Базовый print stylesheet, Для slides (отдельная стратегия), Для лендингов, Footnotes / endnotes для академических, Watermark, Тест в браузере, Когда не нужны print-styles, Антипаттерны.
