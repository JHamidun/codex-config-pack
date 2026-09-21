---
name: "reddit-hn"
description: "Поиск мнений и обсуждений по технологиям в Reddit и Hacker News. Триггеры: «что пишут на реддите», «мнения разработчиков», «обсуждают ли X»."
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


# Reddit & Hacker News Research

Search developer communities for opinions, trends, and discussions.

## Sources

### Reddit
Use WebSearch with site filter:
```
WebSearch: "site:reddit.com [topic] [year]"
```

Key subreddits:
- r/programming, r/webdev, r/javascript, r/python
- r/devops, r/sysadmin, r/selfhosted
- r/MachineLearning, r/artificial
- r/startups, r/SaaS, r/Entrepreneur

### Hacker News
Use Algolia HN Search API:
```
WebFetch: https://hn.algolia.com/api/v1/search?query=[topic]&tags=story
Prompt: "Extract top discussions about [topic] with scores and comment counts"
```

Or via WebSearch:
```
WebSearch: "site:news.ycombinator.com [topic]"
```

## Research Templates

### Technology Comparison
```
1. Search: "[tech A] vs [tech B] site:reddit.com 2025 2026"
2. Search HN: same query
3. Aggregate: pros/cons from community
4. Output: balanced comparison with sources
```

### Problem/Bug Research
```
1. Search: "[error message] site:reddit.com"
2. Search: "[error message] site:news.ycombinator.com"
3. Search: "[error message] site:stackoverflow.com"
4. Synthesize solutions
```

### Trend Analysis
```
1. Search: "[technology] site:reddit.com" (sort by relevance)
2. HN API: tags=story, sorted by points
3. Analyze sentiment over time
4. Report: trending up/down/stable
```

## Output Format

```markdown
# Community Research: [topic]

## Summary
[2-3 sentence overview of community sentiment]

## Key Opinions

### Positive
- [opinion + source link]

### Negative/Concerns
- [concern + source link]

### Neutral/Nuanced
- [balanced view + source link]

## Recommendations
[Based on community consensus]

## Sources
- [links to discussions]
```

## Notes
- Always include source links
- Distinguish between popular opinion and expert opinion
- Note recency of discussions (old opinions may be outdated)
- Reddit/HN can be biased — note potential biases
