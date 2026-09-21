---
name: "away-summary"
description: "Пересказ «пока тебя не было»: на чём остановились и что сделано в сессии. Триггеры: «где остановился», «recap», «while you were away»."
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


# Away Summary

Generate a short session recap for returning after a break.

## Rules

1. Write exactly 1-3 short sentences
2. Start by stating the **high-level task** — what was being built or debugged, not implementation details
3. Then: the **concrete next step**
4. Skip status reports and commit recaps
5. Use only the last ~30 messages for context

## Example Output

> Building the admin panel with AI chat integration. Next: test the briefing cron job and verify collector scheduling.

## How to Generate

1. Look at the recent conversation context
2. Identify the main task/goal
3. Identify where work left off
4. Write 1-3 sentences following the rules above
