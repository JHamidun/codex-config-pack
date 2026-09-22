# Executable Codex migration

## Acceptance target

An ordinary user prompt selects a relevant workflow, resolves its prerequisites,
performs the requested work with native tools or reviewed helpers, and verifies an
actual artifact/readback. A catalog match, renamed command or valid manifest alone
does not meet that target. This public pack must never depend on its author's private
configuration, memory, transcripts, credentials or machine paths.

## Implemented

All 573 catalog entries have an explicit execution path; none silently falls back
to executing the historical Claude scripts:

| Mode | Entries | What is implemented | What is not proved |
|---|---:|---|---|
| `native-procedure` | 464 | Codex execution procedures plus preserved domain guidance; explicit operations for every GSD command | Independent, live end-to-end execution of every recipe |
| `native-helper` | 4 | Git status, CSV profiling, version snapshots/restore, redacted hygiene scan | Every possible request in those domains; a clean scan is not a security certificate |
| `connection-required` | 105 | Exact service/engine requirements, native capability discovery, authorization and readback protocol | A bundled SDK, a connected account or a tested provider action; 9 specialized engines additionally need reviewed adapters |

The builder retains original methodology, templates and references. Full bodies
remain cold; the model loads a selected procedure and only the domain references it
needs. Native agent profiles prepare an exact catalog ID rather than loading obsolete
Claude tool contracts as active instructions. Models and permissions are inherited.

### Reviewed offline helpers

- `runtime.py`: read-only Git porcelain-v2 status, bounded CSV profiling, explicit-file
  snapshots and atomic restore with a pre-restore snapshot.
- `planning.py`: initialize from an explicit project brief, inspect project-state
  files and append continuation checkpoints. It never infers verified completion from
  a summary file, resets an existing project, commits or schedules background work.
- `memory.py`: explicit curated-note ingestion, provenance, bounded lexical retrieval
  and an explicit relationship graph. It does not import chats or create an embedding
  index. No private source is discovered automatically.
- `hygiene.py`: bounded read-only scans with redacted findings, optional explicit
  identity literals and injection heuristics. It is not an exhaustive DLP product.

Business and author context now belongs in the selected workspace's `.codex-context/`,
not in the installed library. Blank questionnaires ship without personal contents.
The dependency inventory includes shared GSD, scripts, tools, hooks, docs, prompts,
MCP reference code and the full public configuration-file accounting. Historical code
stays `.source`; preserving it does not enable it or prove its compatibility.

### Verification performed

Installed command-line tests exercise real temporary Git repositories, CSV data,
file mutation/restore, planning state, continuation checkpoints and curated-memory
query/graph. Tests also cover tampering, path escapes, secret redaction, Unicode,
transient Windows locks, idempotency and preserving user edits on uninstall.

Native Codex discovery and deterministic catalog routing are different from testing
automatic model selection. See [VALIDATION.md](VALIDATION.md) for exact evidence.

## Explicit remaining boundaries

1. **Connections.** A public configuration cannot distribute accounts, OAuth grants,
   API credits, servers, local applications or model weights. Per-service scope is
   listed in [CONNECTIONS.md](CONNECTIONS.md). A profile read is not an end-to-end test
   of sending, exporting, generating or publishing.
2. **Specialized engines.** Nine recipes still need an engine and reviewed project-
   owned adapter. This is actual remaining adaptation work, not merely a login step.
   CAD COM, GPU music generation, segmentation/OCR and local PII filtering cannot be
   certified by a generic media instruction.
3. **Host differences.** A CLI does not automatically supply the Desktop browser,
   documents, media, task-management or automation tools. Native capability absence
   is reported rather than bypassed through private databases or subscription tokens.
4. **Memory and hooks.** Lexical notes/graph are not the old semantic-history system.
   Claude hooks are not registered as Codex hooks. Guard rules live in native guidance;
   no technical event-level equivalence is claimed.
5. **Independent workflow evaluation.** All recipes have preparation/integrity checks,
   but they have not all been selected and executed by fresh model sessions. A repeated
   self-review is not independent evaluation or cross-model consensus.

Therefore this version is a native-procedure runtime candidate, **not a claim that
the entire Claude installation works out of the box unchanged**. Remaining adapter
and live-verification gaps must stay visible in release descriptions.
