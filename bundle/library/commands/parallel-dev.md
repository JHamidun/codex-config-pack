---
name: "parallel-dev"
description: "Параллельная разработка фичи используя git worktrees"
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


# Параллельная разработка: $ARGUMENTS

Создай 3 параллельные имплементации используя git worktrees:

## Фаза 1: Подготовка
1. Создай worktrees для каждого подхода:
   - `git worktree add ../feature-performance feature/$ARGUMENTS-performance`
   - `git worktree add ../feature-ux feature/$ARGUMENTS-ux`
   - `git worktree add ../feature-maintainable feature/$ARGUMENTS-maintainable`

## Фаза 2: Параллельная разработка
2. Назначь специализированных агентов:
   - @software-architect: Подход A (performance-focused) в worktree feature-performance
   - @frontend-dev: Подход B (UX-focused) в worktree feature-ux
   - @backend-dev: Подход C (maintainability-focused) в worktree feature-maintainable

3. Каждый агент работает независимо в своём worktree

## Фаза 3: Сравнение и выбор
4. Сравни результаты всех подходов:
   - Производительность (benchmarks)
   - User experience (простота использования)
   - Поддерживаемость кода (читаемость, тестирование)

5. Выбери лучший подход или объедини лучшие части

## Фаза 4: Очистка
6. Удали неиспользованные worktrees:
   - `git worktree remove ../feature-performance`
   - `git worktree remove ../feature-ux`
   - `git worktree remove ../feature-maintainable`

Каждый agent сохраняет результаты в `docs/features/$ARGUMENTS/[agent-name].md`
