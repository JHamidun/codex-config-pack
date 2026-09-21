---
name: "design-md-brands"
description: "Банк DESIGN.md брендов (Stripe, Linear, Vercel, Notion, Apple — 73+). Триггеры: «как у Linear», «эстетика Notion». НЕ стиль по URL → brand-extractor."
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


# DESIGN.md brands — банк дизайн-систем брендов

Reference-пак поверх открытого репо **[VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md)** (MIT). Не хранит копии брендов локально — тянет актуальный `DESIGN.md` по требованию. Комплементарен нашим дизайн-скиллам, ничего не заменяет.

## Что такое DESIGN.md

Концепт **Google Stitch**: один plain-text markdown-файл в корне проекта, который ИИ-агент читает и по нему генерит консистентный UI. Без тулинга, без токен-JSON — просто разметка, которую понимает и человек, и модель. Репо awesome-design-md — курируемый банк таких файлов, снятых с сайтов известных брендов.

**Когда это нужно нам:** пользователь говорит «сделай в стиле Stripe / как у Linear / эстетика Notion». Раньше выбор был: (а) угадать палитру, (б) `brand-extractor` скрейпит живой сайт (риск anti-bot). Теперь для популярных брендов есть готовая, вычищенная дизайн-система — забрать и применить.

## Как достать DESIGN.md конкретного бренда

Файлы лежат по схеме `design-md/<brand>/DESIGN.md`. Забирай raw-версию через WebFetch:

```
https://raw.githubusercontent.com/VoltAgent/awesome-design-md/main/design-md/<brand>/DESIGN.md
```

Примеры (проверенные пути): `.../design-md/stripe/DESIGN.md`, `.../design-md/linear.app/DESIGN.md`, `.../design-md/vercel/DESIGN.md`, `.../design-md/notion/DESIGN.md`, `.../design-md/apple/DESIGN.md`.

**Гоча — имя папки ≠ всегда чистое имя бренда.** Некоторые с доменом/суффиксом: `linear.app`, `mistral.ai`, `x.ai`, `together.ai`, `opencode.ai`, `cal` (не cal.com), `bmw-m`, `dell-1996`, `nintendo-2001`, `runway ml`. Если прямой путь дал 404 — сперва глянь листинг папок: WebFetch `https://github.com/VoltAgent/awesome-design-md/tree/main/design-md`, найди точное имя, потом тяни raw.

## Каталог брендов (73+, на момент аудита 100+ папок — репо растёт)

| Категория | Бренды (имена ≈ папки) |
|---|---|
| **AI / LLM** | claude, cohere, elevenlabs, mistral.ai, minimax, together.ai, x.ai, ollama, replicate, runway ml, composio, opencode.ai |
| **Dev-tools** | cursor, vercel, warp, raycast, expo, lovable, resend, sentry, hashicorp, voltagent |
| **Backend / DB** | supabase, mongodb, posthog, sanity, clickhouse |
| **SaaS / Productivity** | linear.app, notion, cal, zapier, airtable, intercom, slack, superhuman, clay, miro |
| **Design / Content** | figma, framer, webflow, pinterest, theverge, wired |
| **Fintech / Crypto** | stripe, wise, coinbase, binance, kraken, mastercard, revolut |
| **Consumer / E-com** | airbnb, shopify, starbucks, spotify, uber, nike, meta |
| **Big Tech / Hardware** | apple, ibm, nvidia, hp, spacex, playstation, vodafone |
| **Automotive** | tesla, ferrari, bmw, bmw-m, lamborghini, bugatti, renault |
| **Ретро-веб (стилизация)** | dell-1996, nintendo-2001 |

Список неполный и меняется — источник истины всегда листинг репо. Нет нужного бренда — см. «Брендов нет в банке» ниже.

## Структура файла DESIGN.md (схема Stitch, 9 блоков)

Заголовки чуть плавают от бренда к бренду, но каркас один (пример со Stripe):

1. **Overview** — визуальная тема, атмосфера, философия
2. **Colors** — семантические роли + hex (Brand & Accent / Surface / Text / Semantic)
3. **Typography** — семейства, иерархия, принципы, заметка о шрифтах-заменах
4. **Layout** — spacing-шкала, grid/контейнер, философия воздуха
5. **Elevation & Depth** — тени, слои поверхностей (обычно таблица)
6. **Shapes** — border-radius шкала, геометрия фото/иллюстраций
7. **Components** — buttons, cards, inputs/forms, nav, pills/tags, signature-компоненты (со стейтами)
8. **Do's and Don'ts** — гардрейлы
9. **Responsive Behavior** — брейкпоинты, тач-таргеты, стратегия схлопывания, поведение картинок
   (+ иногда финальный **Iteration / Agent Prompt Guide** — краткая шпаргалка цветов для промпта агенту)

Формат цвета внутри — семантическое имя + токен + hex + где применять, напр.:
`**Indigo** (`{colors.primary}` — `#533afd`): signature CTA. Filled-pill button, link emphasis, gradient anchor.`

## Как применять (workflow)

1. Пользователь назвал бренд-референс → определи имя папки (листинг репо при сомнении).
2. WebFetch raw `DESIGN.md` → получил дизайн-систему.
3. Отдай её как контекст в `design-orchestrator` / нужный артефакт-скилл (`slides`, `interactive-prototype`, `website-creation`). Дальше весь артефакт держи в этой системе — палитра, типографика, радиусы, тени берутся из файла, не выдумываются.
4. Нужен один файл в корень проекта для другого ИИ-агента (Cursor/Stitch/Copilot) — просто положи `DESIGN.md` туда.

## Брендов нет в банке / нужен свой

- **Живой сайт по URL** → `brand-extractor` (Playwright, вытащит цвета/шрифты/копирайт), результат оформи по шаблону `references/design-md-template.md`.
- **С нуля / свой продукт** → `design-system-create` + `color-system-builder` + `type-scale`, финал — в тот же шаблон DESIGN.md.
- Авторский DESIGN.md пиши по `references/design-md-template.md` (9 блоков Stitch).

## Этика / границы

- Репо MIT, файлы существуют для генерации консистентного UI и НЕ передают права на чужую айдентику. Не выдавай брендированную систему чужого продукта за свою — см. `content-policy`.
- Для НАШЕГО бренда (Anthropic look-and-feel) — `brand-guidelines`, не этот скилл.
- Требует только сетевого доступа к github/raw.githubusercontent — прокси/ключи не нужны.

## Соседние скиллы

`design-orchestrator` (диспетчер) · `brand-extractor` (скрейп живого сайта) · `design-system-create` (генерация с нуля) · `color-system-builder` / `type-scale` (сборка палитры/шкалы) · `frontend-design` (выбор эстетики когда системы нет) · `brand-guidelines` (Anthropic).
