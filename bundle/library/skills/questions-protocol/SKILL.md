---
name: "questions-protocol"
description: "Уточняющие вопросы в начале задачи с коротким или неоднозначным брифом; не для мелких правок. Триггеры: «уточни задачу», «вопросы перед дизайном»."
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


# Questions protocol

Один цикл уточнений в начале — почти всегда правильно. Меньше вопросов = больше переделок.

## Когда задавать

| Запрос | Спрашивать? |
|---|---|
| «Сделай дек на 6 слайдов по этому PRD» | Нет — есть всё. |
| «Сделай дек по теме онбординга» | Да — аудитория, длина, тон, бренд. |
| «Прототип онбординга для доставки» | Очень много — платформа, шаги, фичи, референсы. |
| «Поправь отступы в хедере» | Нет — делать. |
| «Сделай красиво» | Да — что значит «красиво» для тебя. |

## Правила

- **Один заход**, не растягивать на 3 раунда.
- **Минимум 4 вопроса**, в ambiguous-кейсах 8–12.
- Каждый вопрос с вариантами: радио / чекбоксы / слайдер / файл / свободный текст.
- Всегда добавляй **«Explore a few options»** и **«Decide for me»** в варианты — пользователь часто не хочет выбирать.
- Добавляй **«Other»** для опен-энд.

## Список обязательных вопросов

Стартовая точка:
- Есть ли дизайн-система / UI-кит / кодовая база / Figma / скрины?
- Если нет — попроси приложить, прежде чем начинать.

Объём:
- Сколько вариантов? (1 / 2-3 / 4+ / decide for me)
- По каким осям варьировать (визуал / UX / копирайт / анимации)?

Тон и риск:
- «Безопасно по учебнику» / «средне» / «эксперимент» / decide for me.

Контекст использования:
- Куда это пойдёт? (печать / экран / шер по почте / соцсети)
- Аудитория: кто эти люди.

## Доменные вопросы

Для **слайдов**:
- Размер кадра (16:9 / 1:1 / vertical).
- Спикер-ноты нужны?
- Длительность выступления, плотность.
- Экспорт (PDF / PPTX / только HTML).

Для **прототипов**:
- Платформа (iOS / Android / web / desktop).
- Сколько экранов в флоу.
- Какие фичи кликабельны, какие — заглушки.
- Тёмная тема нужна?

Для **анимаций**:
- Длительность.
- Сопровождает ли звук.
- Где будет показываться (соцсети / сайт / в составе видео).

Для **лендингов**:
- Есть ли бренд-гайд.
- Какие секции обязательны.
- Адаптив (десктоп-only / mobile-first / оба).

## Чего избегать

- Вопросов «А что вы хотели?» — он уже ответил, спрашивая задачу.
- Вопросов про технические детали реализации — это твоя работа.
- 20 вопросов в форме за раз — устанет, ответит мусором.
- Спрашивать после того, как пользователь дал чёткий бриф.

## Формат форм

В Claude Code — обычная markdown-форма с пунктами. Если используешь skill в среде с `questions-tool` — JSON-блоб с типами вопросов.

Пример hand-rolled:

```
Несколько уточнений перед стартом:

1. Стартовая точка — есть ли дизайн-система?
   [a] Да, прикреплена
   [b] Нет, начинай с нуля
   [c] Возьми из этого репо: <link>

2. Сколько вариантов хочется?
   [a] 1 финальный
   [b] 2-3 на выбор
   [c] 4+
   [d] Decide for me

3. Тон визуала?
   ...
```

Жди ответа, не приступай к работе до него.

## Legacy reference

Прежняя расширенная версия скилла (дерево @2026-04-30) сохранена целиком в `references/legacy-questions-protocol.md`. Секции там: Когда спрашивать, Минимальный пакет вопросов (большая задача), Что НЕ спрашивать, Хорошие vs плохие формулировки, Когда задавать вопросы посреди работы, Что делать, если юзер не ответил, Антипаттерны.
