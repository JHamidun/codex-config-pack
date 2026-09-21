---
name: "meta-ads-analyzer"
description: "Диагностика кампаний Meta Ads: Breakdown Effect. Триггеры: «почему дорого в Meta», «не выходит из обучения». НЕ запуск→meta-ads-launch-ru."
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


# Meta Ads Analysis & Diagnosis

Expert framework for Meta Ads campaign analysis with focus on the Breakdown Effect.

## Scope & Boundary

**Этот скилл — ДИАГНОСТИКА существующих Meta-кампаний:** что сломалось, почему стало дорого, выходит ли кампания из обучения, не паузить ли сегмент по высокому avg CPA. Работаешь с метриками уже запущенной рекламы.

| Задача | Куда идти |
|:---|:---|
| Анализ метрик, что сломалось, почему дорого, Breakdown Effect, Learning Phase, Ad Relevance | **этот скилл** |
| ЗАПУСК / настройка пикселя+CAPI / выбор события / стратегии ставок / lookalike / масштабирование | **`meta-ads-launch-ru`** |
| Анализ КОНКУРЕНТОВ, шпионаж за креативами, Meta Ad Library, longest-running ads | **`ad-spy`** |
| Нормы CPM/CPL/CPA/ROAS по каналам и нишам | **`ad-benchmarks-ru`** |

> Граница: `meta-ads-launch-ru` **запускает и ведёт** кампанию (setup → launch → scale). Этот скилл **диагностирует** уже работающую. Если по ходу диагностики выясняется, что причина — в неправильной настройке (событие, аудитория, lookalike), передавай в `meta-ads-launch-ru`.

## Core Principle

**The Breakdown Effect:** When breaking down campaign data by dimension (placement, age, gender, device), the sum of segment CPAs weighted by their spend does NOT equal the campaign-level CPA due to Meta's marginal cost optimization.

**Critical rule:** NEVER recommend pausing segments based solely on higher average CPA. Higher average cost does NOT mean poor performance — it often reflects the system capturing low marginal cost opportunities earlier.

## Analysis Workflow

### Step 1: Identify Evaluation Level

| Campaign Setup | Correct Evaluation Level |
|:---|:---|
| Advantage+ Campaign Budget (CBO) | **Campaign Level** |
| Automatic Placements (without CBO) | **Ad Set Level** |
| Multiple Ads in single Ad Set | **Ad Set Level** |

### Step 2: Analyze with Meta-Specific Lens

1. **Marginal Efficiency Analysis** — Infer marginal CPA trends from time-series data
2. **Ad Relevance Diagnostics** — Quality, Engagement, Conversion Rate Rankings
3. **Learning Phase Status** — ~50 results needed to exit learning phase

### Step 3: Synthesize Through Breakdown Effect Lens

Interpret all findings through marginal vs average cost dynamics.

## Key Concepts

### Marginal vs Average CPA

- **Average CPA** = Total Spend / Total Results
- **Marginal CPA** = Cost of the NEXT result
- System optimizes for lowest marginal CPA, not lowest average

**Example:** Placement A shows $10 avg CPA vs Placement B's $15. But Placement A's marginal CPA is rising sharply — system correctly shifts budget to Placement B to get more total results.

### Ad Auction Mechanics

Total Value = Advertiser Bid x Estimated Action Rate + Ad Quality

Winners are determined by Total Value, not just bid amount.

### Learning Phase

- Ad sets need ~50 optimization events to exit
- Performance during learning is unstable
- Avoid edits that reset learning (budget >20%, audience changes, creative swaps)

### Pacing

Meta distributes budget evenly across the day using pacing algorithms. Early underspend or overspend are normal system behavior.

## Mandatory Report Rules

1. **NEVER** recommend pausing segments based solely on higher average CPA
2. **ALWAYS** justify recommendations with data evidence + system mechanics
3. **USE** qualified language: "Estimated Reach of ~1,000" not "You reached 1,000"
4. **DISAMBIGUATE** clicks: "Clicks (all)" vs "Link Clicks" — always specify
5. **CHECK** `get_recommendations` API first if Meta API access available
6. Every insight must include data evidence and explanation

## Data Import

Users provide data via:
- CSV export from Meta Ads Manager
- Excel file with campaign data
- Manual data entry
- Meta Marketing API (if access token available)

### CSV Import Pattern

```python
import pandas as pd

# Read Meta Ads export
df = pd.read_csv("meta_ads_export.csv")

# Key columns
# Campaign name, Ad Set Name, Ad Name
# Impressions, Reach, Frequency
# Link Clicks, CPC, CTR
# Results, Cost per Result, Amount Spent
# Relevance Score / Quality Ranking
```

## When to Use

**Trigger words:** "meta ads", "facebook ads", "instagram ads", "рекламный кабинет", "CPA analysis", "breakdown effect", "ad performance", "campaign optimization", "ROAS", "cost per result", "диагностика Meta кампании", "почему дорого в Meta", "воронка обучения Meta", "не выходит из обучения", "Meta vs Google различие", "когда не Meta", "проблема не Meta-специфична"

**НЕ для:** запуска/настройки/масштабирования (→ `meta-ads-launch-ru`), анализа конкурентов (→ `ad-spy`), норм по каналам (→ `ad-benchmarks-ru`).

## Reference Documents

For deep analysis, read these bundled references:
- `references/breakdown_effect.md` — The Breakdown Effect with examples
- `references/core_concepts.md` — Ad Auction, Pacing, Learning Phase
- `references/analysis_checklist.md` — Step-by-step analysis template
- `references/meta-vs-google-diagnostic.md` — Meta vs Google различие при диагностике: разная длительность Learning Phase (Google 5-7 дней vs Meta <24ч), привязка событий, как отличить Meta-специфику от универсальной проблемы аукциона
- `references/learning-funnel-diagnostic.md` — воронка обучения Meta (общая → CPC-кластер → ядро) + 7 факторов сброса + 4 безопасных действия как диагностический чеклист «почему не выходит из обучения»

## Related Skills

- **`meta-ads-launch-ru`** — ЗАПУСК/настройка/масштабирование Meta (пиксель+CAPI, выбор события, стратегии ставок, lookalike-лестница, scaling rules). Куда передавать, если диагноз — «неправильно настроено».
- **`ad-spy`** — анализ креативов КОНКУРЕНТОВ (Meta Ad Library, longest-running ads, Atria).
- **`ad-benchmarks-ru`** — нормы CPM/CPL/CPA/ROAS по каналам и нишам для сверки.
