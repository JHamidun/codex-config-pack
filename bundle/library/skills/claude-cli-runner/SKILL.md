---
name: "claude-cli-runner"
description: "Запуск Claude из Python БЕЗ API-ключа — claude CLI по подписке; модуль claude_cli.py. Триггеры: «клод из скрипта», «без API ключа»."
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


# Claude CLI Runner

Use this skill when the user needs to run Claude models from Python code WITHOUT API keys — via the `claude` CLI binary that uses Claude Code's built-in authentication.

## When to Use

- User asks to "run Claude from Python" or "call Claude without API key"
- User needs to process text with Claude in a backend/script
- User wants to integrate Claude into a project that doesn't have API keys configured
- User mentions "claude CLI" or "claude binary"

## Module Location

`${CODEX_PACK_ROOT}/library/tools/claude_cli.py`

## Quick Usage

```python
import sys
sys.path.insert(0, "${CODEX_PACK_ROOT}/library/tools")
from claude_cli import claude, claude_async, claude_json, claude_stream, validate_response

# Simple call
result = claude("Fix spelling: Привет мр")

# With system prompt and model
result = claude(
    "Review this code for bugs",
    system="You are a senior developer",
    model="claude-opus-5",
)

# Async
result = await claude_async("Translate to English: ...")

# JSON output
data = claude_json("List 3 colors as JSON array")

# Streaming
for chunk in claude_stream("Write a story"):
    print(chunk, end="")

# Validate LLM response
ok, cleaned = validate_response(original_text, llm_response)
```

## Available Models

- `claude-opus-5` — most capable (алиас `opus`)
- `claude-fable-5-1` — канон text-субагентов/воркеров (алиас `fable`; `claude-fable-5` помечена Legacy)
- `claude-sonnet-5` — balanced (default)
- `claude-haiku-4-5` — fastest, cheapest

Канон актуальных ID/алиасов → `config/models.md`.

## Requirements

Claude CLI must be installed: `npm install -g @anthropic-ai/claude-code`

Or set `CLAUDE_CLI_PATH` env var to the binary path.

## On Server (your-server)

```bash
ssh your-server "which claude"  # verify installation
ssh your-server "claude -p --model claude-sonnet-5 'Hello'"  # test
```
