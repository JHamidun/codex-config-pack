# Native development and review workflow

Use the selected guide's domain-specific requirements, architecture patterns and
acceptance criteria. Execute with the current Codex file/search/patch/shell tools in
the explicitly selected repository, not with legacy agent/tool names or source-home
scripts. Read the nearest project instructions and current manifest/lockfiles first.

Inspect the real implementation and existing working patterns. For bugs, reproduce
and observe a failing behavior before making a minimal fix. For a feature, connect
the actual entrypoint, persistence and UI/API path; a stub or schema alone is not
delivery. For refactoring, preserve public behavior and existing user changes.

Use project-supported runtimes and package commands. Historical version/model IDs
and install snippets are not current configuration. Check primary documentation when
needed. Do not auto-install system services, global packages, credentials or paid APIs.
Commands that only appear in `.source` are not installed executables. Translate their
purpose to current project tooling or implement a small project-owned helper with a
failing test and explicit inputs; do not copy unreviewed source defaults.

For browser/a11y/performance work, discover the native browser/testing capability,
exercise the requested route and viewport, and distinguish measured findings from
static code review. No silent browser-cookie extraction, profile reuse or background
server; use an explicit project test server and stop only processes started for this
task when appropriate. Keep automated checks distinct from manual accessibility review.

For read-only reviewer/security/architect roles, do not edit unless the user requests
a fix and the active role allows it. Source `Task/Agent` calls are logical subtasks,
not permission to delegate. Use authorized native collaboration with disjoint ownership
or execute sequentially. Inherit active model settings; never pretend cross-model review.

Run applicable type checks, build and tests, inspect the actual resulting diff and
report commands/results. Deployment, publishing, migrations against production, PR
creation and deletion need their own explicit authorization. After an authorized
remote mutation, verify the real readback/health, not just a successful CLI exit.
