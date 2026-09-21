---
name: "canonical-html"
description: "Канонический HTML: закрытые теги, double-quotes, без implied-close — для предсказуемых правок инструментами. Триггеры: «почини разметку», «закрой теги»."
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


# Canonical HTML

Цель — чтобы любая дальнейшая инструментальная правка (find-replace, AST, форматтеры, патчи через WebSocket в `visual-edit`) работала предсказуемо.

## Правила

### 1. Закрывай каждый non-void тег явно
```html
<!-- плохо -->
<p>Привет
<p>Мир

<!-- хорошо -->
<p>Привет</p>
<p>Мир</p>
```

`<p>`, `<li>`, `<dt>`, `<dd>`, `<option>`, `<thead>`, `<tbody>`, `<tr>`, `<td>` — у всех implied-close. Закрывай все вручную.

### 2. Double-quote атрибуты
```html
<!-- плохо -->
<input type=text required>
<a href=/foo class=link>foo</a>

<!-- хорошо -->
<input type="text" required>
<a href="/foo" class="link">foo</a>
```

Boolean-атрибуты без значения — OK (`required`, `disabled`, `hidden`).

### 3. Не self-close non-void
```html
<!-- плохо -->
<div class="card" />
<span/>

<!-- хорошо -->
<div class="card"></div>
<span></span>
```

Self-closing валиден только в SVG/MathML и для void-элементов (`<br>`, `<hr>`, `<img>`, `<input>`, `<meta>`, `<link>`, `<source>`, `<area>`, `<col>`, `<embed>`, `<wbr>`).

### 4. Атрибуты в стабильном порядке
Не обязательно, но удобно. Рекомендую:
1. `id`
2. `class`
3. `data-*`
4. `aria-*`
5. role
6. остальное

### 5. Никаких `<style>`/`<script>` без `</style>`/`</script>`
Даже если пустой.

### 6. Мета-теги — full open/close не нужны (void)
```html
<meta charset="utf-8">
<link rel="stylesheet" href="...">
```

## Список void-элементов (самозакрывающихся БЕЗ слеша)

`area`, `base`, `br`, `col`, `embed`, `hr`, `img`, `input`, `link`, `meta`, `source`, `track`, `wbr`.

Всё остальное — открывать и закрывать парой.

## Почему это важно

- Регэкспы вида `</p>` начинают находить настоящие пары, а не воздух.
- AST-парсеры (cheerio, jsdom, htmlparser2) одинаково видят дерево, как браузер.
- Find-replace в редакторе не превращается в лотерею.
- `visual-edit` и `tweaks-panel` (её запись значений на диск) могут патчить файл без неожиданностей.

## Антипаттерны

- ❌ `<p>` перед `<div>` без `</p>` — браузер закроет `p` за тебя, но AST не всегда.
- ❌ `<img />` — лишний слеш. Просто `<img>`.
- ❌ Mixed quotes: `class='card' id="hero"` — выбери один стиль.
- ❌ Attribute-value в одинарных кавычках: `<a href='...'>` — работает, но непоследовательно с большинством стилей.

## Чек-перед-сдачей

```bash
npx html-validate <file>     # отловит implied-close и пр.
npx prettier --check <file>  # форматирование
```
