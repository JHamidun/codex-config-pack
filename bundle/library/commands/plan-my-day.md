---
name: "plan-my-day"
description: "Generate an optimized daily plan from tasks, calendar, and priorities. Use with /plan-my-day or \"спланируй день\"."
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


# Plan My Day

Generate an optimized daily plan based on tasks and energy levels.

## Data Sources

### 1. Calendar Events (if available)
```
Use gcalendar skill to fetch today's events
```

### 2. Current Tasks
Ask user or check:
- Linear issues assigned to me
- Todoist tasks for today
- Any explicit priorities mentioned

### 3. Recent Context
```bash
python ${CODEX_PACK_ROOT}/library/tools/vector_memory.py recall-recent 1
```

## Energy-Based Scheduling

```
MORNING (9:00-12:00) — Peak energy
  -> Complex coding tasks
  -> Architecture decisions
  -> Deep research
  -> Writing/creative work

AFTERNOON (13:00-16:00) — Moderate energy
  -> Code reviews
  -> Meetings
  -> Bug fixes
  -> Testing

EVENING (16:00-19:00) — Low energy
  -> Emails and messages
  -> Documentation
  -> Planning for tomorrow
  -> Routine maintenance
```

## Output Format

```markdown
# Daily Plan: [date]

## Top 3 Priorities
1. [Most important task]
2. [Second priority]
3. [Third priority]

## Schedule

### Morning (high energy)
- [ ] 09:00 - [task]
- [ ] 10:30 - [task]

### Afternoon (moderate energy)
- [ ] 13:00 - [task/meeting]
- [ ] 14:30 - [task]

### Evening (wind down)
- [ ] 16:00 - [task]
- [ ] 17:00 - [review/docs]

## Blocked/Waiting
- [Items waiting on others]

## Tomorrow Preview
- [Key items for tomorrow]
```

## Process

1. Gather tasks from all sources
2. Prioritize by urgency x importance (Eisenhower)
3. Map to energy-appropriate time slots
4. Account for calendar events (fixed blocks)
5. Add buffer time between deep work blocks
6. Output the plan
