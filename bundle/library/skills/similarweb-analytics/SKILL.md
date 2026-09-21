---
name: "similarweb-analytics"
description: "Трафик чужого сайта по публичным данным SimilarWeb: посещаемость, источники. Триггеры: «сколько людей на сайте конкурента»."
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


# SimilarWeb Analytics

Estimate someone else's website traffic from public sources. Research workflow, not a
tool: there is no script here and no API key to add — see "Why there is no script".

## Read this before reporting a single number

**A missing number is not a zero.** Every source below can fail to answer: the public
page is behind a bot wall, the estimate is hidden behind a paid plan, the site is too
small to be measured at all. In all three cases you get nothing back — and "nothing"
must be reported as *not measured*, with the reason, never as "no traffic" or `0`.

Three ways this goes wrong, in order of how often:

| What you see | What it actually means | What to write |
|---|---|---|
| Fetch returns 403 / a challenge page / an empty shell | The source blocked the request | "Не удалось получить: SimilarWeb отдал блокировку. Цифры нет." |
| A field is blank or `null` | Not published on the free tier | "Метрика закрыта бесплатным тарифом." |
| SimilarWeb has no data for the domain | Below the measurement floor (roughly <50K visits/mo) | "Сайт ниже порога измерения SimilarWeb — не значит, что трафика нет." |

**Every figure carries its source and its date.** SimilarWeb estimates lag 1-2 months
and are modelled, not counted — two independent sources for the same domain routinely
disagree by a factor. Report a range and say whose estimate it is; a single confident
number here is the tell that the number was made up.

Own site → the site's own analytics (Метрика / GA4), not this skill. That is measured
data, this is a guess about a competitor.

## Why there is no script

There used to be `scripts/similarweb.py`. It looked like a data tool and was not: it
built a JSON object where `total_visits`, `bounce_rate`, `global_rank` and every other
metric were hard-coded `None`, fetched the page, and never assigned a single value. The
output — `"total_visits": null` — reads exactly like the "no traffic" answer this skill
exists to prevent. Removed, not fixed: there is nothing to fix, the workflow below is
the whole skill.

## Workflow

### Step 1 — search before fetching

Search engines index SimilarWeb pages and the many articles quoting them, and search
does not hit the bot wall. This is the cheapest source and usually the only one that
answers.

```text
WebSearch: similarweb <domain> traffic <year>
WebSearch: <domain> monthly visitors estimate
WebSearch: <domain> vs <competitor> traffic
```

Pull from results: monthly visits, trend direction, rank, and the *date* each figure
refers to.

### Step 2 — try the public page

```text
WebFetch: https://www.similarweb.com/website/<domain>/
```

Expect this to fail more often than it works — the page is bot-protected. Failure is a
normal outcome, not a bug to retry around: fall back to step 1 or step 3 and say so in
the report.

### Step 3 — cross-check with a second source

Never build a conclusion on one estimator. Free tiers that answer without an account:

| Source | What it gives | Catch |
|---|---|---|
| Semrush (free) | domain overview, traffic estimate | few queries/day without an account |
| Ahrefs Website "Authority Checker" / free tools | backlinks, organic keywords | traffic itself mostly gated |
| Google Trends | relative search interest over time | relative only, no absolute numbers |
| Similar sites lists (SimilarWeb, Semrush) | who the competitors are | quality varies |
| BuiltWith / Wappalyzer | tech stack, not traffic | answers "what they run", not "how many" |

If two sources disagree by more than ~2×, say so in the report instead of picking the
prettier number.

### Step 4 — write it up

- Executive summary: the one thing the reader should do differently.
- Traffic: range + trend + as-of date + whose estimate.
- Source mix (see the table below) — where their demand actually comes from.
- Geography: top countries with shares.
- Competitive position: relative, not absolute.
- **Confidence line:** which figures are estimates, which are missing, and why.

## Core metrics

| Metric | Description |
|---|---|
| Total visits | Monthly traffic estimate (modelled) |
| Unique visitors | Deduplicated visitor count |
| Bounce rate | % single-page sessions |
| Pages per visit | Average depth |
| Avg visit duration | Time on site |
| Global rank | Worldwide ranking |
| Country rank | Country-specific ranking |

## Traffic sources

| Channel | Description | What a high share tells you |
|---|---|---|
| Direct | Type-in / untagged | Brand demand — or bad tagging on their side |
| Organic search | SEO | Content engine works; check which keywords |
| Paid search | PPC | They are buying demand — budget exists |
| Social | Social referrals | Audience lives on a platform; find which |
| Referral | Links from other sites | Partnerships, PR, marketplaces |
| Display | Banner ads | Paid reach, usually top-funnel |
| Email | Email marketing | They own a list — the strongest signal of retention |

The mix matters more than the total: two sites with identical visits and opposite mixes
are different businesses.

## Limitations

- No API. Everything here is public data and search results.
- Estimates are modelled, lag 1-2 months, and differ between providers.
- Sites under roughly 50K visits/month are usually not measured at all.
- The public page is bot-protected; fetching it is best-effort by design.
- Subdomains and country domains are counted separately — check which one you measured.
