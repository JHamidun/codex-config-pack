---
name: "standalone-html"
description: "Свернуть HTML со всеми ассетами в один офлайн-файл (inline base64). Триггеры: «один файл html», «self-contained», «чтобы можно было отправить»."
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


# Standalone HTML

Inline-вшивает в один HTML все локальные ресурсы: CSS, JS, изображения, шрифты.

## Скрипт

`templates/inline.mjs`:

```js
import fs from 'node:fs/promises';
import path from 'node:path';

const [, , input, output] = process.argv;
if (!input) { console.error('Usage: node inline.mjs <input.html> [output.html]'); process.exit(1); }

const out = output || input.replace(/\.html?$/, '.standalone.html');
const dir = path.dirname(input);
let html = await fs.readFile(input, 'utf8');

// <link rel="stylesheet" href="..."> → <style>
html = await replaceAsync(html, /<link\s+[^>]*rel=["']stylesheet["'][^>]*>/gi, async (tag) => {
  const m = tag.match(/href=["']([^"']+)["']/);
  if (!m || /^https?:|\/\//.test(m[1])) return tag;
  const css = await fs.readFile(path.join(dir, m[1]), 'utf8');
  return `<style>\n${css}\n</style>`;
});

// <script src="..."> → <script>...</script>
html = await replaceAsync(html, /<script\s+[^>]*src=["']([^"']+)["'][^>]*>\s*<\/script>/gi, async (tag, src) => {
  if (/^https?:|\/\//.test(src)) return tag;
  const code = await fs.readFile(path.join(dir, src), 'utf8');
  const typeMatch = tag.match(/type=["']([^"']+)["']/);
  const type = typeMatch ? ` type="${typeMatch[1]}"` : '';
  return `<script${type}>\n${code}\n</script>`;
});

// <img src="..."> → data URL
html = await replaceAsync(html, /<img\s+[^>]*src=["']([^"']+)["'][^>]*>/gi, async (tag, src) => {
  if (/^https?:|\/\/|data:/.test(src)) return tag;
  try {
    const buf = await fs.readFile(path.join(dir, src));
    const ext = path.extname(src).slice(1).toLowerCase() || 'png';
    const mime = { svg: 'svg+xml', jpg: 'jpeg', jpeg: 'jpeg', png: 'png', webp: 'webp', gif: 'gif' }[ext] || 'octet-stream';
    const data = `data:image/${mime};base64,${buf.toString('base64')}`;
    return tag.replace(src, data);
  } catch { return tag; }
});

// url(...) внутри инлайн-CSS — тоже data URL
html = await replaceAsync(html, /url\(["']?([^"')]+)["']?\)/g, async (m, src) => {
  if (/^https?:|\/\/|data:/.test(src)) return m;
  try {
    const buf = await fs.readFile(path.join(dir, src));
    const ext = path.extname(src).slice(1).toLowerCase();
    const mime = ({ woff2: 'font/woff2', woff: 'font/woff', ttf: 'font/ttf',
      svg: 'image/svg+xml', png: 'image/png', jpg: 'image/jpeg', jpeg: 'image/jpeg' })[ext] || 'application/octet-stream';
    return `url("data:${mime};base64,${buf.toString('base64')}")`;
  } catch { return m; }
});

await fs.writeFile(out, html);
console.log('✓', out);

async function replaceAsync(str, re, fn) {
  const promises = [];
  str.replace(re, (...args) => { promises.push(fn(...args)); return ''; });
  const results = await Promise.all(promises);
  let i = 0;
  return str.replace(re, () => results[i++]);
}
```

## Запуск

```bash
node inline.mjs deck.html
# → deck.standalone.html
```

## Ограничения

- Внешние URL (`https://...`) скрипт не трогает — они останутся ссылками. Если нужен полный офлайн — заранее скачай шрифты и CDN-скрипты в проект.
- `<iframe src="...">` не разворачивается. iframe-вариантные канвасы (см. `design-canvas`) теряют содержимое — для них либо инлайнь HTML внутрь, либо отдай ZIP.
- Размер: один HTML с шрифтами и картинками легко вырастает до 5–10 MB. Для отправки по почте оставь ассеты во внешних папках или сожми изображения.

## Legacy reference

Прежняя расширенная версия скилла (дерево @2026-04-30) сохранена целиком в `references/legacy-standalone-html.md`. Секции там: Какие inline'ятся, Каркас inliner script, CDN scripts — оставлять или embedd'ить?, Размеры — что разумно, Verifier для standalone, Когда НЕ делать standalone, Stacking, Антипаттерны.
