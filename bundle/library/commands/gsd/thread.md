---
name: "gsd:thread"
description: "Manage persistent context threads for cross-session work"
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


<objective>
Create, list, or resume persistent context threads. Threads are lightweight
cross-session knowledge stores for work that spans multiple sessions but
doesn't belong to any specific phase.
</objective>

<process>

**Parse $ARGUMENTS to determine mode:**

<mode_list>
**If no arguments or $ARGUMENTS is empty:**

List all threads:
```bash
ls .planning/threads/*.md 2>/dev/null
```

For each thread, read the first few lines to show title and status:
```
## Active Threads

| Thread | Status | Last Updated |
|--------|--------|-------------|
| fix-task-1 | OPEN | 2026-03-15 |
| task-2 | RESOLVED | 2026-03-12 |
| task-3 | IN PROGRESS | 2026-03-17 |
```

If no threads exist, show:
```
No threads found. Create one with: /gsd:thread <description>
```
</mode_list>

<mode_resume>
**If $ARGUMENTS matches an existing thread name (file exists):**

Resume the thread — load its context into the current session:
```bash
cat ".planning/threads/${THREAD_NAME}.md"
```

Display the thread content and ask what the user wants to work on next.
Update the thread's status to `IN PROGRESS` if it was `OPEN`.
</mode_resume>

<mode_create>
**If $ARGUMENTS is a new description (no matching thread file):**

Create a new thread:

1. Generate slug from description:
   ```bash
   SLUG=$(node "${CODEX_PACK_ROOT}/library/get-shit-done/bin/gsd-tools.cjs" generate-slug "$ARGUMENTS")
   ```

2. Create the threads directory if needed:
   ```bash
   mkdir -p .planning/threads
   ```

3. Write the thread file:
   ```bash
   cat > ".planning/threads/${SLUG}.md" << 'EOF'
   # Thread: {description}

   ## Status: OPEN

   ## Goal

   {description}

   ## Context

   *Created from conversation on {today's date}.*

   ## References

   - *(add links, file paths, or issue numbers)*

   ## Next Steps

   - *(what the next session should do first)*
   EOF
   ```

4. If there's relevant context in the current conversation (code snippets,
   error messages, investigation results), extract and add it to the Context
   section.

5. Commit:
   ```bash
   node "${CODEX_PACK_ROOT}/library/get-shit-done/bin/gsd-tools.cjs" commit "docs: create thread — ${ARGUMENTS}" --files ".planning/threads/${SLUG}.md"
   ```

6. Report:
   ```
   ## 🧵 Thread Created

   Thread: {slug}
   File: .planning/threads/{slug}.md

   Resume anytime with: /gsd:thread {slug}
   ```
</mode_create>

</process>

<notes>
- Threads are NOT phase-scoped — they exist independently of the roadmap
- Lighter weight than /gsd:pause-work — no phase state, no plan context
- The value is in Context and Next Steps — a cold-start session can pick up immediately
- Threads can be promoted to phases or backlog items when they mature:
  /gsd:add-phase or /gsd:add-backlog with context from the thread
- Thread files live in .planning/threads/ — no collision with phases or other GSD structures
</notes>
