---
name: hamidun-pack
description: "Use the portable Hamidun workflows for development, research, writing, media and design requests, including Russian prompts. Select one matching recipe and execute its reviewed Codex procedure; distinguish unavailable integrations."
---

# Hamidun Codex pack

Pack root: `${CODEX_PACK_ROOT}`

Search metadata only:

```text
python "${CODEX_PACK_ROOT}/scripts/catalog.py" "task keywords"
```

Search using the user's actual task keywords. Prefer an exact workflow name when
provided. Inspect the few highest-ranked descriptions; keyword ranking alone does
not establish intent. Ask only when the remaining ambiguity matters to execution.

Prepare the selected catalog ID:

```text
python "${CODEX_PACK_ROOT}/scripts/catalog.py" --prepare "<catalog-id>"
```

Read `${CODEX_PACK_ROOT}/CORE.md` and the prepared instructions, then carry out the
requested task with available Codex tools. `--prepare` does not itself perform the
user task. Do not stop at printing the catalog entry or ask the user to run Python.
For `native-helper`, run the reviewed helper exactly as the prepared recipe says,
using task-specific inputs and an explicit workspace. Verify the actual result.
For `instructions`, use native tools and the selected domain guidance.
For `native-procedure`, execute the prepared procedure and selected operation. Read
its historical domain reference only for methodology/templates, never as a tool API.
Use `catalog.py --read-reference "<pack-relative-path>" --workspace "<workspace>"`
to verify and resolve a needed reference. Workspace context is private and belongs
under the selected project's `.codex-context/`, never in the installed library.
For `needs-adapter`, report the concrete missing adapter; do not claim completion.
For `connection-required`, follow the selected connection procedure with its exact
service and required action. A definition or installed package is not proof of live
access; verify the actual capability before the operation. Never fake a provider call.
If preparation fails, stop and repair installation integrity instead of executing
an unverified historical fallback. Read only the selected recipe and needed references.
Do not read the full catalog or all recipes into the conversation.
Historical `requires-runtime-review` flags describe preserved source, not the native
replacement. Follow `execution` and its explicit verification/dependency contract.
Never execute `.source` files or run legacy source-default commands. Resolve native tools first.
`instructions-adapted` means structural conversion, not an end-to-end workflow test.
Optional custom agents have the `pack-` prefix; they inherit the current model and permissions,
except explicitly read-only reviewers. Claude commands are recipes, not installed slash commands.
