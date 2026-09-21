---
name: "slides"
description: "HTML-презентации: навигация, скейлинг под экран, спикер-ноты, печать в PDF. Триггеры: «сделай слайды», «дек», «питч», «1920x1080 дек». НЕ стили Manus→команда /slides."
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


# Slides

HTML-презентация на основе веб-компонента `<deck-stage>`. Один HTML-файл = одна презентация.

## Принципы

- Канвас фиксированного размера (по умолчанию 1920×1080), отмасштабированный под viewport через `transform: scale()`. Чёрные полосы по краям, если соотношения не совпадают.
- Каждый слайд — `<section>` внутри `<deck-stage>`.
- Навигация: ←/→, Space, клик по краям, цифры на клавиатуре.
- Печать в PDF: одна страница = один слайд (через `@page` + `@media print`).

## Как делать дек

1. Скопируй `templates/deck-stage.js` рядом с HTML-файлом.
2. Возьми `templates/deck-template.html` как стартовый каркас.
3. Сформулируй дизайн-систему ВСЛУХ перед слайдами:
   - Шрифтовая пара (заголовок + основной).
   - Базовая палитра: фон, текст, 0–2 акцента.
   - Сетка: колонки, базовый отступ.
   - Ритм слайдов: где full-bleed, где разделители-секции, где данные.
4. Каждый слайд — `<section>` со своим layout. Не используй один шаблон на всё.
5. На текстовых слайдах не больше ~30 слов. Остальное — в спикер-ноты.

## Размеры

| Формат | Размеры | Когда |
|---|---|---|
| 16:9 FullHD | 1920×1080 | Дефолт. Конференции, ревью. |
| 16:9 lite | 1280×720 | Если важна скорость рендера. |
| Square | 1080×1080 | Соцсети, карусели. |
| Vertical | 1080×1920 | Сторис, мобильные плееры. |

Указывается атрибутами на `<deck-stage>`:

```html
<deck-stage width="1920" height="1080">
  <section>...</section>
  <section>...</section>
</deck-stage>
```

## Спикер-ноты

Если нужны — добавь в `<head>`:

```html
<script type="application/json" id="speaker-notes">
[
  "Заметки к слайду 1",
  "Заметки к слайду 2"
]
</script>
```

Полные разговорные тексты, не тезисы. Это сценарий выступления.

## Типографические правила

- Минимальный размер на 1920×1080: **24px**, и то редко. Заголовки от 80px.
- Не больше 2 шрифтов в деке.
- Контраст текста к фону — минимум 4.5:1.
- Не центрируй длинные абзацы. Центрируй короткие — заголовки и манифесты.

## Композиция слайдов

Полезные архетипы (комбинируй):

- **Statement** — одна большая фраза, всё остальное минимум.
- **Title + supporting** — заголовок сверху, 1–3 пункта или картинка.
- **Two-column** — слева тезис, справа доказательство (картинка / данные).
- **Section divider** — контрастный фон, номер секции и название. Использовать для ритма каждые 4–6 слайдов.
- **Full-bleed image** — фото на весь экран, текст в углу с полупрозрачной плашкой.
- **Data slide** — один график крупно, один вывод текстом.
- **Quote** — большая цитата, мелкая атрибуция.

Не повторяй один и тот же шаблон 10 раз подряд.

## Изображения

Если нет реальных — рисуй плейсхолдер:

```html
<div class="placeholder">
  <span>product shot · 1200×800</span>
</div>
```

```css
.placeholder {
  background: repeating-linear-gradient(
    45deg, #1a1a1a, #1a1a1a 8px, #222 8px, #222 16px
  );
  display: grid; place-items: center;
  font-family: ui-monospace, monospace;
  color: #888; font-size: 14px;
}
```

## Метки для контекста

Поставь `data-screen-label` на каждом `<section>`, тогда при инспекции элементов видно, где какой слайд:

```html
<section data-screen-label="01 Title">...</section>
<section data-screen-label="02 Problem">...</section>
```

Нумерация с 1, как у пользователя в интерфейсе.

## Экспорты

Когда готово — пользователь может попросить:
- PDF → подключи скилл `export-pdf`.
- PNG-кадры → `export-png`.
- PPTX → `export-pptx`.
- Один HTML-файл → `standalone-html`.

## Проверка

Открой результат в браузере — команда своя на каждой ОС:

```bash
open deck.html            # macOS
xdg-open deck.html        # Linux
start deck.html           # Windows (cmd / PowerShell)
```

В Git Bash на Windows нет ни `open`, ни `xdg-open`, ни `start` как команды — там
`start` вызывается через `cmd`: `cmd //c start deck.html`. Кросс-платформенный
однострочник, если не хочется помнить: `python -c "import webbrowser,sys; webbrowser.open(sys.argv[1])" deck.html`.

Если есть скилл `verifier` — позови его проверить консоль и снять скриншоты.

## Legacy reference

Прежняя расширенная версия скилла целиком лежит в `references/legacy-slides.md`. Секции там: Каркас, Правила слайдов, Структура дека (типовая), Стек со связанными скиллами, URL-навигация, Антипаттерны.
