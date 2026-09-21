---
name: "cookbook"
description: "Готовые сценарии из скиллов под типовые задачи: питч-дек, прототип, дизайн-система, лендинг. Триггеры: «pitch deck workflow», «готовый сценарий»."
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


# Cookbook

Сценарии. Каждый — последовательность из существующих скиллов под конкретную задачу.

---

## 1. Питч-дек за 30 минут

**Запрос:** «Сделай дек на 8 слайдов, питчим инвесторам, тема — наш AI-продукт».

**Шаги:**
1. `questions-protocol` — задай 6-8 вопросов: размер раунда, кто инвесторы, главная цифра, бренд, тон.
2. `document-import` — если приложен PRD/одностраничник, извлеки из него.
3. `design-orchestrator` решает: `slides` + `deck-themes:editorial` или `:dark`.
4. Скаффолд: title → problem → solution → market → traction → product → team → ask.
5. `placeholders` для логотипов и скринов продукта.
6. `content-rules` — пройти весь дек, выкинуть слова-паразиты.
7. `verifier` — открыть, поймать ошибки, скриншоты.
8. `export-pdf` или `export-pptx` (editable, через `pptx-editable-extractor`).

**Антипаттерны:** не плодить filler-слайды, не делать «Why us» из 4 общих слов.

---

## 2. Прототип онбординга для мобайла

**Запрос:** «Сделай интерактивный онбординг для приложения доставки еды».

**Шаги:**
1. `questions-protocol` — платформа, шаги, что валидируется на каждом, тёмная тема, реальные данные?
2. `wireframe` — 6-8 экранов в storyboard, согласовать структуру.
3. `frontend-design` — выбрать направление (soft / minimal).
4. `design-system-create` (минимальная) — токены, кнопка, инпут, карточка.
5. `interactive-prototype` + `device-frames:ios` (или android).
6. `mobile-overlays` — клавиатура, bottom sheet, тосты по контексту.
7. `tweaks-panel` — 2-3 крутилки для перебора (тёмная тема, цвет акцента, копирайт CTA).
8. `states-checklist` — empty/loading/error для каждого экрана с данными.
9. `claude-in-html` — если есть AI-фича.
10. `verifier`, `proto-smoketest` — критичные пути работают.

**Антипаттерны:** не имитировать клавиатуру картинкой, не делать «Welcome» на 3 экрана.

---

## 3. Дизайн-система с нуля за неделю

**Запрос:** «Нужна дизайн-система для продукта, света и темы, веб + мобайл».

**Шаги:**
1. `questions-protocol` — продуктовые домены, акцентные цвета, существующие гайды, конкуренты.
2. `moodboard` — собрать 10-15 референсов в один HTML.
3. `frontend-design` — выбрать направление.
4. `color-system-builder` — токены light + dark, 9-step scales.
5. `type-scale` — modular scale, font-pair.
6. `design-system-create` — структура файлов, tokens.css, базовые компоненты.
7. `component-playground` — страница со всеми вариантами всех компонентов.
8. `dark-mode-add` — добавить тёмную тему.
9. `forms-a11y` — формы с правильной семантикой.
10. `a11y-audit` — пройти axe, починить.
11. `dev-handoff` — собрать пакет для разраба.

**Антипаттерны:** не делать 50 компонентов сразу, не добавлять цвета без проверки контраста.

---

## 4. Лендинг продукта с реальными данными

**Запрос:** «Лендинг для нашей SaaS, нужен интерактивный демо-блок с реальными данными».

**Шаги:**
1. `questions-protocol` — аудитория, главное обещание, есть ли бренд, формат демо.
2. `wireframe` — 4-6 структур, согласовать.
3. `figma-import` — если есть бренд в Figma.
4. `frontend-design` — направление.
5. `design-canvas` — 2-3 варианта первого экрана бок-о-бок.
6. После выбора: основной HTML.
7. `microinteractions` — skeleton, hover-states, scroll-reveal.
8. `real-data` — подключить демо-блок к настоящему датасету.
9. `print-styles` — чтобы PDF лендинга выглядел прилично.
10. `perf-audit` — Lighthouse, починить LCP.
11. `a11y-audit`, `i18n-stress-test` (если многоязычный).
12. `standalone-html` для шаринга по почте.

**Антипаттерны:** не делать hero «Welcome to <product>», не плодить секции.

---

## 5. Анимация-объяснялка для соцсетей

**Запрос:** «Нужно объяснить нашу фичу за 30 секунд видео для твиттера».

**Шаги:**
1. `questions-protocol` — формат (квадрат / горизонталь / вертикаль), длительность, со звуком ли.
2. Сценарий: 4-6 кадров, на каждый по 4-6 секунд.
3. `wireframe` — раскадровка.
4. `frontend-design` — выбрать визуал, чтобы читалось на маленьком экране.
5. `animations` — `<Stage>` + `<Sprite>` для каждого кадра.
6. `placeholders` для скринов продукта.
7. `verifier` — анимация без ошибок в консоли.
8. `video-export` — MP4 1080×1080 или 1080×1920.
9. Опционально: добавить звук через ffmpeg.

**Антипаттерны:** не делать длиннее 30 сек, не помещать мелкий текст, не использовать `linear` easing.

---

## Как использовать рецепт

- Прочитай шаги до начала. Не пропускай questions.
- Каждый шаг — отдельный коммит / отдельная итерация.
- Если шаг даёт плохой результат — остановись и уточни у пользователя, не идти дальше.
- Можно комбинировать рецепты (питч → внутри один слайд с прототипом из рецепта 2).

## Когда никакой рецепт не подходит

Возвращайся к `design-orchestrator`. Он решает, какие скиллы запускать, без жёсткого сценария.
