---
name: "screen-labels"
description: "Атрибут data-screen-label на каждом экране/слайде артефакта — правки адресуются «слайд 5». Триггеры: «подпиши экраны», «метки слайдов»."
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


# Screen labels

Без меток разговор о правках выглядит так: «там, где синий блок с тремя кнопками». С метками: «слайд 05 Roadmap» — однозначно.

## Правило

На каждый «экран» (слайд, маршрут прототипа, артборд canvas) — атрибут `data-screen-label`:

```html
<!-- слайды -->
<deck-stage>
  <section data-screen-label="01 Title">...</section>
  <section data-screen-label="02 Problem">...</section>
  <section data-screen-label="03 Solution">...</section>
</deck-stage>

<!-- прототип -->
<div class="screen" data-screen-label="Login">...</div>
<div class="screen" data-screen-label="Feed">...</div>
<div class="screen" data-screen-label="Profile">...</div>

<!-- design-canvas -->
<dc-artboard data-screen-label="Hero — variant A" width="1440" height="900">
```

## Соглашения именования

### Для слайдов
**1-indexed двузначные**: `01 Title`, `02 Agenda`, `10 Roadmap`. Совпадает со счётчиком, который видит юзер (`5/12`).

```html
<!-- хорошо -->
<section data-screen-label="01 Title">

<!-- плохо: 0-индексация ломает диалог -->
<section data-screen-label="00 Title">
```

Когда юзер говорит «исправь слайд 5» — он подразумевает 5-й слайд, *никогда* index 4.

### Для экранов прототипа
Короткое имя экрана, человеческое: `Login`, `Feed`, `Settings`, `Onboarding step 2`.

### Для артбордов canvas
`<имя экрана> — <вариант>`: `Hero — minimal`, `Hero — editorial`, `Pricing — 3-tier`.

## Использование

### При правке
В чате юзер: «слайд 05, измени h1 на ...» → в HTML находим `[data-screen-label="05 ..."]` и точечно правим.

### В deck-stage
`deck_stage.js` автоматически тегирует слайды — если нет ручного `data-screen-label`. Но ручной — лучше: говорящий, не «slide-3».

### В DOM-комментарии
Когда юзер кликает на элемент в превью с подключённым `comment-injector` — в clipboard падает селектор; присутствие `data-screen-label` у предка делает его читаемым:

```
SELECTOR: section[data-screen-label="03 Solution"] h1
```

## Антипаттерны

- ❌ Не использовать `id="slide-1"` вместо `data-screen-label`. ID должен быть уникальным и не привязанным к визуальному порядку — а слайды переставляются.
- ❌ Не делать `data-screen-label="Слайд 1 — Заголовок страницы — версия 2 от 28 апреля"`. Короче.
- ❌ Не забывать менять label, когда меняешь содержимое. «05 Roadmap» с финансами внутри — путаница.

## Бонус: автогенерация

Если хочется не вручную:

```js
document.querySelectorAll('deck-stage > section').forEach((s, i) => {
  if (s.dataset.screenLabel) return;
  const h = s.querySelector('h1, h2');
  const idx = String(i + 1).padStart(2, '0');
  s.dataset.screenLabel = `${idx} ${h?.textContent || 'untitled'}`;
});
```

Запускать при загрузке. Но лучше — вручную, label остаётся стабильным.
