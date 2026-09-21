---
name: "telegram-bot-toolkit"
description: "Разработка Telegram-ботов: python-telegram-bot, Telethon, деплой; антипаттерн бот-воронки из TG Ads. Триггеры: «напиши бота», «deploy бота»."
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


# Telegram Bot Toolkit

Разработка, отладка и деплой Telegram-ботов на Python (python-telegram-bot,
Telethon).

> **Бота планируют как воронку из TG Ads?** Прочитай
> `references/tg-ads-bot-funnel.md` ДО написания кода: 80% бот-воронок из платного
> трафика убыточны, и правильный ответ — не «написать бота лучше», а поменять место
> бота в воронке (TG Ads → лендинг с регистрацией → бот для прогрева).
> Смежное: `telegram-ads-pro-ru`, `manychat-funnel-ru`.

## ConversationHandler: четыре поломки

Все четыре выглядят как «бот завис» и все четыре чинятся в объявлении хендлера.

1. **`per_user=True, per_chat=True`** — без них сцены разных юзеров лезут друг в
   друга, и баг проявляется только когда в боте больше одного человека, то есть на
   проде.
2. **`filters.TEXT & ~filters.COMMAND`** в состояниях. С голым `filters.TEXT`
   состояние съедает `/start` как обычный текст, и юзер не может выйти. Это и есть
   классическое «застрял в онбординге».
3. **Команды в `fallbacks`** (`/start`, `/cancel`) — аварийный выход из любого
   состояния. Без него единственный способ выйти — удалить чат.
4. **`per_message=False`**, если состояния ловят сообщения, а не callback-и.

## Порядок хендлеров

Группы обрабатываются по возрастанию, и порядок здесь не косметика: команда,
зарегистрированная после ConversationHandler, до неё просто не доходит.

```python
app.add_handler(MessageHandler(filters.ALL, log_all_updates), group=-1)   # видеть всё
app.add_handler(MessageHandler(filters.ALL, check_auth),      group=0)
app.add_handler(CommandHandler('start', start_command),       group=1)    # ДО conversation
app.add_handler(CommandHandler('help',  help_command),        group=1)
app.add_handler(conversation_handler,                          group=2)
app.add_handler(MessageHandler(filters.TEXT, unknown),        group=999)  # ловит остальное
```

## Callback queries

`await query.answer()` — **первой строкой** обработчика, до любой логики. Пока
callback не отвечен, у юзера крутится часик на кнопке, и он жмёт её ещё раз.

## Гонки и утечки

- **Критические секции** (баланс, платежи) — `asyncio.Lock` на `user_id`. Два
  быстрых сообщения от одного юзера обрабатываются параллельно, и списание
  проходит дважды.
- **`context.user_data.clear()`** при завершении conversation + периодическая
  чистка юзеров, у которых `last_seen` старше суток. Иначе в long-polling
  `user_data` растёт до перезапуска процесса.
- **`app.add_error_handler(...)`** обязателен: логировать с `exc_info=True` и
  ответить юзеру человеческим текстом с подсказкой `/start`. Без него ошибка
  выглядит как молчание бота.

## Деплой

- **Разработка** — `app.run_polling(allowed_updates=Update.ALL_TYPES)`.
- **Прод** — webhook: FastAPI-эндпоинт `POST /webhook`, внутри
  `Update.de_json(await request.json(), app.bot)` → `app.process_update(update)`,
  плюс `await app.bot.set_webhook(url=..., allowed_updates=Update.ALL_TYPES)`.
  Отдельный `GET /health` — для healthcheck контейнера.
- **Конфиг** — `pydantic_settings.BaseSettings` с `env_file=".env"`. Токен в коде
  не хранится никогда; в Docker передаётся через `environment`.

## Публичный LLM-бот: ловушки

Когда бот публичный (один токен — много юзеров) и управляется LLM с tool-calling,
стандартный wiki python-telegram-bot не покрывает ничего из этого списка.
Реализация каждого пункта → `references/multi-tenant-llm-bot.md`.

- **Секрет юзера (BYOK) не должен попасть в контекст LLM.** Оттуда он уедет в
  `history.jsonl` и во все последующие промпты. Перехватывать ввод FSM-флагом в
  `profile.json` ДО вызова агента, шифровать Fernet, в ответе не эхоить значение.
- **Данные — по папке на `tg_user_id`**, не глобальными таблицами: удаление юзера
  должно быть одной `rm -rf`, а не DELETE по десятку таблиц.
- **Shortcuts — reply keyboard, не inline.** Кнопка reply-клавиатуры приходит
  обычным текстом и идёт в тот же tool-routing, что и свободный ввод. У
  `callback_query` нет text content — это отдельный поток и отдельный роутинг.
  Inline оставить только для действий над конкретным объектом (✅ Опубликовать /
  ✏️ Edit), где нужен `callback_data`.
- **`parse_mode=HTML` + конвертер markdown→HTML.** LLM генерит `**bold**`;
  `Markdown` устарел, `MarkdownV2` требует экранировать `_*[]()~>#+-=|{}.!`.
  Без конвертера юзер видит буквальные звёздочки.
- **В memory писать `tool_calls`, а не только тексты.** Иначе следующий ход агента
  не помнит `draft_ts` / `job_id` из предыдущего tool-вызова.
- **`MSYS_NO_PATHCONV=1` при тестах из Git bash на Windows.** MSYS превращает
  `/start` в `C:/Program Files/Git/start` ДО запуска Python, и бот получает мусор:
  ```bash
  MSYS_NO_PATHCONV=1 python tg_client.py send @bot "/start"
  ```

## Telethon: каналы и лимиты

**Поиск реальных каналов** (вместо LLM-галлюцинаций) — MTProto `SearchRequest`:

```python
from telethon.tl.functions.contacts import SearchRequest
from telethon.tl.types import Channel

result = await client(SearchRequest(q=query, limit=limit))
chans = [c for c in result.chats
         if isinstance(c, Channel) and (c.broadcast or c.megagroup)]
```

Фильтр `broadcast or megagroup` нужен, чтобы попали и каналы, и супергруппы;
различать их потом по этим же полям.

**FloodWait.** `SearchRequest` и `iter_messages` под нагрузкой дают
`FloodWaitError(seconds=N)`. Ждать и ретраить при `e.seconds <= 20`, иначе падать
с человекочитаемой ошибкой «retry later». Плюс в system prompt агента:
`"Call discover_channels AT MOST 2 times per user message"` — без этого LLM
выпускает 6 запросов на одно сообщение юзера и flood-wait накапливается.

**`iter_messages` одинаков для channel и megagroup**, `get_entity(@username)`
резолвит оба. Разница в метриках: у супергруппы `msg.views = 0`, но есть
`msg.reactions`. Поэтому виральность считать по всем трём сигналам:

```python
virality = views + 3 * reactions + 5 * forwards
```

## Ссылки

- [python-telegram-bot docs](https://docs.python-telegram-bot.org/) ·
  [код-сниппеты wiki](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Code-snippets)
- [Telegram Bot API](https://core.telegram.org/bots/api) ·
  [Telethon docs](https://docs.telethon.dev/)
