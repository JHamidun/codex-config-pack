# Validation — 2026-09-22

## Portable native runtime and optional adapters

- **109 unit/integration tests passed**, no skips, on Windows/Python 3.13.
- **Thirteen implementation modules passed mypy** with
  `--check-untyped-defs --follow-imports=skip --ignore-missing-imports`.
- **2898 manifest files**, **573 catalog entries**, **73 native TOML profiles** validated.
- All 5138 tracked public configuration files are retained or explicitly accounted
  for in exclusions. No previously distributed runtime path was silently removed.
- The shipped bundle manifest matches a fresh build from the clean pinned source.
  Fixture-level deterministic rebuilds and source immutability are regression-tested.
- All 573 entries prepare without legacy execution fallback. Tests distinguish
  execution modes and never turn procedure coverage into a live-verification claim.
- Installed CLI tests execute actual Git status, CSV profiling, snapshots, restore,
  leak scanning, planning initialization/inspection/checkpoint and memory add/query/graph.
  They verify real files, hashes, notes and structured outputs, not mock provider results.
- Full isolated installation verified **2973 managed files** by hash. Repeat installation
  planned zero changes. Uninstall removed **2972 unchanged files** and preserved the
  deliberately modified router; user configuration was not created or changed.
- Native Codex Desktop `0.155.0-alpha.9.2` detected the router in that isolated home
  through `skills/list`. The test did not modify the active Codex home or run a model.
- Gitleaks 8.30.1 and the custom path/state/secret validator found no unresolved
  release-tree findings. No source script or private credential file was executed/read.
- A network-disabled static audit of the router/native runtime completed; heuristic
  candidates were reviewed, not suppressed globally. Details: [AUDIT.md](AUDIT.md).

## Added failure-path regressions

- Windows directory initialization retries a transient sharing denial with a bounded
  backoff, but preserves a permanent failure and removes only its own staging files.
- Russian prompt aliases round-trip without locale-dependent decoding corruption.
- Memory insertion stays idempotent when the note limit has been reached.
- Unlisted reference paths are rejected before their contents are opened.
- Planning summaries are not accepted as evidence of verified completion.
- Context placeholders resolve to the explicit workspace rather than writable pack state.
- Every group/connection member exists; no ambiguous or unmapped full-catalog entry remains.
- Previously omitted shared scripts/tools/hooks/docs/prompts/MCP code are retained as
  reference-only files. Every tracked public configuration file has a disposition.
- Optional adapters generate real PNG/ICO/PWA assets, looping GIF, transparent WebP
  and VP9 WebM; the local FFmpeg test decodes and compares alpha/frame count.
- Tight sticker cropping retains a transparent margin, including square filled subjects.
- Privacy span offsets/coreference/Unicode round trips, placeholder collisions,
  tokenizer mismatches, staged rollback, unknown paths and redacted CLI failures are tested.
- Synthetic mocks test ACE submit/pending/completed contracts, actual WAV validation,
  OPF construction, CAD geometry/readback, Edit-Banana missing/valid XML, local model
  selection, Tesseract dual outputs and segmentation mask union. These are not GPU,
  CAD-application or model-inference live tests.
- Installed optional-adapter CLI restores a real synthetic OCR artifact; all 13
  helper routes prepare from an isolated installed bundle with integrity checks.

## Exact scope of the evidence

Catalog routing/preparation is tested deterministically. Native `skills/list` proves
router discovery, not automatic selection by a model. Installed helper execution
proves the listed offline operations, not all 573 workflow outcomes.

Neither this test count nor a successful read-only connector profile call validates
all provider APIs, OAuth scopes, media jobs, exports, sends, publication or billing.
Nine specialized recipes now have reviewed engine adapters; their engines and models
are user-side optional dependencies. Lexical/graph notes
are not semantic memory. Seventeen MCP examples and two Claude hook event types remain
inactive. No technical Claude hook equivalence is claimed.

## Historical and cross-platform evidence

The current workflow runs Windows, Ubuntu and macOS with Python 3.11/3.13 and installs
the pinned image-test dependency. Consult the GitHub Actions run whose `headSha`
matches the exact checkout, not merely the latest green badge. FFmpeg artifact tests
skip on CI runners without the executable; the local Windows run included that test.
No live CAD/GPU engine test on those operating systems is implied by green CI.

No personal configuration, memory, transcripts, credentials or locally merged skills
are included. The author's active Codex home is not modified by these isolated tests.
Public attribution is retained deliberately. Scanners are bounded checks, not proof
that every possible private datum or vulnerability is impossible.
