---
name: "slack-gif-creator"
description: "Анимированные GIF под лимиты Slack (emoji 64KB): валидаторы и анимационные примитивы. Триггеры: «гифка для slack», «slack emoji»."
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


# Slack GIF Creator

Набор кубиков, а не готовых рецептов: валидаторы под ограничения Slack,
композируемые примитивы анимации и хелперы отрисовки. Как их сочетать — решай под
замысел.

## Ограничения Slack

|  | Message GIF | Emoji GIF |
|---|---|---|
| Максимальный размер | ~2 MB | **64 KB (жёстко)** |
| Размер кадра | 480×480 | 128×128 |
| FPS | 15–20 | 10–12 |
| Палитра | 128–256 цветов | 32–48 цветов |
| Длительность | 2–5 с | 1–2 с |

**Emoji — сложный случай.** 64 KB не обходятся ничем, кроме сокращения: 10–15
кадров всего, ≤48 цветов, простая композиция без градиентов (сплошные цвета
жмутся кратно лучше). Проверяй размер файла ПО ХОДУ работы, а не в конце: узнать
на двадцатом кадре, что не влезаешь, значит переделывать всю анимацию.

## Рабочий цикл

```python
from core.gif_builder import GIFBuilder
from core.validators import check_slack_size

builder = GIFBuilder(width=128, height=128, fps=10)
# ... добавляешь кадры любым способом: builder.add_frame(frame) ...
info = builder.save('emoji.gif', num_colors=48, optimize_for_emoji=True)
passes, details = check_slack_size('emoji.gif', is_emoji=True)
```

`save()` сам квантует палитру, выбрасывает дубли кадров и предупреждает о
превышении лимита; `info` возвращает `size_kb`, `frame_count`,
`duration_seconds`. Полная валидация — `validate_gif(path, is_emoji=True)`,
быстрая проверка — `is_slack_ready(path, is_emoji=True)`.

## Что уже написано

| Модуль | Что даёт |
|---|---|
| `templates/shake · bounce · spin · pulse · wiggle` | тряска, отскок, вращение/спиннер, пульс и «сердцебиение», желейное дрожание |
| `templates/move · slide · zoom · flip` | движение по прямой/дуге/окружности/волне, выезд с overshoot, наезд с motion blur, переворот двух объектов |
| `templates/fade · morph · explode · kaleidoscope` | появление/исчезание, кроссфейд и морфинг, взрыв/осколки/растворение и частицы, калейдоскоп и зеркала |
| `core/gif_builder` | сборка, квантование, выброс дублей, предупреждения о лимитах |
| `core/validators` | проверки размера, габаритов, полная валидация |
| `core/easing` | `interpolate(start, end, t, easing=...)`: `ease_in/out`, `bounce_out`, `elastic_out`, `back_out` |
| `core/frame_composer` | градиентный фон, эмодзи с тенью, фигуры, звёзды |
| `core/typography` | `draw_text_with_outline` — обводка, без неё текст на 128×128 нечитаем |
| `core/color_palettes` | готовые палитры: `vibrant`, `pastel`, `dark`, `neon`, `professional` |
| `core/visual_effects` | частицы (`ParticleSystem`), вспышка удара, ударные волны |

**Точные сигнатуры вызовов и примеры композиции → `references/primitives.md`.**
Открывай, когда берёшь конкретный примитив и нужен его набор аргументов. Каждый
хелпер можно заменить своим кодом — они не обязательны, обязательны только лимиты
Slack.

## Когда GIF не влезает

**Message (>2 MB):** меньше кадров (ниже FPS или короче) → меньше цветов (128 →
64) → меньше габарит (480 → 320) → включить выброс дублей.

**Emoji (>64 KB) — резать агрессивно:** 10–12 кадров всего, 32–40 цветов, убрать
градиенты, упростить композицию, `optimize_for_emoji=True` в `save()`.

Порядок именно такой: число кадров даёт самую большую экономию при наименьшей
потере смысла, габарит — самую заметную потерю.

## Как подходить к запросу

1. Понять замысел: что происходит и какое настроение.
2. Разбить на фазы — подготовка, действие, реакция. Без фаз анимация читается как
   дёрганье.
3. Собрать из примитивов, смешивая свободно.
4. Проверить лимиты, особенно для emoji.
5. Не влезло — сокращать по лестнице выше, а не пережимать палитру вслепую.

## Зависимости

Ставить, только если их ещё нет:

```bash
pip install pillow imageio numpy
```
