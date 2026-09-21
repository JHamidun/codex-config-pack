---
name: "beads"
description: "Beads — git-трекер задач и багов для AI-агентов (команды bd). Триггеры: «заведи задачу в beads», «issue tracking», «список задач репо»."
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


# Beads Issue Tracking Skill

> **Attribution**: [Beads](https://github.com/steveyegge/beads) by [Steve Yegge](https://github.com/steveyegge)

## Description

Beads is a git-backed, AI-native issue tracking system. This skill helps AI agents work with Beads effectively.

## When to Use

- Starting a new work session (bd prime → bd ready)
- Creating, updating, or closing issues
- Managing task dependencies
- Running workflow formulas
- Coordinating multi-session work

## Quick Reference

### Session Workflow

```bash
# START
bd prime                    # Inject context
bd ready                    # Find available work

# WORK
bd update ID --status in_progress  # Take task
# ... implement ...
bd close ID --reason "Done"        # Complete task
/push patch                        # Commit

# END (MANDATORY!)
bd sync
git push
```

### Issue Creation

```bash
# Basic
bd create "Title" -t type -p priority

# With files (auto-labels)
bd create "Fix button" --files src/components/Button.tsx

# Emergent work
bd create "Found bug" -t bug --deps discovered-from:current-id
```

### Types & Priorities

| Type | When |
|------|------|
| feature | New functionality |
| bug | Bug fix |
| chore | Tech debt, config |
| docs | Documentation |
| test | Tests |
| epic | Group of tasks |

| Priority | Meaning |
|----------|---------|
| 0 | Critical (blocks release) |
| 1 | Critical |
| 2 | High |
| 3 | Medium (default) |
| 4 | Low / backlog |

### Formulas (Workflows)

```bash
bd formula list                                    # List all
bd mol wisp exploration --vars "question=How?"    # Ephemeral
bd mol pour bigfeature --vars "feature_name=auth" # Persistent
bd mol squash WISP_ID                             # Save result
bd mol burn WISP_ID                               # Discard
```

## Resources

See `resources/` for detailed guides:
- COMMANDS_QUICKREF.md - Command cheat sheet
- DECISION_MATRIX.md - When to use what
- WORKFLOWS.md - Common workflows
- SPECKIT_BRIDGE.md - Integration with Spec-kit

## Integration with Spec-kit

For large features (>1 day):
1. `/speckit.specify` → requirements
2. `/speckit.plan` → design
3. `/speckit.tasks` → task breakdown
4. `/speckit.tobeads` → import to Beads
5. `bd ready` → work with Beads

## Links

- [Beads GitHub](https://github.com/steveyegge/beads)
- [CLI Reference](https://github.com/steveyegge/beads/blob/main/docs/CLI_REFERENCE.md)
