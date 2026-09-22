---
name: "popup-cro-ru"
description: "Попапы, модалки, баннеры: захват email на news.your-domain.com, exit-intent. Триггеры: «всплывающее окно», «sticky bar». НЕ формы вне попапов→form-cro-ru."
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


# CRO попапов и модалок (RU)

Попапы, которые конвертят, не раздражая и не убивая доверие к бренду. Порт `popups` из marketingskills: триггеры, типы, дизайн и частоты сохранены; согласие/приватность переведены с GDPR на 152-ФЗ.

**Перед началом прочитай `${CODEX_WORKSPACE}/.codex-context/business-context.md`** (заведи из `${CODEX_PACK_ROOT}/library/templates/business-context.md`, если файла ещё нет) — лид-магниты, trial продукта, карта воронки. **Частый приоритет — закрыть дыру воронки, где контент-портал не связан с продуктом/консультацией.** Если портал гонит трафик только на соцсети и блог — попапы должны захватывать email и сквозным CTA вести в середину воронки (trial продукта / бесплатная консультация).

## Первичная оценка

1. **Цель попапа:** email-подписка на рассылку, лид-магнит (скачивание), баннер trial продукта, exit-intent save, анонс воркшопа/вебинара, фидбэк/опрос.
2. **Текущее состояние:** перформанс существующих попапов, триггеры, жалобы, мобильный опыт.
3. **Контекст трафика:** источники (Директ/органика/прямой/соцсети), новые vs вернувшиеся, типы страниц (портал vs блог vs лендинг услуг).

## Базовые принципы

1. **Тайминг решает.** Слишком рано = раздражает; слишком поздно = упущено; вовремя = полезный оффер в момент нужды.
2. **Ценность очевидна.** Чёткая немедленная выгода, релевантная контексту страницы, стоящая прерывания.
3. **Уважать пользователя.** Легко закрыть, не запирать/обманывать, помнить предпочтения, не портить опыт.

## Стратегии триггеров

- **По времени:** не «через 5 сек» — лучше 30-60 сек (доказанная вовлечённость).
- **По скроллу:** 25-50% глубины — индикатор вовлечённости; для блога/новостных лонгридов.
- **Exit-intent:** курсор к закрытию/уходу — последний шанс; для лидгена (email + лид-магнит). На мобайле — back/scroll up.
- **По клику:** пользователь инициирует (кнопка/ссылка) — ноль раздражения; для лид-магнитов, гейтед-контента.
- **По числу страниц/сессии:** после X статей — поведение вовлечённого читателя → апсейл в продукт.
- **По поведению:** посетители лендинга услуг/воркшопа, повторные визиты — высокий интент.

## Типы попапов

- **Email-захват (рассылка):** чёткий value prop (не «Подписаться»), конкретная выгода («полезное раз в неделю, кратко»), одно поле, опц. стимул-лид-магнит. Сабмит → эндпоинт подписки → таблица подписчиков.
- **Лид-магнит:** показать, что дают (обложка/превью), конкретное обещание (чек-лист, подборка инструментов, гайд), минимум полей, мгновенная доставка.
- **Баннер trial продукта (фикс дыры портал→продукт):** на портале/блоге «Освоить системно → trial бесплатно», sticky или slide-in.
- **Exit-intent:** признать уход, другой оффер чем на входе (лид-магнит / trial / бесплатная консультация), закрыть возражение, финальная причина остаться.
- **Анонс воркшопа/вебинара:** верх страницы (sticky/static), одно сообщение, dismissable, ограниченный по времени.
- **Слайд-ин:** из угла/снизу, не блокирует контент, легко свернуть; для CTA продукта, чата/AI-ассистента, вторичных CTA.

## Дизайн

- **Иерархия:** заголовок (крупнейший) → value prop/оффер → форма/CTA → закрытие.
- **Размер:** десктоп 400-600px, не на весь экран; мобайл — full-width снизу или центр, не fullscreen.
- **Кнопка закрытия:** видимый X (правый верх), крупная на тач, «Нет, спасибо» как альтернатива, клик вне = закрыть. Кто не нашёл закрытие — уйдёт совсем.
- **Мобайл:** нет exit-intent (альтернативы), bottom slide-up работает, крупные таргеты, лёгкие жесты dismiss.

## Частота и правила

- **Капинг:** максимум 1 раз за сессию, помнить dismiss (cookie/localStorage), 7-30 дней до повтора.
- **Таргетинг:** новые vs вернувшиеся, по источнику, по типу страницы, исключить уже подписавшихся и недавно закрывших.
- **Правила страниц:** исключить чекаут/конверсионные флоу, оффер под контекст страницы (на статье про презентации → лид-магнит «инструменты для презентаций»).

## Комплаенс и доступность (RU)

- **152-ФЗ (ключевое для захвата данных):** явное согласие на обработку ПД (не пред-отмеченный чекбокс), ссылка на политику обработки ПД, честная отписка от рассылки. Реклама воркшопа в попапе → маркировка по 38-ФЗ при необходимости.
- **Доступность:** клавиатурная навигация (Tab/Enter/Esc), focus trap, скринридеры, контраст, не только цвет.
- **Поисковые гайдлайны:** интрузивные интерстишелы вредят SEO (особенно мобайл, критично для контентного трафика) — избегать fullscreen до контента на мобайле; cookie/152-ФЗ-уведомления и разумные баннеры допустимы.

## Измерение

- **Метрики:** impression rate, conversion rate (показы → сабмиты), close rate, engagement rate, time to close.
- **Бенчмарки:** email-попап 2-5%; exit-intent 3-10%; click-triggered выше (10%+).
- Данные — твоя веб-аналитика (Метрика/GA: цель на сабмит попапа; счётчик — в `${CODEX_WORKSPACE}/.codex-context/business-context.md`) + таблица подписчиков.

## Формат вывода

- **Дизайн попапа:** тип, триггер, таргетинг, частота, копия (заголовок/подзаголовок/CTA/отказ), дизайн-заметки.
- **Стратегия нескольких попапов:** цель/триггер/аудитория каждого + правила конфликтов.
- **Гипотезы для A/B** — через `ab-testing-ru`.

## References (читать по необходимости)

- `references/copy-and-experiments.md` — формулы копирайта (заголовки, подзаголовки, CTA, отказы), стратегии по типам бизнеса (захват email, лид-магниты, trial продукта, B2B-консультация), полный набор A/B-экспериментов (размещение/формат, триггеры, месседжинг, персонализация, частота).

## Связки

| Нужно | Скилл |
|------|-------|
| Оптимизация формы внутри попапа | `form-cro-ru` |
| Контекст страницы вокруг попапа | `page-cro-ru` |
| Что после конверсии (письма/nurture) | `html-email`, `n8n` |
| Данные конверсии попапа | твоя веб-аналитика (Метрика/GA) |
| Эксперименты | `ab-testing-ru` |

## Вопросы под задачу

1. Главная цель попапа (email-захват / лид-магнит / trial продукта / консультация)?
2. Текущий перформанс (если есть)?
3. Под какие источники трафика (портал / блог / лендинг услуг)?
4. Какой стимул можешь дать (какой лид-магнит)?
5. Требования 152-ФЗ (захват ПД)?
6. Mobile vs desktop сплит?
