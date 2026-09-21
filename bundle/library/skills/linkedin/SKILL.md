---
name: "linkedin"
description: "LinkedIn-разведка (Scraping API): профили, компании, посты. Триггеры: «пробей профиль linkedin», «найди контакты в linkedin». НЕ реклама→ad-spy; свой пост→linkedin-post-writer."
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


# LinkedIn Intelligence (ScraperVendor)

> One API key covers all endpoints. Auth: `SCRAPER_API_KEY` from `${CODEX_PACK_ROOT}/library/.credentials.master.env`

## API Endpoints

| Endpoint | Path | Credits | Use Case |
|----------|------|---------|----------|
| Person Profile | `/v1/linkedin/profile` | 1 | Полное досье: опыт, навыки, образование |
| Company Page | `/v1/linkedin/company` | 1 | Размер, индустрия, описание, HQ |
| Company Posts | `/v1/linkedin/company/posts` | 1 | Контент-мониторинг конкурентов |
| Post Details | `/v1/linkedin/post` | 1 | Engagement: likes, comments, reposts |
| Ad Search | `/v1/linkedin/ads/search` | 1 | Рекламные кампании конкурентов |
| Ad Details | `/v1/linkedin/ad` | 1 | Детали конкретного объявления |

## Base URL & Auth

```
BASE_URL = https://api.your-scraper.example
HEADER: x-api-key: $SCRAPER_API_KEY
```

## Operations

### 1. Profile Enrichment (основное)

Получить полные данные о человеке по LinkedIn URL или username.

```bash
# Load API key
source ${CODEX_PACK_ROOT}/library/.credentials.master.env

# By LinkedIn URL
curl -s "https://api.your-scraper.example/v1/linkedin/profile?url=https://www.linkedin.com/in/username/" \
  -H "x-api-key: $SCRAPER_API_KEY" | python3 -m json.tool

# By username
curl -s "https://api.your-scraper.example/v1/linkedin/profile?username=username" \
  -H "x-api-key: $SCRAPER_API_KEY" | python3 -m json.tool
```

**Output:** name, headline, summary, experience[], education[], skills[], certifications[], location, connections, profilePicture

**Use cases:**
- Обогащение лидов перед звонком (`/call-prep`)
- Исследование спикеров/экспертов
- Подготовка персонализированного outreach

### 2. Company Research

```bash
curl -s "https://api.your-scraper.example/v1/linkedin/company?url=https://www.linkedin.com/company/company-name/" \
  -H "x-api-key: $SCRAPER_API_KEY" | python3 -m json.tool
```

**Output:** name, description, industry, companySize, headquarters, specialties, founded, website, followers

### 3. Company Posts Monitoring

```bash
curl -s "https://api.your-scraper.example/v1/linkedin/company/posts?url=https://www.linkedin.com/company/company-name/" \
  -H "x-api-key: $SCRAPER_API_KEY" | python3 -m json.tool
```

**Use cases:**
- Мониторинг контент-стратегии конкурентов
- Анализ engagement rate по постам
- Выявление тем, которые резонируют с аудиторией

### 4. Post Deep Dive

```bash
curl -s "https://api.your-scraper.example/v1/linkedin/post?url=https://www.linkedin.com/feed/update/urn:li:activity:1234567890/" \
  -H "x-api-key: $SCRAPER_API_KEY" | python3 -m json.tool
```

### 5. LinkedIn Ad Library

```bash
# Search ads by company or keyword
curl -s "https://api.your-scraper.example/v1/linkedin/ads/search?query=YourProduct" \
  -H "x-api-key: $SCRAPER_API_KEY" | python3 -m json.tool

# Get specific ad details
curl -s "https://api.your-scraper.example/v1/linkedin/ad?id=AD_ID" \
  -H "x-api-key: $SCRAPER_API_KEY" | python3 -m json.tool
```

**Use cases:**
- Конкурентная разведка: какую рекламу крутят конкуренты
- Benchmarking рекламных креативов
- Мониторинг рекламной активности в нише

## Outreach Workflow

1. **Find targets:** WebSearch `site:linkedin.com/in [role] [company] [location]`
2. **Enrich profiles:** `/v1/linkedin/profile` — получить полные данные
3. **Research company:** `/v1/linkedin/company` — контекст о компании
4. **Check their posts:** `/v1/linkedin/company/posts` — темы для персонализации
5. **Generate message:** Персонализированный outreach на основе данных
6. **Track:** Сохранить в свою CRM (через её API) или Google Sheets

## Batch Processing

Для массового обогащения используй Python-скрипт:

```bash
python3 -c "
import json, os, time
import urllib.request

API_KEY = os.getenv('SCRAPER_API_KEY')
urls = ['https://www.linkedin.com/in/user1/', 'https://www.linkedin.com/in/user2/']

for url in urls:
    req = urllib.request.Request(
        f'https://api.your-scraper.example/v1/linkedin/profile?url={url}',
        headers={'x-api-key': API_KEY}
    )
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read())
    print(json.dumps({'name': data.get('name'), 'headline': data.get('headline'), 'company': data.get('company')}, ensure_ascii=False))
    time.sleep(1)  # rate limit courtesy
"
```

## Integration with Other Skills

| Workflow | Skills Chain |
|----------|------------|
| Lead enrichment → Call prep | `linkedin` → `call-prep` |
| Company research → Outreach | `linkedin` → `account-research` → `draft-outreach` |
| Competitor monitoring → Analysis | `linkedin` (company posts) → `competitive-analysis` |
| Ad intelligence → Campaign planning | `linkedin` (ads) → `campaign-planning` |
| Profile → CRM | `linkedin` → импорт в твою CRM (создать контакт/сделку через её API) |

## Safety & Limits

- ScraperVendor кредиты: 1 credit per request
- Не отправляй сообщения через API — только сбор данных
- Для outreach используй персонализированные шаблоны, не спам
- Храни результаты локально или в CRM, не в git
- Rate limit courtesy: 1 sec delay между запросами в batch mode
