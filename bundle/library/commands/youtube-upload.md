---
name: "youtube-upload"
description: "Upload a video to YouTube with metadata"
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


Upload a video to YouTube via the YouTube Data API v3.

**Usage:**
- `/youtube-upload final.mp4 --title "DeepSeek обошёл GPT-5" --private`
- `/youtube-upload video.mp4 --title "Title" --tags "ai,tech" --thumbnail thumb.png`

Аргументы: `$ARGUMENTS`

**Prerequisites (одноразово):**
1. Google Cloud Console → включи **YouTube Data API v3** → OAuth client type *Desktop app* →
   скачай JSON и положи в `${CODEX_PACK_ROOT}/library/.youtube-client-secrets.json`.
2. `pip install google-api-python-client google-auth-oauthlib`
3. Первый запуск сам откроет браузер и сохранит токен в `${CODEX_PACK_ROOT}/library/.youtube-oauth-token.json`.

Готового скилла-обёртки в паке нет — команда работает напрямую по API. Разбери `$ARGUMENTS`
(путь к файлу + флаги) и выполни:

```python
import os, sys
from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube",
          # captions().insert() без force-ssl отвечает 403 — субтитры не зальются.
          # Меняешь скоуп — удали ${CODEX_PACK_ROOT}/library/.youtube-oauth-token.json, иначе
          # подхватится старый токен с прежними правами и ошибка не уйдёт.
          "https://www.googleapis.com/auth/youtube.force-ssl"]
TOKEN   = Path.home() / ".claude" / ".youtube-oauth-token.json"
SECRETS = Path.home() / ".claude" / ".youtube-client-secrets.json"

# --- параметры из $ARGUMENTS ---
video     = "final.mp4"
title     = "TITLE"
desc      = ""
tags      = []            # --tags "ai,tech" -> ["ai","tech"]
privacy   = "private"     # private | unlisted | public
thumbnail = None          # --thumbnail thumb.png

if TOKEN.exists():
    creds = Credentials.from_authorized_user_file(str(TOKEN), SCOPES)
else:
    if not SECRETS.exists():
        sys.exit(f"нет {SECRETS} — заведи OAuth client (Desktop app) в Google Cloud Console")
    creds = InstalledAppFlow.from_client_secrets_file(str(SECRETS), SCOPES).run_local_server(port=0)
    TOKEN.write_text(creds.to_json(), encoding="utf-8")

yt = build("youtube", "v3", credentials=creds)
req = yt.videos().insert(
    part="snippet,status",
    body={"snippet": {"title": title, "description": desc, "tags": tags},
          "status": {"privacyStatus": privacy, "selfDeclaredMadeForKids": False}},
    media_body=MediaFileUpload(video, chunksize=-1, resumable=True),
)
resp = None
while resp is None:                       # resumable upload: цикл обязателен
    status, resp = req.next_chunk()
    if status:
        print(f"{int(status.progress() * 100)}%")
vid = resp["id"]
print(f"https://youtube.com/watch?v={vid}")

if thumbnail and os.path.exists(thumbnail):   # требует верифицированного канала
    yt.thumbnails().set(videoId=vid, media_body=MediaFileUpload(thumbnail)).execute()
```

**Гочи:**
- Заливай сначала `private`, посмотри результат, потом переключай видимость:
  `yt.videos().update(part='status', body={'id': vid, 'status': {...'privacyStatus':'public'}})` —
  в `status` передавай **весь** объект из `videos().list(part='status')`, иначе снесёшь остальные поля.
- Дневная квота API — 10 000 единиц, одна заливка ≈ 1600. То есть ~6 видео в сутки на проект.
- Shorts определяются автоматически: вертикаль ≤ 3 минут. Отдельного флага нет.
- Субтитры отдельным вызовом `captions().insert(part='snippet', body=..., media_body=srt)`.
