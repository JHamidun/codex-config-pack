---
name: "content-policy"
description: "Что НЕ воспроизводить: защищённые UI крупных продуктов, бренды, шрифты, brand-цвета. Триггеры: «сделай как в Notion», «можно ли копировать интерфейс»."
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


# Content policy

Защищённые элементы интерфейсов и бренды нельзя копировать 1-в-1, даже если технически легко. Это касается команды, которая раздаёт скиллы — нарушение может прилететь как претензия.

## Что нельзя без явного подтверждения

### 1. Distinctive UI крупных продуктов
- **Slack** — кастомный composer, sidebar с workspaces.
- **Notion** — block editor с slash-меню.
- **Linear** — keyboard-first command palette + tickets.
- **Figma** — canvas с layers panel в специфичной компоновке.
- **Gmail/Outlook** — список тредов + chrome.
- **VS Code** — file explorer + tabs + status bar.

Если юзер просит «как в Slack» — спроси: «Ты работаешь в Slack или это для своего продукта? Если для своего — сделаю **похожий по принципам** (channel-based чат), но **не клон**».

### 2. Брендированные графические элементы
- Логотипы (Apple, Google, Meta и т.д.).
- Иконки с защищёнными формами (Apple Music, Spotify glyph).
- Маскоты (GitHub Octocat, Figma F).

Не рисуй SVG-копии. Используй placeholder.

### 3. Защищённые шрифты
- **SF Pro** — только в Apple-продуктах. Не Apple — `Inter` / `System UI`.
- **Roboto** — Apache 2.0, можно везде, но не имитируй Material Design 1-в-1.
- Корпоративные кастомные (Söhne, GT America) — лицензируются за деньги.

См. `license-check` — пробежать по странице перед финишем.

### 4. Защищённые цвета
Brand-цвета компаний охраняются tradedress-ом. Slack-фиолетовый, Spotify-зелёный, Tiffany-голубой. Не используй именно их в копии чужих интерфейсов.

## Исключение — domain check

Если у юзера email в домене компании — допустимо: значит, он там работает, и работает над их продуктом.

```
gmail.com → нельзя копировать UI Slack
slack.com → можно делать макет для Slack-команды
notion.so → можно работать с Notion UI
```

Если домен не виден — спроси.

## Что **можно** делать

- ✅ **Вдохновляться паттернами**. Slash-меню, command palette, kanban, three-pane email — это паттерны, не интеллектуальная собственность.
- ✅ **Описывать, как «похоже на ...»** — это допустимо в диалоге, не в производстве.
- ✅ **Делать собственный продукт** в той же категории. Свой логотип, свои цвета, своя копирайт.
- ✅ **Recreating own work** — если юзер показывает свой проект и просит recreate своего же UI.

## Промпт-формула при сомнении

Когда юзер просит «как в X»:

1. Уточни: «Ты работаешь в X / делаешь X / делаешь конкурента X?»
2. Если конкурент — «Сделаю по тем же принципам, но визуально отличающимся». Свои цвета, свои шрифты, свой layout.
3. Если работает в X — попроси email-домен или скриншот их Figma-доступа в подтверждение.
4. Если просто фанат — мягкий отказ: «Не могу сделать клон. Могу сделать свой вариант в той же категории».

## Тон отказа

Не моралистично, по делу:

> «UI Linear защищён tradedress'ом. Сделать клон не могу. Если у тебя своя продакт-задача типа issue tracker — сделаю похожее по структуре, но с твоим брендом и собственной композицией. Расскажи, что у тебя?»

## Чего ещё избегать

- Графики «10 крупных компаний используют наш продукт» с настоящими логотипами без разрешения.
- Скриншоты конкурентов в питч-деке без атрибуции.
- Use-case-карточки с реальными именами/фото без указания «mock».

## После решения сделать

- Подпиши в комментарии HTML: `<!-- Inspired by patterns from <X>; not a copy. Custom brand. -->`.
- Не выдавай за чужое. Не пиши «ваш Slack-клон» в дек.

## License-check рядом

После генерации — `license-check` пробежит по картинкам/шрифтам и подсветит проблемные. Не панацея, но снимает 80% случайных нарушений.
