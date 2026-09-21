---
name: "rollback-changes"
description: "Откат упавшей фазы воркфлоу по changes-log: восстановление файлов, чистка артефактов, отмена команд. Триггеры: «откати изменения», «верни как было»."
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


# Rollback Changes

Rollback failed workflow phases by reading changes log and reversing tracked modifications.

## When to Use

- Workflow phase fails and needs state restoration
- Error recovery in worker agents
- Quality gate failures requiring revert

## Input

```json
{
  "changes_log_path": ".bug-changes.json",
  "phase": "bug-fixing",
  "confirmation_required": true
}
```

## Changes Log Format

```json
{
  "phase": "bug-fixing",
  "timestamp": "2025-10-18T14:30:00Z",
  "files_modified": [{"path": "src/app.ts", "backup": ".rollback/src-app.ts.backup"}],
  "files_created": ["src/new-file.ts"],
  "commands_executed": ["pnpm install", "pnpm build"],
  "git_commits": ["abc123"],
  "artifacts": [".bug-fixing-plan.json"]
}
```

## Process

### 1. Read & Parse Changes Log
Use Read tool to load JSON. Validate required fields: phase, timestamp, files_modified, files_created, commands_executed, git_commits.

### 2. Request Confirmation (if required)
Show summary of changes to revert. If user declines, return dry run result.

### 3. Restore Modified Files
```bash
cp "{backup}" "{path}"  # For each {path, backup} in files_modified
```

### 4. Delete Created Files
```bash
rm -f "{file}"  # For each file in files_created
```

### 5. Revert Commands
- `pnpm install` → re-run to restore lockfile
- `git add *` → `git restore --staged .`
- `pnpm build` → `rm -rf dist/`
- Other → log warning (cannot auto-revert)

### 6. Revert Git Commits
```bash
git revert --no-edit {sha}  # In reverse order
```

### 7. Cleanup Artifacts
Remove plan files and temporary artifacts.

## Output

```json
{
  "success": true,
  "phase": "bug-fixing",
  "actions_taken": ["Restored src/app.ts", "Deleted src/new-file.ts", "Reverted abc123"],
  "files_restored": 1,
  "files_deleted": 1,
  "git_commits_reverted": 1,
  "errors": [],
  "warnings": ["Backup not found: .rollback/file.backup (skipped)"]
}
```

## Error Handling

- **Missing log**: Return error "Changes log not found"
- **Invalid JSON**: Return parsing error
- **Backup not found**: Log warning, continue (partial rollback OK)
- **Git conflicts**: Log error with manual instructions, continue

## Safety Features

- Confirmation by default before any changes
- Partial rollback acceptable (documented in warnings)
- Never delete without verifying backup exists
- All actions logged for audit trail

## Worker Integration

Workers should track changes during operations:
1. Create `.{domain}-changes.json` before modifications
2. Create backups in `.rollback/` for modified files
3. Log all file creates, commands, and commits
4. On failure: invoke rollback-changes with confirmation_required=false
