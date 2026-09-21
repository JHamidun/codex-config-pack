---
name: "postiz"
description: "Дефолт публикации в соцсети — self-hosted Postiz, 14 платформ. Триггеры: «опубликуй везде», «запланируй пост». НЕ эксклюзивы Publora→publora-post."
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


# Postiz — Social Media Publishing Hub

**Postiz — дефолтная система публикации**: self-hosted, 14 платформ, без лимита на
число постов, REST API + опциональный MCP. Любая публикация или планирование постов
идёт сюда, если явно не нужен эксклюзив Publora.

## Что понадобится (без этого навык не работает)

Postiz — **не облачный сервис с ключом**, а приложение, которое ты поднимаешь сам.

| Нужно | Как получить |
|---|---|
| Свой инстанс Postiz | Docker на VPS или на своей машине — 3 контейнера: приложение, PostgreSQL, Redis |
| `POSTIZ_URL` | адрес своего инстанса, например `http://localhost:4007` |
| `POSTIZ_API_KEY` | в UI: Settings → Developers → Public API |
| OAuth-приложения соцсетей | для каждой площадки заводится своё; часть (X, Instagram) требует аккаунта разработчика |

Обе переменные — в `${CODEX_PACK_ROOT}/library/.credentials.master.env`
(шаблон: `${CODEX_PACK_ROOT}/library/templates/.credentials.master.env.example`).

### Развернуть у себя

Официальный образ и compose — в репозитории проекта (`gitroom-hq/postiz-app`,
AGPL-3.0, self-host бесплатно). Минимальный контур:

```
postiz          — приложение (Next.js + NestJS), порт 4007 наружу
postiz-postgres — PostgreSQL 17
postiz-redis    — Redis 7.2
```

Порядок первого запуска:

1. Поднять compose, открыть `http://<свой-хост>:4007`.
2. Зарегистрировать **первого** пользователя — это будешь ты.
3. **Сразу после этого поставить `DISABLE_REGISTRATION=true`** и перезапустить.
   Инстанс, открытый в интернет с включённой регистрацией, к вечеру будет чужим:
   регистрация открыта по умолчанию, и это самая частая ошибка при self-host.
4. Подключить соцсети кнопками OAuth в дашборде.
5. Забрать API-ключ и положить в переменные окружения.

Не хочешь выставлять наружу — держи на localhost или за VPN; для публикации
исходящего соединения достаточно, входящий доступ нужен только тебе и OAuth-редиректам.

## Разграничение с publora-post

| Задача | Куда |
|--------|------|
| Публикация/планирование постов: X, LinkedIn, Instagram, TikTok, Facebook, Threads, Reddit, Pinterest, YouTube, Bluesky, Mastodon, Slack, Discord | **postiz (дефолт)** |
| LinkedIn-аналитика: post/account stats, followers, profile summary | `publora-post` (в Postiz этого нет) |
| LinkedIn-реакции и комментарии (create_reaction, create_comment) | `publora-post` (в Postiz этого нет) |
| Telegram | `python ${CODEX_PACK_ROOT}/library/tools/tg_client.py send` — канон для своего канала (в Postiz Telegram отсутствует) |
| Reddit, Pinterest, Slack, Discord, LinkedIn Pages | только postiz (в Publora их нет) |

## Commands

Все команды — тонкая обёртка над `scripts/postiz_cli.py` (stdlib, зависимостей нет):

| Команда | Что делает |
|---------|-------------|
| `python ${CODEX_PACK_ROOT}/library/skills/postiz/scripts/postiz_cli.py channels` | список подключённых аккаунтов |
| `... publish "<text>"` | опубликовать сейчас во все подключённые платформы |
| `... publish "<text>" --platforms x,linkedin` | опубликовать в конкретные |
| `... schedule 2026-09-01T10:00:00Z "<text>" --platforms x` | запланировать (ISO 8601) |
| `... list --from 2026-08-01 --to 2026-08-31` | список постов за период |
| `... delete <post_id>` | удалить запланированный/черновик |
| `... upload <file>` | загрузить медиа для поста |

Скрипт сам читает `${CODEX_PACK_ROOT}/library/.credentials.master.env`, если переменных нет в окружении.
Не настроено — печатает, чего именно не хватает, и выходит с кодом 1 (не «пустой успех»).

## Supported Platforms

| Platform | Type | Settings |
|----------|------|----------|
| X / Twitter | `x` | who_can_reply, community, made_with_ai |
| LinkedIn | `linkedin` | carousel support |
| LinkedIn Page | `linkedin-page` | carousel, company pages |
| Instagram | `instagram` | post, story, reel, collaborators |
| TikTok | `tiktok` | privacy_level, duet, stitch, comment |
| Facebook | `facebook` | url attachment |
| Threads | `threads` | (no extra settings) |
| Reddit | `reddit` | subreddit, title, type, flair |
| Pinterest | `pinterest` | board, title, link |
| YouTube | `youtube` | title, privacy, kids, thumbnail, tags |
| Bluesky | `bluesky` | (no extra settings) |
| Mastodon | `mastodon` | (no extra settings) |
| Slack | `slack` | channel ID |
| Discord | `discord` | channel ID |

## MCP-путь (необязательный)

У Postiz есть MCP-сервер — если он подключён, доступны инструменты
`postiz-get-channels`, `postiz-upload-file`, `postiz-create-post`,
`postiz-list-posts`, `postiz-update-post`, `postiz-delete-post`.

В паке MCP-сервер **не прописан** намеренно: он требует твоего URL и ключа, а без
них молча висит нерабочим. Хочешь MCP — добавь сервер в свой `mcp.json` сам,
передав ему `POSTIZ_URL` и `POSTIZ_API_KEY`. CLI выше делает то же самое и не
требует настройки MCP.

## REST API напрямую

```bash
# List channels
curl -H "Authorization: $POSTIZ_API_KEY" "$POSTIZ_URL/public/v1/integrations"

# Create post (publish now)
curl -X POST "$POSTIZ_URL/public/v1/posts" \
  -H "Authorization: $POSTIZ_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "now",
    "posts": [{
      "integration": {"id": "INTEGRATION_ID"},
      "value": [{"content": "Post text here"}],
      "group": "post",
      "settings": {"__type": "x"}
    }]
  }'

# Upload media
curl -X POST "$POSTIZ_URL/public/v1/upload" \
  -H "Authorization: $POSTIZ_API_KEY" \
  -F "file=@/path/to/image.jpg"
```

## Content Pipeline Integration

Типовой контур публикации своего канала:

```
1. trend-engine    → найти тему, которая сейчас растёт
2. content-engine  → один исходник → версии под каждую площадку
3. image-generation → визуал
4. postiz          → публикация в X + LinkedIn + Instagram + Threads
```

Для Telegram — `python ${CODEX_PACK_ROOT}/library/tools/tg_client.py send`: возможностей больше,
чем в Postiz-интеграции TG.

## Gotchas

- Заголовок авторизации — **сырой ключ, без префикса `Bearer`**. С префиксом будет 401.
- Обновление поста **не частичное** — отправляй контент целиком.
- `value` — массив: несколько элементов = тред.
- Поле `group` всегда `"post"`.
- TikTok требует медиа по HTTPS-адресу, доступному извне.
- Лимит по умолчанию — 30 запросов в час (`API_LIMIT` в окружении инстанса).
- Мультиплатформенная публикация — **одним вызовом API** со всеми платформами
  в массиве `posts`: так тратится один запрос из лимита вместо пяти.
