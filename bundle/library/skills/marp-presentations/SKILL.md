---
name: "marp-presentations"
description: "Marp: Markdown → слайды (HTML/PDF/PPTX) через npx marp-cli, бесплатная альтернатива Gamma. Триггеры: «слайды из markdown», «marp»."
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


# Marp — Markdown Presentations

> Use when: "презентация", "слайды из markdown", "marp", "slides from markdown"
> Free alternative to Gamma. Markdown → PDF/PPTX/HTML slides.

## Overview

Marp converts Markdown files into professional presentations.
Output formats: HTML, PDF, PPTX, PNG, JPEG.

## Installation

```bash
# CLI (one-shot via npx, no install needed)
npx @marp-team/marp-cli slide.md --pdf

# Or install globally
npm install -g @marp-team/marp-cli

# VSCode extension (recommended for preview)
# Install: "Marp for VS Code" (marp-team.marp-vscode)
```

## Slide Syntax

```markdown
---
marp: true
theme: default
paginate: true
header: "Company Name"
footer: "2026"
style: |
  section {
    font-family: 'Arial', sans-serif;
  }
  h1 {
    color: #2563eb;
  }
---

# Slide 1 Title

Content for first slide

---

# Slide 2 Title

- Bullet point 1
- Bullet point 2
- Bullet point 3

![bg right:40%](image.png)

---

<!-- _class: lead -->

# Big centered text

Subtitle underneath

---

# Code Example

```python
def hello():
    print("Hello from Marp!")
```

---

# Two Columns

<div style="display: flex; gap: 2rem;">
<div>

**Left column**
- Point A
- Point B

</div>
<div>

**Right column**
- Point C
- Point D

</div>
</div>
```

## Built-in Themes

| Theme | Style |
|-------|-------|
| `default` | Clean, professional |
| `gaia` | Bold, colorful |
| `uncover` | Minimalist |

## Key Directives

```markdown
<!-- _class: lead -->        <!-- Centered large text -->
<!-- _class: invert -->      <!-- Dark background -->
<!-- _backgroundColor: #1a1a2e -->  <!-- Custom bg -->
<!-- _color: white -->       <!-- Text color -->
<!-- _paginate: false -->    <!-- Hide page number -->
<!-- _header: "" -->         <!-- Remove header for this slide -->
```

## Background Images

```markdown
![bg](image.jpg)             <!-- Full background -->
![bg right:40%](photo.jpg)   <!-- Split layout -->
![bg left:50%](chart.png)    <!-- Left split -->
![bg contain](diagram.svg)   <!-- Fit to slide -->
![bg blur:5px](photo.jpg)    <!-- Blurred background -->
![bg opacity:0.3](bg.jpg)    <!-- Semi-transparent -->
```

## CLI Commands

```bash
# Markdown → PDF
npx @marp-team/marp-cli slides.md --pdf

# Markdown → PPTX
npx @marp-team/marp-cli slides.md --pptx

# Markdown → HTML (single file)
npx @marp-team/marp-cli slides.md --html

# Markdown → PNG images (one per slide)
npx @marp-team/marp-cli slides.md --images png

# Watch mode (auto-rebuild on save)
npx @marp-team/marp-cli slides.md --pdf --watch

# Custom theme
npx @marp-team/marp-cli slides.md --pdf --theme ./custom-theme.css

# Server mode (preview in browser)
npx @marp-team/marp-cli slides.md --server --watch
```

## Workflow: Research → Presentation

```bash
# 1. Claude generates markdown with slide content
# 2. Save as slides.md with Marp frontmatter
# 3. Convert to desired format

# For PDF (best for sharing):
npx @marp-team/marp-cli slides.md --pdf --allow-local-files

# For PPTX (if client needs editable):
npx @marp-team/marp-cli slides.md --pptx

# For HTML (for web hosting):
npx @marp-team/marp-cli slides.md --html
```

## Custom Theme Example

```css
/* custom-theme.css */
@import 'default';

section {
  background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
  color: #e0e0e0;
  font-family: 'Inter', sans-serif;
}

h1 {
  color: #7c3aed;
  border-bottom: 2px solid #7c3aed;
  padding-bottom: 0.3em;
}

h2 {
  color: #a78bfa;
}

code {
  background: rgba(124, 58, 237, 0.2);
  color: #c4b5fd;
}
```

## Dependencies

- Node.js v18+ (for npx)
- Chrome/Chromium (for PDF export, auto-detected)

## Notes

- Marp is 100% free and open-source
- VSCode extension gives live preview while editing
- `---` separates slides (standard Markdown horizontal rule)
- Supports math via KaTeX: `$E = mc^2$`
- Supports emoji: `:rocket:` → 🚀
