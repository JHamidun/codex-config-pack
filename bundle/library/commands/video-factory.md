---
name: "video-factory"
description: "Full video production pipeline — from trends to YouTube in one command"
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


Launch the Video Factory agent to produce a complete video.

**Usage:**
- `/video-factory DeepSeek V4 release` — make a video about a specific topic
- `/video-factory auto` — auto-detect best trending topic
- `/video-factory auto --format short` — YouTube Short (15-25s)
- `/video-factory auto --format medium` — Medium video (60-90s)
- `/video-factory "тема" --no-avatar` — AI video only, no HeyGen avatar
- `/video-factory "тема" --no-upload` — produce video but don't upload to YouTube

**What happens:**
1. Trend Discovery (if auto) — finds viral topics across Reddit, X, TikTok, YouTube
2. Script Generation — hook-value-abrupt formula, optimized for retention
3. Visual Production — HeyGen avatar + Veo 3.1 b-roll (parallel)
4. Audio Production — ElevenLabs voiceover + music with ducking
5. Post-Production — assembly, subtitles, thumbnail
6. YouTube Upload — as Private first, then you review and approve

Topic: $ARGUMENTS

Read the Agent `video-factory` definition and execute the full pipeline for the specified topic.
