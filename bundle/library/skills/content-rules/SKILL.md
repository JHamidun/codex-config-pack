---
name: "content-rules"
description: "Анти-слоп правила дизайна — что НЕ добавлять, чтобы не выглядело ИИ-выхлопом; проверка перед сдачей артефакта. Триггеры: «не лей воду в дизайн»."
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


# Content rules

Список того, чего избегать. Каждый пункт здесь — паттерн, который выдаёт ИИ-сгенерированный дизайн с первого взгляда.

## Не добавлять filler-контент

- **Никакого «lorem ipsum».** Если тема технологическая — пиши осмысленные технологические тезисы. Если про доставку — про доставку.
- **Никаких выдуманных метрик.** «43% увеличение конверсии» без источника = ложь. Если данных нет — не показывай числа.
- **Не плоди секции** «Why us / Features / Testimonials / FAQ» автоматом. Только то, что просили или явно нужно.
- **Не добавляй CTA «Get started»** на каждый блок. Один на лендинг, может два.

## Анти-визуальные клише

- ❌ Карточка с цветной полоской слева (`border-left: 4px solid var(--accent)`).
- ❌ Иконка размером 24px рядом с каждым пунктом списка.
- ❌ Градиентный фон без причины (особенно фиолетово-розовый).
- ❌ Hero-секция с фразой «Welcome to <product>».
- ❌ Картинка-плейсхолдер с надписью «Image» в сером прямоугольнике.
- ❌ Три иконки в ряд под заголовком "Features", все с одинаковыми абстрактными SVG.
- ❌ Иконка «галочка в зелёном круге» рядом с пунктами.
- ❌ Заголовок + 4 одинаковых блока с иконками («наши преимущества»).
- ❌ Полупрозрачный градиент-туман на фоне.
- ❌ Стеклянная карточка с `backdrop-filter: blur` (если это не часть бренда).

## Шрифтовые клише

- ❌ Inter повсюду (стало generic).
- ❌ Roboto, Arial, system-ui без причины.
- ❌ Fraunces везде, где «нужно красиво».
- ❌ Заглавный display-шрифт + Inter в теле — самая узнаваемая ИИ-пара.
- ❌ Заголовок 24px и тело 16px — слишком одинаково. Делай разрыв минимум 2x.

## Эмодзи

- ❌ ✨ 🚀 💡 🎯 🔥 в заголовках и пунктах.
- ✓ Эмодзи допустимы, **только если они часть бренда** или явно просили.

## Иконография

- ❌ Не рисуй сложные SVG-иллюстрации руками. Получится плохо.
- ❌ Не вставляй 12 разных «Lucide-style» иконок там, где хватит 3 текстовых заголовков.
- ✓ Если иконка нужна — используй placeholder с подписью, попроси у пользователя реальные ассеты.

## Текст

- ❌ Слова-паразиты: «seamless», «cutting-edge», «next-generation», «empower», «leverage», «революционный», «инновационный», «бесшовный».
- ❌ «We help X to Y by Z» — формула из всех маркетинг-сайтов 2018-2024.
- ❌ Маркированные списки длиннее 5 пунктов.
- ❌ Списки, в которых каждый пункт начинается с одного и того же слова.
- ✓ Конкретность бьёт абстракцию. «Загружайте 1000 файлов одной командой» лучше, чем «Эффективная работа с большими массивами данных».

## Композиция

- ❌ Один и тот же layout на всех слайдах.
- ❌ Идеальная симметрия везде. Намеренная асимметрия читается как работа человека.
- ❌ Центрирование длинных абзацев.
- ❌ Заголовок ровно посередине между верхом и контентом — выглядит как Word.

## Когда нечего сказать

Если тебе нечем заполнить секцию — это сигнал, что секция лишняя. **Удаляй**, не наполняй ватой.

Лучше 4 насыщенных слайда, чем 12 жидких.

## Финальный фильтр

Перед сдачей пройди артефакт и спроси о каждом элементе:
1. Зачем он здесь?
2. Что станет хуже, если его убрать?
3. Если ответ «ну, симметричнее будет» — убирай.

«One thousand no's for every yes». Каждое «да» что-то добавить должно быть осознанным.
