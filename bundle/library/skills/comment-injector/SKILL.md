---
name: "comment-injector"
description: "Overlay в HTML: Alt+Click по элементу кладёт в clipboard CSS-селектор и outerHTML — правки без скриншотов. Триггеры: «ревью прототипа в браузере». НЕ правка мышкой→visual-edit."
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


# Comment injector

Добавь `<script src="comment-injector.js"></script>` в страницу или дёрни `?cc=1` через query-параметр (snippet ниже).

При нажатии **Alt+Click** на элемент — копирует в clipboard:

```
SELECTOR: .product-card .title
OUTER_HTML: <h3 class="title">Apex Pro</h3>
```

Пользователь вставляет это в чат → ты сразу знаешь, что править.

## Snippet

`templates/comment-injector.js`:

```js
(function () {
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') document.body.removeAttribute('data-cc-on');
  });
  document.addEventListener('click', (e) => {
    if (!e.altKey) return;
    e.preventDefault(); e.stopPropagation();
    const el = e.target;
    const sel = cssPath(el);
    const text = `SELECTOR: ${sel}\nOUTER_HTML: ${el.outerHTML.slice(0, 400)}`;
    navigator.clipboard.writeText(text);
    flash(el);
  }, true);

  function cssPath(el) {
    const parts = [];
    while (el && el.nodeType === 1 && parts.length < 6) {
      let part = el.tagName.toLowerCase();
      if (el.id) { part += '#' + el.id; parts.unshift(part); break; }
      if (el.className) part += '.' + [...el.classList].slice(0, 2).join('.');
      const sib = [...el.parentNode.children].filter(c => c.tagName === el.tagName);
      if (sib.length > 1) part += `:nth-of-type(${sib.indexOf(el) + 1})`;
      parts.unshift(part);
      el = el.parentElement;
    }
    return parts.join(' > ');
  }
  function flash(el) {
    const o = el.style.outline;
    el.style.outline = '2px solid #ff3b30';
    setTimeout(() => { el.style.outline = o; }, 600);
  }
})();
```

## Auto-inject через live-preview

В `live.mjs` добавь `?cc=1` логику или просто включи всегда — много места не занимает.

## Антипаттерны

- Не используй в production-сборке. Это инструмент работы.
- Не объединяй с обычным `click` — будет конфликтовать. Только `alt+click`.
