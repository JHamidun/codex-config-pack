---
name: "design-canvas"
description: "N вариантов дизайна бок-о-бок в одном HTML: pan/zoom, фокус. Триггеры: «сравни 3 версии», «покажи варианты». НЕ постеры/арт → canvas-design."
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


# Design canvas

Один HTML, в котором лежит N карточек-артбордов в сетке, каждый — независимый дизайн. Пользователь может:
- зумить и панорамировать всю сетку колесом / трекпадом
- открыть любой артборд во весь экран по клику
- листать артборды стрелками в фокус-режиме

Лучше, чем плодить `option-1.html`, `option-2.html`, `option-3.html`.

## Каркас

`templates/canvas-template.html` содержит готовый шаблон с:
- зум-сценой через `transform: scale()`
- секциями (`<dc-section title="...">`)
- артбордами (`<dc-artboard label="..." width="..." height="...">`)
- фокус-оверлеем

## Использование

```html
<dc-canvas>
  <dc-section title="Header variations">
    <dc-artboard label="A — minimal"     width="1200" height="600">
      <iframe src="header-a.html"></iframe>
    </dc-artboard>
    <dc-artboard label="B — with hero"   width="1200" height="600">
      <iframe src="header-b.html"></iframe>
    </dc-artboard>
    <dc-artboard label="C — full bleed"  width="1200" height="600">
      <iframe src="header-c.html"></iframe>
    </dc-artboard>
  </dc-section>
</dc-canvas>
```

Содержимое артборда — либо inline-разметка, либо iframe со ссылкой на отдельный HTML-вариант.

## Правила

- Артборды — это **статичные кадры**, не скролл-зоны. Не используй `height: 100%; overflow: auto` внутри. Размер артборда задаётся атрибутами `width`/`height`, и контент должен в них помещаться.
- Между секциями делай минимум 80px вертикального расстояния, чтобы при зум-ауте читалось как разные группы.
- Лейбл артборда (`label="..."`) должен описывать **отличие** от соседей, не содержание. «A — без иконок» лучше, чем «Header v1».
- Не больше 6 артбордов в одной секции — глаза устают.

## Что хорошо вынести в варианты

- Ось визуала: минимализм vs богатая графика
- Ось плотности: компактно vs воздушно
- Ось копирайта: лаконично vs развёрнуто
- Ось взаимодействия: статика vs анимация
- Ось интерфейсной парадигмы: классика vs нестандартный layout

Лучше дать 4 артборда, явно различающихся по одной оси, чем 8 случайных вариаций.
