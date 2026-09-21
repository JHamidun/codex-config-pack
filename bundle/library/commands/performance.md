---
name: "performance"
description: "Профилирование КОДА: cProfile, memory_profiler, node --prof, SQL/N+1. Триггеры: «медленный код»."
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


# Performance Analysis & Optimization

**Аргументы:** $ARGUMENTS (путь к файлу/модулю или тип анализа: cpu/memory/io/all)

## Задача

Проанализируй производительность и предложи оптимизации.

## Типы анализа

### 1. CPU Profiling

**Python:**
```python
import cProfile
import pstats

# Профилирование функции
cProfile.run('function_to_profile()', 'output.prof')

# Анализ результатов
stats = pstats.Stats('output.prof')
stats.sort_stats('cumulative')
stats.print_stats(20)
```

**Node.js:**
```bash
node --prof app.js
node --prof-process isolate-*.log > processed.txt
```

### 2. Memory Analysis

**Python:**
```python
from memory_profiler import profile

@profile
def memory_hungry_function():
    pass
```

**Node.js:**
```bash
node --inspect app.js
# Открыть chrome://inspect
```

### 3. Database Queries

```sql
-- PostgreSQL slow queries
SELECT query, calls, mean_time, total_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 20;
```

### 4. Code Review для производительности

Ищи:
- **N+1 queries** - циклы с запросами к БД
- **Неиспользуемые импорты** - лишний overhead
- **Синхронный I/O** - блокирующие операции
- **Большие объекты в памяти** - утечки
- **Отсутствие кэширования** - повторные вычисления

## Формат отчёта

```markdown
# Performance Report

## Bottlenecks найдены

| Место | Проблема | Impact | Fix |
|-------|----------|--------|-----|
| file.py:42 | N+1 query | High | Use prefetch_related |

## Метрики

- Response time: X ms → target Y ms
- Memory usage: X MB → target Y MB
- CPU usage: X% → target Y%

## Рекомендации по приоритету

1. [Critical] ...
2. [High] ...
3. [Medium] ...
```

## Инструменты

- **Python:** cProfile, memory_profiler, line_profiler, py-spy
- **Node.js:** clinic, 0x, node --prof
- **General:** Sentry performance, New Relic
