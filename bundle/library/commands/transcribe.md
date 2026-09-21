---
name: "transcribe"
description: "Транскрибация аудио и видео через Deepgram: файл или URL, SRT-субтитры, диаризация. Триггеры: «транскрибируй», «расшифруй запись», «субтитры из аудио»."
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


# Transcribe

/transcribe - Audio/video transcription via Deepgram

## Usage
```
/transcribe <file_path>              - Transcribe audio/video file
/transcribe <url>                    - Transcribe from URL
/transcribe <file_path> --srt        - Generate SRT subtitles
/transcribe <file_path> --speakers   - With speaker diarization
/transcribe <file_path> --lang ru    - Specify language
```

## Instructions for Claude

Uses Deepgram API (nova-2 model). Full reference: `${CODEX_PACK_ROOT}/library/skills/deepgram/SKILL.md`

### Quick transcribe

```python
from deepgram import DeepgramClient, PrerecordedOptions
import os
from dotenv import load_dotenv

load_dotenv(os.path.expanduser('${CODEX_PACK_ROOT}/library/.credentials.master.env'))
client = DeepgramClient(os.getenv('DEEPGRAM_API_KEY'))

# From file
with open("audio.mp3", "rb") as f:
    source = {"buffer": f.read()}

options = PrerecordedOptions(
    model="nova-2",
    language="ru",         # or "en", auto-detect with detect_language=True
    smart_format=True,
    punctuate=True,
    diarize=True,          # speaker separation
    paragraphs=True,
    utterances=True
)

response = client.listen.prerecorded.v("1").transcribe_file(source, options)
print(response.results.channels[0].alternatives[0].transcript)
```

### From URL

```python
source = {"url": "https://example.com/audio.mp3"}
response = client.listen.prerecorded.v("1").transcribe_url(source, options)
```

### With speaker labels

```python
for utterance in response.results.utterances:
    print(f"Speaker {utterance.speaker}: {utterance.transcript}")
```

### Generate SRT subtitles

```python
srt_lines = []
for i, utt in enumerate(response.results.utterances, 1):
    start = format_srt_time(utt.start)
    end = format_srt_time(utt.end)
    srt_lines.append(f"{i}\n{start} --> {end}\n{utt.transcript}\n")

def format_srt_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
```

## Supported formats

Audio: mp3, wav, flac, m4a, ogg, webm
Video: mp4, mov, avi, mkv, webm (extracts audio automatically)

## Languages

Auto-detect or specify: en, ru, uk, de, fr, es, it, pt, nl, ja, ko, zh, ar, hi, pl, tr

## Important

- DEEPGRAM_API_KEY from `${CODEX_PACK_ROOT}/library/.credentials.master.env`
- Model `nova-2` is best quality for most tasks
- Cost: ~$0.0043/min
- `smart_format=True` adds punctuation automatically
