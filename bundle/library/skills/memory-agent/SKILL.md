---
name: "memory-agent"
description: "Оркестратор 4 слоёв памяти: файловая, граф, чаты, Second Brain. Триггеры: «запомни», «что мы решали про»."
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


# Memory Agent — оркестратор многослойной памяти

Единая точка входа в память. Не хранилище само по себе, а **маршрутизатор**: по типу запроса выбирает нужный слой (или несколько) и применяет знание невидимо — как свой опыт, не как «извлечённый факт» (см. `rules/auto-learning.md`).

> Устаревшее (НЕ использовать): `vector_memory.py` (ChromaDB), `chat_ingester.py`, `${CODEX_PACK_ROOT}/library/memory/knowledge_base.md`, таксономия `learnings/decisions/preferences/`. Заменено слоями ниже.

## Четыре слоя памяти

| Слой | Что это | Хранилище | Инструмент | Когда |
|------|---------|-----------|-----------|-------|
| **1. Файловая (курируемая)** | MEMORY.md индекс + topic-файлы, bi-temporal frontmatter | `${CODEX_PACK_ROOT}/library/projects/<project>/memory/*.md` | Read/Write/Edit + команды `/memory-*` | Каноничные решения, root cause, паттерны, решения пользователя — то, что должно жить долго и читаться человеком |
| **2. Граф** | Заметки+сущности как узлы, [[wikilinks]]+supersedes как рёбра | `${CODEX_PACK_ROOT}/library/memory-graph/graph.db` (SQLite, офлайн) | `scripts/memory_graph.py` | Связи, многохоповые вопросы, хронология, хабы, кейсы по проекту/человеку/компании |
| **3. Полнотекст чатов** | Вся история сессий, FTS5+BM25 + knowledge base | `${CODEX_PACK_ROOT}/library/chats.db` | `tools/search_chats.py` | «Что мы делали с X», recall решений/грабель, точная цитата из прошлой сессии |
| **4. Семантический (опционально)** | Векторный recall поверх личного архива; в паке не поставляется — поднимается собственным MCP-сервером | своё хранилище (гибрид FTS5+вектор, напр. LanceDB) | свой MCP + `scripts/memory_brief.py` | Семантический recall, брифинги; тяжёлый векторизатор — только вручную под ресурс-гардом |

## Первый запуск — баз ещё нет

Пак приезжает **без данных**: ни `chats.db`, ни `memory-graph/graph.db`, ни каталога
`projects/<project>/memory/`. Это не поломка — память наполняется твоей работой. Поэтому
первый же `search`/`stats` честно ответит «пусто» либо «нет базы», и это ожидаемо.

```bash
python ${CODEX_PACK_ROOT}/library/tools/search_chats.py index    # слой 3: собрать chats.db из своих сессий
python ${CODEX_PACK_ROOT}/library/scripts/memory_graph.py build  # слой 2: граф из заметок (пока их нет — 0 узлов)
```

Слой 1 создаётся первой же записью: `Write` topic-файла в `${CODEX_PACK_ROOT}/library/projects/<project>/memory/`
плюс строка в `MEMORY.md` (создать файл, если его нет). Слой 4 в паке не поставляется вовсе.

## Маршрутизация: запрос → слой

| Запрос пользователя | Слой(и) | Действие |
|---------------------|---------|----------|
| «запомни это / сохрани в память / чтобы не забыл» | 1 (+3 knowledge) | Записать topic-файл + строку в MEMORY.md; при желании продублировать в knowledge base |
| «что мы решали про X / какие были грабли с X» | 3 → 1 | `search_chats.py search` → при попадании `get`/`timeline`; сверить с MEMORY.md |
| «что связано с X / кто связан с X / хронология проекта» | 2 | `memory_graph.py neighbors/path/timeline/cases` |
| «где я остановился / recap» | 3 | `search_chats.py search` по проекту, свежее окно |
| «собери контекст для воркера по теме Y» | 4+1 | `memory_brief.py "Y"` → вставить KNOWN GOTCHAS в промпт |
| «консолидируй / почисти память» | 1+2 | skill `dream` (rethink/decay/prune) + `memory_graph.py build` |
| семантический recall личного/семейного | 4 | свой семантический MCP (если поднят; в паке слоя 4 нет) |

**Recall-дисциплина:** любой вопрос о ПРОШЛОМ (решения / грабли / статусы / «что делали с X») → СНАЧАЛА слой 3 или 4, ПОТОМ веб/grep. Найденное применяй невидимо.

---

## Слой 1 — Файловая память (канон записи)

Директория: `${CODEX_PACK_ROOT}/library/projects/<project>/memory/`

`<project>` Claude Code создаёт сам из пути рабочего каталога: `<UPSTREAM_HOME>\code\shop`
превращается в `C--Users-ivan-code-shop`. Подставлять руками не нужно — оба инструмента
памяти обходят `${CODEX_PACK_ROOT}/library/projects/*` целиком.

- **MEMORY.md** — краткий индекс (держать < 200 строк / ~25KB): одна строка + ссылка на topic-файл.
- **Topic-файлы** — детальные заметки (`debugging.md`, `<тема>-<дата>.md`), структурированные, с примерами кода.

**Что ВСЕГДА сохранять:** решения багов + root cause; новые паттерны/конвенции/арх-решения; рабочие команды и конфиги; решения пользователя («выбрал X потому что Y»); неочевидное поведение инструментов; **успехи тоже** (если подход сработал и был неочевиден).

**Bi-temporal (иммутабельность):** факт не удаляем, а закрываем. Противоречие с прошлой заметкой → новая заметка с `supersedes: [[старый-id]]`; старой — `status: superseded` / `superseded_by:` / `invalid_at:`. История «что считали верным и когда» = данные (её читает граф, слой 2).

**Как записать:**
```bash
# Ручной способ: Write topic-файл + Edit одну строку в MEMORY.md.
# Обёртки-команды:
/memory-learn <категория>: <что запомнить>   # + в knowledge base
/memory-search <запрос>                        # поиск чаты + knowledge
```
Полный 4-уровневый пайплайн (topic + MEMORY.md + routing.md + vector) → skill `save-knowledge-base`.

---

## Слой 2 — Граф памяти (`memory_graph.py`)

`${CODEX_PACK_ROOT}/library/scripts/memory_graph.py` — офлайн SQLite-граф из заметок (Layer 1) + сущностей из корпуса чатов (Layer 2). БД `${CODEX_PACK_ROOT}/library/memory-graph/graph.db`.

```bash
python ${CODEX_PACK_ROOT}/library/scripts/memory_graph.py stats                 # узлы/рёбра/типы/битые ссылки
python ${CODEX_PACK_ROOT}/library/scripts/memory_graph.py neighbors <name> [d]  # соседи (депт по умолч. 1)
python ${CODEX_PACK_ROOT}/library/scripts/memory_graph.py path <a> <b>          # кратчайший путь (BFS)
python ${CODEX_PACK_ROOT}/library/scripts/memory_graph.py timeline <name>       # цепочка supersedes
python ${CODEX_PACK_ROOT}/library/scripts/memory_graph.py hubs [N]              # топ-N связанных узлов
python ${CODEX_PACK_ROOT}/library/scripts/memory_graph.py search <substr>       # узлы по подстроке
python ${CODEX_PACK_ROOT}/library/scripts/memory_graph.py orphans               # узлы без рёбер
python ${CODEX_PACK_ROOT}/library/scripts/memory_graph.py dangling              # ссылки на несуществующие узлы
python ${CODEX_PACK_ROOT}/library/scripts/memory_graph.py gaps [stale_days]     # gap-анализ (0 LLM)
python ${CODEX_PACK_ROOT}/library/scripts/memory_graph.py build                 # пересобрать из заметок
```
Узлы-сущности: `person:Имя` / `company:X` / `tool:Y` / `proj:Z`. Пересборка (`build`) — в рамках `dream`.

> Старый графовый бэкенд на FalkorDB (внешний сервер) заморожен. Каноничный локальный движок — `memory_graph.py`; доступ через MCP — `mcps/graph-memory/`.

---

## Слой 3 — Полнотекст чатов (`search_chats.py`)

`${CODEX_PACK_ROOT}/library/tools/search_chats.py` — FTS5+BM25 над `${CODEX_PACK_ROOT}/library/chats.db`. 3-слойный token-aware recall:

```bash
python ${CODEX_PACK_ROOT}/library/tools/search_chats.py search "query"          # L1: компактный индекс (id/дата/проект/сниппет)
python ${CODEX_PACK_ROOT}/library/tools/search_chats.py search "query" --days 30 # окно свежести (деф 90; --days 0 = всё время)
python ${CODEX_PACK_ROOT}/library/tools/search_chats.py timeline <msg_id>       # L2: контекст вокруг якоря
python ${CODEX_PACK_ROOT}/library/tools/search_chats.py get <id1,id2>           # L3: полные тексты только этих id
python ${CODEX_PACK_ROOT}/library/tools/search_chats.py export <session_id>     # восстановить сессию в markdown (даже удалённую)
python ${CODEX_PACK_ROOT}/library/tools/search_chats.py index                   # инкрементальный переиндекс
# Knowledge base (извлечённые знания):
python ${CODEX_PACK_ROOT}/library/tools/search_chats.py learn "content" "category"
python ${CODEX_PACK_ROOT}/library/tools/search_chats.py knowledge "query" [--type code|error|learning|decision]
```
Токен-экономия: `search` (дёшево) → сузить → `get` только по нужным id. Не тяни полные тексты без нужды. Шум `ai-news-bot` скрыт по умолчанию (`--include-newsbot` чтобы вернуть).

---

## Слой 4 — Семантическая память (опционально) + брифинг для воркеров

Семантический recall поверх личного архива (семья/личное/встречи). **В паке этот слой не поставляется** — это отдельный MCP-сервер с векторным индексом, который поднимается самостоятельно. Если он тебе нужен:
- подними свой MCP с инструментами вида «семантический поиск / запомнить / статистика» над своим хранилищем (гибрид FTS5 + векторный индекс, например LanceDB);
- тяжёлую векторизацию запускай ТОЛЬКО вручную под ресурс-гардом (idle-gated) — никакого молчаливого крона.

**Брифинг для Fable-воркера** — перед промптом по знакомой теме собери грабли из семантического слоя (если поднят) + MEMORY.md:
```bash
python ${CODEX_PACK_ROOT}/library/scripts/memory_brief.py "<тема задачи>" [--max-tokens 600]
```
Печатает компактный блок `KNOWN GOTCHAS` (деф ≤600 ток) для вставки verbatim в промпт воркера. Read-only, деградирует мягко (embedding down → FTS-only; семантический слой не поднят → только MEMORY.md).

---

## Auto-learning триггеры (signal-extraction)

Сохраняй **при сигналах** (не «вспомни всё в конце»), + 2-3 хода контекста:
- Решение бага → root cause + фикс + профилактика.
- Новый инструмент/библиотека → назначение, конфиг, гочи.
- Коррекция пользователя → что поправил, почему, новое правило/предпочтение.
- «Выбрал X потому что Y» → решение + trade-off.
- Неожиданно сработавший подход → сохрани (иначе память = только ошибки → чрезмерная осторожность).

Куда по умолчанию: **слой 1** (topic-файл + строка MEMORY.md). Дублировать в knowledge base (слой 3 `learn`) — если запись должна находиться полнотекстовым поиском.

**Чувствительное** (семья/финансы/здоровье/конфликты): из памяти первым НЕ поднимать — пока пользователь сам не затронул тему.

---

## Процедура (по типу задачи)

**A. Сохранить знание**
1. Определи слой: долгоживущее решение → 1; быстро-находимый факт → 1+3.
2. Проверь дубли: `search_chats.py knowledge` / `memory_graph.py search` — не дублируй.
3. Противоречит прошлому? → bi-temporal (`supersedes`, не переписывай).
4. Write topic-файл → Edit одну строку в MEMORY.md.

**B. Достать контекст (recall)**
1. О прошлом? → `search_chats.py search` (слой 3) ПЕРЕД веб/grep.
2. Про связи/хронологию → `memory_graph.py neighbors/timeline/path`.
3. Семантический/личный → свой семантический MCP (слой 4, если поднят).
4. Сузь → `get <ids>` только нужное. Применяй невидимо.

**C. Брифинг воркера**
1. `memory_brief.py "<тема>"` → блок KNOWN GOTCHAS → в промпт Fable-воркера.

**D. Консолидация**
1. skill `dream` (orient → gather → consolidate → prune; decay −0.02/нед; prune pending>30д).
2. `memory_graph.py build` — пересобрать граф после правок заметок.
3. Держи MEMORY.md < 200 строк; anti-churn: нечего менять — не трогай файл (ломает prompt-cache).

## Выход
- **Сохранение:** путь к topic-файлу + добавленная строка MEMORY.md (абсолютные пути).
- **Recall:** найденные факты, применённые невидимо в ответе; при необходимости — id сессий/узлов.
- **Брифинг:** блок KNOWN GOTCHAS готовый к вставке в промпт.

## Чек-лист
- [ ] Recall о прошлом сделан ДО веб-поиска (слой 3/4)?
- [ ] Дубли проверены перед записью?
- [ ] Противоречие оформлено bi-temporal (supersedes), а не перезаписью?
- [ ] MEMORY.md < 200 строк / ~25KB после правки?
- [ ] Не тронул неизменённые файлы зря (prompt-cache / anti-churn)?
- [ ] Знание применено невидимо, без «судя по памяти»?
- [ ] Тяжёлый векторизатор не запущен молча (только guarded)?
- [ ] Не использованы устаревшие vector_memory.py / chat_ingester.py / knowledge_base.md?

## Связанные
- `save-knowledge-base` — полный 4-уровневый пайплайн записи.
- `dream` — периодическая консолидация + frontmatter v2.
- MCP `mcps/graph-memory/` — граф как MCP-инструменты поверх того же `memory_graph.py`.
- Команды: `/memory-search`, `/memory-learn`, `/memory-stats`, `/memory-ingest`, `/search-chats`.
