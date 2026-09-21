---
name: "weekly-synthesis"
description: "Generate weekly synthesis report from git log, vector memory, and subagent logs. Use with /weekly-synthesis or \"итоги недели\"."
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


# Weekly Synthesis Report

Generate a comprehensive weekly summary from multiple data sources.

## Data Collection

### 1. Git Activity (last 7 days)
```bash
git log --since="7 days ago" --oneline --all --no-merges
```
Extract: commits count, files changed, main areas of work.

### 2. Vector Memory (last 7 days)
```bash
python ${CODEX_PACK_ROOT}/library/tools/vector_memory.py search "session" --limit 20
```
Extract: key decisions, errors fixed, tools discovered.

### 3. Subagent Logs (optional — the pack does not create this log itself)
```bash
powershell -c "if (Test-Path $env:USERPROFILE\.claude\logs\subagents.log) { Get-Content $env:USERPROFILE\.claude\logs\subagents.log | Select-Object -Last 50 } else { 'no subagent log - skipping' }"
```
Extract (if present): which agents were used, frequency, patterns.

### 4. Session Files
```bash
powershell -c "Get-ChildItem $env:USERPROFILE\.claude\projects\ -Recurse -Filter '*.jsonl' | Where-Object { $_.LastWriteTime -gt (Get-Date).AddDays(-7) } | Select-Object Name, Length, LastWriteTime"
```

## Report Format

```markdown
# Weekly Synthesis: [date range]

## Highlights
- [Top 3 achievements]

## Git Activity
- Commits: N
- Key areas: [list]
- Notable changes: [list]

## Decisions Made
- [From vector memory]

## Errors Fixed
- [From vector memory]

## Agents Used
- [From subagent logs with frequency]

## Patterns & Insights
- [What repeated? What can be improved?]

## Next Week Focus
- [Based on trends and unfinished work]
```

## Process

1. Run all data collection commands
2. Analyze and cross-reference findings
3. Generate the report in the format above
4. Save key insights to vector memory:
```bash
python ${CODEX_PACK_ROOT}/library/tools/vector_memory.py learn "Weekly synthesis [date]: [key insight]" "meta"
```
5. Output the report to the user
