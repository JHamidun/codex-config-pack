---
name: "proofread"
description: "AI корректура русского текста — 3-этапный пайплайн (орфография → пунктуация → типографика)"
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


# AI Корректура: $ARGUMENTS

## Пайплайн
Последовательно прогоняем текст через 3 субагента-корректора:

```
Исходный текст → [1. Орфография] → [2. Пунктуация] → [3. Типографика] → Результат
```

## Инструкция по выполнению

### Подготовка
1. Прочитай входной файл: `$ARGUMENTS`
2. Определи имя файла без расширения и расширение для формирования промежуточных файлов
3. Создай директорию для промежуточных результатов рядом с исходным файлом (если её нет)

### Этап 1: Орфография
Запусти субагент @proofreader-ortho:
- **Вход:** исходный файл `$ARGUMENTS`
- **Задача:** Прочитай файл `$ARGUMENTS`, выполни ТОЛЬКО орфографическую корректуру по своим правилам. Запиши результат в файл с суффиксом `_1_ortho` рядом с исходным файлом (например, `text_1_ortho.txt`).
- **Выход:** файл `*_1_ortho.*`

### Этап 2: Пунктуация
Запусти субагент @proofreader-punctuation:
- **Вход:** файл `*_1_ortho.*` (результат этапа 1)
- **Задача:** Прочитай файл с результатом этапа 1, выполни ТОЛЬКО пунктуационную корректуру по своим правилам. Не трогай орфографию — она уже проверена. Сохрани все теги `<err>`. Запиши результат в файл с суффиксом `_2_punct` (например, `text_2_punct.txt`).
- **Выход:** файл `*_2_punct.*`

### Этап 3: Типографика
Запусти субагент @proofreader-typography:
- **Вход:** файл `*_2_punct.*` (результат этапа 2)
- **Задача:** Прочитай файл с результатом этапа 2, выполни ТОЛЬКО типографическую корректуру по своим правилам. Не трогай орфографию и пунктуацию — они уже проверены. Сохрани все теги `<err>`. Запиши результат в файл с суффиксом `_final` (например, `text_final.txt`).
- **Выход:** файл `*_final.*`

### Завершение
После выполнения всех 3 этапов:
1. Покажи пользователю путь к финальному файлу
2. Покажи краткую сводку: сколько изменений на каждом этапе (если можно определить)
3. Если были найдены речевые ошибки (теги `<err>`), перечисли их списком

## Важно
- Каждый этап запускается ПОСЛЕДОВАТЕЛЬНО — результат предыдущего является входом следующего
- Субагенты НЕ должны выходить за рамки своей зоны ответственности
- Теги `<err comment="...">...</err>` должны сохраняться на протяжении всего пайплайна
- Промежуточные файлы сохраняются для возможности ревью каждого этапа
