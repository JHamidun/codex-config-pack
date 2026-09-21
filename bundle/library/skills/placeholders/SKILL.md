---
name: "placeholders"
description: "Плейсхолдеры картинок и иконок, когда реального ассета нет: полосатый SVG с подписью. Триггеры: «placeholder image», «аватар инициалы»."
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


# Placeholders

Принцип: **хороший плейсхолдер лучше плохой попытки нарисовать настоящее.**

## Image placeholder

```html
<div class="placeholder" style="aspect-ratio: 16/9;">
  <span>product hero · 1920×1080</span>
</div>
```

```css
.placeholder {
  background: repeating-linear-gradient(
    45deg, #1a1a1a, #1a1a1a 8px, #222 8px, #222 16px
  );
  display: grid; place-items: center;
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  color: #888; font-size: 14px;
  border-radius: 8px;
  text-align: center; padding: 16px;
}
```

Светлый вариант:

```css
.placeholder.light {
  background: repeating-linear-gradient(
    45deg, #ececec, #ececec 8px, #f4f4f4 8px, #f4f4f4 16px
  );
  color: #888;
}
```

## Icon placeholder

```html
<span class="icon-ph" data-name="settings"></span>
```

```css
.icon-ph {
  display: inline-block; width: 24px; height: 24px;
  background: currentColor; mask: linear-gradient(#000, #000);
  border: 1.5px solid currentColor; border-radius: 4px;
  background: transparent;
  position: relative;
}
.icon-ph::after {
  content: attr(data-name);
  position: absolute; top: 100%; left: 50%; transform: translateX(-50%);
  font-family: ui-monospace, monospace; font-size: 9px;
  white-space: nowrap; color: #888;
  margin-top: 2px;
}
```

## Avatar placeholder

```html
<div class="avatar-ph">JD</div>
```

```css
.avatar-ph {
  width: 40px; height: 40px;
  background: #d4d4d4; color: #555;
  display: grid; place-items: center;
  border-radius: 50%;
  font-family: ui-monospace, monospace;
  font-size: 13px; font-weight: 500;
}
```

## Что писать в подписи

Конкретное:
- `product hero · 1920×1080`
- `screenshot · settings page`
- `team photo · 6 people`
- `chart · revenue Q1-Q4`

Не «image», не «placeholder», не «coming soon».

## Когда плейсхолдер НЕ подходит

- В финальном артефакте, который пойдёт клиенту, — попроси у пользователя реальные изображения.
- Для логотипа — он критичен; либо проси настоящий, либо ставь `[brand mark]` текстом, не рисуй.
- В презентации с фотографиями людей — без реальных фото секция не работает; не имитируй.

## Антипаттерны

- ❌ Серый прямоугольник с текстом «Image».
- ❌ SVG с попыткой нарисовать «иконку лупы / шестерёнки» от руки. Ты не угадаешь стиль системы.
- ❌ Текст «Coming soon», «WIP», «Lorem».
- ❌ Картинки с unsplash.com, если не сказали — могут быть лицензионные сюрпризы.

## Legacy reference

Прежняя расширенная версия скилла (дерево @2026-04-30) сохранена целиком в `references/legacy-placeholders.md`. Секции там: Базовый image placeholder, Аватары, Logo placeholder, Charts placeholder, Иконки, User-uploaded references, Антипаттерны.
