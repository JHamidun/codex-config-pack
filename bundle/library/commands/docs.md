---
name: "docs"
description: "Генерация документации из кода с примерами"
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


# 📖 Documentation: $ARGUMENTS

Создай документацию для: **$ARGUMENTS**

## Process:

### 1. Code Analysis
- Читай код и комментарии
- Определи API endpoints, функции, классы
- Найди примеры использования

### 2. Generate Docs
**Для API:**
- API Reference (endpoints, methods, parameters)
- Request/Response examples
- Authentication requirements
- Error codes и descriptions

**Для Modules/Classes:**
- Purpose и overview
- Public API
- Constructor/initialization
- Methods с параметрами
- Usage examples

### 3. Format Output

**Выбери формат:**
- **Markdown** для README
- **.docx** для formal specifications — `python-docx`, готовый пример: `skills/seo-machine-ru/scripts/build_report_docx.py`
- **api-documentation skill** для OpenAPI/Swagger
- **Notion** для team wiki (если Notion MCP настроен)

### 4. Include Examples

```python
# Example usage
from mymodule import MyClass

client = MyClass(api_key="...")
result = client.do_something(param="value")
print(result)
```

```javascript
// Example usage
const client = new MyClass({ apiKey: '...' });
const result = await client.doSomething({ param: 'value' });
console.log(result);
```

```bash
# CLI example
mycli command --param value
```

## Output:

1. **Documentation file(s)** в выбранном формате
2. **Code comments** improvements (если нужно)
3. **README updates** (если есть)
4. **API spec** (OpenAPI/Swagger если API)

## Examples:

```
/docs ./backend/api/main.py
/docs ./telegram-bot/handlers/
/docs ./frontend/src/components/UserProfile.tsx
```

**Создаю документацию! 📖**
