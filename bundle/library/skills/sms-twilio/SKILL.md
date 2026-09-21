---
name: "sms-twilio"
description: "SMS через Twilio (CLI sms_client.py): bulk с dry-run, статус доставки, баланс. Триггеры: «отправь смс». НЕ Telegram → tg-bot-publish."
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


# SMS via Twilio

CLI-коннектор к Twilio REST API (`https://api.twilio.com/2010-04-01`). Без twilio-SDK — `requests` (стоит) или stdlib urllib fallback. Подключился → сделал → напечатал → вышел.

**Файл:** `${CODEX_PACK_ROOT}/library/tools/sms_client.py`

## Когда использовать

- Отправить SMS одному получателю или списку (bulk с анти-спам гардами)
- Проверить статус доставки (queued/sent/delivered/failed)
- Посмотреть историю сообщений, баланс, номера аккаунта
- Понять, как принять входящие SMS (webhook-инструкция)

## Установка / настройка

**Пак приезжает без кредов** — Twilio платный, аккаунт заводится свой. Добавь в `${CODEX_PACK_ROOT}/library/.credentials.master.env` (образец — `${CODEX_PACK_ROOT}/library/templates/.credentials.master.env.example`):

- `TWILIO_ACCOUNT_SID` — начинается с `AC`, Twilio Console → Account Info
- `TWILIO_AUTH_TOKEN` — там же
- `TWILIO_PHONE_NUMBER` — купленный SMS-capable номер в E.164 (`+1555...`)

Без кредов CLI не падает — печатает, что именно добавить (exit 2). Зависимостей ставить не нужно (`requests` уже есть; без него — urllib).

Регистрация: https://console.twilio.com → купить SMS-capable номер (~$1-1.15/мес US).

## Команды

| Команда | Что делает |
|---------|-----------|
| `send <to> <text> [--from +1...] [--json]` | Одно SMS. `to` в E.164. Печатает SID |
| `bulk <file> <text> [--rate 2.0] [--limit 50] [--confirm] [--json]` | Рассылка по файлу (1 номер/строка, `#`=коммент). **По умолчанию DRY-RUN**; реальная отправка только с `--confirm`. Джиттер `rate + 0..50%`, cap `--limit` (деф. 50), дедуп номеров |
| `status <sid> [--json]` | Статус доставки по Message SID (SM…) + error_code если fail |
| `list [--limit 20] [--to +...] [--from +...] [--json]` | Последние сообщения (входящие+исходящие) с ценой |
| `balance [--json]` | Баланс аккаунта |
| `numbers [--json]` | Номера аккаунта с capabilities (sms/voice/mms) |
| `receive-webhook` | Инструкция как поднять приём входящих (сервер НЕ стартует) |

## Примеры

```bash
# одно SMS (from = TWILIO_PHONE_NUMBER)
python ${CODEX_PACK_ROOT}/library/tools/sms_client.py send +15551234567 "Тест"

# рассылка: сначала dry-run (дефолт), потом реальная
python ${CODEX_PACK_ROOT}/library/tools/sms_client.py bulk numbers.txt "Текст всем"
python ${CODEX_PACK_ROOT}/library/tools/sms_client.py bulk numbers.txt "Текст всем" --confirm --rate 3

# статус и история
python ${CODEX_PACK_ROOT}/library/tools/sms_client.py status SMxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
python ${CODEX_PACK_ROOT}/library/tools/sms_client.py list --limit 10 --json
```

## Стоимость и согласие получателей

- **Оплата за сегмент**: GSM-7 — 160 симв./сегмент, **кириллица = UCS-2 — 70 симв./сегмент**. Русский текст в 3 раза «дороже на символ». Порядок величин: US ~$0.0083 за сегмент, большинство стран Латинской Америки и ЕС в 4-8 раз дороже, РФ дороже всех и часто фильтруется операторами. Точные цены смотри на twilio.com/sms/pricing для СВОЕЙ страны отправки — они меняются.
- **Trial-аккаунт**: слать можно ТОЛЬКО на verified-номера (ошибка 21608), к тексту добавляется префикс «Sent from your Twilio trial account».
- **Согласие (opt-in) обязательно**: слать только тем, кто дал согласие на SMS; включать способ отписки (STOP). Массовый спам = блок аккаунта Twilio + нарушение TCPA (США) / GDPR (ЕС) / LGPD (Бразилия) / 152-ФЗ (РФ). A2P 10DLC-регистрация нужна для массовых отправок на US-номера.
- Мобильные вне США (в частности РФ и Бразилия) принимают SMS с международных номеров нестабильно — операторские фильтры режут молча. Прежде чем закладывать канал в продукт, проверь доставку на реальный номер своей страны.

## Гочи

- Номера ТОЛЬКО в E.164 (`+5511...`) — без плюса Twilio вернёт 21211.
- `bulk` без `--confirm` = всегда dry-run; это фича, не баг. Cap 50 получателей — поднимать `--limit` осознанно.
- Error 21608 = trial + неверифицированный получатель; 21606 = From-номер не SMS-capable.
- `status` сразу после `send` часто показывает `queued`/`sent` — `delivered` приходит через секунды-минуты, перепроверить позже.
- Кириллица режет лимит сегмента до 70 симв. — длинный русский текст = много сегментов = дороже.
- Приём входящих требует публичный HTTPS-webhook + валидацию `X-Twilio-Signature`. Сервер не писать с нуля — взять `${CODEX_PACK_ROOT}/library/tools/webhook_server.py` (навык `webhook-receiver`), но **подпись он за тебя не проверит**: у Twilio своя схема (HMAC-SHA1 по URL + отсортированным POST-параметрам, base64), а не HMAC-SHA256 по телу, как у GitHub/Stripe. Значит `--provider none` + своя валидация (`twilio.request_validator.RequestValidator` или ~15 строк на `hmac`). Без валидации любой, кто узнал URL, подсунет фальшивое входящее.
- Endpoints `Balance.json` и `IncomingPhoneNumbers.json` — стандартные Twilio 2010-04-01, но на живом аккаунте в этой сборке не прогонялись. Считай их «требует проверки» при первом запуске: расхождение с докой Twilio возможно.

## Чек-лист

- [ ] Креды в `${CODEX_PACK_ROOT}/library/.credentials.master.env` (3 переменные выше)
- [ ] `numbers` — убедиться что есть SMS-capable номер
- [ ] `balance` — хватает ли денег
- [ ] Для bulk: список = только opt-in получатели, есть STOP-механика
- [ ] Bulk: сначала dry-run, глазами проверить список, потом `--confirm`
- [ ] После отправки: `status <sid>` → дождаться `delivered`
