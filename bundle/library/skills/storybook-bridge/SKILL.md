---
name: "storybook-bridge"
description: "Экспорт component-playground в Storybook 7+ (CSF3) для команды с существующим Storybook. Триггеры: «выгрузи в Storybook», «CSF3»."
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


# Storybook bridge

`component-playground` — самописный demo-pageset. Storybook — стандарт. Этот скилл — мост: компоненты → CSF3 stories.

## Целевой формат (CSF3)

```js
// Button.stories.js
import { Button } from './Button';

export default {
  title: 'Inputs/Button',
  component: Button,
  argTypes: {
    variant: { control: 'select', options: ['primary', 'secondary', 'ghost'] },
    size:    { control: 'select', options: ['sm', 'md', 'lg'] },
    disabled:{ control: 'boolean' },
  },
};

export const Primary   = { args: { variant: 'primary', label: 'Click me' } };
export const Secondary = { args: { variant: 'secondary', label: 'Secondary' } };
export const Loading   = { args: { variant: 'primary', loading: true, label: 'Loading...' } };
```

## Конвертер из data.json

`component-playground` хранит описание в `data.json`. Скрипт:

```js
import fs from 'node:fs/promises';
import path from 'node:path';

const data = JSON.parse(await fs.readFile('data.json', 'utf8'));
const outDir = 'stories';
await fs.mkdir(outDir, { recursive: true });

for (const [group, items] of Object.entries(data.groups)) {
  for (const it of items) {
    if (!it.props) continue;
    const argTypes = {};
    const args = {};
    for (const [name, spec] of Object.entries(it.props)) {
      if (spec.type === 'select') {
        argTypes[name] = { control: 'select', options: spec.options };
        args[name] = spec.options[0];
      } else if (spec.type === 'bool') {
        argTypes[name] = { control: 'boolean' };
        args[name] = false;
      } else {
        argTypes[name] = { control: 'text' };
        args[name] = spec.default || '';
      }
    }

    const componentName = it.name.replace(/\s+/g, '');
    const file = `${outDir}/${componentName}.stories.js`;
    const code = `
import { ${componentName} } from '../components/${componentName}';

export default {
  title: '${group}/${it.name}',
  component: ${componentName},
  argTypes: ${JSON.stringify(argTypes, null, 2)},
};

export const Default = { args: ${JSON.stringify(args, null, 2)} };
${(it.variants || []).map(v => `
export const ${v.name.replace(/\s+/g,'')} = { args: ${JSON.stringify({ ...args, ...v.args }, null, 2)} };
`).join('')}
`;
    await fs.writeFile(file, code.trim());
    console.log('✓', file);
  }
}
```

## Установка Storybook (если нет)

```bash
npx storybook@latest init
```

Storybook сам определит React/Vue/Web Components, подсунет нужный builder.

## Структура

```
src/
  components/
    Button.jsx
    Card.jsx
  stories/
    Button.stories.js
    Card.stories.js
  index.css            ← твои tokens.css
.storybook/
  main.js
  preview.js          ← импорт tokens.css
```

`preview.js`:
```js
import '../src/index.css';

export default {
  parameters: {
    backgrounds: {
      values: [
        { name: 'light', value: '#fff' },
        { name: 'dark',  value: '#0d0d0d' },
      ],
      default: 'light',
    },
  },
};
```

## Что **не** переносится автоматически

- **Real-data блоки** (`real-data` скилл) — Storybook isolated, тащить туда настоящие fetch'и обычно нельзя. Замени на mock'и через MSW.
- **Tweaks-panel** — у Storybook свой контролов панель (`controls`). Используй её, не свою.
- **Animations engine** — Stage/Sprite не нужны внутри Storybook (там нет таймлайна). Для них отдельный demo-page остаётся.

## Альтернатива: только tokens

Если у вас нет компонентов в JS, но есть design tokens — Storybook может показывать их как documentation. Используй `@storybook/addon-themes` или собственный story:

```js
// Tokens.stories.mdx
# Color tokens

<div style="display:grid; grid-template-columns: repeat(5, 1fr); gap: 8px;">
  <div style="background: var(--primary-500); padding: 16px; color: white">primary 500</div>
  ...
</div>
```

## Когда переходить на Storybook

- Команда >3 человек.
- Компонентов >20.
- Есть npm-пайплайн.
- Нужны: snapshot tests, a11y addon, viewport addon.

Иначе — `component-playground` достаточно.
