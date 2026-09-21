# Artifact snapshots in Codex

Create a byte-for-byte version of a specific artifact before a requested edit,
or when the user asks for a snapshot. Use the project workspace, not a home or
configuration directory. This complements version control; it does not replace it.

```text
python "${CODEX_PACK_ROOT}/scripts/runtime.py" snapshot --workspace "<workspace>" --file "relative/path/index.html"
```

The result contains an ID, original relative path and SHA-256. Store that ID in
the task response when useful. Data lives in `.snapshots/<id>/content` with
`metadata.json`. Files are bounded to 20 MB. Links, protected configuration,
obvious credential/state files, `.source` files and workspace escape are rejected.
The helper does not scan arbitrary directories or take automatic screenshots.

To restore an explicitly requested version:

```text
python "${CODEX_PACK_ROOT}/scripts/runtime.py" snapshot --workspace "<workspace>" --restore "<id>"
```

Restore validates the checksum and takes a new snapshot of the current target
before atomically replacing it. It returns `before_restore_id` for undo. A target
change detected during restore aborts the operation. This is not a filesystem
sandbox against hostile concurrent processes; use a trusted project workspace.

Do not restore or delete versions without the user's authorization. Do not run
automatic age-based cleanup. Keep `.snapshots/` out of publication and inspect the
project's ignore rules before adding any narrow ignore entry.
