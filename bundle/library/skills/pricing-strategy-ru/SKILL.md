---
name: "pricing-strategy-ru"
description: "Ценообразование и упаковка: тарифы, trial, value metric. Триггеры: «сколько брать за», «freemium». НЕ экраны апгрейда→paywall-cro-ru."
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


# Стратегия ценообразования (RU)

Спроектировать ценообразование продуктов (подписка/курс, воркшопы, консалтинг), которое захватывает ценность, двигает рост и соответствует готовности платить. Порт `pricing` из marketingskills: фреймворки (3 оси, value-based, value metric, good-better-best, методы исследования) сохранены; валюта, психология и примеры под рублёвый рынок.

**Перед началом прочитай `${CODEX_PACK_ROOT}/library/business-context.md`** — разделы «Продукт», «ICP», «Цены» (действующая линейка и валюта), «Экономика» (средний чек, CAC, LTV, отток) и «Позиционирование» (с кем тебя сравнивают). Файла нет — заведи из `${CODEX_PACK_ROOT}/library/templates/business-context.md`.

Без него навык назовёт цифру из воздуха: ценообразование — единственная тема, где правдоподобная выдумка сразу стоит денег. Пустые поля помечай `[TODO]` и уточняй, «не знаю» в файле — рабочее значение.

## Перед стартом — собрать контекст

Всё это лежит в `business-context.md`; если раздела там нет — заполни его сначала, потом возвращайся.

1. **Бизнес-контекст** (раздел «Продукт»): что продаёшь — подписка good-better-best, разовый флагман, корпоративный воркшоп, консалтинг, B2B-когорты, add-on. И какой GTM: self-serve B2C (trial), sales-led B2B (демо/консультация) или оба сразу.
2. **Ценность и конкуренты** (разделы «Продукт» → «Чем отличаешься» и «Позиционирование»): за что клиент реально платит и какая у него следующая лучшая альтернатива, включая «делать руками» и «не делать вовсе».
3. **Текущий перформанс** (раздел «Экономика»): конверсия trial→paid, ARPU, churn, что говорят о цене в отказах. Нет данных — так и напиши, навык построит вилку, а не точку.
4. **Цели:** первые продажи из имеющегося трафика / рост подписки / апселл в B2B — от цели зависит, двигать цену вверх или упаковку вниз.

## Основы

### Три оси ценообразования
1. **Упаковка** — что входит в каждый тариф (треки, симуляторы, поддержка/куратор, сертификаты).
2. **Value metric** — за что берёшь (подписка фикс, разовый курс, per-seat для когорт, проект для консалтинга).
3. **Price point** — сколько (конкретные суммы в рублях — из твоего контекста).

### Value-based pricing
Цена от ценности, не от себестоимости: воспринимаемая ценность клиента = потолок; цена между альтернативой и ценностью; следующая лучшая альтернатива = пол; себестоимость = только baseline. **Инсайт:** цена между следующей альтернативой (бесплатные туториалы / другой курс) и воспринимаемой ценностью (системное обучение + AI-тьютор + доступ к моделям + автор-практик).

## Value metric

То, за что берёшь, должно расти с получаемой ценностью.

| Метрика | Лучше для | Пример |
|---------|-----------|--------|
| Подписка (фикс/мес) | Непрерывный доступ к контенту | Basic/Plus/Pro |
| Разовый платёж | Завершаемый продукт | флагманский курс (Solo/Group) |
| За место/per-seat | Командное обучение | B2B-когорты от 5 человек |
| За проект | Кастомная работа | консалтинг (диагностика→внедрение) |
| Add-on | Доп-сервис | сопровождение/concierge |

Для линейки естественны гибриды: подписка (фикс по тарифу) + разовый флагман + per-seat для B2B-когорт + проектный консалтинг. Вопрос: «Чем больше клиент получает ценности, тем больше платит?» Да → хорошая метрика.

## Структура тарифов

### Good-Better-Best
- **Good = Basic:** вход, базовые треки, снять барьер.
- **Better = Plus (рекомендованный):** больше треков/симуляторов, якорная цена, где приземляется большинство; **founding-цена пожизненно для первых N** как acquisition-двигатель.
- **Best = Pro:** все треки включая флагман, максимум симуляторов, ~2x от Plus.
- **Над тарифами:** разовый флагман (Solo / Group / 1:1) + add-on + B2B-когорты.

### Дифференциация тарифов
Фиче-гейтинг (базовые vs premium-треки, флагман), доступ к симуляторам/AI-тьютору, поддержка (self → куратор для когорт), сертификаты, доступ к моделям, командная аналитика и SSO (B2B).

Детальные структуры, персоны, freemium/trial vs курс, B2B-когорты — `references/tier-structure.md`.

## Исследование цены

- **Van Westendorp** (4 вопроса): слишком дорого / слишком дёшево / дорого но рассмотрю / выгодно. Пересечения → оптимальная ценовая зона (особенно для калибровки воркшопа/консалтинга).
- **MaxDiff** (best-worst): какие треки/фичи ценят больше → информирует упаковку тарифов.
- Методы детально (+ Gabor-Granger, conjoint, usage-value correlation) — `references/research-methods.md`. Опросы — через `yandex` (Формы), бота или email-базу; данные использования — из аналитики продукта.

## Когда повышать цены

**Сигналы:** конкуренты подняли; не морщатся от цены; «так дёшево!»; высокая конверсия trial→paid (>40%); низкий churn (<3%/мес); добавлена значимая ценность (новые треки, симуляторы, флагман).
**Стратегии:** грандфатеринг существующих (founding-цена — пожизненно); отложенное повышение (анонс за 3-6 мес); привязка к ценности (поднять + добавить треки); реструктуризация планов.

## Лучшие практики страницы тарифов (кратко)

Above the fold: таблица сравнения Basic/Plus/Pro, рекомендованный (Plus) выделен, тумблер месяц/год (скидка), primary CTA «7 дней бесплатно» на каждый тариф. Элементы: сравнение треков/фич, для кого тариф, FAQ, founding-оффер, гарантия (trial без карты), отзывы участников, регалии автора.
**Психология (RU):** якорение (Pro первым / «дороже»); decoy (Plus = лучшая ценность); «charm pricing» с окончанием на 90 (X/Y/Z); founding-цена как срочность-дефицит (первые N). Конверсию самой страницы оптимизирует `page-cro-ru`.

## Чеклист

**До цен:** определены персоны (B2C-профи / соло-премиум / B2B-когорта); исследованы конкуренты (курсы, корп-тренинги); определён value metric по каждому продукту; проведено WTP-исследование (особенно воркшоп/консалтинг); треки/фичи замаплены на тарифы.
**Структура:** число тарифов (3 + разовый флагман + add-on); чёткая дифференциация; price points (подписка подтверждена, воркшоп/консалтинг откалибровать); стратегия годовой скидки; B2B-когорта/custom.

## Связки

| Нужно | Скилл |
|------|-------|
| Данные ARPU/конверсии/использования | `performance-analytics` |
| Опросы (Van Westendorp) / Метрика | `yandex` |
| Цены конкурентов (RU курсы/тренинги) | `competitive-analysis` |
| A/B-тест цен | `ab-testing-ru` |
| Конверсия страницы тарифов | `page-cro-ru` |
| In-app экраны апгрейда (Basic→Plus→Pro) | `paywall-cro-ru` |
| Cancel-флоу / годовая скидка как save | `churn-prevention-ru` |

## Вопросы под задачу

1. Какое исследование цены делали (особенно воркшоп/консалтинг)?
2. Текущие конверсия trial→paid и ARPU (по мере данных)?
3. Основной value metric для каждого продукта?
4. Главные ценовые персоны (B2C-профи / соло-премиум / B2B-когорта)?
5. Self-serve подписка, sales-led воркшоп/консалтинг или гибрид?
6. Какие изменения цен рассматриваете?

---

*Адаптировано из [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) (MIT), скилл pricing. Фреймворки сохранены; валюта, психология окончаний и примеры адаптированы под рублёвый рынок.*
