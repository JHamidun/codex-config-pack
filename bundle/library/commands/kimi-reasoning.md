---
name: "kimi-reasoning"
description: "Глубокий reasoning через Kimi K2 (k2-thinking): алгоритмы, трудные баги, архитектура, математика. Триггеры: «спроси kimi». Агент-обёртка → kimi-algorithm-specialist."
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


# /kimi-reasoning - Глубокий анализ с Kimi K2

**Назначение:** Используй Kimi K2 (k2-thinking модель) для глубокого reasoning и анализа сложных проблем.

**Когда использовать:**
- Сложные алгоритмические задачи
- Debugging трудных багов
- Архитектурные решения
- Математические задачи
- Code optimization стратегии

**Аргументы:**
- `problem` - описание проблемы или задачи (обязательно)

**Пример использования:**
```
/kimi-reasoning Why is my async function deadlocking in Python?
/kimi-reasoning Optimal data structure for real-time chat with 1M users
/kimi-reasoning Best approach to migrate from SQLite to PostgreSQL with zero downtime
```

---

## Задача для агента

Ты используешь **Kimi K2** (k2-thinking модель) - специализированную модель для reasoning с **1 trillion параметров** (MoE архитектура, 32B активных).

**Преимущества Kimi K2:**
- 🎯 Top results на coding benchmarks (SWE-bench: 65.8%, LiveCodeBench: 53.7%)
- 🧠 128K контекстное окно
- 💡 Отлично для: coding, debugging, test generation, math reasoning
- 💰 ~10x дешевле чем GPT-4 для coding tasks

**Шаги:**

1. **Получи problem** из аргументов команды
2. **Сформируй запрос** к Kimi K2 API (OpenAI-compatible):
   ```python
   import os
   from openai import OpenAI

   client = OpenAI(
       api_key=os.getenv('KIMI_API_KEY'),
       base_url='https://api.moonshot.ai/v1'
   )

   response = client.chat.completions.create(
       model='kimi-k2-thinking',  # Включает chain-of-thought reasoning
       messages=[
           {
               'role': 'system',
               'content': 'Ты expert в reasoning и problem-solving. Используй step-by-step анализ для решения сложных проблем.'
           },
           {
               'role': 'user',
               'content': problem
           }
       ],
       temperature=0.7,
       max_tokens=8000
   )

   answer = response.choices[0].message.content
   ```

3. **Верни детальный анализ** в формате:
   ```markdown
   ## 🧠 Kimi K2 Reasoning: {problem title}

   ### Анализ проблемы:
   {step-by-step breakdown}

   ### Рассуждение:
   {reasoning process}

   ### Решение:
   {proposed solution with code examples if applicable}

   ### Альтернативы:
   {other approaches to consider}

   ### Рекомендации:
   {best practices and next steps}
   ```

**ВАЖНО:**
- Используй chain-of-thought reasoning
- Покажи промежуточные шаги
- Объясни "почему", а не только "как"