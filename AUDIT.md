# Dependency and release audit — 2026-09-21

This report describes published baseline `b3a320b`. The subsequent local runtime
development slice, including changed dependency counts, is tracked separately in
[RUNTIME-MIGRATION.md](RUNTIME-MIGRATION.md). It is not a completed runtime release.

## Scope

Source: public `JHamidun/claude-code-config-pack`, pinned at
`e9f5f9e019d3c6dc9fe83b00499f223b5f9e6d32`. No personal Codex/Claude
configuration, credentials, sessions, memory, or local merged skills are inputs.
The builder selects tracked public source files only; it does not run upstream code.

This is a documentation-first port, **not a working replacement for every integration**.

## Dependency coverage

- All 573 distributed entries covered: 344 skills, 156 command recipes, 73 agent profiles.
- 134 entries have no detected runtime blockers; 439 require runtime review.
- Whole skill directories plus transitive local Markdown references are inspected.
- 711 code files remain reference-only `.source`; 343 Python sources parse successfully,
  but are neither imported nor executed by the audit.
- Local links distinguish present files, quarantined code, unresolved/illustrative links,
  parameterized locations, and dependencies outside the bundle.
- Import names and candidate environment-variable names are recorded, never values.
  Import names are not guaranteed PyPI package names; examples and local modules can appear.
- Seventeen MCP configurations and two hook event types remain uninstalled.

See [the full dependency map](bundle/dependency-audit.json) for per-entry closure,
file/line references and blockers. Missing links in examples can be false positives;
the report does not assert that every unresolved string is a production failure.

## Corrections since the initial structural port

1. The first dependency detector inspected recipe text, not its complete linked resources.
   Dependency classification now includes file trees and transitive Markdown links.
2. Privacy normalization previously did not cover quarantined code. It now covers source
   references as well as prose and metadata. These sanitized sources are not runtime adapters.
3. Raw n8n workflow exports can contain pinned example data, contacts and service identifiers.
   All 2060 exports are excluded rather than claiming a regex can reliably anonymize them.
4. The source license explicitly withholds a grant for `doc-coauthoring` and
   `building-an-exo`. Their 27 files are excluded. Public availability alone is not treated
   as permission to redistribute. Original license/notice attribution is retained.
5. Gitleaks 8.30.1 supplements the custom path/secret scan. The scanner binary was checked
   against its upstream SHA-256 checksum. Its only project-specific exception is an exact
   generated-manifest line containing a verified 64-character hexadecimal SHA-256 digest.
   Source, scripts, documentation, and other JSON files are not excluded from secret scanning.

## Installed versus optional dependencies

The installer and catalog search need Python 3.11+ and its standard library only.
Rebuilding and build tests additionally need pinned `PyYAML==6.0.3`.
An OSV query for that exact version returned no listed advisories on the audit date;
this is not a guarantee against unknown vulnerabilities.

Imports such as requests, Pillow, NumPy, provider SDKs, Playwright and Telethon occur
in optional historical recipes. They are **not** installed globally or declared as one
giant runtime environment. Each requested integration needs its own pinned environment,
native-tool decision, credentials and a real smoke test. npm manifests in reference
material are likewise not installed or claimed vulnerability-free.

## Runtime adaptation decisions

- Agents use native TOML `name`, `description`, `developer_instructions`, inherited models,
  and read-only mode for selected reviewers. No guessed model-alias translation.
- Commands are searchable recipes, not registered Claude slash commands.
- Legacy tool names are mapped conceptually to available native tools, not replayed.
- Source paths and scripts are not activated by a global rename of `.claude` to `.codex`.
- One discoverable router loads a selected recipe on demand; optional agents remain opt-in.
- Install/uninstall preserve existing configuration and user edits; provider authentication,
  hooks, paid calls, scheduled tasks and background services are never enabled implicitly.

Native formats checked against [custom-agent documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents),
[skill loading](https://learn.chatgpt.com/docs/build-skills) and
[configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference).

## Boundaries

No real API workflow has been verified end to end. Syntax, hashes, tests and secret scans
do not prove full functional compatibility or the absence of every possible sensitive datum.
Published author names, repository provenance, third-party attribution, and example.com
addresses remain intentionally. Private histories, personal files and secrets are not inputs.
See [VALIDATION.md](VALIDATION.md) for the exact executed checks.
