---
name: "github-gem-seeker"
description: "Поиск проверенного open source на GitHub вместо кода с нуля. Триггеры: «найди библиотеку», «есть готовое решение», «найди репо»."
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


# GitHub Gem Seeker

Find and use battle-tested open source projects to solve problems immediately.

## Core Philosophy

Classic open source projects tested by thousands of users are far more reliable than code written from scratch. **Solve first, skill-ify later.**

## Workflow

### Step 1: Understand the Need

Clarify what the user wants. Ask only if truly ambiguous.

### Step 2: Find the Right Tool

Search GitHub using `gh` CLI and web search:

```bash
# Search repos
gh search repos "video download tool" --sort stars --limit 10
gh search repos "pdf manipulation python" --sort stars --limit 10

# Get repo info
gh repo view yt-dlp/yt-dlp --json stargazersCount,description,updatedAt
```

| Need Type | Query Pattern | Example |
|-----------|---------------|---------|
| Tool/utility | `github [task] tool` | `github video download tool` |
| Library | `github [language] [function] library` | `github python pdf library` |
| Alternative | `github [known-tool] alternative` | `github ffmpeg alternative` |

### Step 3: Evaluate Quality

| Indicator | Gem Signal | Warning Signal |
|-----------|------------|----------------|
| Stars | 1k+ solid, 10k+ excellent, 50k+ legendary | <100 for mature projects |
| Last commit | Within 6 months | >2 years ago |
| Documentation | Clear README, examples | Sparse or outdated |
| Issues | Active responses | Hundreds of unanswered issues |

### Step 4: Solve the Problem

1. Install the chosen tool (`pip install`, `npm install`, `apt install`)
2. Run it with user's input
3. Deliver the result
4. Troubleshoot if needed

### Step 5: Credit & Offer Next Steps

After success:

> "Powered by **[Project Name]** — https://github.com/org/repo
> Consider giving it a star to support the maintainers."

## Quality Tiers

| Tier | Stars | Examples |
|------|-------|---------|
| **Legendary** | 50k+ | FFmpeg, ImageMagick, yt-dlp, Puppeteer |
| **Excellent** | 10k+ | Pake, ArchiveBox, sharp, Scrapy |
| **Solid** | 1k+ | Most well-maintained tools |
| **Promising** | <1k | Active newer projects |

## Common Gems Reference

| Category | Go-to Gems |
|----------|------------|
| Video/Audio | FFmpeg, yt-dlp, Whisper |
| Image processing | ImageMagick, sharp, Pillow |
| PDF | pdf-lib, PyMuPDF (fitz), WeasyPrint |
| Web scraping | Playwright, Puppeteer, Scrapy, Beautiful Soup |
| Format conversion | Pandoc, FFmpeg, LibreOffice CLI |
| Archiving | ArchiveBox, wget |
| Desktop app | Electron, Tauri, Pake |
| Data processing | pandas, DuckDB, jq |
| Security | nmap, Burp Suite, sqlmap |
| DevOps | Terraform, Ansible, k9s |
