---
name: "linkedin-post-audit"
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
name: linkedin-post-audit
description: Audit a LinkedIn post draft against 2026 algorithm heuristics and voice rules before publishing. Use when the user has a draft and wants to catch AI tells, algorithm penalties, or structural issues before shipping. Returns a pass/fail report with specific fixes and optional auto-rewrites. Keywords: post audit, linkedin review, algorithm check, EnterpriseTool, humanizer, AI detection, pre-publish check.
---

# LinkedIn Post Audit

Run any post draft through the 2026 heuristic checklist. Catches AI tells, timing/format issues, length violations, and structural weaknesses before publishing.

## When to use

- Before publishing a hand-written or AI-drafted post
- When `linkedin-post-writer` finishes a draft (auto-invoked)
- When a recent post didn't land and the user wants a post-mortem

## Input

- A post draft (plain text)
- Optional: target audience, scheduled time, format (text / carousel / video / image)

## Output

- **Pass/Fail** header
- **Blockers** (must fix before publishing): em dashes, AI vocab, external links in body
- **Warnings** (ship-risky): uniform sentence rhythm, missing numbers, generic close
- **Score estimates:** OriginalityAI AI-likelihood, approximate first-hour reach fit
- **Suggested fixes:** inline rewrites for each issue
- **Timing recommendation:** best window given audience

## Checks

### Blockers (auto-fail)
1. Em dash / en dash / double dash present
2. External link in body (not in first comment)
3. Post exceeds 3,000 chars (LinkedIn hard limit)
4. Opens with "In today's fast-paced world..." or similar
5. Ends with "What do you think?" or "Thoughts?"
6. Contains AI vocabulary blacklist words (see `references/ai-tells.md`)
7. Frames LinkedIn as inferior in a LinkedIn post (algo penalty)

### Warnings (flag with suggested fix)
8. Hook doesn't fit in first 210 chars (mobile `…see more` cutoff)
9. Length outside 900-1,300 sweet spot (or 1,500-1,900 for long-form with breaks)
10. Uniform sentence length (all 15-22 words)
11. No specific number per 100 words
12. No named entity
13. No first-person sensory detail
14. Rule-of-three list without receipts
15. More than 2 hashtags
16. User's own product named more than once
17. Missing reaction-prompting moment (vulnerability, stakes, question)
18. Passive voice >10%

### Info (neutral notes)
19. Suggested posting time given audience
20. Format recommendation (text / carousel / video) given topic
21. Similar-hook detection: if this post's first 100 chars match a recent post

## Steps

1. Parse draft into sentences, paragraphs, first-210-char hook.
2. Run each blocker check; collect failures.
3. If any blockers, return **FAIL** with specific fix suggestions; optionally offer auto-rewrite.
4. If no blockers, run warnings.
5. Estimate OriginalityAI score (heuristic proxy: avg sentence length variance, unique 3-gram ratio, passive voice ratio).
6. Return structured report.

## Example

> Input: "In today's fast-paced world, businesses are fundamentally leveraging AI to unlock massive ROI — here's what I learned..."

> Output:
> - **FAIL** (3 blockers)
> - L1 "In today's fast-paced world" (filler opener)
> - L1 "fundamentally" (AI vocab)
> - L1 "leveraging" (AI vocab)
> - L1 em dash `—`
> - **Suggested rewrite:** "Businesses are using AI to cut costs 40%. Here's what I learned."

## Files

- `SKILL.md` — this file
- `references/ai-tells.md` — complete blacklist + regex patterns
- `references/audit-checklist.md` — full 20-point checklist with thresholds

## Related skills

- `linkedin-humanizer` — aggressive rewrite if audit fails
- `linkedin-post-writer` — regenerate draft using a proven formula
