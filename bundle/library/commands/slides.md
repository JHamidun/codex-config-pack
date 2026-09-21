---
name: "slides"
description: "Презентация из темы через Manus Slides: 24 AI-стиля, экспорт PPTX/PDF/HTML. Триггеры: «сделай слайды», «в стиле Manus». НЕ skill slides (ручные HTML-деки)."
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


Create a professional slide presentation using the Manus Slides pipeline.

## Instructions

Read the skill `${CODEX_PACK_ROOT}/library/skills/manus-slides/SKILL.md` for full reference.

### Mode Detection

- If $ARGUMENTS contains "html" or "editable" → **HTML Mode**
- If $ARGUMENTS starts with "edit" → **Edit Mode**
- Default → **AI Mode** (best visual quality, 24 styles)

### AI Mode (Default, Recommended)

1. **Analyze the topic** — Determine audience, goal, key messages
2. **Recommend style** — Run:
   ```bash
   python ${CODEX_PACK_ROOT}/library/skills/manus-slides/scripts/whiteboard_generator.py recommend "$ARGUMENTS"
   ```
   Present top 3-5 styles to the user. Let them choose or accept default.
3. **Research** — If user provides docs/files, read them first
4. **Generate outline** — Plan 8-12 slides with titles and content summaries
5. **Write prompts** — For each slide, create a content prompt adapted to chosen style:
   ```text
   TITLE in large bold text: "Заголовок"
   SUBTITLE: "Подзаголовок"
   [Layout: diagrams, icons, lists, charts]
   At the bottom: "Ключевой вывод"
   ```
6. **Create config** — Write `slides.json`:
   ```json
   {
     "title": "Title",
     "style": "whiteboard",
     "slides": [
       {"id": "slide_01", "prompt": "TITLE: ..."},
       {"id": "slide_02", "prompt": "TITLE: ..."}
     ]
   }
   ```
7. **Generate** — Run:
   ```bash
   python ${CODEX_PACK_ROOT}/library/skills/manus-slides/scripts/whiteboard_generator.py generate slides.json ./generated
   ```
8. **Review** — Check each generated image, note any that need fixes
9. **Deliver** — PPTX and HTML preview are auto-created alongside the images

### HTML Mode (If Requested)

1. **Analyze** → 2. **Outline as JSON** → 3. **Confirm with user**
4. **Init project:**
   ```bash
   python ${CODEX_PACK_ROOT}/library/skills/manus-slides/scripts/slide_manager.py init "<title>" outline.json ./<project-dir>
   ```
5. **For each slide** — Generate HTML using templates:
   ```bash
   python ${CODEX_PACK_ROOT}/library/skills/manus-slides/scripts/slide_templates.py get <template_key> '<data_json>'
   ```
6. **Export:**
   ```bash
   python ${CODEX_PACK_ROOT}/library/skills/manus-slides/scripts/slide_export.py html ./<project-dir> ./presentation.html
   ```

### Edit Mode

If $ARGUMENTS starts with "edit", extract the project directory and modify existing slides.

### AI Styles (24 available)

**Manus Originals:** vinyl, whiteboard, grove, fresco, easel, diorama, chromatic
**Manus Hybrid:** sketch, glamour, amber, arctic, neon, patina, onyx
**Bonus:** chalkboard, notebook, blueprint, glassmorphism, corporate, dark-tech, dashboard, infographic, watercolor, minimal-clean

| Task | Recommended Styles |
|:--|:--|
| Pitch deck, investors | vinyl, chromatic, onyx |
| Business, strategy | whiteboard, corporate, dashboard |
| Education, training | chalkboard, sketch, whiteboard |
| Tech, engineering | blueprint, dark-tech, chromatic |
| Creative, design | easel, watercolor, glassmorphism |
| Data, analytics | dashboard, infographic, arctic |
| Luxury, premium | glamour, onyx, fresco |

Default style: `whiteboard`

### HTML-Only Styles (13)

If user asks for: cerulean, cobalt, emerald, basalt, mist, sand, linen, alabaster, quartz, mahogany, ginkgo, sunset, lavender — switch to HTML Mode automatically.

Topic: $ARGUMENTS
