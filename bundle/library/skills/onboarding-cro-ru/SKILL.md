---
name: "onboarding-cro-ru"
description: "Онбординг и активация trial ExampleProduct — до аха-момента. Триггеры: «activation rate», «дроп после регистрации». НЕ: сама форма регистрации→form-cro-ru; апгрейд→paywall-cro-ru."
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


# CRO онбординга и активации (RU)

Помочь новому пользователю дойти до «аха-момента» как можно быстрее в trial и закрепить привычку, ведущую к конверсии в платящего. Порт `onboarding` из marketingskills: принципы, паттерны и чеклисты сохранены; примеры адаптируются под подписочный SaaS/образовательный продукт (trial → платящий).

**Перед началом прочитай `${CODEX_WORKSPACE}/.codex-context/business-context.md`** (заведи из `${CODEX_PACK_ROOT}/library/templates/business-context.md`, если файла ещё нет) — позиционирование, ядро ценности, длина trial, набор ключевых функций/сценариев, карта воронки. Не дублируй позиционирование и метрики.

## Первичная оценка

1. **Контекст продукта:** что за продукт, ядро ценности, ключевые функции, формат доставки ценности, прогресс/геймификация. B2C или B2B-когорта. Сформулируй ядро ценности одной фразой («ради чего пользователь остаётся»).
2. **Определение активации:** что за «аха-момент»? Гипотеза — **первое ключевое действие, дающее ценность**, в первой сессии. Другие: завершён первый значимый шаг; первый достигнутый результат; вернулся на 2-й день trial.
3. **Текущее состояние:** что происходит после регистрации, где дропают (поэкранно), сколько из trial доходят до первого ключевого действия.

## Базовые принципы

1. **Time-to-value решает всё.** Убрать каждый шаг между регистрацией и первой ценностью. В коротком trial каждый день дропа критичен.
2. **Одна цель на сессию.** Первый успех — один. Продвинутое — позже.
3. **Делать, а не показывать.** Интерактив > туториал. Дать выполнить действие > читать про него.
4. **Прогресс мотивирует.** Показывать продвижение (%, шаги), отмечать завершения, делать путь видимым.

## Определение активации

### Найти аха-момент
Действие, сильнее всего коррелирующее с конверсией trial→paid. Что делают конвертировавшиеся, чего не делают ушедшие после trial? Самый ранний индикатор будущей оплаты?

**Как формулировать гипотезы:**
- Первое ключевое действие, дающее ощутимую ценность, в первой сессии.
- Завершён первый значимый шаг/сценарий.
- Возврат на 2-й день trial и продолжение работы.
- Для B2B-когорты: первый рабочий сценарий / онбординг-встреча с менеджером.

**Метрики активации:** % регистраций trial, дошедших до активации; время до активации; шаги до активации; активация по когортам/источникам. Считать в своей веб-аналитике (счётчик — раздел «Учёт и аналитика» в `${CODEX_WORKSPACE}/.codex-context/business-context.md`).

## Дизайн потока онбординга

### Первые 30 секунд после регистрации trial

| Подход | Лучше для | Риск |
|--------|-----------|------|
| Product-first (сразу в продукт) | Пользователь с ясной целью | Паралич перед выбором |
| Guided setup (квиз «какая цель») | Нужна персонализация | Трение до ценности |
| Value-first (демо результата) | Есть готовый сценарий | Может казаться «ненастоящим» |

Что бы ни выбрал: одно понятное следующее действие, нет тупиков, прогресс при мультишаге. Часто хорошо работает короткий квиз цели → рекомендованный сценарий → сразу первое ключевое действие.

### Паттерн «чеклист онбординга»
- Когда: несколько шагов настройки, много функций для открытия, self-serve B2B-когорта.
- Практики: 3-7 пунктов, порядок по ценности, начать с быстрых побед, прогресс-бар/%, празднование завершения, возможность скрыть (не запирать).

### Пустые состояния (empty states)
Это возможность онбординга, не тупик. Хорошее: объясняет, для чего раздел; показывает, как выглядит с прогрессом; чёткое первичное действие; опц. демо-данные (пример результата, превью).

### Тултипы и туры
Когда: сложный UI, неочевидные фичи. Практики: макс. 3-5 шагов, dismiss в любой момент, не повторять для вернувшихся.

## Мультиканальный онбординг

### Email + in-app
**Триггерные письма по trial:** приветствие (сразу), незавершённый онбординг (день 1, день 2), достигнута активация (поздравление + след. шаг), trial заканчивается (за 1-2 дня до конца → переход в paid, см. `paywall-cro-ru`).
**Письмо должно:** усиливать in-app действия, не дублировать; вести в продукт с конкретным CTA; быть персонализированным по действиям.
- **RU-инструменты:** вёрстка писем — `html-email`; триггерная логика/отправка — `n8n` (через ESP). Согласие на рассылку + отписка по 152-ФЗ.

## Застрявшие пользователи

- **Детект:** критерии «застрял» (зарегистрировал trial, но не сделал ключевое действие за 24-48ч).
- **Реактивация:** email-серия (напомнить ценность, снять блокеры, «осталось N дней trial»); in-app «с возвращением, продолжим»; человеческий контакт / менеджер для B2B-когорт.

## Измерение

| Метрика | Описание |
|---------|----------|
| Activation rate | % trial, дошедших до первого ключевого действия |
| Time to activation | Время до первой ценности |
| Onboarding completion | % завершивших чеклист |
| Trial→paid conversion | % trial, ставших платящими |
| Retention D1/D7 (в trial) | Возврат внутри trial |

**Анализ воронки:** трекать дроп на каждом шаге (Регистрация trial → Первичная настройка → Первое действие → Ключевое действие → Возврат D2 → Конверсия в paid), бить по самому большому провалу. Данные — из своей веб-аналитики (Метрика/GA).

## Идеи экспериментов

Полный набор — `references/experiments.md` (упрощение потока, гайды/туры, персонализация, быстрые победы, email/мультиканал по trial, реактивация, технические/UX). Запуск — `ab-testing-ru`.

## Связки

| Нужно | Скилл |
|------|-------|
| Данные активации/когорт | твоя веб-аналитика (Метрика/GA) — см. `business-context.md` → «Учёт и аналитика» |
| Вёрстка онбординг-писем | `html-email` |
| Триггерные письма/автоматизация | `n8n` |
| Эксперименты | `ab-testing-ru` |
| Оптимизация формы регистрации/trial до онбординга | `form-cro-ru` |
| Переход trial→paid во время онбординга | `paywall-cro-ru` |
| Удержание/отток после конверсии | `churn-prevention-ru` |

## Вопросы под задачу

1. Какое действие сильнее всего коррелирует с конверсией trial→paid?
2. Что происходит сразу после регистрации trial?
3. Где сейчас дропают (по дням trial)?
4. Какой таргет по activation rate и trial→paid?
5. Есть ли когортный анализ конвертировавшихся vs ушедших после trial?
