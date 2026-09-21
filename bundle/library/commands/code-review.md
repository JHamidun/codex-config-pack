---
name: "code-review"
description: "Комплексный code review с проверкой всех аспектов"
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


# Code Review: $ARGUMENTS

## 1. Структурный анализ

### Читаемость
- Понятные названия переменных и функций?
- Есть docstrings/комментарии для сложной логики?
- Код следует style guide проекта?

### Архитектура
- Соблюдается ли принцип единой ответственности?
- Нет дублирования кода (DRY)?
- Правильная декомпозиция на функции/классы?

## 2. Функциональность

### Логика
- Код делает то, что должен?
- Обработаны edge cases?
- Нет логических ошибок?

### Тесты
```bash
# Запусти тесты
pytest $ARGUMENTS -v

# Проверь coverage
pytest $ARGUMENTS --cov --cov-report=html
```

Coverage должен быть >80% для новых фич.

## 3. Безопасность

### Проверь на уязвимости:
- SQL injection (используется ли ORM/параметризованные запросы?)
- XSS (экранируется ли user input?)
- Аутентификация/авторизация на месте?
- Секреты не в коде (используются env vars)?

### Security scan
```bash
# Python
bandit -r $ARGUMENTS

# npm
npm audit

# SAST
semgrep --config=auto $ARGUMENTS
```

## 4. Производительность

### Оптимизация
- Нет N+1 запросов к БД?
- Используется кэширование где нужно?
- Эффективные алгоритмы (O(n) vs O(n²))?

### Profiling (если нужно)
```bash
# Python
python -m cProfile $ARGUMENTS

# Node.js
node --prof $ARGUMENTS
```

## 5. Maintainability

### Зависимости
- Минимальное количество dependencies?
- Все dependencies актуальные?
- Нет конфликтов версий?

### Документация
- README обновлён?
- API docs актуальны?
- Есть примеры использования?

## 6. Git лучшие практики

### Commits
- Атомарные коммиты (один логический change)?
- Понятные commit messages?
- Нет debug кода/комментариев?

### Branch
- Актуальная ветка (merged с main)?
- Нет merge conflicts?
- Clean history (нет "fix typo" коммитов)?

## Итоговый чеклист

**Code Quality:**
- [ ] Читаемый и понятный код
- [ ] Следует style guide
- [ ] Нет code smells

**Functionality:**
- [ ] Работает как ожидается
- [ ] Тесты покрывают функциональность
- [ ] Edge cases обработаны

**Security:**
- [ ] Нет очевидных уязвимостей
- [ ] Security scanners прошли
- [ ] Секреты в env vars

**Performance:**
- [ ] Нет очевидных bottlenecks
- [ ] Эффективные алгоритмы
- [ ] Кэширование где нужно

**Documentation:**
- [ ] Код задокументирован
- [ ] README актуален
- [ ] Changelog обновлён

## Рекомендации

### 👍 Approve - если:
- Все чеклисты пройдены
- Код улучшает кодовую базу
- Готов к production

### 🔄 Request Changes - если:
- Есть критичные проблемы
- Нужны тесты
- Security issues

### 💬 Comment - если:
- Есть suggestions для улучшения
- Нужно обсуждение подхода
- Вопросы по implementation

---

**Final Score:** [Оцени от 1 до 10]

**Summary:** [Краткий вердикт и ключевые моменты]
