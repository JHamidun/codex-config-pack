---
name: "youtube-analytics"
description: "Аналитика YouTube-канала (Data API v3): метрики видео, кластеризация тем, вовлечение. Триггеры: «аналитика ютуб», «почему просмотры упали»."
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


# YouTube Analytics

Deep analytics for YouTube channels via Data API v3. No browser needed.

## Что понадобится

| Что | Платно | Где взять |
|---|---|---|
| `YOUTUBE_API_KEY` | нет (квота 10 000 единиц/сутки бесплатно) | Google Cloud Console → включить **YouTube Data API v3** → Credentials → API key |
| `YOUTUBE_CHANNEL_ID` | — | ID начинается с `UC…`. Найти: YouTube Studio → Settings → Channel → Advanced settings, либо в исходнике страницы канала по строке `"channelId"` |
| Python 3.x | — | stdlib only: json, urllib, datetime, collections |

Ключ читается **только из окружения**, никаких файлов: `export YOUTUBE_API_KEY=…`.
Держишь свой `.credentials.master.env` — подтяни его перед запуском (`source …`).
Публичные метрики (просмотры, лайки, комментарии) видны по API-ключу без OAuth;
приватные (удержание, CTR, источники трафика) требуют OAuth и YouTube **Analytics** API —
этот навык их не трогает.

## Quick Start

```bash
export YOUTUBE_API_KEY=...          # или: source ${CODEX_PACK_ROOT}/library/.credentials.master.env
export YOUTUBE_CHANNEL_ID=UC...     # свой канал

python ${CODEX_PACK_ROOT}/library/skills/youtube-analytics/scripts/yt_fetch.py            # → <временный каталог ОС>/yt_videos.json
python ${CODEX_PACK_ROOT}/library/skills/youtube-analytics/scripts/yt_fetch.py out.json   # свой путь
```

Отдельного `yt_analyze.py` в навыке нет и он не нужен: `yt_fetch.py` отдаёт полный JSON
по всем роликам, а разбор по модулям ниже делает сам агент — так проще менять срезы,
чем править скрипт под каждый новый вопрос.

## API Endpoints Used

| Endpoint | Purpose | Quota Cost |
|----------|---------|------------|
| `channels?part=statistics,snippet` | Channel overview (subs, total views) | 1 unit |
| `playlistItems?part=snippet` | List all videos from uploads playlist | 1 unit/page |
| `videos?part=statistics,contentDetails,snippet` | Per-video metrics (views, likes, duration) | 1 unit/50 videos |

**Quota:** 10,000 units/day. Full channel scan of 300 videos ≈ 15 units.

## Analytics Modules

### 1. Distribution Analysis
- Views distribution (top 10%, median, bottom 10%)
- Likes-to-views ratio by tier
- Comment density analysis
- Identify viral outliers (>3σ from mean)

### 2. Topic Clustering
- Extract keywords from titles (Russian + English)
- Group by topic: AI models (DeepSeek, GPT, Gemini), companies (NVIDIA, Tesla, Musk), business/money
- Views per topic cluster with engagement rates
- Identify winning vs underperforming topics

### 3. Time & Day Optimization
- Views by day of week (aggregate)
- Views by hour of publication (в часовом поясе основной аудитории, не в UTC)
- Best publishing windows
- Seasonal trends (monthly aggregation)

### 4. Duration Analysis
- Group by duration buckets: <30s, 30-60s, 1-3min, 3-10min, 10min+
- Average views per bucket
- Engagement rate (likes/views) per bucket
- Optimal duration range

### 5. Title Analysis
- Title length vs views correlation
- Emoji usage impact
- Question marks / numbers in titles
- Hashtag effectiveness (какие из твоих постоянных хэштегов реально коррелируют с просмотрами)

### 6. Growth Trajectory
- Cumulative uploads over time
- Publishing frequency (videos/week rolling average)
- Views trend by cohort (first 30 days, 90 days, lifetime)

### 7. Shorts vs Long-Form
- Separate metrics for Shorts (<60s, 9:16) vs regular videos
- Compare engagement rates
- Identify format sweet spot

## Output Format

Generate structured report with:

```
## Channel Overview
- Subscribers: X
- Total videos: X
- Total views: X
- Average views/video: X
- Median views: X

## Top Performers (>3σ)
| # | Title | Views | Likes | Published |
...

## Topic Performance
| Topic | Videos | Avg Views | Best Video |
...

## Publishing Optimization
| Day | Avg Views | Best Hour (в поясе аудитории) |
...

## Recommendations
1. ...
2. ...
```

## Профиль своего канала — заполняется по итогам первого прогона

Это **не справочные значения**, а карточка, которую ты заполняешь СВОИМИ числами и
дальше держишь актуальной. Смысл в том, чтобы выводы не пересчитывались заново каждый
раз, а следующий прогон сравнивался с предыдущим. Копию удобно положить в
`${CODEX_WORKSPACE}/.codex-context/business-context.md` — оттуда её читают `trend-engine` и `shorts-pipeline`.

```markdown
Канал: [@handle] ([UC…])
Дата анализа: [YYYY-MM-DD], видео в выборке: [N]

- Медиана просмотров: [N]  (среднее не берём: его перекашивают виральные выбросы)
- Топ-темы: [3-5 тем, что реально залетают — S-tier]
- Стабильные темы: [3-5 тем — A-tier]
- Лучший формат: [длина и ориентация]
- Лучшие дни: [дни недели]
- Лучшее время: [часы, в поясе аудитории]
- Паттерн виральных: [что общего у выбросов >3σ]
- Паттерн заголовка: [длина, эмодзи да/нет, что внутри]
- Хэштеги: [постоянный набор]
```

Как это заполнить — пройти модули 1-7 выше по свежему `yt_videos.json`.
**Каждое поле должно быть посчитано, а не оценено на глаз**: «лучшие дни» без таблицы
средних просмотров по дням — это ощущение, а не факт, и решения по нему стоят охвата.

## Integration

Works with:
- Skill `shorts-pipeline` — выводы аналитики → темы и формат новых роликов
- Skill `trend-engine` — S/A-tier темы отсюда идут в скоринг новых тем
- Google Docs / Sheets API — выгрузка отчётов и сырых данных

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| API quota exceeded | Cache the JSON (path is printed on the last line) and don't re-fetch the same day |
| Wrong channel ID | UC prefix = channel, UU prefix = uploads playlist. Convert: replace UC→UU |
| Missing duration parsing | ISO 8601 format (PT1M30S). Use regex: `r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?'` |
| Timezone confusion | YouTube API отдаёт UTC. Для анализа времени публикации переводи в пояс СВОЕЙ аудитории, а не в свой собственный: они совпадают не всегда |
