---
name: "beads-init"
description: "Initialize Beads issue tracking in your project with interactive configuration setup."
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


# Beads Initialization

> **Attribution**: [Beads](https://github.com/steveyegge/beads) is created by [Steve Yegge](https://github.com/steveyegge).

## User Input

```text
$ARGUMENTS
```

## Prerequisites Check

First, verify Beads CLI is installed:

```bash
bd version
```

If not installed, provide installation options:

**Option 1: Go (recommended)**
```bash
go install github.com/steveyegge/beads/cmd/bd@latest
```

**Option 2: npm**
```bash
npm install -g @beads/bd
```

**Option 3: Homebrew (macOS)**
```bash
brew install steveyegge/tap/beads
```

Beads stores its state in `.beads/` inside the repo and syncs through git, so run
everything below from the repository root (`git rev-parse --show-toplevel`).

## Project Prefix

Ask the user for their issue prefix (3-8 characters, lowercase):
- Should be a short project name
- All issues will be `PREFIX-xxx`
- Examples: `myapp`, `web`, `api`, `proj`

## Initialization Steps

> **This pack ships no `.beads-templates/` directory** — no config presets, no
> formula files, no PRIME template. Earlier versions of this command told you to
> `cp` from there and failed on the first step. `bd init` writes its own config,
> and Beads brings its own formulas, so nothing needs copying.

1. **Initialize Beads** — this creates `.beads/` with a default config:
   ```bash
   bd init
   ```

2. **Set the issue prefix** in the generated `.beads/config.yaml`. Read the file
   first (`bd init` may already have prompted for it), then edit `issue-prefix`
   in place. Do not overwrite the whole file — you would lose whatever else
   `bd init` put there for this version of the CLI.

3. **Decide on auto-push** while you are in the config. Local-only ("stealth")
   work means turning the auto-push/remote-sync option off; leaving it on means
   `bd sync` will push. Pick deliberately — this decides whether teammates see
   your issues.

4. **Check what formulas the CLI already gives you** before writing any:
   ```bash
   bd formula list
   ```
   Formulas are Beads' own workflow templates (`bd mol wisp <name>`,
   `bd patrol run <name>`). If the one you want is not listed, author it as a
   `.toml` under `.beads/formulas/` — there is nothing in this pack to copy from.

5. **Initial sync**:
   ```bash
   bd sync
   ```

6. **Commit the result** so the tracker exists for everyone else on the repo:
   ```bash
   git add .beads && git commit -m "chore: init beads issue tracking"
   ```

## Post-Setup Instructions

After initialization, display:

```
## Beads Initialized!

**Prefix**: {PREFIX}

### Quick Start

1. Create your first task:
   bd create "Setup project" -t chore -p 3

2. View available work:
   bd ready

3. Start working:
   bd update {PREFIX}-xxx --status in_progress

4. Complete task:
   bd close {PREFIX}-xxx --reason "Done"

### Session Workflow

START:  bd prime -> bd ready
WORK:   bd update -> work -> bd close -> git commit -m "... ({PREFIX}-xxx)"
END:    bd sync -> git push

### Documentation

- Quick reference: .claude/docs/beads-quickstart.md
- Skill (commands, workflows, decision matrix): .claude/skills/beads/
- Official docs: https://github.com/steveyegge/beads

### Next Steps

- [ ] Review .beads/config.yaml and customize directory-labels
- [ ] Create REF: issues for project knowledge (optional)
```

## Troubleshooting

If `bd init` fails:
- Check whether `.beads/` already exists — that is the usual cause
- Only then: `rm -rf .beads && bd init`. This destroys local issue state that
  has not been `bd sync`ed, so run `bd sync` first if the directory has anything
  in it you care about.

If the daemon does not start:
- Check logs: `cat .beads/daemon.log`
- Restart: `bd daemon restart`

## Example Session

```
User: /beads-init

Claude: bd version
        -> bd version 0.x.y

Claude: What prefix should issues use? (3-8 chars, lowercase)
User:   web

Claude: bd init
        -> created .beads/

Claude: [reads .beads/config.yaml, sets issue-prefix: web]
        [asks: auto-push on sync, or local-only?]

Claude: bd formula list
        -> shows the workflow templates this CLI version ships

Claude: bd sync && git add .beads && git commit -m "chore: init beads issue tracking"

        Beads initialized. First task:
        bd create "Setup project" -t chore -p 3
```
