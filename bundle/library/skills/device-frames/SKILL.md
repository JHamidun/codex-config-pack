---
name: "device-frames"
description: "CSS-рамки iOS, Android, окно macOS и браузера вокруг макета. Триггеры: «в iPhone», «iOS frame», «browser frame»."
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


# Device frames

Чистые CSS+SVG рамки. Никаких внешних библиотек.

## Что есть в `templates/`

- `ios-frame.html` — iPhone-style рамка с Dynamic Island, статус-баром (время, сеть, батарея), home-indicator. Размер screen: 390×844 (iPhone 14).
- `android-frame.html` — Android-style рамка с notification bar и системными кнопками. Размер: 412×892.
- `macos-window.html` — окно macOS с traffic-lights (красный/жёлтый/зелёный) и заголовком.
- `browser-window.html` — окно браузера с табами, адресной строкой.

Каждый шаблон — одиночный HTML-файл, который можно либо открыть напрямую и заменить контент внутри `.frame-screen`, либо через iframe встроить в свой макет.

## Использование

Самый простой способ — копируй HTML рамки и заменяй её содержимое своим:

```html
<div class="ios-frame">
  <div class="ios-status-bar">...</div>
  <div class="ios-screen">
    <!-- ВОТ СЮДА твой макет -->
  </div>
  <div class="ios-home-indicator"></div>
</div>
```

## Важные размеры

- **iPhone safe-area:** статус-бар 47px сверху, home-indicator 34px снизу. Контент должен дышать в этих границах.
- **Android system bars:** 24px сверху, 48px снизу для жестовой навигации.
- **Хит-таргеты:** не меньше 44×44px (iOS) / 48×48dp (Android).

## Реалистичность

- В статус-баре пиши осмысленное время — не «9:41» (это шаблон Apple). Пиши «09:24» или другое произвольное.
- Уровень батареи — 60–90%. Не 100% (выглядит фейково) и не 5% (отвлекает).
- Сигнал/wifi — full bars.
- Динамический Island — оставь чёрным, если в твоём прототипе нет активного приложения, требующего его.

## Что НЕ нужно делать

- Не рисуй кнопку Home на новых iPhone — её нет с 2017.
- Не рисуй три точки в меню Android Material 3 в местах, где обычно гамбургер.
- Не используй iOS-рамку для Android-макета и наоборот.
