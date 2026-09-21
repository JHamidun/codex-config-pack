---
name: "schema-markup-ru"
description: "Schema.org / JSON-LD разметка: Organization, Course, FAQPage; Яндекс читает JSON-LD. Триггеры: «микроразметка», «rich snippets», «звёздочки в выдаче»."
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


# Микроразметка Schema.org / JSON-LD (RU)

Реализация структурированных данных schema.org на своих сайтах, чтобы поисковики (Яндекс, Google) лучше понимали контент и показывали расширенные сниппеты, а AI-поверхности (Яндекс.Нейро, Alice, GigaChat) точнее цитировали. Порт `schema` из marketingskills: вокабуляр schema.org международный, адаптированы примеры под реальные сущности (YourFirstName, академия, воркшоп, news, блог) и заметка про Яндекс.

**Перед началом прочитай `${CODEX_PACK_ROOT}/library/business-context.md`** — раздел «Продукт» (какие сущности вообще размечаем: организация, персона, курс, услуга, товар) и раздел «Цены» (суммы и URL страниц). Файла нет — заведи из `${CODEX_PACK_ROOT}/library/templates/business-context.md`.

Здесь последствие жёстче обычного: разметка обязана совпадать с тем, что видно на странице. Выдуманная цена или несуществующий рейтинг в JSON-LD — это не «неточность», а повод для санкций поисковика. Чего не знаешь — помечай `[TODO]` и уточняй, а не подставляй правдоподобное.

**AEO/GEO связка:** JSON-LD — один из сильнейших сигналов для попадания в AI-ответы. После разметки сверяйся с `seo-machine-ru` → `skills/seo-machine-ru/references/aeo-geo.md` (цитируемость в Яндекс.Нейро/Alice/GigaChat/ChatGPT/Perplexity).

## Принципы

1. **Точность прежде всего.** Разметка обязана соответствовать видимому контенту. Не размечать то, чего нет на странице. Обновлять при изменении контента.
2. **Используй JSON-LD.** Рекомендуемый формат (и Google, и Яндекс). Скрипт `<script type="application/ld+json">` в `<head>` или конце `<body>`.
3. **Только то, что поддерживается.** Без спам-тактик. Проверять требования к rich-результатам.
4. **Валидируй всё.** Тест перед деплоем, мониторинг в Вебмастере.

## Заметка про Яндекс (важно для RU-рынка)

- Яндекс читает JSON-LD и микроформаты; расширенные сниппеты в выдаче формируются по разметке (товары, организации, FAQ, хлебные крошки, события).
- Проверка: **Яндекс.Вебмастер → Инструменты → Валидатор микроразметки** (а не только Google Rich Results Test). Дёргать через скилл `yandex` (Вебмастер) либо вручную.
- Для бизнеса/локалки — карточка в **Яндекс.Бизнес** (отдельно от JSON-LD), но `Organization`/`Person` всё равно ставим на сайт.
- AI-цитируемость: чёткий `Person` (YourFirstName как эксперт), `Organization`, `FAQPage`, `Course` помогают Яндекс.Нейро/GigaChat понять, кто автор и что за продукт.

## Типы под свои сайты

| Тип | Где ставить | Обязательные поля |
|-----|-------------|-------------------|
| Organization | your-domain.com (главная/обо мне) | name, url |
| WebSite (+SearchAction) | главная / news (поиск по сайту) | name, url |
| Person | страница «Обо мне» (YourFirstName как эксперт) | name |
| Course | academy.your-domain.com и страницы треков | name, description, provider |
| Article | блог, статьи на /media, новости news | headline, image, datePublished, author |
| FAQPage | лендинги услуг/воркшопа/academy с FAQ | mainEntity (Q&A) |
| Event | воркшоп, конференция, вебинар | name, startDate, location |
| BreadcrumbList | любая страница с навигацией/крошками | itemListElement |

Полные JSON-LD примеры под каждую сущность — `references/schema-examples.md`.

## Объединение типов на странице (@graph)

Несколько типов на одной странице — через `@graph`:

```json
{ "@context": "https://schema.org", "@graph": [
  { "@type": "Organization", "@id": "https://your-domain.com/#org", "...": "..." },
  { "@type": "Person", "@id": "https://your-domain.com/#user", "...": "..." },
  { "@type": "BreadcrumbList", "...": "..." }
]}
```

## Валидация и тестирование

- **Яндекс.Вебмастер** — валидатор микроразметки + раздел «Структурированные данные» (через `yandex`).
- **Google Rich Results Test** — search.google.com/test/rich-results.
- **Schema.org Validator** — validator.schema.org.

Типичные ошибки: нет обязательных полей; даты не в ISO 8601; URL не абсолютные; значения enum неточные (`https://schema.org/InStock`); разметка не совпадает с видимым контентом.

## Реализация под свой стек

- **Tilda** (your-domain.com, лендинги): JSON-LD вставляется в блок T123 (custom HTML) или в настройки страницы (head). Деплой и публикация — через скилл `tilda`. Учти граблины T123 (scope, лимит кода) — см. `tilda`.
- **Свой фронтенд** (Next.js, Express и подобные — блог, медиа, платформа курсов): рендерить `<script type="application/ld+json">` на сервере (SSR), сериализуя данные в JSON-LD на каждой странице (статья → Article, лендинг → Course/FAQPage).

## Связки

| Нужно | Скилл |
|------|-------|
| Контекст сущностей, URL, цены | `${CODEX_PACK_ROOT}/library/business-context.md` (заведи из `templates/`) |
| AEO/GEO (цитируемость в AI) | `seo-machine-ru` (`skills/seo-machine-ru/references/aeo-geo.md`) |
| Валидация в Вебмастере | `yandex` |
| Вставка JSON-LD на Tilda + публикация | `tilda` |
| SEO-контент страницы целиком | `seo-machine-ru` |

## Формат вывода

1. Полный JSON-LD блок (готов к вставке).
2. Куда вставлять (Tilda T123 / head / SSR-компонент).
3. Чеклист: валидируется в Вебмастере + Rich Results; нет ошибок/предупреждений; совпадает с контентом; все обязательные поля; даты ISO 8601; URL абсолютные.

## Вопросы под задачу

1. Какой тип страницы (главная / обо мне / курс или его модуль / статья / лендинг услуги / новость)?
2. Какой rich-результат целевой (FAQ-аккордеон, карточка организации, событие, курс)?
3. Какие данные есть на странице для заполнения (цены, даты, автор, изображения)?
4. Есть ли уже разметка (не дублировать)?
5. Стек страницы — Tilda или Next.js/Express?
