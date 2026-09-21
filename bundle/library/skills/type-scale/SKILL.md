---
name: "type-scale"
description: "Modular type scale из base + ratio, плюс 30 проверенных font-пар. Триггеры: «modular scale», «font pair», «причесать размеры шрифтов»."
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


# Type scale

## Modular scale

Размеры выводятся из base × ratio^n. Не подбираются «на глаз».

| Ratio | Имя | Подходит |
|---|---|---|
| 1.125 | Major Second | плотные UI, дашборды |
| 1.2   | Minor Third  | дефолт |
| 1.25  | Major Third  | редактирование длинных текстов |
| 1.333 | Perfect Fourth | питчи, лендинги |
| 1.414 | Augmented 4th | dramatic, манифесты |
| 1.5   | Perfect Fifth | максимум контраста |

Базовый размер: 16px веб, 17px iOS, 14px компактный UI.

## Скрипт

`templates/type-scale.mjs`:

```js
const base  = +(process.argv[2] || 16);
const ratio = +(process.argv[3] || 1.25);
const names = ['xs','sm','base','lg','xl','2xl','3xl','4xl','5xl','6xl'];
const offset = -2;

console.log(':root {');
names.forEach((n, i) => {
  const px = (base * Math.pow(ratio, i + offset)).toFixed(0);
  console.log(`  --text-${n}: ${px}px;`);
});
console.log('}');
```

```bash
node type-scale.mjs 16 1.25
# → :root { --text-xs: 10px; --text-sm: 13px; --text-base: 16px; ... }
```

## Готовые пары шрифтов

Не Inter+Inter и не Roboto-везде. Эти 30 пар проверены:

### Безопасные

| Display | Body |
|---|---|
| Helvetica Neue Bold | Helvetica Neue Regular |
| GT Walsheim | Söhne Buch |
| Söhne | Söhne Mono (для кода) |
| Gotham | Gotham Book |

### Sans + Sans

| Display | Body |
|---|---|
| Untitled Sans | Untitled Sans (light) |
| GT America Mono | GT America |
| Founders Grotesk | Source Sans Pro |
| Aktiv Grotesk | Aktiv Grotesk |
| Neue Haas Unica | Neue Haas Unica |

### Serif + Sans

| Display | Body |
|---|---|
| Source Serif Pro | Source Sans Pro |
| Spectral | Inter (тут уместно) |
| GT Sectra | GT America |
| Tiempos Headline | Tiempos Text |
| Domaine Display | Founders Grotesk |
| Canela | Söhne |
| Editorial New | PP Neue Montreal |

### Serif + Serif (только если умеешь)

| Display | Body |
|---|---|
| Lyon Display | Lyon Text |
| Domaine Display | Domaine Text |
| Tiempos Headline | Tiempos Text |

### Mono + Sans

| Display | Body |
|---|---|
| JetBrains Mono | Inter |
| GT America Mono | GT America |
| Berkeley Mono | Söhne |
| iA Writer Mono | iA Writer Quattro |

### Бесплатные с Google Fonts

| Display | Body |
|---|---|
| Fraunces | Inter |
| Bricolage Grotesque | Inter |
| Outfit | Outfit |
| Space Grotesk | Space Mono (для меток) |
| DM Serif Display | DM Sans |

## Правила пары

- **Контраст в категории** — serif + sans лучше двух sans.
- **Один вес для тела** — не используй italic как акцент в теле, это шум.
- **Один шрифт для длинных пассажей** — не миксуй два serif в одном абзаце.
- **Mono — только для кода и меток**, не для тела.

## Проверка

После выбора:
1. Напиши заголовок 5 слов, подзаголовок 12 слов, абзац 60 слов.
2. Уменьши до 50% масштаба — читаемо?
3. Распечатай (или PDF) — выглядит ли как «дизайн», а не «Word»?

## Legacy reference

Прежняя расширенная версия скилла (дерево @2026-04-30) сохранена целиком в `references/legacy-type-scale.md`. Секции там: Math, Готовые ratio, Пример: ratio 1.25 (Major Third), base 16, Line-height по уровню, Letter-spacing, Font-weight scale, 5 проверенных пар head + body + mono, Self-hosted vs Google Fonts, Как применить в tokens.css, Антипаттерны.
