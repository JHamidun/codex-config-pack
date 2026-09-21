---
name: "write-spec"
description: "Write a feature spec or PRD from a problem statement or feature idea"
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


# Write Spec

> If you see unfamiliar placeholders or need to check which tools are connected, see the MCP registry: `${CODEX_PACK_ROOT}/library/config/mcp-servers.md`.

Write a feature specification or product requirements document (PRD).

## Usage

```
/write-spec $ARGUMENTS
```

## Workflow

### 1. Understand the Feature

Ask the user what they want to spec. Accept any of:
- A feature name ("SSO support")
- A problem statement ("Enterprise customers keep asking for centralized auth")
- A user request ("Users want to export their data as CSV")
- A vague idea ("We should do something about onboarding drop-off")

### 2. Gather Context

Ask the user for the following. Be conversational — do not dump all questions at once. Ask the most important ones first and fill in gaps as you go:

- **User problem**: What problem does this solve? Who experiences it?
- **Target users**: Which user segment(s) does this serve?
- **Success metrics**: How will we know this worked?
- **Constraints**: Technical constraints, timeline, regulatory requirements, dependencies
- **Prior art**: Has this been attempted before? Are there existing solutions?

### 3. Pull Context from Connected Tools

If **project tracker** is connected:
- Search for related tickets, epics, or features
- Pull in any existing requirements or acceptance criteria
- Identify dependencies on other work items

If **knowledge base** is connected:
- Search for related research documents, prior specs, or design docs
- Pull in relevant user research findings
- Find related meeting notes or decision records

If **design** is connected:
- Pull related mockups, wireframes, or design explorations
- Search for design system components relevant to the feature

If these tools are not connected, work entirely from what the user provides. Do not ask the user to connect tools — just proceed with available information.

### 4. Generate the PRD

Produce a structured PRD with these sections. See the **feature-spec** skill for detailed guidance on user stories, requirements categorization, acceptance criteria, and success metrics.

- **Problem Statement**: The user problem, who is affected, and impact of not solving it (2-3 sentences)
- **Goals**: 3-5 specific, measurable outcomes tied to user or business metrics
- **Non-Goals**: 3-5 things explicitly out of scope, with brief rationale for each
- **User Stories**: Standard format ("As a [user type], I want [capability] so that [benefit]"), grouped by persona
- **Requirements**: Categorized as Must-Have (P0), Nice-to-Have (P1), and Future Considerations (P2), each with acceptance criteria
- **Success Metrics**: Leading indicators (change quickly) and lagging indicators (change over time), with specific targets
- **Open Questions**: Unresolved questions tagged with who needs to answer (engineering, design, legal, data)
- **Timeline Considerations**: Hard deadlines, dependencies, and phasing

### 5. Review and Iterate

After generating the PRD:
- Ask the user if any sections need adjustment
- Offer to expand on specific sections
- Offer to create follow-up artifacts (design brief, engineering ticket breakdown, stakeholder pitch)

## Output Format

Use markdown with clear headers. Keep the document scannable — busy stakeholders should be able to read just the headers and bold text to get the gist.

## Optional Agent Delegation

For complex specs, consider delegating to specialized agents:
- **@business-analyst** — business goals, stakeholder analysis, ROI assessment
- **@system-analyst** — technical feasibility, dependencies, integration points
- **@product-designer** — UX flows, UI components, user experience considerations

## Tips

- Be opinionated about scope. It is better to have a tight, well-defined spec than an expansive vague one.
- If the user's idea is too big for one spec, suggest breaking it into phases and spec the first phase.
- Success metrics should be specific and measurable, not vague ("improve user experience").
- Non-goals are as important as goals. They prevent scope creep during implementation.
- Open questions should be genuinely open — do not include questions you can answer from context.
