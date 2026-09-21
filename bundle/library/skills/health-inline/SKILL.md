---
name: "health-inline"
description: "Codebase health инлайн (сам оркестратор): детекция→фикс→верификация. Триггеры: /health-bugs, /health-cleanup, /health-deps, /health-reuse, /health-security."
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


# Health Checks (Inline Orchestration) — 5 modes

You ARE the orchestrator. Execute the workflow directly without spawning a
separate orchestrator agent. Pick the mode, open its full workflow in
`references/modes/<mode>.md`, use worker prompts from
`references/worker-prompts/<mode>.md`.

## Mode table

| Mode | Command | Detect worker | Fix worker | Priorities | Report | Changes log | Fixes artifact |
|---|---|---|---|---|---|---|---|
| bug | /health-bugs | bug-hunter | bug-fixer | critical → high → medium → low | bug-hunting-report.md | bug-changes.json | bug-fixes-implemented.md |
| cleanup | /health-cleanup | dead-code-hunter | dead-code-remover | critical → high → medium → low | dead-code-report.md | cleanup-changes.json | dead-code-cleanup-summary.md |
| deps | /health-deps | dependency-auditor | dependency-updater | critical → high → medium → low | dependency-scan-report.md | deps-changes.json | dependency-updates-implemented.md |
| reuse | /health-reuse | reuse-hunter | reuse-fixer | high → medium → low (no critical) | reuse-hunting-report.md | reuse-changes.json | reuse-consolidation-implemented.md |
| security | /health-security | security-scanner | vulnerability-fixer | critical → high → medium → low | security-scan-report.md | security-changes.json | security-fixes-implemented.md |

All 10 workers live in `agents/health/workers/` (verified 2026-07-18).

## Shared workflow skeleton (identical in every mode)

```
Detection → Validate → Fix/Remove/Update/Consolidate by Priority → Verify → Repeat if needed
```

**Max iterations**: 3

1. **Phase 1 — Pre-flight**: `mkdir -p .tmp/current/{plans,changes,backups}`;
   validate environment (`package.json`, `type-check` + `build` scripts exist);
   initialize TodoWrite with one item per priority + detection + verification.
2. **Phase 2 — Detection**: invoke the mode's detect worker via Task tool
   (prompt in the mode file); read the report, parse counts by priority;
   zero findings → skip to Final Summary.
3. **Phase 3 — Quality Gate (Detection)**: `pnpm type-check && pnpm build`
   inline; fail → report to user, exit.
4. **Phase 4 — Fixing Loop**: for each priority — invoke the mode's fix worker
   via Task tool (backup each file, log to the mode's changes json, produce the
   fixes artifact), then inline quality gate; FAIL → report error, suggest
   rollback, exit; PASS → next priority.
5. **Phase 5 — Verification**: re-invoke the detect worker in verification mode,
   compare with the previous report. remaining == 0 → Final Summary;
   iteration < 3 and remaining > 0 → back to Phase 2; iteration >= 3 → Final
   Summary with remaining items.
6. **Phase 6 — Final Summary**: iterations {count}/3, status SUCCESS/PARTIAL,
   found/fixed/remaining totals, per-priority breakdown, validation status,
   artifacts list (exact templates — in the mode files).

**Error handling** (all modes): quality gate fails → rollback available from the
mode's changes log + `.tmp/current/backups/` (or `rollback-changes` skill);
worker fails → report error, suggest manual intervention, exit workflow.

## Per-mode deltas (details in references/modes/<mode>.md)

- **bug** — scan: type-check/build, security vulns, dead code, debug statements.
- **cleanup** — scan: unused imports/exports, commented blocks, unreachable
  code, debug statements, unused variables/functions/dependencies; Knip.
- **deps** — extra pre-flight: lockfile must exist (pnpm-lock.yaml,
  package-lock.json, yarn.lock); updater works ONE dependency at a time with
  validate-after-each and per-dependency rollback; rollback additionally
  restores package.json + lockfile and runs `pnpm install`.
- **reuse** — priorities high/medium/low only (no critical); extra section
  «Duplication Categories» + Single Source of Truth pattern (canonical
  `packages/shared-types/src/`, re-export `export * from
  '@package/shared-types/{module}'`, NEVER copy code between packages).
- **security** — scan: SQLi, XSS, auth/authz, RLS policy violations, hardcoded
  secrets, insecure dependencies.

## Why inline (vs old orchestrator agent)

| Old (Orchestrator Agent) | New (Inline Skill) |
|--------------------------|-------------------|
| 9+ orchestrator calls | 0 orchestrator calls |
| ~1400 lines (cmd + agent) | ~150 lines |
| Context reload each call | Single session context |
| Plan files for each phase | Direct execution |
| ~10,000+ tokens overhead | ~500 tokens |

## References

- `references/modes/{bug,cleanup,deps,reuse,security}.md` — full original
  workflows, verbatim (formerly the 5 standalone skills).
- `references/worker-prompts/{bug,cleanup,deps,reuse,security}.md` — detailed
  worker prompts (bug = original; other 4 written at merge time, closing the
  links that used to point at a single non-existent worker-prompts file).
