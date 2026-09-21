---
name: "visual-edit"
description: "Overlay: двигать и resize элементы мышкой, правки патчатся в CSS через локальный сервер. Триггеры: «drag handle в браузере», «alt+click resize». НЕ ревью→comment-injector."
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


# Visual edit

Сложно, но реально. Делается на двух частях:

1. **Браузерная** — overlay с draggable/resizable, шлёт через WebSocket `{selector, prop, value}`.
2. **Серверная** — слушает WebSocket, патчит inline-style в HTML или CSS-правило в `<style>`.

## Минимальная реализация

`templates/visual-edit.js` (браузер):

```js
(function () {
  let target = null, mode = null, startX, startY, startRect;
  const overlay = document.createElement('div');
  overlay.style.cssText = 'position:fixed;inset:0;pointer-events:none;z-index:99999';
  document.body.appendChild(overlay);

  document.addEventListener('contextmenu', (e) => {
    if (!e.altKey) return;
    e.preventDefault();
    select(e.target);
  });

  function select(el) {
    target = el;
    const r = el.getBoundingClientRect();
    overlay.innerHTML = `<div style="
      position:absolute;left:${r.left}px;top:${r.top}px;
      width:${r.width}px;height:${r.height}px;
      outline:2px solid #007aff;pointer-events:auto;cursor:move
    " data-mode="move"></div>`;
    overlay.firstChild.addEventListener('pointerdown', start);
  }
  function start(e) {
    e.preventDefault();
    mode = e.currentTarget.dataset.mode;
    startX = e.clientX; startY = e.clientY;
    startRect = target.getBoundingClientRect();
    addEventListener('pointermove', move);
    addEventListener('pointerup', end);
  }
  function move(e) {
    const dx = e.clientX - startX, dy = e.clientY - startY;
    if (mode === 'move') {
      target.style.transform = `translate(${dx}px,${dy}px)`;
    }
  }
  function end() {
    removeEventListener('pointermove', move);
    removeEventListener('pointerup', end);
    if (window.__ve_socket) {
      window.__ve_socket.send(JSON.stringify({
        selector: cssPath(target),
        prop: 'transform',
        value: target.style.transform,
      }));
    }
  }
  function cssPath(el){/* как в comment-injector */}
})();
```

`templates/visual-edit-server.mjs`:

```js
import { WebSocketServer } from 'ws';
import fs from 'node:fs/promises';

const wss = new WebSocketServer({ port: 5174 });
wss.on('connection', ws => {
  ws.on('message', async (raw) => {
    const { selector, prop, value } = JSON.parse(raw);
    const file = process.argv[2];
    let css = await fs.readFile(file, 'utf8');
    const rule = `${selector} { ${prop}: ${value}; }`;
    css = css.replace(/\/\* visual-edit \*\/[\s\S]*?\/\* \/visual-edit \*\//,
      `/* visual-edit */\n${rule}\n/* /visual-edit */`);
    if (!css.includes('/* visual-edit */')) css += `\n/* visual-edit */\n${rule}\n/* /visual-edit */`;
    await fs.writeFile(file, css);
    console.log('✓ patched', selector, prop, value);
  });
});
console.log('visual-edit server on :5174 — patches', process.argv[2]);
```

## Как использовать

```bash
# Терминал 1
node visual-edit-server.mjs styles.css

# Терминал 2
node live.mjs index.html
```

Подключи в HTML:
```html
<script src="visual-edit.js"></script>
<script>window.__ve_socket = new WebSocket('ws://localhost:5174');</script>
```

Alt+ПКМ выбирает элемент, drag двигает.

## Ограничения

- Работает только с inline-стилями или одним помеченным CSS-блоком. Не для production.
- Селекторы могут быть нестабильны — лучше явные `id` на ключевых элементах.
- Не делай для слайдов (pptx/print) — там точные позиции в pixel-units, drag создаёт `transform`, который может ломать экспорт.

## Legacy reference

Прежняя расширенная версия скилла (дерево @2026-04-30) сохранена целиком в `references/legacy-visual-edit.md`. Секции там: Architectural overview, Overlay script (browser side), Server side (Claude Code patches), Ограничения, Альтернативы, Когда НЕ использовать, Stack, Антипаттерны.
