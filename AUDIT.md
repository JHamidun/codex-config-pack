# Dependency and release audit — 2026-09-22

## Scope and provenance

Source: public `JHamidun/claude-code-config-pack`, pinned at
`e9f5f9e019d3c6dc9fe83b00499f223b5f9e6d32`. Only tracked public source files are
build inputs. Personal configuration, memory, transcripts, credentials, locally
merged skills and the author's current connector accounts are not exported.
The source checkout remains read-only. Source scripts are inspected, never executed.

This is a portable native runtime release, not proven full Claude runtime parity.
[Runtime scope](RUNTIME-MIGRATION.md) and [connection requirements](CONNECTIONS.md)
separate implementation, prerequisites and verification.

## Complete source accounting

All **5138** tracked files under the public `.claude/` tree are accounted for:

- 2779 preserved reference files, including 786 quarantined code files.
- 2060 raw n8n exports excluded because pinned example data cannot safely be removed
  by a generic text substitution.
- 27 files excluded from two skills without an established redistribution grant
  (`doc-coauthoring`, `building-an-exo`). Public availability is not a license.
- 266 binary/large/unsupported assets explicitly listed for separate dependency review.
- One state/secret-named file excluded without importing its contents.
- Five root runtime/configuration/coverage files explicitly excluded; MCP/hook names
  are indexed as inactive. Their original configuration is not installed.

No source file disappears silently from this inventory. Source hashes, transformed
paths and exclusions appear in [bundle/compatibility.json](bundle/compatibility.json).
Compared with the preceding runtime build, no previously distributed path was removed.
Newly retained shared tools, scripts, hooks, docs, prompts and MCP source resolve
references that were previously missing; they do not become executable adapters.

## Dependency coverage

- 573 entries: 344 skills, 156 command recipes, 73 native agent profiles.
- 2140 relevant files statically inspected, including transitive Markdown references.
- 387 Python reference sources parse successfully; none is imported or executed.
- Reference inventory: 1326 present, 1078 reference-code-only, 902 missing/illustrative,
  35 parameterized and 14 external-local references.
- Import candidates and environment variable **names**, never secret values, are recorded.
  Import names are not a verified list of installable packages.
- Historical source flags: 124 instructions-adapted and 449 requires-runtime-review.
  These are separate from native execution routes: 464 procedures, 13 helper entries,
  96 connection contracts. No entry claims a completed live provider test.

See [bundle/dependency-audit.json](bundle/dependency-audit.json) for file/line evidence.
Missing links in examples can be false positives. Conversely, a valid link or parsed
source does not prove a working dependency.

## Native changes reviewed

- Agent profiles load a bounded native procedure with preserved domain guidance,
  inherited models and the existing explicit read-only reviewer policy.
- Every GSD command has a native operation; project initialization, inspection and
  continuation have a reviewed local helper rather than a copied `gsd-tools` command.
- Business/author context writes target the user's selected workspace, not the pack.
- Local memory accepts only explicit curated notes; no automatic transcript ingestion,
  source-home access, embedding service or background job is introduced.
- Preparation verifies manifest membership before reading a document and checks all
  recipe/helper hashes. Historical `.source` execution remains forbidden by contract.
- Install/uninstall are additive, idempotent, link-aware and preserve user modifications.
  The pack never merges credentials, enables hooks or installs all providers implicitly.

## Privacy and security checks

The builder sanitizes contacts and machine paths in prose, metadata and quarantined
code. Gitleaks 8.30.1 and the pack path/state/secret validator report no unresolved
findings in the exported release tree. The scanner binary is checksum-pinned; the only
special secret-scan exception is an exact generated SHA-256 manifest line.

A separate network-disabled static audit of the router/native runtime completed,
including the optional adapters. Its 39 heuristic findings were reviewed: defensive
credential denylists, fixed Git/engine argument lists, inactive public MCP indexing,
public domain-reference paths and declared routing metadata. Engine execution accepts
only explicit trusted user installations; it is not a sandbox for malicious executables.
No new scanner-wide exceptions were added. Private-map handling, output boundaries,
endpoint origins and actual artifact validation were also reviewed. This was a primary-
agent review, not an independent security certification. Historical reference code
is not covered by a claim that it is safe to run. Scanner-only hits in untracked local
type-check caches are not distributed; publication checks run on the exact Git export.

## Runtime dependencies

Installation, catalog routing and reviewed offline helpers use Python 3.11+ standard
library only; Git status additionally requires Git. Building/tests need pinned
`PyYAML==6.0.3`. No bulk pip/npm install of historical dependencies occurs.

Optional accounts, local engines, GPU models, browser/document tools and third-party
SDKs must be available for the selected action. Nine specialized recipes have reviewed adapters with explicit operation coverage;
their engines remain optional user prerequisites. Existing native connectors are preferred,
but an account lookup does not prove all operations or scopes.

## Limits

No live test of every recipe/provider, technical Claude-hook equivalence, exhaustive
DLP guarantee or security audit of all historical dependencies is claimed. Public
upstream authorship, repository URLs and third-party license attribution are retained
intentionally. Exact executed checks are in [VALIDATION.md](VALIDATION.md).
