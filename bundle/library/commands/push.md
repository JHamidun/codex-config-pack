---
name: "push"
description: "Релиз вручную по шагам — bump версии, два чейнджлога, тег и пуш. Скрипта-автомата нет."
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


# /push — релиз

**Автоматизации нет.** Команда раньше вызывала `bash .claude/scripts/release.sh` в
корне проекта. Такого файла в паке нет — ни в `${CODEX_PACK_ROOT}/library/scripts/`, ни где-либо ещё
(проверяется: `ls ${CODEX_PACK_ROOT}/library/scripts/release.sh`). Всё, что перечислено ниже, делается
руками по шагам — либо навыком `changelog-generator`, который закрывает пункты 2-3 и
умеет `gh release`.

Обещание без файла хуже прямого «не автоматизировано»: по нему идут и упираются в
`bash: .claude/scripts/release.sh: No such file or directory`. На Windows без Git Bash
до этой строки дело даже не дойдёт — оболочка сначала не найдёт `bash`, и человек
решит, что дело в нём.

## Шаги

1. **Синхронизировать версию с последним тегом** — иначе `package.json` и
   `git tag` разъезжаются, и следующий bump считается от неверной базы.
   ```bash
   git describe --tags --abbrev=0
   ```
2. **Собрать коммиты с прошлого релиза** и определить тип bump'а по conventional
   commits: `feat:` → minor, `fix:` → patch, `BREAKING CHANGE`/`!` → major.
   Аргумент `patch|minor|major` перебивает автоопределение.
   ```bash
   git log $(git describe --tags --abbrev=0)..HEAD --oneline
   ```
3. **Два чейнджлога** — у них разные читатели, поэтому и файлов два:
   - `CHANGELOG.md` — формат Keep a Changelog, для разработчиков, все коммиты.
   - `RELEASE_NOTES.md` — для людей: человеческие имена скоупов
     (auth → Authentication, db → Database), эмодзи по разделам
     (✨ Features, 🐛 Fixes, 🔒 Security), без `chore`/`ci`/`docs`.
4. **Проставить версию** во всех `package.json` монорепо (не только в корневом).
5. **Тег и пуш**:
   ```bash
   git tag -a vX.Y.Z -m "release: vX.Y.Z" && git push --follow-tags
   ```

## Откат

Автоматического rollback тоже нет. Если релиз испорчен до пуша — `git tag -d vX.Y.Z`
и `git reset` на релизный коммит. После пуша тег не переписывать: выпускать
следующий патч, иначе у тех, кто уже подтянул тег, останется другое содержимое.

## Что стоит сделать перед релизом

Незакоммиченное — отдельным коммитом с осмысленным префиксом, чтобы оно попало в
`RELEASE_NOTES.md`: `feat(worker): add worker readiness pre-flight system`.
Коммит без `feat:`/`fix:` в пользовательский чейнджлог не попадёт.
