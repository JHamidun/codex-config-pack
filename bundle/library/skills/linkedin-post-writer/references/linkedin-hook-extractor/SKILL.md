---
name: "linkedin-hook-extractor"
description: "---"
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


---
name: linkedin-hook-extractor
description: Reverse-engineer the hook formula from any viral LinkedIn post. Use when the user finds a post they want to learn from — paste the URL and get a structural breakdown. Identifies which of the 10 canonical 2026 formulas it uses (anaphora, R.I.P. obituary, year-over-year pivot, time-anchor confession, self-proving meta, odd-precision money, paid-vs-free reversal, curiosity-gap, contrarian historical, comment-gate). Returns a blank template you can fill with your own voice. Keywords: hook formula, viral teardown, reverse engineer, post structure, 2026 formulas.
---

# LinkedIn Hook Extractor

Paste a viral LinkedIn post URL. Get back: which hook formula it uses, the exact structure, why it worked, and a blank template mapped to your topic.

## When to use

- User finds a viral post they want to study
- User wants to replicate a specific creator's pattern (Jake Ward, Lara Acosta, etc.)
- Before `linkedin-post-writer` to seed a draft with a proven structure

## Input

A LinkedIn post URL (any type: activity, share, ugcPost).

## Output

- **Formula identified** (F1-F10 from `linkedin-post-writer/references/hook-formulas.md`) with confidence score
- **Structural breakdown:**
  - Hook lines (first 210 chars)
  - Body architecture (sections + what each does)
  - Close pattern
  - Reaction-triggering devices (numbers, named entities, vulnerabilities)
- **Why it worked** psychologically
- **Blank template** filled with slot markers matched to the original, ready for the user's voice
- **Cautions:** anything in the original post that would fail 2026 audit (em dashes, AI vocab, outdated tactics)

## Steps

1. **Parse URL.** `lib.url_parser.parse_linkedin_url` → `post_urn`.
2. **Fetch post body.** HarvestAPI preferred; fall back to asking user to paste text.
3. **Classify.** Match against the 10 formulas using features:
   - First 2 lines: anaphoric? question? confession? number-led?
   - Body: numbered list? dated receipts? ledger? teardown?
   - Close: mirror question? identity reframe? commitment?
4. **Score confidence.** If multiple formulas fit, return top 2 with fit scores.
5. **Extract structure.** Pull each logical section and label it by formula role.
6. **Generate blank template.** Replace specifics with `{slot}` markers that match the user's topic.
7. **Audit the source.** Flag any AI tells in the original so the user doesn't copy them.

## Example

> **Input:** `https://www.linkedin.com/posts/dharmesh_every-b2b-software-company-is-or-should-activity-7448808898326654978-iW20`

> **Output:**
> - **Formula:** F10 Contrarian + Historical Receipts (confidence 0.72). Secondary: F5 Self-Proving Meta (0.28).
> - **Hook (first 210 chars):** "Every B2B software company is (or should be) building an agentic version of their product."
> - **Body:** single bold claim → 3 paragraphs of reasoning → specific list of product changes required
> - **Close:** implicit call to action ("Seen this play out in your market yet?")
> - **Blank template:**
>   ```
>   Every {category} {bold claim}.
>
>   {Reasoning paragraph 1 — the forcing function}
>   {Reasoning paragraph 2 — what it requires}
>   {Reasoning paragraph 3 — what breaks if you don't}
>
>   {Closing question that invites reader to take a side}
>   ```
> - **Cautions:** none (post is clean)

## Formulas reference

See `linkedin-post-writer/references/hook-formulas.md` for the 10 canonical formulas with full skeletons.

## Files

- `SKILL.md` — this file
- `references/classification-rules.md` — feature extraction + scoring heuristics

## Related skills

- `linkedin-post-writer` — use the extracted template to draft your own
- `linkedin-post-audit` — audit your draft before shipping
