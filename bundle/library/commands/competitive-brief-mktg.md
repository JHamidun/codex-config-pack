---
name: "competitive-brief-mktg"
description: "Research competitors and generate a positioning and messaging comparison"
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


# Competitive Brief

> If you see unfamiliar placeholders or need to check which tools are connected, see the MCP registry: `${CODEX_PACK_ROOT}/library/config/mcp-servers.md`.

Research competitors and generate a structured competitive analysis comparing positioning, messaging, content strategy, and market presence.

## Trigger

User runs `/competitive-brief` or asks for a competitive analysis, competitor research, or market comparison.

## Inputs

Gather the following from the user:

1. **Competitor name(s)** — one or more competitors to analyze (required)

2. **Your company/product context** (optional but recommended):
   - What you sell and to whom
   - Your positioning or value proposition
   - Key differentiators you want to highlight

3. **Focus areas** (optional — if not specified, cover all):
   - Messaging and positioning
   - Product and feature comparison
   - Content and thought leadership strategy
   - Recent announcements and news
   - Pricing and packaging (if publicly available)
   - Market presence and audience

## Research Process

For each competitor, research using web search:

1. **Company website** — homepage messaging, product pages, about page, pricing page
2. **Recent news** — press releases, funding announcements, product launches, partnerships (last 6 months)
3. **Content strategy** — blog topics, resource types, social media presence, webinars, podcasts
4. **Review sites and comparisons** — third-party comparisons, analyst mentions, customer review themes
5. **Job postings** — hiring signals that indicate strategic direction (optional)

## Competitive Brief Structure

### 1. Executive Summary
- 2-3 sentence overview of the competitive landscape
- Key takeaway: your biggest opportunity and biggest threat

### 2. Competitor Profiles

For each competitor:

#### Company Overview
- What they do (one-sentence positioning)
- Target audience
- Company size/stage indicators (funding, employee count if available)
- Key recent developments

#### Messaging Analysis
- Primary tagline or headline
- Core value proposition
- Key messaging themes (3-5)
- Tone and voice characterization
- How they describe the problem they solve

#### Product/Solution Positioning
- How they categorize their product
- Key features they emphasize
- Claimed differentiators
- Pricing approach (if publicly available)

#### Content Strategy
- Blog frequency and topics
- Content types produced (ebooks, webinars, case studies, tools)
- Social media presence and engagement approach
- Thought leadership themes
- SEO strategy observations (what terms they appear to target)

#### Strengths
- What they do well
- Where their messaging resonates
- Competitive advantages

#### Weaknesses
- Gaps in their messaging or positioning
- Areas where they are vulnerable
- Customer complaints or criticism themes (from reviews)

### 3. Messaging Comparison Matrix

| Dimension | Your Company | Competitor A | Competitor B |
|-----------|-------------|--------------|--------------|
| Primary tagline | ... | ... | ... |
| Target buyer | ... | ... | ... |
| Key differentiator | ... | ... | ... |
| Tone/voice | ... | ... | ... |
| Core value prop | ... | ... | ... |

(Include user's company only if they provided their positioning context)

### 4. Content Gap Analysis
- Topics your competitors cover that you do not (or vice versa)
- Content formats they use that you could adopt
- Keywords or themes they own vs. opportunities they have missed

### 5. Opportunities
- Positioning gaps you can exploit
- Messaging angles your competitors have not claimed
- Audience segments they are underserving
- Content or channel opportunities

### 6. Threats
- Areas where competitors are strong and you are vulnerable
- Trends that favor their positioning
- Recent moves that could shift the market

### 7. Recommended Actions
- 3-5 specific, actionable recommendations based on the analysis
- Quick wins (things you can act on this week)
- Strategic moves (longer-term positioning or content investments)

## Output

Present the full competitive brief with clear formatting. Note the date of the research so the user knows the freshness of the data.

After the brief, ask:

"Would you like me to:
- Create a battlecard for your sales team based on this analysis?
- Draft messaging that exploits the positioning gaps identified?
- Dive deeper into any specific competitor?
- Set up a competitive monitoring plan?"
