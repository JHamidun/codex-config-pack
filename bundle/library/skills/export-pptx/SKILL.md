---
name: "export-pptx"
description: "HTML-дек в PPTX: режим картинок (надёжный) или редактируемый (нативный текст, pptxgenjs). Триггеры: «html в pptx», «выгрузи в PowerPoint»."
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


# Export PPTX

Два режима. Выбирай по запросу.

## Режим 1: screenshots (надёжно, не редактируется)

Каждый слайд → PNG → вставка в пустой PPTX. Pixel-perfect, но текст внутри картинки.

**Зависимости:** Node + Playwright + python-pptx + Pillow (или JS-аналог).

```bash
npm i -D playwright pptxgenjs
npx playwright install chromium
```

Скрипт `templates/pptx-screenshots.mjs` — рендерит слайды через тот же путь, что `export-png`, и собирает их через **pptxgenjs**:

```js
import pptxgen from 'pptxgenjs';
import { chromium } from 'playwright';
import { pathToFileURL } from 'node:url';
import path from 'node:path';

const [, , file, out = 'deck.pptx'] = process.argv;
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }});
await page.goto(pathToFileURL(path.resolve(file)).href, { waitUntil: 'networkidle' });

const total = await page.evaluate(() => document.querySelector('deck-stage').total);
await page.evaluate(() => document.querySelector('deck-stage').setAttribute('noscale', ''));

const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE'; // 13.33×7.5 inch ~ 1920×1080

for (let i = 0; i < total; i++) {
  await page.evaluate(idx => document.querySelector('deck-stage').go(idx), i);
  await page.waitForTimeout(600);
  const buf = await page.screenshot({ type: 'png' });
  const slide = pres.addSlide();
  slide.background = { data: 'data:image/png;base64,' + buf.toString('base64') };
}

await pres.writeFile({ fileName: out });
await browser.close();
console.log('✓', out);
```

## Режим 2: editable (текст и фигуры — нативные)

Сложнее. Идея: пройти по DOM каждого слайда, для каждого text-node создать `slide.addText(...)`, для прямоугольника — `slide.addShape(...)`, для картинки — `slide.addImage(...)`.

`pptxgenjs` это умеет. Но 1:1 не получится — отказывайся от градиентов, теней, нестандартных шрифтов. Хорошо работает для деков, где макет = заголовок + текст + 1–2 фигуры.

Алгоритм:

1. Запусти страницу в Playwright.
2. На каждом слайде через `page.evaluate` собери список объектов:
   ```js
   [
     { type: 'text', x, y, w, h, text, font, size, color, bold, align },
     { type: 'rect', x, y, w, h, fill, stroke },
     { type: 'image', x, y, w, h, src },
   ]
   ```
   Координаты — относительно слайда, в пикселях, потом конвертируй в дюймы (`px / 96`).
3. Для каждого объекта вызови соответствующий `slide.addX(...)`.
4. `pres.writeFile({ fileName })`.

Готовый экстрактор писать заново не нужно — он лежит в соседнем навыке:
`../pptx-editable-extractor/templates/extract.mjs` (Playwright, `node extract.mjs <html>
[--slide-selector "deck-stage > section"] [--width 1920] [--height 1080]` → `slides.json`),
а сборка из этого JSON — `../pptx-editable-extractor/templates/build_pptx.py`.
Это **черновик**: для сложных макетов потребуется ручная подкрутка.

## Что выбирать когда

| Ситуация | Режим |
|---|---|
| Дек уйдёт в PowerPoint, его будут править | editable (с компромиссами по визуалу) |
| Просто переслать как PPTX, без правок | screenshots |
| В деке много кастомных эффектов / SVG | screenshots, иначе сломается |
| Текст должен искаться / переводиться в PowerPoint | editable |

## Замечания

- Шрифты: PowerPoint использует системные шрифты получателя. Если в HTML Helvetica Neue, а у получателя Windows — он увидит fallback. Закладывай это в выбор шрифтов.
- 16:9 в PowerPoint — `LAYOUT_WIDE` (13.33×7.5 in). 4:3 — `LAYOUT_STANDARD` (10×7.5 in).
- Если используешь Google Fonts — заранее предупреди пользователя, что PPT не подтянет их и шрифт подменится.

## Legacy reference

Прежняя расширенная версия скилла (дерево @2026-04-30) сохранена целиком в `references/legacy-export-pptx.md`. Секции там: Зависимости, Каркас, Workflow целиком, PPTX размеры, Альтернативный путь: LibreOffice, Когда нужен **редактируемый** PPTX, Скрытые слайды, Speaker notes, Метаданные, Антипаттерны.
