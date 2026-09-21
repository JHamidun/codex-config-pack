---
name: "scaling-stage"
description: "Letterbox-обёртка контента фиксированного canvas (1920×1080): вписывается в любой viewport. Триггеры: «letterbox обёртка», «вписать 1920x1080»."
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


# Scaling stage

`deck-stage` решает эту задачу для слайдов. Для остального — нужен такой же простой обёртчик.

## Принцип

Контент рисуется в **фиксированном размере** (например 1920×1080). Внешняя обёртка занимает viewport и масштабирует контент через `transform: scale()` так, чтобы он целиком влезал, оставляя letterbox по краям.

## Минимальная реализация

```html
<style>
  html, body { margin: 0; height: 100%; background: #000; overflow: hidden; }

  .stage {
    position: fixed; inset: 0;
    display: grid; place-items: center;
    background: #000;
  }

  .canvas {
    width: 1920px; height: 1080px;
    transform-origin: center center;
    background: #fff;     /* фон контента */
    overflow: hidden;
    position: relative;
  }
</style>

<div class="stage">
  <div class="canvas" id="canvas">
    <!-- здесь рисуется всё, что должно быть 1920×1080 -->
  </div>
</div>

<script>
(function () {
  const W = 1920, H = 1080;   // меняй под свой формат
  const canvas = document.getElementById('canvas');
  function fit() {
    const sx = window.innerWidth / W;
    const sy = window.innerHeight / H;
    const s  = Math.min(sx, sy);
    canvas.style.transform = `scale(${s})`;
  }
  addEventListener('resize', fit);
  fit();
})();
</script>
```

Всё. 30 строк.

## Форматы

| Формат | W × H | Использование |
|---|---|---|
| 16:9 landscape | 1920×1080 | Слайды, видео для YouTube, презентации |
| 9:16 portrait  | 1080×1920 | Stories, Reels, TikTok |
| 1:1 square     | 1080×1080 | Twitter/X, Instagram feed |
| 4:5 portrait   | 1080×1350 | Instagram feed (выше) |
| Cinema         | 2560×1080 | Ultrawide / cinematic |
| Print A4       | 2480×3508 (300dpi) | Постеры, печать |

## С controls (play / pause / scrub) для анимации

`animations`-скилл делает это через `<Stage>`. Если без React:

```html
<div class="controls">
  <button id="playBtn">▶</button>
  <input type="range" id="scrub" min="0" max="100" value="0">
  <span id="time">0.00s</span>
</div>

<style>
  .controls {
    position: fixed; bottom: 16px; left: 50%;
    transform: translateX(-50%);
    display: flex; gap: 12px; align-items: center;
    padding: 8px 16px; background: rgba(0,0,0,0.7);
    color: #fff; border-radius: 8px;
    font-family: ui-monospace, monospace; font-size: 12px;
    z-index: 100;
  }
</style>
```

Контролы **снаружи** `.canvas` — иначе они тоже отскейлятся, на маленьком экране станут нечитаемы.

## С persistent playback position

Для видео — сохраняй позицию в `localStorage`, чтобы refresh не сбрасывал:

```js
const KEY = 'video:stage:t';
const stored = +(localStorage.getItem(KEY) || 0);
let t = stored;

function setTime(v) {
  t = v;
  localStorage.setItem(KEY, String(t));
  render(t);
}
```

Это критично — итеративная работа постоянно перегружает страницу.

## Print

Для печати убери трансформ:

```css
@media print {
  .stage { position: static; height: auto; }
  .canvas {
    width: 1920px; height: 1080px; transform: none !important;
    page-break-after: always;
  }
  body { background: #fff; }
}
```

## Антипаттерны

- ❌ Делать canvas responsive (`width: 100%`). Тогда нет фиксированных координат, motion design ломается.
- ❌ Контролы внутри scaled-канваса — на маленьком viewport крошечные.
- ❌ Использовать `vw/vh` для шрифтов внутри canvas. Используй px — масштабирование сделает всё пропорционально.
- ❌ `transform-origin: top left` — без явного `place-items: center` контент уезжает.

## Печать в PDF / экспорт

После сборки — `export-pdf` (через Playwright) или `video-export` (для motion). Оба ожидают именно такую обёртку.
