---
name: "tiktok-intel"
description: "Аналитика TikTok и Instagram через Scraping API: тренды, инфлюенсеры, демография, TikTok Shop, Reels. Триггеры: «тикток тренды», «популярные рилсы»."
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


# TikTok & Instagram Intelligence

> Deep platform analytics via a 3rd-party scraping API.
> Key: `SCRAPER_API_KEY` from `${CODEX_PACK_ROOT}/library/.credentials.master.env`

## When to Use

- "тикток тренды" — что сейчас viral
- "инфлюенсеры в [нише]" — поиск и анализ блогеров
- "TikTok Shop [товар]" — товары и отзывы на маркетплейсе
- "популярные рилсы" — тренды Instagram Reels
- "аудитория [блогер]" — демография подписчиков
- "популярные хештеги/песни" — для контент-планирования
- Поиск блогеров для Your Tracker (строительная ниша)
- Контент-идеи для YourChannel YouTube канала

## API Endpoints

```
BASE = https://api.your-scraper.example
AUTH: x-api-key: $SCRAPER_API_KEY
```

### TikTok — Profiles & Content

| Endpoint | Path | Input | Returns |
|----------|------|-------|---------|
| Profile | `/v1/tiktok/profile` | `?username=handle` | Bio, followers, likes, videos count |
| Audience Demographics | `/v1/tiktok/user/audience` | `?username=handle` | Age, gender, country distribution |
| Videos | `/v3/tiktok/profile/videos` | `?username=handle` | All videos with engagement |
| Video Info | `/v2/tiktok/video` | `?url=video_url` | Full video data + engagement |
| Transcript | `/v1/tiktok/video/transcript` | `?url=video_url` | Speech-to-text |
| Comments | `/v1/tiktok/video/comments` | `?url=video_url` | Comment tree |
| Live | `/v1/tiktok/user/live` | `?username=handle` | Current live stream |
| Following | `/v1/tiktok/user/following` | `?username=handle` | Who they follow |
| Followers | `/v1/tiktok/user/followers` | `?username=handle` | Their followers |

### TikTok — Discovery & Trends

| Endpoint | Path | Input | Returns |
|----------|------|-------|---------|
| Search Users | `/v1/tiktok/search/users` | `?query=keyword` | Find creators by keyword |
| Search Keyword | `/v1/tiktok/search/keyword` | `?query=keyword` | Videos by keyword |
| Search Hashtag | `/v1/tiktok/search/hashtag` | `?query=hashtag` | Hashtag pages |
| Top Search | `/v1/tiktok/search/top` | `?query=keyword` | Top results (mixed) |
| Trending Feed | `/v1/tiktok/get-trending-feed` | — | Current trending videos |
| Popular Songs | `/v1/tiktok/songs/popular` | — | Trending audio tracks |
| Popular Creators | `/v1/tiktok/creators/popular` | — | Rising creators |
| Popular Videos | `/v1/tiktok/videos/popular` | — | Viral videos right now |
| Popular Hashtags | `/v1/tiktok/hashtags/popular` | — | Trending hashtags |
| Song Details | `/v1/tiktok/song` | `?id=song_id` | Song metadata |
| Videos Using Song | `/v1/tiktok/song/videos` | `?id=song_id` | All videos with this audio |

### TikTok Shop

| Endpoint | Path | Input | Returns |
|----------|------|-------|---------|
| Shop Search | `/v1/tiktok/shop/search` | `?query=product` | Товары на маркетплейсе |
| Shop Products | `/v1/tiktok/shop/products` | `?shop_id=ID` | Все товары магазина |
| Product Details | `/v1/tiktok/product` | `?url=product_url` | Цена, рейтинг, описание |
| Product Reviews | `/v1/tiktok/shop/product/reviews` | `?product_id=ID` | Отзывы покупателей |
| User Showcase | `/v1/tiktok/user/showcase` | `?username=handle` | Витрина блогера |

### Instagram — Profiles & Content

| Endpoint | Path | Input | Returns |
|----------|------|-------|---------|
| Profile | `/v1/instagram/profile` | `?username=handle` | Full profile data |
| Basic Profile | `/v1/instagram/basic-profile` | `?username=handle` | Lightweight lookup |
| Posts | `/v2/instagram/user/posts` | `?username=handle` | Feed posts |
| Reels | `/v1/instagram/user/reels` | `?username=handle` | Reels only |
| Post/Reel Info | `/v1/instagram/post` | `?url=post_url` | Full post data |
| Transcript | `/v2/instagram/media/transcript` | `?url=reel_url` | Speech-to-text for Reels |
| Comments | `/v2/instagram/post/comments` | `?url=post_url` | Comments |
| Story Highlights | `/v1/instagram/user/highlights` | `?username=handle` | Highlight covers |
| Highlight Detail | `/v1/instagram/user/highlight/detail` | `?highlight_id=ID` | Stories in highlight |
| Search Reels | `/v2/instagram/reels/search` | `?query=keyword` | Search Reels by keyword |

## Workflows

### 1. Influencer Research (найти блогеров в нише)

```bash
source ${CODEX_PACK_ROOT}/library/.credentials.master.env
API="https://api.your-scraper.example"
H="x-api-key: $SCRAPER_API_KEY"

# Step 1: Search creators by keyword
curl -s "$API/v1/tiktok/search/users?query=строительство ремонт" -H "$H" > /tmp/tt_creators.json

# Step 2: Get top creator profiles + demographics (parallel)
# Extract usernames from step 1, then:
curl -s "$API/v1/tiktok/profile?username=CREATOR1" -H "$H" > /tmp/tt_p1.json &
curl -s "$API/v1/tiktok/user/audience?username=CREATOR1" -H "$H" > /tmp/tt_d1.json &
curl -s "$API/v1/tiktok/profile?username=CREATOR2" -H "$H" > /tmp/tt_p2.json &
curl -s "$API/v1/tiktok/user/audience?username=CREATOR2" -H "$H" > /tmp/tt_d2.json &
wait
```

Output format:
```markdown
# Influencer Report: [Niche]

| Creator | Followers | Avg Views | Engagement | Audience (top country) | Age Group |
|---------|-----------|-----------|------------|----------------------|-----------|
| @xxx | 500K | 50K | 10% | your-region 65% | 25-34 |
```

### 2. Trend Monitor (что сейчас в тренде)

```bash
source ${CODEX_PACK_ROOT}/library/.credentials.master.env
API="https://api.your-scraper.example"
H="x-api-key: $SCRAPER_API_KEY"

# All trending data in parallel
curl -s "$API/v1/tiktok/get-trending-feed" -H "$H" > /tmp/tt_trending.json &
curl -s "$API/v1/tiktok/songs/popular" -H "$H" > /tmp/tt_songs.json &
curl -s "$API/v1/tiktok/hashtags/popular" -H "$H" > /tmp/tt_hashtags.json &
curl -s "$API/v1/tiktok/creators/popular" -H "$H" > /tmp/tt_rising.json &
wait
```

### 3. Competitor Content Analysis

```bash
# Analyze what a competitor posts on both platforms
curl -s "$API/v3/tiktok/profile/videos?username=COMPETITOR" -H "$H" > /tmp/tt_vids.json &
curl -s "$API/v2/instagram/user/posts?username=COMPETITOR" -H "$H" > /tmp/ig_posts.json &
curl -s "$API/v1/instagram/user/reels?username=COMPETITOR" -H "$H" > /tmp/ig_reels.json &
wait
```

### 4. TikTok Shop Product Research

```bash
# Search products
curl -s "$API/v1/tiktok/shop/search?query=строительный клей" -H "$H" > /tmp/shop_results.json

# Get reviews for top product
curl -s "$API/v1/tiktok/shop/product/reviews?product_id=PRODUCT_ID" -H "$H" > /tmp/shop_reviews.json
```

### 5. Audio/Song Trend Analysis

```bash
# Find trending songs, then see who uses them
curl -s "$API/v1/tiktok/songs/popular" -H "$H" > /tmp/songs.json

# Get videos using a specific trending song
curl -s "$API/v1/tiktok/song/videos?id=SONG_ID" -H "$H" > /tmp/song_vids.json
```

## Credit Budget

| Operation | Credits |
|-----------|---------|
| Single profile lookup | 1 |
| Profile + demographics | 2 |
| Full creator audit (profile + demos + videos + top video comments) | 4-5 |
| Trend snapshot (feed + songs + hashtags + creators) | 4 |
| 10 influencers with demographics | ~20 |
| TikTok Shop search + 5 product reviews | ~6 |
| Instagram competitor (profile + posts + reels) | 3 |

## Integration

| Next Step | Skill |
|-----------|-------|
| 30-day topic research | `last30days` |
| Full social dossier | `social-intel` |
| Ad analysis | `ad-spy` |
| YouTube content ideas | `youtube-analytics` |
| Create content brief | `content-creation` |
| Your-Brand blogger monitoring | Your Tracker (your-server cron) |
