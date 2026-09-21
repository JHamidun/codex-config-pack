---
name: "sharing-skills"
description: "Отправка своего навыка в upstream-репозиторий через PR: ветка, коммит, пуш. Триггеры: «поделись навыком», «контрибьютни skill»."
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


# Sharing Skills

## Overview

Contribute skills from your local branch back to upstream repositories.

**Workflow:** Branch → Edit/Create skill → Commit → Push → PR

## When to Share

**Share when:**
- Skill applies broadly (not project-specific)
- Pattern/technique others would benefit from
- Well-tested and documented
- Follows writing-skills guidelines

**Keep personal when:**
- Project-specific or organization-specific
- Experimental or unstable
- Contains sensitive information
- Too narrow/niche for general use

## Prerequisites

- `gh` CLI installed and authenticated
- Skill has been tested

## Sharing Workflow

### 1. Ensure You're on Main and Synced

```bash
cd ${CODEX_PACK_ROOT}/library/skills/
git checkout main
git pull origin main
```

### 2. Create Feature Branch

```bash
skill_name="your-skill-name"
git checkout -b "add-${skill_name}-skill"
```

### 3. Create or Edit Skill

```bash
# Create skill file
# skills/your-skill-name.md
```

### 4. Commit Changes

```bash
git add skills/your-skill-name.md
git commit -m "Add ${skill_name} skill

Brief description of what this skill does and why it's useful.

Tested with: [describe testing approach]"
```

### 5. Push to Your Fork

```bash
git push -u origin "add-${skill_name}-skill"
```

### 6. Create Pull Request

```bash
gh pr create \
  --title "Add ${skill_name} skill" \
  --body "$(cat <<'EOF'
## Summary
Brief description of the skill and what problem it solves.

## Testing
Describe how you tested this skill.

## Context
Any additional context about why this skill is needed.
EOF
)"
```

## After PR is Merged

```bash
# Sync your local main
git checkout main
git pull origin main

# Delete feature branch
git branch -d "add-${skill_name}-skill"
git push origin --delete "add-${skill_name}-skill"
```

## Multi-Skill Contributions

**Do NOT batch multiple skills in one PR.**

Each skill should:
- Have its own feature branch
- Have its own PR
- Be independently reviewable

**Why?** Individual skills can be reviewed, iterated, and merged independently.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "gh: command not found" | Install GitHub CLI: https://cli.github.com/ |
| "Permission denied" | Check SSH keys: `gh auth status` |
| "Skill already exists" | Consider different name or coordinate |
| PR merge conflicts | Rebase: `git fetch origin && git rebase origin/main` |
