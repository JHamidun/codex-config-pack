---
name: "performance-report"
description: "Build a marketing performance report with key metrics, trends, and optimization recommendations"
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


# Performance Report

> If you see unfamiliar placeholders or need to check which tools are connected, see the MCP registry: `${CODEX_PACK_ROOT}/library/config/mcp-servers.md`.

Generate a marketing performance report with key metrics, trend analysis, insights, and optimization recommendations.

## Trigger

User runs `/performance-report` or asks for a marketing report, performance analysis, campaign results, or metrics summary.

## Inputs

1. **Report type** — determine which type of report the user needs:
   - **Campaign report** — performance of a specific campaign
   - **Channel report** — performance across a specific channel (email, social, paid, SEO, etc.)
   - **Content performance** — how content pieces are performing
   - **Overall marketing report** — cross-channel summary (weekly, monthly, quarterly)
   - **Custom** — user-defined scope

2. **Time period** — the reporting window (last week, last month, last quarter, custom date range)

3. **Data source**:
   - If product analytics is connected: pull performance data automatically
   - If not connected: ask the user to provide metrics. Prompt with: "Please paste or share your performance data. I can work with spreadsheets, CSV data, dashboard screenshots described in text, or just the key numbers."

4. **Comparison period** (optional) — prior period or year-over-year for trend context

5. **Stakeholder audience** (optional) — who will read this report (executive summary style vs. detailed analyst view)

## Report Structure

### 1. Executive Summary
- 2-3 sentence overview of performance in the period
- Headline metric with trend direction (up/down/flat vs. prior period)
- One key win and one area of concern

### 2. Key Metrics Dashboard

Present core metrics in a summary table:

| Metric | This Period | Prior Period | Change | Target | Status |
|--------|------------|--------------|--------|--------|--------|

Status indicators:
- On track (meeting or exceeding target)
- At risk (below target but within acceptable range)
- Off track (significantly below target)

#### Metrics by Report Type

**Campaign Report:**
- Impressions and reach
- Click-through rate (CTR)
- Conversion rate
- Cost per acquisition (CPA)
- Return on ad spend (ROAS) or ROI
- Total conversions/signups/leads

**Channel Report (Email):**
- Emails sent, delivered, bounced
- Open rate
- Click-through rate
- Unsubscribe rate
- Conversion rate

**Channel Report (Social):**
- Impressions and reach
- Engagement rate (likes, comments, shares)
- Follower growth
- Click-through rate
- Top-performing posts

**Channel Report (Paid):**
- Spend
- Impressions and clicks
- CTR
- CPC and CPM
- Conversions and CPA
- ROAS

**Channel Report (SEO/Organic):**
- Organic sessions
- Keyword rankings (movement)
- Pages indexed
- Backlinks acquired
- Top-performing pages

**Content Performance:**
- Pageviews and unique visitors
- Time on page
- Bounce rate
- Social shares
- Conversions attributed to content
- Top and bottom performers

**Overall Marketing Report:**
- Total leads generated
- Marketing qualified leads (MQLs)
- Pipeline contribution
- Customer acquisition cost (CAC)
- Channel-by-channel summary

### 3. Trend Analysis
- Performance trend over the period (week-over-week or month-over-month)
- Notable inflection points and what caused them
- Seasonal or cyclical patterns observed
- Comparison to benchmarks or targets

### 4. What Worked
- Top 3-5 wins with specific data
- Why these performed well (hypothesis)
- How to replicate or scale

### 5. What Needs Improvement
- Bottom 3-5 performers with specific data
- Hypotheses for underperformance
- Recommended fixes

### 6. Insights and Observations
- Patterns in the data that are not obvious from the metrics alone
- Audience behavior insights
- Content or creative themes that resonated
- External factors that may have influenced performance (seasonality, news, competitive moves)

### 7. Recommendations
For each recommendation:
- What to do
- Why (linked to a specific insight from the data)
- Expected impact (high, medium, low)
- Effort to implement (high, medium, low)
- Priority (immediate, next sprint, next quarter)

Prioritize recommendations in a 2x2 matrix format:

| | Low Effort | High Effort |
|---|---|---|
| **High Impact** | Do first | Plan for next sprint |
| **Low Impact** | Do if time allows | Deprioritize |

### 8. Next Period Focus
- Top 3 priorities for the upcoming period
- Tests or experiments to run
- Targets for key metrics

## Output Formatting

- Use tables for data presentation
- Bold key numbers and trends
- Keep the executive summary concise (suitable for forwarding to leadership)
- Include a "detailed appendix" section for granular data if the user provided a lot of metrics

## After the Report

Ask: "Would you like me to:
- Create a slide-ready summary of these results?
- Draft a stakeholder email with the key takeaways?
- Dive deeper into any specific metric or channel?
- Set up a reporting template you can reuse next period?"
