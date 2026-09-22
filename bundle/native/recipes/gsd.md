# Native Codex project workflow

Run the selected operation below using Codex file, patch, search and shell tools.
Do not run `gsd-tools.cjs`, install Claude plugins, execute the quarantined source,
or treat copied `Task`, `AskUserQuestion`, slash commands or Bash substitutions as
Codex APIs. Planning files stay compatible Markdown; no provider or Node dependency
is required for project planning itself.

## Context and state

Resolve the user's actual project workspace. Read its nearest project instructions.
Inspect existing state without changing it:

```text
python "${CODEX_PACK_ROOT}/scripts/planning.py" --workspace "<workspace>" inspect
```

Read `.planning/PROJECT.md`, `STATE.md`, `ROADMAP.md` and `REQUIREMENTS.md` as needed,
then only the selected phase's context, plans, summaries and verification. Missing
state is not permission to reset a project. Existing Markdown is authoritative;
inventory counts and a SUMMARY file alone are not proof of a passed verification.

For an explicitly requested new project, write its real brief to a workspace-relative
Markdown file and run `planning.py --workspace "<workspace>" init --spec "<brief.md>"`.
Initialization refuses existing `.planning`. Then create the actual requirements
and roadmap with native file tools. It does not invent project requirements.

For pause/handoff, write a note with current work, uncommitted changes, evidence,
blockers and the exact next action, then run
`planning.py --workspace "<workspace>" checkpoint --note "<note.md>"`.
Checkpoints are append-only. Do not assume they pause a Codex task or schedule work.

## Methodology and execution

The selected original command and its referenced GSD templates remain available as
domain references. Preserve scope, requirement IDs, dependency order, must-have
artifacts, checkpoints and acceptance tests. Translate old helper operations to
native reads/patches of explicit project paths. Read original scripts only for
algorithmic reference, never execute or rename them. Do not load all workflows.

Use current native tools for questions and web research. Inherit the active model.
If independent workers are explicitly authorized, discover available `pack-gsd-*`
roles, assign disjoint file ownership, respect the configured concurrency limit and
integrate their results. Otherwise execute the same logical stages sequentially;
do not describe self-review as independent verification. No hidden model/API fallback.

Before a phase implementation, confirm each plan has concrete tasks, files, dependencies,
verification commands, must-haves and stop/checkpoint conditions. For each change:
reproduce/test the behavior, implement, run applicable type checks/build/tests, inspect
actual artifacts and record results. Mark requirements complete only from evidence.
Keep failed/unavailable checks explicit. Commits follow project policy; do not commit
unrelated changes or automatically push, tag, merge or deploy.

Structural edits to phase IDs must update dependencies, requirement traceability,
roadmap and state together. Preview destructive moves/removals, preserve completed
history and user edits, and obey the host's approval boundary. Use the current native
Git/worktree tools rather than source-specific home paths or shell aliases.

## Completion

Read back changed state, reconcile it against files and Git, and give the concrete
next action. A plan is a plan, not implemented functionality. Unsupported host-level
features require the actual host tool; writing a file is not equivalent to changing
the runtime's model, task title, permissions or scheduler.
