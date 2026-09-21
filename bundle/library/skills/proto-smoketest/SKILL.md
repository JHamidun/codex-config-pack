---
name: "proto-smoketest"
description: "Минимальные e2e smoke-тесты прототипа: критичные пути не отвалились, не unit. Триггеры: «playwright smoke», «happy path тест»."
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


# Proto smoketest

Не пытайся писать unit-тесты для прототипа — это не production. Зато 5 e2e-проверок «не сломалось ли главное» окупаются с первой регрессии.

## Стек

Playwright Test — самый простой запуск.

```bash
npm i -D @playwright/test
npx playwright install chromium
```

## smoketest.spec.js

`templates/smoketest.spec.js`:

```js
import { test, expect } from '@playwright/test';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const FILE = pathToFileURL(path.resolve('proto.html')).href;

test('страница загружается без console error', async ({ page }) => {
  const errors = [];
  page.on('console', m => m.type() === 'error' && errors.push(m.text()));
  page.on('pageerror', e => errors.push(e.message));
  await page.goto(FILE);
  await page.waitForLoadState('networkidle');
  expect(errors, errors.join('\n')).toEqual([]);
});

test('главный CTA ведёт на следующий экран', async ({ page }) => {
  await page.goto(FILE);
  await page.click('text=Начать');
  await expect(page.locator('h1')).toContainText('Шаг 1');
});

test('форма входа принимает email и password', async ({ page }) => {
  await page.goto(FILE);
  await page.click('text=Войти');
  await page.fill('input[type=email]', 'user@example.com');
  await page.fill('input[type=password]', 'password123');
  await page.click('button[type=submit]');
  await expect(page).toHaveURL(/dashboard/);
});

test('навигация по табам работает', async ({ page }) => {
  await page.goto(FILE + '#dashboard');
  for (const tab of ['Главная', 'Лента', 'Профиль']) {
    await page.click(`role=tab[name=${tab}]`);
    await expect(page.locator(`[role=tabpanel][aria-label=${tab}]`)).toBeVisible();
  }
});

test('тёмная тема переключается', async ({ page }) => {
  await page.goto(FILE);
  await page.click('#theme-toggle');
  const bg = await page.evaluate(() => getComputedStyle(document.body).backgroundColor);
  expect(bg).toMatch(/rgb\(\s*(\d+)/);
  // Просто проверяем, что фон стал тёмным:
  const [r,g,b] = bg.match(/\d+/g).map(Number);
  expect(r + g + b).toBeLessThan(150);
});
```

```bash
npx playwright test smoketest.spec.js
```

## Что покрывать

5–10 ключевых сценариев. **Не** покрывай каждый клик.

Хорошие кандидаты:
- ✅ Прототип вообще открывается без ошибок.
- ✅ Главный путь от первого экрана до целевого.
- ✅ Самые ломкие переходы (после большого UI-рефакторинга).
- ✅ Форма с валидацией.
- ✅ Тёмная/светлая тема.

Плохие:
- ❌ Каждый текст в каждом блоке (это уже unit-тест).
- ❌ Анимации (хрупко, ломается на каждом изменении CSS).
- ❌ Точные пиксельные значения (нет смысла).

## Снимки UI

Опционально — снимки экранов для визуальной регрессии:

```js
test('скриншот главной страницы', async ({ page }) => {
  await page.goto(FILE);
  await expect(page).toHaveScreenshot('home.png', { maxDiffPixels: 100 });
});
```

При первом запуске Playwright создаст baseline. При следующих — сравнит. Чувствительность настраивается через `maxDiffPixels` / `threshold`.

## Когда запускать

- Перед сдачей пользователю — обязательно.
- После каждого крупного рефакторинга.
- В CI, если репо приватный (для прототипа CI обычно избыточен).

## Когда НЕ нужно

- Прототип на 1 день.
- Один экран без интерактива.
- Дек слайдов.
- Анимация-видео.

## Поддержка

Тесты — тоже код. Если не обновляешь их вместе с прототипом, они становятся ложными срабатываниями. Лучше **меньше** актуальных, чем больше устаревших.

## Legacy reference

Прежняя расширенная версия скилла (дерево @2026-04-30) сохранена целиком в `references/legacy-proto-smoketest.md`. Секции там: Инсталляция, Структура, Какие сценарии писать, Что НЕ тестировать, Selectors — best practices, Multi-viewport, Скриншот failures, CI integration, Output: PASS / FAIL, Когда НЕ запускать, Антипаттерны.
