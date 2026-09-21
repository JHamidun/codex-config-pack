---
name: "gads"
description: "Google Ads по API (GAQL): аккаунты, кампании, отчёты по расходам. Триггеры: «гугл реклама», «отчёт google ads»."
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


# Google Ads Operations

/gads - Работа с Google Ads

## Описание
Управление рекламными кампаниями и отчётами через Google Ads API.

## Использование
```
/gads accounts                   - Список аккаунтов
/gads campaigns <customer_id>    - Кампании аккаунта
/gads report <customer_id>       - Отчёт по кампаниям
```

## Инструкции для Claude

**ВАЖНО:** Google Ads использует собственную клиентскую библиотеку, а не стандартный `googleapiclient`.

### Установка
```bash
pip install google-ads
```

### 1. Загрузи credentials (Google Ads Client):
```python
import os
import json
from google.ads.googleads.client import GoogleAdsClient

with open(os.path.expanduser('${CODEX_PACK_ROOT}/library/google_oauth_token.json'), 'r') as f:
    token_data = json.load(f)

# Google Ads требует developer token + login customer ID
config = {
    'developer_token': 'YOUR_DEVELOPER_TOKEN',
    'client_id': token_data.get('client_id'),
    'client_secret': token_data.get('client_secret'),
    'refresh_token': token_data.get('refresh_token'),
    'use_proto_plus': True,
    'login_customer_id': '1234567890'  # MCC ID без дефисов
}
client = GoogleAdsClient.load_from_dict(config)
```

### 2. Список доступных аккаунтов:
```python
customer_service = client.get_service('CustomerService')
accessible = customer_service.list_accessible_customers()
for resource_name in accessible.resource_names:
    print(resource_name)  # customers/1234567890
```

### 3. Кампании аккаунта (GAQL):
```python
ga_service = client.get_service('GoogleAdsService')
query = """
    SELECT campaign.id, campaign.name, campaign.status,
           campaign_budget.amount_micros
    FROM campaign
    WHERE campaign.status != 'REMOVED'
    ORDER BY campaign.id
"""
response = ga_service.search(customer_id='1234567890', query=query)
for row in response:
    c = row.campaign
    budget = row.campaign_budget.amount_micros / 1_000_000
    print(f"{c.id} | {c.name} | {c.status.name} | budget: {budget}")
```

### 4. Отчёт по метрикам:
```python
query = """
    SELECT campaign.name,
           metrics.impressions,
           metrics.clicks,
           metrics.cost_micros,
           metrics.conversions,
           metrics.average_cpc
    FROM campaign
    WHERE segments.date DURING LAST_30_DAYS
      AND campaign.status = 'ENABLED'
    ORDER BY metrics.cost_micros DESC
"""
response = ga_service.search(customer_id='1234567890', query=query)
for row in response:
    cost = row.metrics.cost_micros / 1_000_000
    cpc = row.metrics.average_cpc / 1_000_000
    print(f"{row.campaign.name} | impr: {row.metrics.impressions} "
          f"| clicks: {row.metrics.clicks} | cost: {cost:.2f} | cpc: {cpc:.2f}")
```

### 5. Ключевые слова:
```python
query = """
    SELECT ad_group_criterion.keyword.text,
           ad_group_criterion.keyword.match_type,
           metrics.impressions, metrics.clicks, metrics.cost_micros
    FROM keyword_view
    WHERE segments.date DURING LAST_7_DAYS
    ORDER BY metrics.impressions DESC
    LIMIT 25
"""
response = ga_service.search(customer_id='1234567890', query=query)
```

## GAQL (Google Ads Query Language)
- `DURING LAST_7_DAYS`, `LAST_30_DAYS`, `THIS_MONTH`
- `WHERE campaign.status = 'ENABLED'`
- Суммы в `_micros` — делить на 1,000,000

## Примеры
- `/gads accounts` - доступные рекламные аккаунты
- `/gads campaigns 1234567890` - кампании аккаунта
- `/gads report 1234567890` - метрики за 30 дней
