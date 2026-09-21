---
name: "sketch-to-html"
description: "Скетч, фото доски, салфетки или Excalidraw → HTML-каркас. Триггеры: «из скетча в html», «whiteboard в каркас». НЕ PDF/DOCX → document-import."
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


# Sketch to HTML

Не пытайся «распознавать» руками. У тебя есть способность видеть картинку — используй её прямо.

## Алгоритм

1. **Открой картинку.** Просто через `view_image` (или эквивалент в Claude Code — Read с путём к картинке).
2. **Опиши вслух, что видишь.** Не сразу строй HTML, сначала проговори:
   - Это один экран или флоу?
   - Сколько секций / прямоугольников / зон?
   - Есть ли подписи и стрелки между ними?
   - Что ты считаешь заголовком, что — текстом, что — кнопкой?
3. **Покажи описание пользователю.** «Вижу 3 экрана. На первом форма входа, на втором лента карточек, на третьем настройки. Между ними стрелки 1→2→3. Правильно понял?»
4. **Дождись подтверждения.** Не строй HTML, пока пользователь не согласился с описанием.
5. **Перейди в `wireframe`** — собери черновик в low-fi.
6. После утверждения — переходи в hi-fi через `interactive-prototype` или `slides`.

## Чего не делать

- ❌ Не угадывай детали, которых не видно. «Сделай красиво» — это сигнал спросить.
- ❌ Не игнорируй стрелки и подписи. Они часто несут важную инфу о флоу.
- ❌ Не теряй пропорции. Если на скетче sidebar занимает 1/4 ширины — на твоём wireframe тоже.

## Если скетч сделан в excalidraw / tldraw / .napkin

- `.napkin` — рисовалка с превью рядом. Если есть `scraps/.{name}.thumbnail.png` — открой превью.
- Excalidraw export — `.excalidraw.json` или `.png`. JSON парси, PNG смотри глазами.
- tldraw — `.tldr` это JSON. Можно вытащить shapes, но проще смотреть PNG-экспорт.

## Полезные пометки в описании

Когда описываешь скетч, размечай так:

```
Экран 1 — Login
  ┌────────────────┐
  │ [LOGO]         │
  │                │
  │ Email   [____] │
  │ Pass    [____] │
  │                │
  │   [Sign in →]  │
  │   forgot pwd?  │
  └────────────────┘
       ↓ on submit
Экран 2 — Feed
  ...
```

Эту разметку отправь пользователю как часть описания. Так ему легче подтвердить или поправить.

## После HTML

Сохрани оригинал скетча рядом с артефактом (`assets/sketch-source.png`), сошлись на него в комментарии в HTML — пригодится при будущих правках.

## Legacy reference

Прежняя расширенная версия скилла (дерево @2026-04-30) сохранена целиком в `references/legacy-sketch-to-html.md`. Секции там: Workflow, Identification (визуально), Output: wireframe-style HTML, Excalidraw / draw.io / Whimsical, Photo recognition (whiteboard), Что НЕ переносить, Что переносить, Уточняющие вопросы, Stack, Антипаттерны.
