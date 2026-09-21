---
name: "security-scan"
description: "Security-аудит проекта: секреты в коде, pip/npm audit, OWASP Top 10, конфигурация DEBUG/CORS. Триггеры: «аудит безопасности», «проверь на уязвимости»."
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


# Комплексный Security Audit

**Аргументы:** $ARGUMENTS (путь к проекту или пусто для текущей директории)

## Задача

Проведи комплексный security audit проекта по всем направлениям.

## Чеклист проверки

### 1. Секреты в коде
```bash
# Поиск потенциальных секретов
grep -rn --include="*.py" --include="*.js" --include="*.ts" --include="*.env*" \
  -E "(api_key|apikey|secret|password|token|credential|auth).*=" . 2>/dev/null | head -50

# Проверка .gitignore
cat .gitignore 2>/dev/null | grep -E "(\.env|secret|credential|key)"
```

### 2. Уязвимости зависимостей

**Python:**
```bash
pip audit 2>/dev/null || echo "pip-audit not installed"
safety check 2>/dev/null || echo "safety not installed"
```

**Node.js:**
```bash
npm audit 2>/dev/null || echo "Not a Node.js project"
```

### 3. OWASP Top 10 проверка

Проверь код на:
- **Injection** (SQL, Command, XSS)
- **Broken Authentication**
- **Sensitive Data Exposure**
- **Security Misconfiguration**
- **Insecure Deserialization**

### 4. Конфигурация

- DEBUG режим выключен?
- HTTPS enforced?
- CORS правильно настроен?
- Rate limiting есть?

## Формат отчёта

```markdown
# Security Audit Report

**Дата:** [дата]
**Проект:** [название]

## Критические (требуют немедленного исправления)
- [ ] Issue 1

## Высокий риск
- [ ] Issue 2

## Средний риск
- [ ] Issue 3

## Рекомендации
- Recommendation 1
```

## После аудита

Предложи конкретные fixes для найденных проблем.
