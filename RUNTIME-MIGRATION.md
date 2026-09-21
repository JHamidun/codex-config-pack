# Executable Codex migration

## Acceptance target

After installation, an ordinary user prompt selects a relevant workflow, resolves
its current prerequisites, performs the requested work using native tools or reviewed
helpers, and verifies a real artifact or readback. A catalog hit, renamed command,
manifest validation or schema check alone does not meet this target.

The public pack must remain separate from personal configuration, memory, history,
credentials and machine-specific paths. External services need user-supplied access;
installation must not authorize services or silently enable paid providers.

## Current implemented slice

- Russian prompt aliases and exact workflow names rank reviewed recipes first.
- `catalog.py --prepare <id>` resolves one recipe, checks catalog/recipe/helper hashes,
  and replaces the installation-root placeholder. It never runs historical code.
- The installed pack now retains its integrity manifest for this runtime check.
- Three standard-library helper workflows run without provider credentials:
  Git porcelain-v2 status; bounded CSV profiling; snapshot creation and atomic restore.
- Tests use a real temporary Git repository, CSV fixtures, artifact mutations, an
  isolated installation, installed command-line tools and checksum tampering.
- Shared GSD workflows, schemas, templates and workflow references omitted by the
  first builder are included. Their code remains quarantined pending review.
- The dependency resolver now understands pack-root execution-context references,
  including containment checks, instead of overlooking those dependencies.

Coverage: 3 `native-helper`, 121 `instructions`, 449 `needs-adapter` entries.
The helper tests cover the concrete supported operations, not every possible request
in the broader CSV/Git/snapshot domains. No claim of automatic LLM selection testing.

## Remaining work

1. Port GSD orchestration and its project-state helpers, with explicit project roots,
   no source-home writes, inherited models and authorized collaboration only.
2. Review each remaining dependency closure. Separate genuinely required runtime
   dependencies from historical examples; do not bulk-relabel entries as working.
3. Replace provider-neutral media, documents and browser instructions with native
   capability paths; maintain provider-specific paths only where the user needs them.
4. Give service integrations a reviewed adapter or native connector plus explicit
   setup, capability checks and redacted failure reporting. Test read-only calls
   before independently authorized mutations.
5. Adapt memory/state/hooks without copying private data or treating Claude payloads
   as interchangeable with Codex events.
6. Validate realistic prompts through Codex itself in isolation, including routing,
   artifact correctness, unavailable dependencies and permission boundaries.
7. Re-run cross-platform CI and the privacy audit before publishing the runtime release.

The published baseline and ZIP remain the previous audited release until this
development work is explicitly released. Do not describe this slice as full parity.
