# Inspect Git changes in Codex

Use the existing project workspace. Do not initialize a repository, stage files,
commit, fetch or change Git configuration merely to inspect its state.

Run with the current shell, substituting the explicitly selected workspace:

```text
python "${CODEX_PACK_ROOT}/scripts/runtime.py" git-status --workspace "<workspace>"
```

Read the JSON `result`: branch, tracking branch, ahead/behind, staged, modified,
deleted, renamed, untracked and unmerged files. A file can be both staged and
modified. Report conflicts separately. Detached and unborn branches are valid.
Git must already be available. If the helper fails, report the blocker; do not
invent a clean state or silently initialize a new repository.

This is read-only, uses NUL-delimited porcelain v2, and disables optional index
locking. The helper handles spaces, Unicode names and renames without parsing
localized human-readable Git output. No Claude CLI or provider credentials.
