---
name: "color-system-builder"
description: "Из одного акцента — полная палитра: light+dark, 9-step scale, semantic, WCAG-контраст. Триггеры: «построй цветовую систему», «color tokens»."
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


# Color system builder

Принцип — **oklch + ramp**. Все цвета одного семейства имеют одинаковую chroma, варьируется lightness. Это даёт визуально согласованные шкалы, которых не получишь подбором HEX'ов.

## Скрипт

`templates/build-palette.mjs`:

```bash
node build-palette.mjs "#D97757"
# → palette.css + palette.json
```

Делает:
- 9-step scale базового цвета (50, 100, 200, ..., 900)
- light + dark theme tokens
- semantic: success / warning / danger / info — той же интенсивности
- проверка WCAG AA контраста для каждой пары fg/bg

## Алгоритм

1. Парсим вход → oklch.
2. Для шкалы фиксируем chroma и hue, варьируем lightness:
   - 50: L=98%
   - 100: L=95%
   - 200: L=90%
   - 300: L=82%
   - 400: L=72%
   - 500: L=62% (исходный)
   - 600: L=52%
   - 700: L=42%
   - 800: L=32%
   - 900: L=20%
3. Semantic — те же L/C, разные H:
   - danger: H=25
   - warning: H=80
   - success: H=145
   - info: H=245
4. Контраст проверяется через WCAG-формулу.

## Скрипт целиком

```js
import fs from 'node:fs/promises';
import { converter, formatHex, wcagContrast } from 'culori';

const arg = process.argv[2];
if (!arg) { console.error('Usage: node build-palette.mjs <color>'); process.exit(1); }

const oklch = converter('oklch')(arg);
const C = oklch.c, H = oklch.h;

const steps = [98, 95, 90, 82, 72, 62, 52, 42, 32, 20];
const names = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900];

function ramp(hue, chroma) {
  const out = {};
  steps.forEach((L, i) => {
    out[names[i]] = formatHex({ mode: 'oklch', l: L/100, c: chroma, h: hue });
  });
  return out;
}

const palette = {
  primary: ramp(H, C),
  neutral: ramp(H, 0.01),  // тонированный серый, не «компьютерный»
  success: ramp(145, C),
  warning: ramp(80,  C),
  danger:  ramp(25,  C),
  info:    ramp(245, C),
};

// Светлая и тёмная тема — semantic mappings
const tokens = {
  light: {
    bg:        palette.neutral[50],
    fg:        palette.neutral[900],
    muted:     palette.neutral[600],
    rule:      palette.neutral[200],
    primary:   palette.primary[500],
    'primary-fg': palette.primary[50],
  },
  dark: {
    bg:        palette.neutral[900],
    fg:        palette.neutral[50],
    muted:     palette.neutral[400],
    rule:      palette.neutral[800],
    primary:   palette.primary[400],
    'primary-fg': palette.primary[900],
  },
};

// Контраст
function check(fg, bg) {
  const c = wcagContrast(fg, bg);
  return { ratio: c.toFixed(2), passAA: c >= 4.5, passLarge: c >= 3 };
}
const audit = {
  'light fg/bg': check(tokens.light.fg, tokens.light.bg),
  'light muted/bg': check(tokens.light.muted, tokens.light.bg),
  'light primary-fg/primary': check(tokens.light['primary-fg'], tokens.light.primary),
  'dark fg/bg': check(tokens.dark.fg, tokens.dark.bg),
  'dark muted/bg': check(tokens.dark.muted, tokens.dark.bg),
};

await fs.writeFile('palette.json', JSON.stringify({ palette, tokens, audit }, null, 2));

let css = ':root {\n';
for (const [k, v] of Object.entries(tokens.light)) css += `  --${k}: ${v};\n`;
css += '}\n[data-theme="dark"] {\n';
for (const [k, v] of Object.entries(tokens.dark)) css += `  --${k}: ${v};\n`;
css += '}\n\n';
for (const [name, ramp] of Object.entries(palette)) {
  for (const [step, hex] of Object.entries(ramp)) {
    css += `:root { --${name}-${step}: ${hex}; }\n`;
  }
}
await fs.writeFile('palette.css', css);

console.log('✓ palette.css + palette.json');
console.table(audit);
```

Зависимость: `npm i culori`.

## Что делать с выводом

- `palette.css` подключай в проект первым.
- `palette.json` отдай разработчику или используй в `dev-handoff`.
- Если в `audit` есть `passAA: false` для основных пар — палитра плохая, поправь L-значения.
