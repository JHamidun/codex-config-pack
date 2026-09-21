---
name: "estimate"
description: "Оценка сложности и времени разработки фичи"
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


# ⏱️ Estimate: $ARGUMENTS

Оцени сложность и время для: **$ARGUMENTS**

## Process:

### 1. Feature Analysis
**Разбей на компоненты:**
- Frontend tasks
- Backend tasks
- Database changes
- API integrations
- Testing requirements
- Documentation

### 2. Complexity Assessment

**Оцени каждый компонент:**
- 🟢 Simple (1-2 часа)
- 🟡 Medium (0.5-1 день)
- 🟠 Complex (1-3 дня)
- 🔴 Very Complex (3+ дня)

**Факторы сложности:**
- Technical unknowns
- Dependencies
- Breaking changes
- Performance impact
- Security considerations

### 3. Estimation Breakdown

**По типам работ:**
```
📋 Requirements & Design: X hours
💻 Implementation: X hours
🧪 Testing: X hours
📝 Documentation: X hours
🔄 Code Review: X hours
---
Total: X hours (X days)
```

### 4. Risk Assessment

**Potential blockers:**
- [ ] Technical dependencies
- [ ] External API availability
- [ ] Database migration complexity
- [ ] Performance optimization needed
- [ ] Security review required

### 5. Resource Planning

**Recommended team:**
- Backend: X developers
- Frontend: X developers
- QA: X testers
- DevOps: X engineers

## Output Format:

```
⏱️ Оценка: $ARGUMENTS

**Сложность:** [Simple/Medium/Complex/Very Complex]

**Время разработки:** X days (Y hours)

**Разбивка:**
- Design: X hours
- Implementation: Y hours
- Testing: Z hours

**Риски:**
1. [Risk 1]
2. [Risk 2]

**Рекомендации:**
- [Recommendation 1]
- [Recommendation 2]

**Обновлено в Linear:** [Issue link]
```

## Examples:

```
/estimate Добавить WebSocket поддержку для real-time уведомлений
```

```
/estimate PROJ-123
```

```
/estimate Migration с SQLite на PostgreSQL
```

**Начинаю оценку! ⏱️**