---
name: "perf-audit"
description: "Lighthouse в headless перед публикацией страницы: LCP, CLS, TBT, размер бандла, конкретные советы. Триггеры: «Core Web Vitals», «оптимизация перформанс»."
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


# Perf audit

## Установка

```bash
npm i -D lighthouse playwright chrome-launcher
```

## Скрипт

`templates/perf.mjs`:

```js
import lighthouse from 'lighthouse';
import * as chromeLauncher from 'chrome-launcher';
import http from 'node:http';
import fs from 'node:fs/promises';
import path from 'node:path';

const file = process.argv[2];
if (!file) { console.error('Usage: node perf.mjs <file>'); process.exit(1); }

// Поднимем простейший http-сервер для замера (file:// не работает корректно)
const server = http.createServer(async (req, res) => {
  const f = req.url === '/' ? file : '.' + req.url;
  try {
    const buf = await fs.readFile(f);
    res.writeHead(200); res.end(buf);
  } catch { res.writeHead(404); res.end(); }
});
await new Promise(r => server.listen(0, r));
const port = server.address().port;

const chrome = await chromeLauncher.launch({ chromeFlags: ['--headless'] });
const result = await lighthouse(`http://localhost:${port}/`, {
  port: chrome.port, output: 'json',
  onlyCategories: ['performance', 'accessibility', 'best-practices', 'seo'],
});
await chrome.kill();
server.close();

await fs.writeFile('perf-report.json', JSON.stringify(result.lhr, null, 2));

const cats = result.lhr.categories;
console.log('\nLighthouse:');
for (const [k, v] of Object.entries(cats)) {
  const score = Math.round(v.score * 100);
  const tag = score >= 90 ? '✓' : score >= 50 ? '~' : '✗';
  console.log(`  ${tag} ${k.padEnd(16)} ${score}`);
}

const audits = result.lhr.audits;
console.log('\nВеб-витал:');
for (const k of ['largest-contentful-paint', 'cumulative-layout-shift', 'total-blocking-time']) {
  const a = audits[k];
  console.log(`  ${a.title.padEnd(28)} ${a.displayValue || '—'}`);
}

const fails = Object.values(audits)
  .filter(a => a.score !== null && a.score < 0.9 && a.details)
  .sort((x, y) => x.score - y.score)
  .slice(0, 10);
console.log('\nТоп-10 замечаний:');
for (const a of fails) console.log(`  - ${a.title} (${a.displayValue || ''})`);

process.exit(cats.performance.score >= 0.8 ? 0 : 1);
```

## Использование

```bash
node perf.mjs index.html
# → perf-report.json + табличка в консоль
```

## Ключевые метрики

- **LCP < 2.5s** — Largest Contentful Paint. Когда главный элемент стал видим.
- **CLS < 0.1** — Cumulative Layout Shift. Сколько прыгает layout при загрузке.
- **TBT < 300ms** — Total Blocking Time. Сколько времени main thread заблокирован.

## Типовые проблемы и решения

| Проблема | Решение |
|---|---|
| Большой LCP | Прелоад hero-картинки, `fetchpriority="high"`, AVIF/WebP вместо PNG |
| Высокий CLS | Указывай `width`+`height` на картинках, резервируй место под динамический контент |
| Много TBT | Дробить JS, отложить аналитику, не блокировать main thread |
| Большой бандл | Tree-shake, lazy-load роуты, не тащи moment.js |
| Шрифты | `font-display: swap`, preload only critical weights |
| Картинки | Современные форматы, `loading="lazy"` для below-the-fold |

## Бюджеты

Для лендинга:
- HTML < 50KB
- CSS < 50KB
- JS < 200KB (gzipped)
- Картинки < 500KB суммарно на первый экран
- Шрифты < 100KB (max 2 веса)

## Чего perf-audit **не** покажет

- Воспринимаемая скорость (animation jank).
- Реальные сетевые условия пользователей.
- Стоимость гидратации в SPA.

Для них — Chrome DevTools → Performance с CPU throttling 4x и Slow 3G.

## Legacy reference

Прежняя расширенная версия скилла (дерево @2026-04-30) сохранена целиком в `references/legacy-perf-audit.md`. Секции там: Установка, CLI quick-check, Programmatic через Playwright + Lighthouse, Core Web Vitals — пороги, Типовые проблемы prototype'ов, Output — actionable отчёт, Core Web Vitals, Quick wins (savings ~500ms), Не критично, Когда НЕ делать perf-audit, Антипаттерны.
