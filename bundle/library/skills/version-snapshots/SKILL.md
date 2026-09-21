---
name: "version-snapshots"
description: "Копии артефакта в .snapshots/ + MANIFEST.md — откат без git. Триггеры: «snapshot перед правкой», «откати к baseline», «история версий»."
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


# Version snapshots

Заменяет «сохрани сначала на всякий случай» — Claude должен делать это автоматически.

## Когда снимать снапшот

- Перед большой правкой (рефактор разметки, смена темы).
- После завершения фичи / экрана.
- Перед экспортом.

Каждый раз — копия в `.snapshots/<filename>.<ISO-timestamp>.html`.

## Скрипт

`templates/snapshot.mjs`:

```js
import fs from 'node:fs/promises';
import path from 'node:path';
import { execSync } from 'node:child_process';
import crypto from 'node:crypto';

const file = process.argv[2];
const note = process.argv.slice(3).join(' ') || '(без подписи)';
if (!file) { console.error('Usage: node snapshot.mjs <file> [note]'); process.exit(1); }

const dir = '.snapshots';
await fs.mkdir(dir, { recursive: true });

const ts = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
const ext = path.extname(file);
const base = path.basename(file, ext);
const dest = path.join(dir, `${base}.${ts}${ext}`);
await fs.copyFile(file, dest);

// миниатюра, если есть playwright
let thumb = '';
try {
  const thumbPath = path.join(dir, `${base}.${ts}.png`);
  execSync(`node -e "
    import('playwright').then(async ({chromium}) => {
      const b = await chromium.launch();
      const p = await b.newPage({viewport:{width:1280,height:800}});
      await p.goto('file://${path.resolve(file)}');
      await p.screenshot({path:'${thumbPath}'});
      await b.close();
    })
  "`, { stdio: 'ignore' });
  thumb = `![](${path.basename(thumbPath)})`;
} catch {}

const manifest = path.join(dir, 'MANIFEST.md');
const line = `\n### ${ts}  \n**${path.basename(dest)}** — ${note}  \n${thumb}\n`;
await fs.appendFile(manifest, line);
console.log('✓', dest);
```

## Использование

```bash
node snapshot.mjs index.html "до смены темы на dark"
```

## Откат

```bash
cp .snapshots/index.2026-04-28T15-32-00.html index.html
```

## Чистка

`.snapshots/` может разрастись. Раз в неделю:
```bash
find .snapshots -mtime +30 -delete
```

## Что НЕ делать

- Не коммить `.snapshots/` в git — добавь в `.gitignore`.
- Не используй вместо git. Git делает то же самое лучше. Snapshots — для тех, кто без git, или внутри одной сессии.

## Legacy reference

Прежняя расширенная версия скилла (дерево @2026-04-30) сохранена целиком в `references/legacy-version-snapshots.md`. Секции там: Структура, Snapshot trigger, Snapshot script, List snapshots, Restore, Diff между snapshots, Cleanup, .gitignore, Когда НЕ нужно, Stack, Антипаттерны.
