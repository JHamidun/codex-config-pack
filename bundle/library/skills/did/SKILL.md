---
name: "did"
description: "D-ID: говорящая голова из фото + текст или аудио. Триггеры: «озвучь фото», «видео-презентер из фотографии». НЕ свой аватар → heygen."
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


# D-ID API Skill

## Overview

AI avatar video generation. Create talking head videos from a photo and text/audio input.

## API Key

```python
import os
DID_API_KEY = os.getenv('DID_API_KEY')
# Key from ${CODEX_PACK_ROOT}/library/.credentials.master.env
```

## Base URL

`https://api.d-id.com`

## Create Talking Head Video

```python
import requests, os

headers = {
    "Authorization": f"Basic {os.getenv('DID_API_KEY')}",
    "Content-Type": "application/json"
}

# From text (TTS)
response = requests.post(
    "https://api.d-id.com/talks",
    headers=headers,
    json={
        "source_url": "https://example.com/photo.jpg",
        "script": {
            "type": "text",
            "input": "Hello, this is a demo.",
            "provider": {
                "type": "microsoft",
                "voice_id": "en-US-JennyNeural"
            }
        },
        "config": {"stitch": True}
    }
)
talk_id = response.json()["id"]

# Check status
status = requests.get(
    f"https://api.d-id.com/talks/{talk_id}",
    headers=headers
).json()
video_url = status.get("result_url")
```

## From Audio File

```python
with open("audio.mp3", "rb") as f:
    upload = requests.post(
        "https://api.d-id.com/audios",
        headers={"Authorization": f"Basic {os.getenv('DID_API_KEY')}"},
        files={"audio": f}
    )
audio_url = upload.json()["url"]

response = requests.post(
    "https://api.d-id.com/talks",
    headers=headers,
    json={
        "source_url": "photo.jpg",
        "script": {"type": "audio", "audio_url": audio_url}
    }
)
```

## Clips (Built-in Presenters)

```python
response = requests.post(
    "https://api.d-id.com/clips",
    headers=headers,
    json={
        "presenter_id": "amy-jcwCkr1grs",
        "script": {"type": "text", "input": "Welcome!"},
        "background": {"color": "#FFFFFF"}
    }
)
```

## Tips

1. Use high-quality front-facing photos
2. `stitch: true` improves quality
3. Videos ready in 30-60 seconds
4. Download result_url before expiry
