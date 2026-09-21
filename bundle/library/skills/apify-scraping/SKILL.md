---
name: "apify-scraping"
description: "Скрапинг через Apify Actors: соцсети, e-commerce, поисковики. Триггеры: «спарси сайт», «apify актор». НЕ аудитории VK Ads→vk-ads-pro-ru."
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


# Apify Web Scraping Skill

Навык для использования Apify Actors для парсинга веб-данных.

## Когда использовать
- Парсинг социальных сетей (Instagram, TikTok, YouTube, X/Twitter, LinkedIn)
- Сбор данных с e-commerce (Amazon, eBay, AliExpress)
- Парсинг поисковых систем (Google, Bing, Google Maps)
- Сбор контактов и лидов
- Мониторинг цен и отзывов
- Скрапинг любых веб-сайтов

## Справочники (references/)

- **[references/curated-actors.md](references/curated-actors.md)** — curated индекс 130+ Actor'ов с точными ID по платформам (Instagram, Facebook, TikTok, YouTube, X, LinkedIn, Maps, отзывы, недвижимость, SEO, RAG-краулинг, Telegram/Reddit/Snapchat, обогащение контактов). **Всегда сверяй ID отсюда перед вызовом.**
- **[references/apify-gotchas.md](references/apify-gotchas.md)** — модели оплаты (FREE/PPE/FLAT), протокол оценки стоимости, частые грабли (cookies, rate limits, пустые результаты, deprecated Actors), восстановление после ошибок, лимиты по платформам.

> ⚠️ **Namespace важнее всего.** Таблицы ниже — упрощённые; часть ID неполные. Реальные namespace'ы: TikTok = `clockworks/`, YouTube = `streamers/`, Google Maps = `compass/`, X/Twitter = `apidojo/`, LinkedIn = `harvestapi/` + `apimaestro/`. С неверным namespace (`apify/tiktok-scraper` и т.п.) вызов не найдёт Actor — бери точные ID из `curated-actors.md`.
>
> Схему входа тяни динамически: `apify actors info "ACTOR_ID" --input --json`.

## Популярные Actors

### Социальные сети

| Actor | Назначение | Пример использования |
|-------|------------|---------------------|
| `apify/instagram-scraper` | Instagram посты, профили, хэштеги | "Спарси последние 100 постов @username" |
| `apify/instagram-profile-scraper` | Детальная информация профиля | "Получи статистику профиля" |
| `apify/tiktok-scraper` | TikTok видео, профили, тренды | "Найди топ видео по хэштегу" |
| `apify/youtube-scraper` | YouTube видео, каналы, комментарии | "Спарси видео канала" |
| `apify/twitter-scraper` | X/Twitter посты, профили | "Собери твиты по запросу" |
| `apify/linkedin-profile-scraper` | LinkedIn профили | "Получи данные профиля" |

> **VK-аудитории для рекламы**: Apify VK-actors НЕ покрывают полный workflow парсинга аудиторий для VK Ads (нотация PS/CS/А/ТУ/НВ, метод А, вечные аудитории). Production-grade парсер для VK Ads — **Target Hunter** (не Apify). См. скилл `vk-ads-pro-ru` для VK-аудиторий.

### E-commerce

| Actor | Назначение | Пример использования |
|-------|------------|---------------------|
| `apify/amazon-product-scraper` | Amazon товары, цены, отзывы | "Спарси товары по запросу" |
| `apify/amazon-reviews-scraper` | Отзывы Amazon | "Собери отзывы на товар" |
| `apify/ebay-scraper` | eBay листинги | "Найди товары по категории" |
| `apify/aliexpress-scraper` | AliExpress товары | "Мониторинг цен" |

### Поисковые системы

| Actor | Назначение | Пример использования |
|-------|------------|---------------------|
| `apify/google-search-scraper` | Google поиск | "Топ-100 результатов по запросу" |
| `apify/google-maps-scraper` | Google Maps места | "Найди все рестораны в районе" |
| `apify/bing-search-scraper` | Bing поиск | "Результаты поиска Bing" |

### Универсальные

| Actor | Назначение | Пример использования |
|-------|------------|---------------------|
| `apify/web-scraper` | Любой сайт (конфигурируемый) | "Спарси данные с сайта X" |
| `apify/cheerio-scraper` | Быстрый HTML парсинг | "Извлеки текст со страницы" |
| `apify/puppeteer-scraper` | JS-rendered страницы | "Спарси SPA сайт" |
| `apify/playwright-scraper` | Сложные взаимодействия | "Заполни форму и получи результат" |

## Примеры команд

### Социальные сети
```
"Спарси последние 50 постов Instagram @nasa"
"Собери топ-20 TikTok видео по хэштегу #coding"
"Получи информацию о YouTube канале MrBeast"
"Найди твиты про AI за последнюю неделю"
```

### E-commerce
```
"Найди все iPhone на Amazon до $500"
"Спарси отзывы на товар ASIN B08N5WRWNW"
"Мониторь цены на AliExpress по запросу 'wireless earbuds'"
```

### Поиск и карты
```
"Топ-50 результатов Google по 'best restaurants NYC'"
"Найди все кофейни в радиусе 5км от координат"
"Собери контакты компаний по запросу в Google Maps"
```

### Контакты и лиды
```
"Найди email адреса с сайта company.com"
"Собери контакты IT компаний в LinkedIn"
```

## Формат данных

Apify возвращает структурированные данные в JSON:

```json
{
  "results": [
    {
      "url": "https://...",
      "title": "...",
      "description": "...",
      "price": "...",
      "rating": 4.5,
      "reviews": 123
    }
  ]
}
```

## Лимиты и стоимость

- **Бесплатный план**: $5/месяц в кредитах
- **Оплата**: Pay-per-use за compute units
- **Примерная стоимость**:
  - 1000 Instagram постов: ~$1-2
  - 1000 Amazon товаров: ~$2-3
  - 1000 Google результатов: ~$0.5-1

## Советы

1. **Начинай с малого**: Сначала спарси 10-50 записей для проверки
2. **Используй фильтры**: Сужай запросы для экономии ресурсов
3. **Кэшируй результаты**: Сохраняй в Redis/SQLite для повторного использования
4. **Проверяй лимиты**: Некоторые сайты имеют rate limits
5. **Комбинируй с N8N**: Автоматизируй регулярный парсинг

## Интеграция с другими MCP

```
Apify → Redis (кэш) → PostgreSQL (хранение)
Apify → N8N (автоматизация) → Slack (уведомления)
Apify → Claude (анализ) → Notion (документация)
```
