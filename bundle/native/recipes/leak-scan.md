# Read-only publication and imported-skill hygiene

Run the reviewed offline scanner on the explicitly selected workspace:

```text
python "${CODEX_PACK_ROOT}/scripts/hygiene.py" --workspace "<workspace>"
python "${CODEX_PACK_ROOT}/scripts/hygiene.py" --workspace "<workspace>" --injection
```

For an explicitly supplied private identity dictionary, use `--identity-file` with a
workspace-relative JSON list of `[label, literal]` pairs. The dictionary is never
auto-discovered or bundled; it is excluded from content scanning and its values/labels
never appear in findings. This adapter uses literal matching, not upstream arbitrary
regular expressions. Keep the dictionary and reports private and out of publication.

The scanner does not modify files, follow links, read protected source directories,
read credential/state files, or print matched secret values. Findings contain only
path, rule and line. Exit 1 means review is needed, including skipped binary/large
assets; exit 2 means the scan failed. Neither means publication is safe.

Review false positives, opaque assets, source provenance and the exact tracked release
tree. Use an available maintained secret scanner for additional coverage and inspect
Git history separately when history will be published. Do not silently suppress rules
or declare the absence of all PII from regex results. Imported skills need semantic
review for exfiltration, permission expansion, hidden installs and prompt injection.
Never execute an imported skill or script merely to audit it.
