---
name: "context-optimize"
description: "Сборка контекста под задачу (bug fix/feature/review): источники, few-shot, компрессия. Триггеры: «собери контекст», «оптимизируй контекст». Методология → context-engineering."
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


Оптимизируй контекст для текущей задачи используя Context Engineering принципы.

## Что делает эта команда:

1. **Анализирует тип задачи**:
   - Bug fix → Загружает error logs, git blame, related tests
   - New feature → Загружает requirements, architecture, similar code
   - Code review → Загружает git history, test coverage, review examples
   - Refactoring → Загружает dependency graph, code metrics, tests
   - Testing → Загружает edge cases, test examples, requirements

2. **Собирает релевантный контекст** из multiple sources:
   - CLAUDE.md (project instructions)
   - Memory MCP (previous context)
   - Linear MCP (tasks)
   - GitHub MCP (code history)
   - Sentry MCP (errors)
   - Filesystem MCP (codebase)

3. **Оптимизирует token usage**:
   - Prioritizes by relevance
   - Truncates long sources
   - Applies compression
   - Removes duplicates

4. **Добавляет few-shot examples** для улучшения результатов

## Пример использования:

```bash
# Bug fix
/context-optimize bug_fix "NoneType error in auth.py"

# New feature
/context-optimize new_feature "Add OAuth2 authentication"

# Code review
/context-optimize code_review "Review Your Project security"
```

## Output:

Возвращает JSON с оптимизированным контекстом:
- Релевантные источники данных
- Few-shot примеры
- Token usage stats
- Примененные оптимизации

## Принципы:

**Context Engineering > Prompt Engineering**
- Правильный контекст важнее clever prompts
- Меньше токенов, больше качества
- Dynamic assembly from multiple sources
- Relevance filtering

**Based on:**
- [LangChain Context Engineering](https://blog.langchain.com/the-rise-of-context-engineering/)
- [12 Factor Agents](https://github.com/humanlayer/12-factor-agents)
- [Anthropic MCP Best Practices](https://www.anthropic.com/engineering/writing-tools-for-agents)