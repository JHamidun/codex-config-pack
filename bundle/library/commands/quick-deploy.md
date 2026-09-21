---
name: "quick-deploy"
description: "Быстрый деплой с проверкой тестов и линтеров"
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


# Быстрый деплой в $ARGUMENTS

## Pre-deploy Checks

### 1. Проверка статуса Git
```bash
git status
git diff --stat
```
Убедись, что нет uncommitted изменений.

### 2. Запуск тестов
```bash
# Backend tests
pytest tests/ -v --cov

# Frontend tests
npm test

# Integration tests
npm run test:e2e
```

Все тесты должны пройти ✅

### 3. Lint и форматирование
```bash
# Python
black . --check
pylint src/

# JavaScript/TypeScript
npm run lint
npm run format:check
```

### 4. Build проверка
```bash
# Backend
python setup.py build

# Frontend
npm run build
```

Build должен пройти без ошибок.

## Deploy

### Staging
```bash
git push origin main
# Trigger staging deploy
```

### Production
```bash
# Создай release tag
git tag -a v$(date +%Y.%m.%d) -m "Release $(date +%Y-%m-%d)"
git push origin --tags

# Deploy to production
# [Команда деплоя зависит от твоей инфраструктуры]
```

## Post-deploy Monitoring

### Health checks
```bash
curl https://$ARGUMENTS.yourapp.com/health
```

### Проверь логи
```bash
# Если используешь k8s
kubectl logs -f deployment/app -n $ARGUMENTS

# Если используешь Docker
docker logs -f app-$ARGUMENTS
```

### Smoke tests
- Открой главную страницу
- Проверь key features
- Проверь аналитику (PostHog/другое)

## Rollback (если что-то пошло не так)

```bash
# Откат к предыдущей версии
git revert HEAD
git push

# Или
kubectl rollout undo deployment/app -n $ARGUMENTS
```

---

**Чеклист готовности к деплою:**
- [ ] Все тесты проходят
- [ ] Линтеры без ошибок
- [ ] Build успешен
- [ ] Code review прошёл
- [ ] Changelog обновлён
- [ ] Команда уведомлена
