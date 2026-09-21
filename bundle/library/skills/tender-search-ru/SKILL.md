---
name: "tender-search-ru"
description: "Russian procurement tender search via Playwright: geo-block workaround (zakupki -> rostender), OKPD2 filtering. Triggers: «тендеры», «госзакупки»."
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


# Tender Search (Russia)

## Overview

Find Russian procurement tenders relevant to a product/company and return a curated, filtered shortlist (number, subject, region, deadline, price, link). Built from a real session searching AI/LLM tenders. The core difficulty is not search syntax - it is the **geo-block** on the official portal and the **weak free-tier relevance** on aggregators. This skill encodes the workarounds.

## When to Use

- "найди тендеры / контракты / госзакупки / закупки под <продукт>"
- "поищи подходящие контракты для <компания>"
- "что закупают по <тема> на zakupki / rostender"
- Any procurement-discovery task on the Russian market via the browser.

Not for: writing the commercial proposal (КП) or outreach - that is `kp-deck-factory` / `draft-outreach`.

## Key Facts (non-obvious - read first)

| Fact | Consequence |
|------|-------------|
| **zakupki.gov.ru geo-blocks foreign IPs** -> `ERR_CONNECTION_TIMED_OUT` | From a non-RU IP (any non-RU IP) the official portal will NOT load. Confirm IP first. |
| The MCP Playwright browser **cannot install extensions at runtime** | A VPN browser-extension cannot be added to the running automation browser. Extensions load only at launch (`--load-extension`, headed, persistent profile). |
| Most free VPN extensions give a **foreign** IP, not a Russian one | To open zakupki you need a server *inside* RU. Free Planet VPN / Browsec usually lack RU - won't unblock it. Need a RU-capable paid VPN or RU proxy. |
| **rostender.info works from any IP** and aggregates ALL RF tenders (7600+ sources, incl. zakupki data) | Default to rostender when no RU IP is available - coverage is effectively complete. |
| rostender **free tier hides** customer, НМЦК, documentation, and ЭТП/source link behind registration | Free scan gives subject + region + deadline + method only. To unlock fields -> 7-day demo, or zakupki.gov.ru via RU IP. |
| rostender search ranks **by date, not relevance**, and multi-word queries become fuzzy AND-matches | Use ONE broad phrase + filter client-side. Do not chain 3+ keywords. |

### Эскалация при бот-стене / гео-блоке (patchright)

Обход по умолчанию — уходить с zakupki.gov.ru на **rostender** (см. Key Facts). Но если и
агрегатор начинает палить автоматизацию (Cloudflare-challenge, «Access denied», пустой
контент при headless-скрапе), либо появился RU-прокси и нужно всё-таки открыть саму
zakupki.gov.ru под анти-ботом — эскалируй на **patchright** (стелс-форк Playwright,
drop-in `from patchright.sync_api import sync_playwright`, `channel="chrome"` + persistent
context). Он скрывает `navigator.webdriver` и CDP-утечки, которые ловит защита порталов.
Полный рецепт и таблица «симптом бана → инструмент» — `../playwright-automation/references/stealth-scraping.md`.

## Workflow

### 1. Build the product profile -> query set
Translate the product into procurement language. For an AI/LLM product: subjects are *доступ к нейросетям / большим языковым моделям*, *ИИ-ассистент*, *чат-бот*, *генеративный ИИ*, *неисключительные права на ПО*. Keyword + OKPD2 sets are in `references/playbook.md`.

### 2. Check the IP / decide the route
Navigate to `http://ip-api.com/json/?fields=query,country,countryCode,city` (plain HTTP - `ipapi.co` is Cloudflare-walled).
- **RU IP** -> can use zakupki.gov.ru directly (best: proper OKPD2 search - see `references/playbook.md`).
- **Foreign IP** -> use **rostender.info**. Do not waste time on free VPN extensions (see Key Facts). Only pursue a VPN/proxy route if the user supplies a RU-capable one.

### 3. Search on rostender
1. Go to `https://rostender.info/` and type ONE broad phrase into the homepage search box (placeholder "Введите ключевые слова..."), submit. It redirects to `https://rostender.info/extsearch?query=<hash>`.
2. Broad recall (`искусственный интеллект`) returns thousands sorted newest-first - relevant active ones cluster on **pages 1-2**.
3. Paginate by appending `&page=N` to the query URL (20 rows/page).

### 4. Extract + filter (client-side relevance)
Run the extractor (full version in `references/playbook.md`) via `browser_evaluate`. Critical detail: the tender **title** is `a.tender-info__description` - the first `a[href*="/tender"]` is the *category*, not the title. Filter with an `include` regex (доступ к, нейросет, LLM, генеративн, чат-бот, ассистент, неисключительн, обработк/аналитик...) AND an `exclude` regex (книг, учебник, повышение квалификации, сервер, оборудование, школьн...) to strip courses/hardware/books noise. Compute `active` from the Окончание date >= today.

### 5. Present the shortlist
Markdown table: `№ | предмет | регион | дедлайн | цена | ссылка`, sorted by fit then deadline; separate **active** from **just-closed** (closed ones still inform the market). Note explicitly that customer/НМЦК/ЭТП are behind the registration wall on free tier, and that a "запрос цен / обоснование НМЦК" item = chance to submit a КП that shapes a future tender.

### 6. Offer next steps
Unlock fields via rostender 7-day demo (also enables saved keyword templates + Telegram alerts), or zakupki.gov.ru via RU IP for OKPD2 search; export the shortlist to Excel; or deepen the scan (more pages/queries).

## References

- `references/playbook.md` - read for: the full `browser_evaluate` extractor (correct selectors + relevance regex), rostender pagination details, zakupki.gov.ru direct-search URL params, the AI/LLM keyword set, OKPD2 codes, and the list of alternative aggregators (synapsenet, tenderland, b2b-center, roseltorg, sberbank-ast).
