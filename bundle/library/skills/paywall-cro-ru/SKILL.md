---
name: "paywall-cro-ru"
description: "Пейволлы, экраны апгрейда и фиче-гейты ExampleProduct: trial→платящий. Триггеры: «feature gate», «trial to paid». НЕ страница тарифов→page-cro-ru."
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


# CRO пейволлов и экранов апгрейда (RU)

Конвертировать trial-пользователей в платящих (и апгрейдить между тарифами, продавать флагманский продукт) в моменты, когда они уже получили достаточно ценности. Порт `paywalls` из marketingskills: компоненты, триггеры и анти-паттерны сохранены, оплата и инструменты адаптированы под рублёвый рынок.

**Перед началом прочитай `${CODEX_WORKSPACE}/.codex-context/business-context.md`** (заведи из `${CODEX_PACK_ROOT}/library/templates/business-context.md`, если файла ещё нет) — структура тарифов и цены (месяц/год, trial-период, спец-офферы, разовые продукты, add-ons), карта воронки. Не дублируй цены и метрики.

## Первичная оценка

1. **Контекст апгрейда:** trial → платный (основное)? апгрейд между тарифами (младший→старший)? гейт флагманского продукта? апселл add-on? доступ к premium-функции?
2. **Модель продукта:** что доступно в trial (полный доступ на N дней), что в каждом тарифе (функции, лимиты, что включено), что триггерит промпт, текущая trial→paid конверсия.
3. **Путь пользователя:** когда появляется, что уже испытал (сколько ключевых действий), что пытается сделать.

## Базовые принципы

1. **Ценность до запроса.** Сначала реальный опыт (первое ключевое действие, первый результат), потом апгрейд — после «аха-момента».
2. **Показать, а не рассказать.** Демонстрировать ценность платных функций, превью того, чего лишён после trial.
3. **Путь без трения.** Легко апгрейднуться, когда готов; не заставлять искать цены.
4. **Уважать «нет».** Не запирать, не давить; дать дойти до конца trial; сохранить доверие для будущей конверсии (в т.ч. через контент-nurture).

## Триггеры пейволла

- **Окончание trial (главный):** ранние предупреждения (за 2-3-1 день), что будет после, резюме полученной ценности («Вы сделали N ключевых действий»).
- **Фиче-гейт:** клик по premium-функции или продвинутому сценарию — объяснить, почему платно, показать, что даёт, быстрый путь, опция «без него».
- **Гейт флагманского продукта:** разовый премиум-продукт (например, интенсив/курс в нескольких форматах) — отдельный апселл внутри основного продукта.
- **Апгрейд тарифа:** упёрся в лимит функции младшего тарифа → предложить старший с конкретной выгодой.
- **По времени:** после X дней на младшем тарифе — мягко подсветить неиспользованные функции старших.

## Компоненты экрана

1. Заголовок — про выгоду: «Откройте [функцию] для [результат]».
2. Демонстрация ценности — превью функции/сценария, до/после, «С [старшим тарифом] вы могли бы…».
3. Сравнение тарифов — ключевые отличия, текущий план отмечен.
4. Цена — чётко, в рублях, месяц/год (напр. −20% годовая).
5. Соцпруф — отзывы, релевантная регалия эксперта/компании.
6. CTA — конкретный, про ценность: «Получить [выгода]».
7. Аварийный выход — явное «Не сейчас» / «Остаться на текущем» / «Допройти trial».

## Типы пейволлов (примеры)

### Окончание trial
```
Trial заканчивается через 3 дня
Что потеряете: • полный доступ к функциям • продвинутые сценарии • прогресс/сертификаты
Что успели: • N ключевых действий, K результатов
[Продолжить со старшим тарифом — <цена>/мес]   [Спец-оффер: <цена>/мес]   [Напомнить позже]
```

### Фиче-лок (premium-функция)
```
[🔒] Функция «[название]» доступна на старшем тарифе
[превью сценария]
Функция помогает: • <выгода 1> • <выгода 2> • что включено
[Перейти на старший тариф — <цена>/мес]   [Может позже]
```

### Гейт флагманского продукта (разовый)
```
Флагманский продукт «[название]»
Формат A · Формат B · Формат C (индивидуально)
[превью программы]
[Выбрать формат]   [Узнать на бесплатной консультации]
```

## Тайминг и частота

- **Когда показывать:** после момента ценности, до фрустрации; после активации (первое ключевое действие); на финише trial.
- **Когда НЕ:** во время онбординга (рано), посреди ключевого действия, повторно после отказа.
- **Частота:** лимит на сессию, cool-down после dismiss (дни, не часы), отслеживать сигналы раздражения.

## Поток апгрейда

- **К оплате:** минимум шагов, по возможности in-context, предзаполнить известное.
- **RU-платежи:** через платёжный провайдер (напр. ЮKassa/CloudPayments). Поддержать СБП и карты МИР, промокоды, рефералку.
- **После апгрейда:** мгновенный доступ к функциям, подтверждение + чек (54-ФЗ для физлиц), гид по новым возможностям. Для B2B-когорт — счёт/договор с юрлицом РФ.

## Анти-паттерны

- **Тёмные паттерны:** спрятанная кнопка закрытия, путаный выбор плана, копия с чувством вины.
- **Убийцы конверсии:** просить до получения ценности (до первого ключевого действия); слишком частые промпты; блокировать действие посередине; усложнённый апгрейд.

## A/B-тесты

Что тестировать: тайминг триггера (день trial), заголовок/копию, подачу цены, спец-оффер vs обычный тариф, акцент функций, дизайн. Метрики: показы пейволла, CTR в апгрейд, completion, trial→paid, revenue per user, churn после апгрейда. Полный набор — `references/experiments.md`. Запуск — `ab-testing-ru`.

## Данные (НЕ дублировать)

- **Trial→paid конверсия, показы/клики пейволла, сегменты, revenue, апгрейды тарифов** → твоя веб-аналитика (Метрика/GA; счётчик — в `${CODEX_WORKSPACE}/.codex-context/business-context.md`) + продуктовая БД; платежи — вебхуки платёжного провайдера.
- **A/B-тесты** → `ab-testing-ru`.

## Связки

| Нужно | Скилл |
|------|-------|
| Данные конверсии/revenue | твоя веб-аналитика + платёжный сервис (оба — в `business-context.md` → «Учёт и аналитика») |
| Метрика (события) | `yandex` |
| Эксперименты | `ab-testing-ru` |
| Публичная страница тарифов | `page-cro-ru` |
| Структура цен/тарифов | `pricing-strategy-ru` |
| Cancel-флоу / save-офферы | `churn-prevention-ru` |
| Активация до апгрейда (trial) | `onboarding-cro-ru` |

## Вопросы под задачу

1. Текущая конверсия trial → paid?
2. Что триггерит промпты апгрейда сейчас?
3. Какие функции/сценарии за пейволлом (по тарифам)?
4. Какой «аха-момент» (первое ключевое действие)?
5. Модель цены (подписка по тарифам, разовый продукт, add-on)?
6. Веб, приложение/бот или всё вместе?
