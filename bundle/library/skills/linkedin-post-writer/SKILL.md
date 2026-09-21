---
name: "linkedin-post-writer"
description: "Viral LinkedIn посты на hook-формулах: хук+пост, Publora-schedule. Триггеры: «hook formula», «разбери viral пост»."
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


# LinkedIn Post Writer

Ship long-form LinkedIn posts using hook formulas that actually performed in 2025-2026 (verified engagement multipliers from Jake Ward, Lara Acosta, Cam Trew, Noam Nisand, Alex Vacca, Richard Illingworth, PublicCreator4).

## When to use

- User says "write me a LinkedIn post about X"
- User has a topic + a rough angle and needs a hook + structure
- User wants to pick from known-winning formats and fill in their voice
- User wants to audit + schedule in one flow

## Formulas this skill can use

| Code | Formula | Reference eng | Best for |
|---|---|---|---|
| F1 | Platform Risk Anaphora (Jake Ward) | 4,240 | Category/platform posts, product-as-fix |
| F2 | R.I.P. Obituary (Alex Vacca) | 3,822 | Era-ending claims, industry pivots |
| F3 | Year-over-Year Pivot (Cam Trew) | 494, 3.74x | Identity shifts, founder reflection |
| F4 | Time-Anchor Confession (Lara Acosta) | 1,519+ | Vulnerability, voice reset, ICP re-targeting |
| F5 | Self-Proving Meta (Noam Nisand) | 1,082 / 435 comments | Commitment-based posts, tests in public |
| F6 | Comment-Gate Lead Magnet (Illingworth) | 717-3,008 | List building (use sparingly, capped reach) |
| F7 | Odd-Precision Money Ledger (Jake Ward) | 1,755, 9.4x | Founder build-log, cost breakdowns |
| F8 | Paid-vs-Free Reversal (Illingworth) | 550, 19.64x | Free framework give-away |
| F9 | Curiosity-Gap Teaser (PublicCreator4) | 306, 4.25x | Emergent behavior, behind-the-scenes |
| F10 | Contrarian + Historical Receipts (Jake Ward) | 3,083 | Sacred-cow takes, AI/tech cycles |

Full skeletons in `references/hook-formulas.md`.

## Steps

1. **Gather inputs.** Topic, angle, draft ideas if the user has them, target audience (founders / operators / marketers), desired length (short 300-500 / medium 900-1300 / long 1500-1900 chars).
2. **Pick the formula.** If the user didn't specify, suggest 2-3 formulas that fit the topic and let them pick. Show the reference engagement number next to each.
3. **Draft the post.** Fill the formula skeleton with user voice. Respect the 2026 algorithm rules:
   - Hook in first 210 chars (before "… see more")
   - 900-1,300 char sweet spot for text posts
   - Double line-breaks between ideas, not single
   - 0-2 hashtags, placed at end
   - No external links in body (move to first comment)
4. **Humanizer pass.** Strip em dashes, AI vocab, rule-of-three, generic openers. Add at least 1 specific number, 1 named entity, 1 first-person concrete detail per 100 words.
5. **Run audit.** Optionally run the checklist from `../linkedin-humanizer/references/linkedin-post-audit/` for algorithm + voice checks before showing to user.
6. **Approval card.** Show: formula used, full draft, char count, suggested posting window (Tue/Wed/Thu 7:30-9:00 AM local), reaction targets from likely commenters.
7. **On approval — adapt to the active backend.** Call `lib.active_backend()`:
   - **`socialpublisher`** (SOCIALPUBLISHER_API_KEY set) → schedule via `lib.SocialPublisherClient.create_post` with LinkedIn platformId. If `scheduledTime` omitted, SocialPublisher posts ~90s in the future.
   - **`manual`** (no backend configured — the default) → output the approved post via `lib.manual_mode_message(draft_text, target_url="https://www.linkedin.com/post/new/", kind="post")`. User pastes directly into LinkedIn's post composer. Do NOT attempt to publish programmatically.
   - **`diy`** (LINKEDIN_SKILLS_CUSTOM_POSTER set) → invoke the custom poster with the post content + optional media URLs.

## Hard rules (from user feedback)

- No em dashes. Ever. Period.
- Capitalize all names, companies, products.
- Never frame LinkedIn as inferior in a LinkedIn post (algo penalty).
- Don't name-drop the user's product in a way that reads as self-promo. One mention max, and only when it's the natural conclusion, not the pitch.
- Include at least one moment of real vulnerability or concrete stakes — pure insight posts don't land in 2026.
- Vary sentence length aggressively. Mix 3-word sentences and 25-word sentences.

## Anti-patterns (skill will refuse)

- All-caps first line ("THIS CHANGED EVERYTHING.")
- Em dashes anywhere
- "In today's fast-paced world" openers
- Rule-of-three lists without receipts
- "Game-changer", "deep dive", "leverage", "fundamentally"
- External links in the body
- Reused engagement-bait closers ("tag someone who needs this")

## Resources

- `references/hook-formulas.md` — all 10 formula skeletons with worked examples
- `references/algorithm-heuristics.md` — 2026 posting rules (timing, format, length)
- `references/humanizer-checklist.md` — the full scrub list
- Upstream (EXTERNAL, отсутствует в этом окружении): corporate-knowledge repo, `your-kb/linkedin/2026-04-13-viral-drafts/` — canonical reference drafts

## Related skills

- `../linkedin-humanizer/references/linkedin-post-audit/` — run this on any draft before publishing
- `linkedin-humanizer` — aggressive AI-tell scrubber
- `references/linkedin-hook-extractor/` — reverse-engineer a hook from a viral post you admire
