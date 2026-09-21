---
name: "parse-git-status"
description: "Разбор вывода git status в структуру: staged, изменённые, ветка, ahead/behind. Служебный для пре-флайт-проверок. Триггеры: «разбери git status»."
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


# Parse Git Status

Parse git status command output into structured JSON for programmatic analysis.

## When to Use

- Pre-flight checks before workflow execution
- Validate clean working directory
- List modified files for commit
- Check for uncommitted changes

## Instructions

### Step 1: Receive Git Status Output

Accept raw git status output as input.

**Expected Input**:
- `gitStatusOutput`: String (raw output from `git status --porcelain` or regular `git status`)

### Step 2: Parse Branch Information

Extract current branch and tracking information.

**Patterns**:
- `## branch-name`: Current branch
- `## branch-name...origin/branch-name`: Tracking branch
- `[ahead N]` or `[behind N]`: Ahead/behind commits

### Step 3: Categorize Files

Parse file status indicators and categorize.

**Status Indicators** (porcelain format):
- `M `: Modified (staged)
- ` M`: Modified (unstaged)
- `A `: Added (staged)
- `D `: Deleted (staged)
- `R `: Renamed (staged)
- `??`: Untracked
- `!!`: Ignored

### Step 4: Return Structured Data

Return parsed data as JSON object.

**Expected Output**:
```json
{
  "branch": "main",
  "tracking": "origin/main",
  "ahead": 0,
  "behind": 0,
  "staged": ["file1.ts", "file2.ts"],
  "modified": ["file3.ts"],
  "deleted": [],
  "renamed": [],
  "untracked": ["file4.ts"],
  "clean": false
}
```

## Error Handling

- **Invalid Git Output**: Return error describing format issue
- **Not a Git Repository**: Return error indicating no git repo
- **Empty Output**: Return clean status with empty arrays

## Examples

### Example 1: Clean Working Directory

**Input**:
```
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

**Output**:
```json
{
  "branch": "main",
  "tracking": "origin/main",
  "ahead": 0,
  "behind": 0,
  "staged": [],
  "modified": [],
  "deleted": [],
  "renamed": [],
  "untracked": [],
  "clean": true
}
```

### Example 2: Modified Files

**Input** (porcelain format):
```
## main...origin/main [ahead 2]
M  src/utils.ts
 M src/types.ts
A  src/new-feature.ts
?? temp-file.js
```

**Output**:
```json
{
  "branch": "main",
  "tracking": "origin/main",
  "ahead": 2,
  "behind": 0,
  "staged": ["src/utils.ts", "src/new-feature.ts"],
  "modified": ["src/types.ts"],
  "deleted": [],
  "renamed": [],
  "untracked": ["temp-file.js"],
  "clean": false
}
```

### Example 3: Detached HEAD

**Input**:
```
## HEAD (no branch)
 M README.md
```

**Output**:
```json
{
  "branch": "HEAD (detached)",
  "tracking": null,
  "ahead": 0,
  "behind": 0,
  "staged": [],
  "modified": ["README.md"],
  "deleted": [],
  "renamed": [],
  "untracked": [],
  "clean": false
}
```

## Validation

- [ ] Parses branch information correctly
- [ ] Categorizes files by status
- [ ] Handles empty/clean status
- [ ] Parses ahead/behind indicators
- [ ] Handles detached HEAD state
- [ ] Returns clean:true only when appropriate

## Supporting Files

None required - pure parsing logic.
