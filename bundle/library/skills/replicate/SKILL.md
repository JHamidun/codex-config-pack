---
name: "replicate"
description: "Replicate: запуск 1000+ AI-моделей по API (FLUX, SDXL, Whisper), если модели нет нативно. Триггеры: «запусти модель по api», «stable diffusion»."
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


# Replicate API Skill

## Overview

Run 1000+ open-source AI models via API. Image generation (FLUX, SDXL), video, audio, text, and more.

## API Key

```python
import os
REPLICATE_API_KEY = os.getenv('REPLICATE_API_KEY')
# Key from ${CODEX_PACK_ROOT}/library/.credentials.master.env
```

## MCP Server

Already configured in `${CODEX_PACK_ROOT}/library/mcp.json` as `replicate`. Can use MCP tools directly.

## Dependencies

```bash
pip install replicate
```

## Basic Usage

```python
import replicate

# Image generation with FLUX
output = replicate.run(
    "black-forest-labs/flux-1.1-pro",
    input={
        "prompt": "a beautiful sunset over mountains, photorealistic",
        "aspect_ratio": "16:9",
        "output_format": "png"
    }
)

# Stable Diffusion XL
output = replicate.run(
    "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
    input={
        "prompt": "an astronaut riding a horse on mars",
        "negative_prompt": "blurry, low quality",
        "width": 1024,
        "height": 1024
    }
)
```

## Popular Models

| Category | Model | ID |
|----------|-------|----|
| **Image** | FLUX 1.1 Pro | `black-forest-labs/flux-1.1-pro` |
| **Image** | SDXL | `stability-ai/sdxl` |
| **Image** | Ideogram v2 | `ideogram-ai/ideogram-v2` |
| **Video** | Minimax Video | `minimax/video-01` |
| **Audio** | Whisper | `openai/whisper` |
| **Text** | LLaMA 3.1 | `meta/meta-llama-3.1-405b` |
| **Upscale** | Real-ESRGAN | `nightmareai/real-esrgan` |
| **Remove BG** | RemBG | `cjwbw/rembg` |

## Async Predictions

```python
prediction = replicate.predictions.create(
    model="black-forest-labs/flux-1.1-pro",
    input={"prompt": "..."}
)
prediction = replicate.predictions.get(prediction.id)
print(prediction.status)  # "starting", "processing", "succeeded", "failed"
print(prediction.output)  # URL when done
```

## Tips

1. Check model page on replicate.com for input parameters
2. Use `replicate.models.search("keyword")` to find models
3. Output is usually a URL - download with requests
4. Billing is per-second of GPU time
