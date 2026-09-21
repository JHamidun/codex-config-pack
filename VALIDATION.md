# Validation — 2026-09-21

## Executed locally

- Mypy 1.19.0, five implementation modules, with
  `--check-untyped-defs --follow-imports=skip --ignore-missing-imports`: passed.
- 37 unit/integration tests on Windows/Python 3.13: passed, none skipped.
- Public bundle: 2633 manifested files, 573 unique catalog entries, 73 parsed native TOML agents.
- Final bundle manifest exactly matches the clean pinned-source builder output.
  Fixture rebuild determinism is tested; the source checkout remained unchanged.
- Dependency audit covers all 573 entries and 1955 relevant reference files.
  It records 971 present links, 187 links to reference-only code, 356 unresolved or
  illustrative links, 14 external-local references and two parameterized references.
- All 343 Python reference sources parsed without execution. No library script was imported.
- Full isolated installation: 2707 managed files verified by hash; repeat install planned zero changes.
- Full isolated uninstall: 2706 unchanged files removed; one deliberately modified router preserved.
  User configuration was not created or modified.
- Native Codex Desktop `0.155.0-alpha.9.2` detected the valid retained `hamidun-pack`
  router in the isolated home via `skills/list`. This is discovery, not recipe execution.
- Gitleaks 8.30.1 and custom path/state/secret-pattern validation: no unresolved findings
  in the final release tree. Only exact generated SHA-256 manifest lines are allowlisted.
- OSV query for the build-only dependency PyYAML 6.0.3 returned no listed advisories.
- Native TOML structure and skill loading were checked against current official documentation.

## Regression coverage added in this audit

Sanitization of quarantined source code and exclusion of raw workflow exports first failed
targeted tests, then passed after the smallest builder changes. Further tests cover transitive
missing dependencies, reference-only code resolution, outside-bundle paths, non-execution of
Python imports, and exclusion of materials without an established upstream redistribution license.
An additional regression reproduces CRLF conversion with `core.autocrlf=true` and verifies
that the release `.gitattributes` preserves the LF bytes used by the bundle manifest.
A path-alias regression verifies canonical output containment before any Git invocation,
following a Windows/Python 3.11 CI failure on a short-name temporary-directory alias.
The catalog CLI also round-trips non-ASCII descriptions under legacy Windows output
encodings using portable JSON escapes, without losing the original text.

## Not claimed

- No live verification of all 573 recipes, provider models, authentication, or 711 code references.
- No installation/activation of 17 MCP examples or two Claude hook event types.
- No audit of every vulnerability in optional historical npm/Python dependency trees.
- No exhaustive guarantee against every possible secret or personal datum.
- No local macOS/Linux execution; the supplied GitHub CI matrix is the cross-platform check.
- No migration of personal memory, history, credentials, or locally consolidated skills.
- No installation into the author's active Codex home.

Source code, privacy normalization, export omissions and compatibility limitations are described
in [AUDIT.md](AUDIT.md). Public license attribution is deliberately retained.
