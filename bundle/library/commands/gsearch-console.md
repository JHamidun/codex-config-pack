---
name: "gsearch-console"
description: "Google Search Console: сайты, топ запросов/страниц (клики, CTR, позиции), sitemaps. Триггеры: «GSC», «позиции в google». Яндекс.Вебмастер → yandex."
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


# Google Search Console Operations

/gsearch-console - Работа с Google Search Console

## Описание
Анализ поисковой выдачи, запросов и карт сайта через Search Console API.

## Использование
```
/gsearch-console sites                     - Список сайтов
/gsearch-console analytics <site_url>      - Топ запросы
/gsearch-console sitemaps <site_url>       - Карты сайта
```

## Инструкции для Claude

1. **Загрузи credentials:**
```python
import os
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

with open(os.path.expanduser('${CODEX_PACK_ROOT}/library/google_oauth_token.json'), 'r') as f:
    token_data = json.load(f)
creds = Credentials.from_authorized_user_info(token_data)
sc = build('searchconsole', 'v1', credentials=creds)
```

2. **Список сайтов:**
```python
sites = sc.sites().list().execute()
for site in sites.get('siteEntry', []):
    print(f"{site['siteUrl']} | {site['permissionLevel']}")
```

3. **Топ поисковых запросов (30 дней):**
```python
response = sc.searchanalytics().query(
    siteUrl='https://your-domain.com/',
    body={
        'startDate': '2026-02-06',
        'endDate': '2026-03-08',
        'dimensions': ['query'],
        'rowLimit': 25,
        'orderBy': [{'fieldName': 'clicks', 'sortOrder': 'DESCENDING'}]
    }
).execute()
for row in response.get('rows', []):
    query = row['keys'][0]
    clicks = row['clicks']
    impressions = row['impressions']
    ctr = row['ctr'] * 100
    position = row['position']
    print(f"{query} | clicks: {clicks} | impr: {impressions} | CTR: {ctr:.1f}% | pos: {position:.1f}")
```

4. **Топ страницы:**
```python
response = sc.searchanalytics().query(
    siteUrl='https://your-domain.com/',
    body={
        'startDate': '2026-02-06',
        'endDate': '2026-03-08',
        'dimensions': ['page'],
        'rowLimit': 25
    }
).execute()
for row in response.get('rows', []):
    page = row['keys'][0]
    print(f"{page} | clicks: {row['clicks']} | impr: {row['impressions']}")
```

5. **Запросы + страницы (комбинация):**
```python
response = sc.searchanalytics().query(
    siteUrl='https://your-domain.com/',
    body={
        'startDate': '2026-02-06',
        'endDate': '2026-03-08',
        'dimensions': ['query', 'page'],
        'rowLimit': 50,
        'dimensionFilterGroups': [{
            'filters': [{
                'dimension': 'query',
                'operator': 'contains',
                'expression': 'company'
            }]
        }]
    }
).execute()
```

6. **Карты сайта:**
```python
sitemaps = sc.sitemaps().list(siteUrl='https://your-domain.com/').execute()
for sm in sitemaps.get('sitemap', []):
    print(f"{sm['path']} | {sm.get('lastSubmitted', '')} | errors: {sm.get('errors', 0)}")
```

## Доступные dimensions
- `query` - поисковый запрос
- `page` - URL страницы
- `country` - страна
- `device` - desktop/mobile/tablet
- `date` - дата

## Метрики (всегда возвращаются)
- `clicks` - клики
- `impressions` - показы
- `ctr` - кликабельность (0-1)
- `position` - средняя позиция

## Примеры
- `/gsearch-console sites` - мои сайты
- `/gsearch-console analytics https://your-domain.com/` - топ запросы
- `/gsearch-console sitemaps https://your-domain.com/` - карты сайта
