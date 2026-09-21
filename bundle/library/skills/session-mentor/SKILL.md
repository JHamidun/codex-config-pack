---
name: "session-mentor"
description: "Локальный анализ сессий Claude Code → HTML-отчёт «как ты работаешь». Триггеры: «как я работаю», «где теряю время». НЕ поиск по чатам→/search-chats."
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


# Session Mentor — «как ты работаешь с Claude Code»

Читает локальные транскрипты (`${CODEX_PACK_ROOT}/library/projects/**/*.jsonl`, опц. `~/.codex`), считает реальные метрики и собирает **самодостаточный HTML-отчёт**. Всё локально, ничего не уходит с машины. Три шага: `collect.py` (данные) → агент (анализ 8 секций) → `render_report.py` (HTML).

## Когда использовать
- «Проанализируй, как я работаю» / «где теряю время» / «какие фичи не использую».
- Периодический само-обзор (раз в неделю/месяц) с копипаст-правками для `CLAUDE.md`.
- Онбординг-рефлексия: на что уходят сессии, tool-mix, делегирование субагентам.

**НЕ для:** полнотекстового поиска по истории (`/search-chats`); метрик одной текущей сессии (`/prompt-log`); извлечения знаний в память (`/memory-extract`).

## Процедура

**Шаг 1. Собери метрики.**
```bash
cd ${CODEX_PACK_ROOT}/library/skills/session-mentor/scripts
python collect.py --days 30 --agent both --out stats.json
```
Флаги: `--days N` (окно, деф 30; префильтр по mtime — не парсит все ~50k файлов), `--agent claude|codex|both`. Вывод `stats.json`: totals, tool_mix, per_project, activity_by_day, session_themes (первые промпты для кластеризации), top_sessions_by_tokens.

**Шаг 2. Проанализируй → `analysis.json`.** Прочитай `stats.json` и напиши `analysis.json` СТРОГО по схеме ниже. Пиши **по-русски, конкретно, на основе цифр** (не общими словами). Модельные догадки (темы, «доволен ли») помечай как гипотезы.

Схема:
```json
{"period":"последние 30 дней","sections":[
  {"key":"themes","title":"Над чем ты работаешь","body":"...","items":["кластер темы — N сессий",".."]},
  {"key":"agent_usage","title":"Как ты используешь агента","body":"tool-mix, доля правок/чтения/bash, делегирование (Agent/Workflow), тиры моделей"},
  {"key":"wins","title":"Что получается хорошо","items":["конкретный паттерн из данных",".."]},
  {"key":"friction","title":"Где теряешь время","items":["точка трения → почему видно из метрик → фикс",".."]},
  {"key":"underused","title":"Недоиспользуемые возможности","items":["инструмент/скилл почти не встречается, а помог бы в X",".."]},
  {"key":"claude_md","title":"Правки для CLAUDE.md","body":"вводка","snippets":["готовая строка для вставки в rules/ или CLAUDE.md",".."]},
  {"key":"new_scenarios","title":"Новые сценарии","items":["как ещё применить под твои темы",".."]},
  {"key":"trends","title":"Тренды","body":"что растёт/падает по activity_by_day и tool_mix"}
]}
```
Правила анализа: (1) каждое утверждение опирается на число из stats; (2) «правки для CLAUDE.md» — реально копипастятся; (3) для «trends» смотри `activity_by_day` и сравни первую/вторую половину окна.

**Шаг 3. Собери отчёт.**
```bash
python render_report.py stats.json analysis.json --out mentor-report.html
```
Открой `mentor-report.html` в браузере (self-contained, theme-aware light/dark, count-up метрики, tool-mix бары, спарклайн активности, проекты, 8 секций).

## Выход
`mentor-report.html` — один файл, открывается в любом браузере без сборки. Метрики + 8 секций анализа. Плюс `stats.json`/`analysis.json` как сырьё.

## Пример
Вход: `--days 7`. `collect.py` → 78 сессий, 13 995 tool-calls, Bash 6820 / Read 1568 / Edit 1242, 63.6M токенов. Агент видит: bash-heavy (49% вызовов) + высокое делегирование (Agent 485, Workflow 248) → секция «Как используешь» отмечает «оркестраторский стиль», «friction» ищет повторные Bash-ретраи, «underused» — что почти не звалось. Рендер → HTML.

## Усиления (сверх базового)
- **Кросс-линк с memory_graph**: `python ${CODEX_PACK_ROOT}/library/scripts/memory_graph.py hubs` / `search <тема>` — превратить `session_themes` в реальные проекты/инструменты/людей (у mentor этого нет).
- **Токен-косты по тирам**: в `stats.totals.out_tokens` — грубая оценка нагрузки; в анализе раздели «где жжём токены» по `top_sessions_by_tokens`.
- **CLAUDE.md-привязка**: секция `claude_md` должна ссылаться на реальные файлы (`rules/routing.md`, `CLAUDE.md`), а не абстрактно.

## Чек-лист
- [ ] `stats.json` собран, `totals.sessions > 0`.
- [ ] Каждая секция `analysis.json` опирается на конкретные числа.
- [ ] `claude_md.snippets` — готовые к вставке строки.
- [ ] `mentor-report.html` открывается, светлая/тёмная тема переключается.
- [ ] Никакие данные не отправлялись наружу (всё локально).
