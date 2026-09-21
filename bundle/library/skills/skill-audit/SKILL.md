---
name: "skill-audit"
description: "Проверка ЧУЖОГО скилла/плагина до установки: prompt-injection, хуки, MCP, npm (35 правил). Триггеры: «безопасно ли ставить», «скачал с гитхаба скилл». Своё наружу→leak-scan."
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


# skill-audit

Входящий гейт: **чужой код ко мне**. Любой сторонний скилл или плагин, скачанный
с GitHub, попадает в авто-загружаемый каталог `${CODEX_PACK_ROOT}/library/` **без единой проверки** —
а его SKILL.md уходит в контекст модели, его хуки выполняются на каждом вызове
инструмента, его `.mcp.json` может поднять чужой сервер с твоими правами. Этот скан —
барьер перед тем, как чужой код станет частью твоего окружения.

## Граница с leak-scan

Две противоположные стороны одной двери, их легко перепутать:

| | Направление | Вопрос | Навык |
|---|---|---|---|
| **Сюда** | чужое ко мне | «безопасно ли ставить этот скачанный скилл?» | **skill-audit** (этот) |
| **Отсюда** | моё наружу | «не утечёт ли что-то личное, если я это опубликую?» | `leak-scan` |

Публикуешь свой пак — это `leak-scan`. Ставишь чужой пак — это сюда. Проверки
независимы: скилл может быть безупречно обезличен и при этом нести инъекцию, и наоборот.

## Где лежит скрипт

```bash
python ${CODEX_PACK_ROOT}/library/skills/leak-scan/scripts/skill_injection_scan.py <цель> [опции]
```

Скрипт физически живёт в `skills/leak-scan/scripts/` — там же, где его выходной
близнец `leak_scan.py`. Оба сканера написаны одним заходом и делят внутренности,
поэтому этот навык — инструкция к соседнему скрипту, а не отдельная программа.
Зови **полным путём выше**, не относительным от каталога этого навыка.
Нет каталога `leak-scan` — навык не работает: везти их надо парой.

## Когда запускать

- Скачал скилл/плагин/агента с GitHub и **до** копирования в `${CODEX_PACK_ROOT}/library/skills|plugins|agents`.
- Оцениваешь чужой репозиторий, из которого хочешь забрать код себе.
- Ревизия уже установленного стороннего пакета («а что оно вообще делает при загрузке?»).

## Использование

- `<цель>` — каталог скилла (со `SKILL.md`), каталог плагина (с `plugin.json`), каталог
  агентов/команд, сборник (`skills/`+`agents/`+`hooks/`), **или** одиночный `.md`.
  Тип определяется автоматически.
- `--min-severity CRITICAL|WARN|INFO` — порог печати (по умолчанию INFO).
- `--allow RULE_ID` — заглушить правило (повторяемо), напр. `--allow hooks.registered`
  для заведомо доверенного пакета с хуком.
- `--include-vendor` — сканировать и `node_modules/dist/build` (по умолчанию помечаются
  как **не проверенные**, а не молча пропускаются).
- `--json` — машинный вывод. `--list-rules` — список всех правил.

**Коды выхода:** `0` чисто · `1` есть находки (CRITICAL/WARN) · `2` скан не завершён
достоверно (симлинк-цель, превышен лимит).

```bash
# Гейт перед установкой (пайп теряет код возврата — смотри печатное CRITICAL/ЧИСТО)
python ${CODEX_PACK_ROOT}/library/skills/leak-scan/scripts/skill_injection_scan.py ./downloaded-skill
```

Скрипт — чистый stdlib Python, UTF-8 stdout (Windows-совместимо), **ничего не меняет на диске**.
Ключей и оплаты не требует: всё считается локально, сеть не используется.

## Что ловит (35 правил, severity CRITICAL/WARN/INFO)

| Группа | Правила | Сигнал |
|--------|---------|--------|
| Невидимый Unicode | `unicode.invisible` | ZWSP/ZWNJ/ZWJ/word-joiner/BOM, bidi-override (trojan source), теговый блок U+E0000–E007F. Emoji-ZWJ (👨‍💻) не флагуется |
| Prompt-injection | `prompt.ignore_previous` (RU+EN), `disregard_system`, `role_reassignment`, `fake_system_prefix`, `system_tag`, `chat_template_tag` (`<\|im_start\|>`, `[INST]`), `tool_call_tag`, `covert_directive`, `autonomy_grab`, `memory_write` | фразы-перехваты, поддельные `system:`/`<system>`, разделители чат-шаблонов, приказ действовать скрытно/дописать себя в CLAUDE.md |
| Скрытое в Markdown | `md.hidden_directive`, `md.hidden_style` | инструкция в HTML-комментарии или под `display:none`/белым шрифтом |
| Фронтматтер-захват | `frontmatter.allowed_tools`, `model_invocation_enabled`, `permission_mode` | скилл сам себе выдаёт `Bash(*)`/`*`, включает автовызов, понижает режим разрешений |
| Эксфильтрация | `tool.exfiltration_shape`, `net.suspicious_sink`, `code.credential_exfil_chain`, `content.base64_blob` | секрет по сети на литеральный посторонний хост; webhook.site/ngrok/paste-сервисы; чтение кред + отправка в одном файле; длинный base64-блоб |
| Опасный код | `code.remote_exec`, `dynamic_eval`, `detached_spawn`, `destructive`, `claude_config_write` | `curl\|sh`, исполнение декодированного base64, фоновый отвязанный процесс, `rm -rf ~`, запись в твой конфиг Claude Code |
| Конфиг | `config.permission_widening` | пакет расширяет `permissions` в settings.json — тихо добавляет себе разрешения |
| **Хуки** (нет у источника) | `hooks.registered`, `hooks.dangerous_command` | плагин регистрирует хук, что выполнится **на каждом** вызове инструмента (matcher `*`) |
| **MCP** (нет у источника) | `mcp.server_declared`, `mcp.arbitrary_command`, `mcp.remote_server` | `.mcp.json` поднимает сервер с произвольной командой (`bash -c …`) или удалённый хост, куда уходит сессия |
| **npm lifecycle** (нет у источника) | `npm.lifecycle_script`, `npm.obfuscated_lifecycle` | `postinstall/preinstall`, исполняющий код при `npm install`; вскрывает и локальный скрипт, который тот вызывает (реальный кейс: postinstall маскировал `spawn`) |
| Файловая система | `fs.symlink`, `fs.binary_artifact` | симлинк (содержимое не проверено, может указывать наружу); исполняемый бинарник без исходников |

Точный список идентификаторов — всегда `--list-rules`, а не эта таблица: она пересказ.

## Как читать результат

- **CRITICAL** — не устанавливать, пока не понятно, зачем это в пакете.
- **WARN** — бывает легитимно (хук, MCP-сервер, объявленный `allowed-tools`), но должно
  быть заявлено в README пакета; сверь, что ожидаемо.
- Правила ловят **форму, а не смысл**: текст про безопасность/LLM может совпасть (напр.
  статья, объясняющая инъекции). Всегда смотри строку в контексте — `> excerpt`
  печатается рядом.
- **Этот навык ловит сам себя.** Таблица правил выше цитирует `<|im_start|>`, `system:`
  и webhook/paste-хосты, поэтому скан каталога скиллов даёт на `skill-audit/SKILL.md`
  находки уровня CRITICAL (`prompt.chat_template_tag`, `prompt.system_tag`,
  `net.suspicious_sink`). Это тот самый случай «форма, а не смысл» — не находка.
  Полезный побочный эффект: так проверяется, что сканер вообще работает.
- ЧИСТО — не гарантия: прочитай `SKILL.md` и скрипты глазами. Скан — первый барьер,
  не последний.

## Расширение правил

Правила инлайн в `${CODEX_PACK_ROOT}/library/skills/leak-scan/scripts/skill_injection_scan.py`:
текстовые — `_TEXT_RULES`, кодовые — `_CODE_RULES`, структурные (JSON) — функции
`_scan_hooks` / `_scan_mcp` / `_scan_package_json` / `_scan_json_file`.
Полный список id — `--list-rules`. Для разового доверия — `--allow RULE_ID`,
не редактируй файл.

## Происхождение

Идея и часть правил — из `virgiliojr94/book-to-skill` (`tools/scan_generated_skill.py`),
адаптировано и расширено проверками hooks / MCP / npm-lifecycle, которых у источника нет.
