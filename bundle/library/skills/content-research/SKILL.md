---
name: "content-research"
description: "Research под контент-артефакт: источники, CRAAP, цитаты с пруфами. Триггеры: «найди источники», «проверь факты для статьи». НЕ лонгрид → /deep-research."
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


# Content Research Skill

> **Overlap:** для глубокого автономного исследования (10+ источников, лонгрид-отчёт) используй команду `/deep-research`. Этот skill — компактный research-цикл под конкретный контент-артефакт (статья, пост, презентация, документация): 3-7 источников, верифицированные факты, готовые цитаты.

## Когда использовать

- Пишешь статью/пост/презентацию и нужны проверенные факты с источниками.
- Нужно верифицировать 1-5 конкретных утверждений («правда ли, что X?»).
- Готовишь документацию или отчёт, где каждая цифра должна иметь ссылку.
- Клиент/редактор требует «пруфы» под тезисы черновика.

## Процедура

**Шаг 1: Определи вопросы (DEFINE).**
Разбей задачу на 3-7 конкретных проверяемых вопросов/утверждений. Каждое — одной строкой: «Какой % X делает Y?», «Верно ли, что Z?». Зафиксируй список — он станет скелетом отчёта.

**Шаг 2: Найди источники (SEARCH).**
На каждый вопрос — 1-2 вызова `WebSearch` (запрос на языке вероятного источника; для цифр добавляй год: «statistics 2025»). Из выдачи выбери 2-3 кандидата, приоритет по таблице надёжности (ниже). Первоисточник > пересказ: если новость ссылается на исследование — ищи само исследование.

**Шаг 3: Извлеки и проверь (FETCH + EVALUATE).**
`WebFetch` каждого кандидата с промптом «извлеки: точную цифру/утверждение по [вопрос], дату публикации, автора/организацию». Прогони источник по компакт-CRAAP (ниже); сомнительный (< 15/25) — замени или помечай факт как «слабо подтверждён». Ключевые цифры подтверждай из 2 независимых источников (не цитирующих друг друга). Полный CRAAP-шаблон и фреймворки → `references/evaluation-frameworks.md`.

**Шаг 4: Собери отчёт (SYNTHESIZE + CITE).**
Заполни шаблон из «## Выход»: таблица «факт → источник → статус верификации» + готовые к вставке формулировки с inline-ссылками. Формат цитирования — по назначению контента: веб-контент = inline-ссылка `[Название](URL)`; академический = APA/MLA (→ `references/citation-formats.md`).

**Шаг 5: Проверь по чек-листу** (внизу) и отдай отчёт.

## Источники: надёжность (для Шага 2-3)

| Тип источника | Надёжность | Примеры |
|---|---|---|
| Академические журналы | Высшая | Nature, Science, IEEE |
| Официальные отчёты | Высокая | Госорганы, WHO, World Bank |
| Рецензируемые книги | Высокая | Академические издательства |
| Авторитетные СМИ | Средне-высокая | Reuters, AP |
| Индустриальные отчёты | Средне-высокая | Gartner, McKinsey |
| Экспертные блоги | Средняя | Зависит от автора |
| Wikipedia | Средняя | Для обзора; проверяй её источники |
| Соцсети | Низко-средняя | Верифицируй независимо |
| Случайные сайты | Низкая | Только с перепроверкой |

## Компакт-CRAAP (быстрая оценка, 5 × 1-5 баллов)

- **Currency** — свежесть достаточна для темы?
- **Relevance** — отвечает именно на твой вопрос?
- **Authority** — кто автор/издатель, каковы регалии?
- **Accuracy** — есть данные/методология, подтверждается ли ещё где-то?
- **Purpose** — информирует или продаёт/агитирует (bias)?

Сумма: 20-25 отлично · 15-19 годен · 10-14 сомнителен, ищи замену · <10 не использовать.

## Выход

Один markdown-отчёт (в чат или файл рядом с черновиком контента):

```markdown
# Research Report: [тема контента]
Дата: [YYYY-MM-DD] · Вопросов: [N] · Источников: [M]

## Факты и верификация

| # | Утверждение | Источник (ссылка) | Дата | CRAAP | Статус |
|---|---|---|---|---|---|
| 1 | [точная формулировка с цифрой] | [Название](URL) + [Название2](URL2) | 2025 | 21/25 | ✅ Verified (2 источника) |
| 2 | [утверждение] | [Название](URL) | 2024 | 16/25 | ⚠️ Один источник |
| 3 | [утверждение] | — | — | — | ❌ Не подтверждено — НЕ использовать |

## Готовые формулировки (вставить в контент)
1. «[Формулировка с фактом]» — по данным [Источник](URL), [год].
2. …

## Не подтвердилось / нюансы
- [Утверждение X]: источники говорят [что на самом деле] — скорректируй тезис.

## Список источников
1. [Полная ссылка/цитирование по нужному формату]
```

## Пример

**Вход:** «Пишу пост про удалёнку, нужен пруф: „удалённые сотрудники продуктивнее офисных"».

**Выход (фрагмент отчёта):**

| # | Утверждение | Источник | Дата | CRAAP | Статус |
|---|---|---|---|---|---|
| 1 | Гибридный формат не снижает продуктивность и сокращает отток на ~33% | [Stanford / Nature, Bloom et al.](https://www.nature.com/articles/s41586-024-07500-2) | 2024 | 24/25 | ✅ Verified |
| 2 | «Удалёнка всегда продуктивнее офиса» | — | — | — | ❌ Обобщение не подтверждено: RCT показывают паритет, не превосходство |

**Готовая формулировка:** «Рандомизированное исследование Стэнфорда (Nature, 2024) не нашло падения продуктивности у гибридных сотрудников — при этом отток снизился на треть». Тезис поста скорректирован с «продуктивнее» на «не хуже + меньше текучка» — так он верифицируем.

## Чек-лист (перед выдачей)

- [ ] Каждый факт в отчёте имеет рабочий URL (WebFetch вернул контент, не 404).
- [ ] Ключевые цифры подтверждены ≥2 независимыми источниками (или явно помечены ⚠️).
- [ ] Для каждой цифры источник — первоисточник, а не пересказ пересказа.
- [ ] Даты источников свежие для темы (tech ≤ 2 года; фундаментальное — можно старше).
- [ ] Неподтверждённые тезисы явно помечены ❌ с рекомендацией убрать/переформулировать.
- [ ] Ни одного URL «по памяти» — только реально открытые в этой сессии (anti-phantom-citation).
- [ ] Формат цитирования соответствует назначению контента (inline для веба, APA/MLA для академического → `references/citation-formats.md`).

## References

- `references/evaluation-frameworks.md` — полный CRAAP-шаблон, cross-reference, трассировка к первоисточнику, Cornell-заметки, source card, каталоги инструментов (academic search, fact-checking, citation managers).
- `references/citation-formats.md` — APA 7 / MLA 9 / Chicago с примерами, интеграция цитат в текст, анти-плагиат.
