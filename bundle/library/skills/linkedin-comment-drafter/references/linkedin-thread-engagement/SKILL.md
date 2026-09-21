---
name: "linkedin-thread-engagement"
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
name: linkedin-thread-engagement
description: Monitor LinkedIn threads where the user commented for author replies and inbound signals. Use when the user wants to track which of their comments earned personal replies from post authors (the highest-value engagement signal). Flags the 6-24h author-reply window where author replies are most likely, drafts follow-up responses, and optionally routes to DM. Keywords: thread monitoring, author reply, inbound tracking, comment follow-up, engagement compound.
---

# LinkedIn Thread Engagement

The engagement compounding layer. Tracks which of the user's comments earned author replies, drafts timely follow-ups, and flags the 6-24 hour window where thread momentum is highest.

## When to use

- Daily: "What threads need follow-up today?"
- After posting a batch of comments: "Check back in 6 hours"
- When an author replied personally (e.g., the post author replied to you): "Draft the response"

## Input

- The user's LinkedIn profile URL (to pull their recent comments)
- Optional: specific post URL to monitor

## Output

### Daily report

| Posted | Author | Post | Comment | Reply? | Stage | Action |
|---|---|---|---|---|---|---|
| 18h ago | Alex M. | legaltech SaaS | "key takeaway" | ✅ author replied 14h ago | Warm (6-24h window) | **Reply now** |
| 22h ago | Dana R. | CRM vendor | "integration depth moat" | No | Cold | Skip |
| 3h ago | Priya S. | retail AI | "twin economies" | No | Watch | Check in 3h |

### For each warm thread
- Thread preview (last 3 turns)
- Suggested response (drafted via `linkedin-reply-handler`)
- Reaction target (the specific reply URN, not the post)
- Priority (high / medium / low)

### Weekly roll-up
- Total comments posted
- Author-reply rate (target: 15%+)
- Conversion to DM (when thread closes warm)

## Steps

1. **Fetch user's recent comments** via HarvestAPI `/linkedin/profile-comments`.
2. **For each comment posted in last 72h:** fetch the parent post's comment tree and look for:
   - Replies to the user's comment
   - Whether the author posted any of those replies
   - Timestamps (time since user's comment, time since latest reply)
3. **Classify stage:**
   - **Hot (<6h):** author just replied — respond within 90 min for max thread momentum
   - **Warm (6-24h):** the author-reply window — author replies most happen here
   - **Cool (24-72h):** still respondable but lower velocity
   - **Dormant (>72h):** don't reply in thread; consider DM
4. **Draft responses** for warm threads using `linkedin-reply-handler` (which adapts to the active backend per `lib.active_backend()` — SocialPublisher auto-posts, manual mode returns copy-paste, DIY invokes custom poster).
5. **Flag suspicious patterns:**
   - Author replied but also deleted someone else's comment (author is actively moderating, tread carefully)
   - Commenter is in thread self-promoting (your reply shouldn't engage them)
6. **DM routing:** if thread is dormant but the author engaged meaningfully, draft a DM that references the thread specifically.

## The 6-24h author-reply window

Typical shape: the post author replies to your comment 20-30h after publishing. This is the sweet spot.

- **0-6h:** 70% of author replies happen here if they're going to happen
- **6-24h:** ~25% of author replies, but these are higher-quality (author took time to think)
- **>24h:** thread rarely produces new author engagement

**Follow-up timing:**
- If author replied in 0-6h window: respond within 90 minutes
- If author replied in 6-24h window: respond within 2 hours (they're still checking)
- If author replied >24h: respond within 4 hours before thread goes cold

## Inbound-quality signals

High-quality commenter = worth the follow-up:
- Founder/operator title in profile
- Company in user's ICP
- Active posting history (not just reactions)
- Mutual 2nd-degree connections >10
- Prior thoughtful comments on user's posts

Low-quality = skip:
- Generic praise with no specifics
- Template language ("I'd love to hop on a quick call")
- Profile is sales/agency with no operator history
- Same comment across many creators' posts

## Hard rules

- Never reply to a reply later than 72h after the thread's last turn. Switch to DM.
- Never chain 3+ replies under one comment (thread spam).
- If the author deleted their reply, do not reply — they reconsidered.
- Don't DM a warm thread before first replying publicly (skips a step).

## Example

> Input: monitor your-handle profile, last 24h

> Output:
> - **1 warm thread:** the post author replied 14h ago. Current stage: Warm (8-24h). Suggested response ready. Action: post within 2 hours.
> - 8 cold threads (no author engagement). Skip.
> - 3 watching threads (<6h old, author may still reply). Check again in 3-6h.

## Files

- `SKILL.md` — this file
- `references/thread-timing.md` — the timing matrix with examples

## Related skills

- `linkedin-reply-handler` — drafts the actual follow-up message
- `linkedin-comment-drafter` — drafts the initial comment that starts threads
