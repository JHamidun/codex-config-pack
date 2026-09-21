---
name: hamidun-pack
description: "Search the portable Hamidun workflow catalog for development, research, writing, media, design, integrations, and agent roles. Load one recipe on demand; report unadapted runtime dependencies."
---

# Hamidun Codex pack

Pack root: `${CODEX_PACK_ROOT}`

Search metadata only:

```text
python "${CODEX_PACK_ROOT}/scripts/catalog.py" "task keywords"
```

Read `${CODEX_PACK_ROOT}/CORE.md` and only the selected recipe plus needed references.
Do not read the full catalog or all recipes into the conversation.
`requires-runtime-review` entries are NOT working script/connector integrations.
Never execute `.source` files or run legacy source-default commands. Resolve native tools first.
`instructions-adapted` means structural conversion, not an end-to-end workflow test.
Optional custom agents have the `pack-` prefix; they inherit the current model and permissions,
except explicitly read-only reviewers. Claude commands are recipes, not installed slash commands.
