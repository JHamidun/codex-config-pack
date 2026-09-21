---
name: "gcalendar"
description: "Google Calendar (gcal_client.py): события сегодня/неделя, создание. Триггеры: «календарь», «что по расписанию», «свободные слоты». Токен: google_oauth_token_calendar.json."
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


# Google Calendar Operations

> Готовый клиент: `python ${CODEX_PACK_ROOT}/library/skills/google-workspace/scripts/gcal_client.py {today|week|list|free|add|calendars}` — проверен на живом календаре.
> Права ТОЛЬКО в `google_oauth_token_calendar.json`. В общем `google_oauth_token.json`
> календарных прав нет: именно из-за этой строки поднимали авторизацию заново.


/gcalendar - Работа с Google Календарём

## Описание
Просмотр, создание и управление событиями в Google Calendar.

## Использование
```
/gcalendar today              - События на сегодня
/gcalendar week               - События на неделю
/gcalendar list [дней]        - События на N дней
/gcalendar create <событие>   - Создать событие
/gcalendar free               - Свободные слоты
```

## Инструкции для Claude

1. **Загрузи credentials:**
```python
import json
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

with open('${CODEX_PACK_ROOT}/library/google_oauth_token_calendar.json', 'r') as f:
    token_data = json.load(f)
creds = Credentials.from_authorized_user_info(token_data)
calendar = build('calendar', 'v3', credentials=creds)
```

2. **Получить события:**
```python
now = datetime.utcnow().isoformat() + 'Z'
end = (datetime.utcnow() + timedelta(days=7)).isoformat() + 'Z'

events_result = calendar.events().list(
    calendarId='primary',
    timeMin=now,
    timeMax=end,
    maxResults=50,
    singleEvents=True,
    orderBy='startTime'
).execute()
events = events_result.get('items', [])

for event in events:
    start = event['start'].get('dateTime', event['start'].get('date'))
    print(f"{start}: {event['summary']}")
```

3. **Создать событие:**
```python
event = {
    'summary': 'Встреча с командой',
    'location': 'Zoom',
    'description': 'Обсуждение проекта',
    'start': {
        'dateTime': '2025-12-22T10:00:00',
        'timeZone': YOUR_TIMEZONE,  # например 'Europe/Berlin'
    },
    'end': {
        'dateTime': '2025-12-22T11:00:00',
        'timeZone': YOUR_TIMEZONE,  # например 'Europe/Berlin'
    },
    'reminders': {
        'useDefault': False,
        'overrides': [
            {'method': 'popup', 'minutes': 10},
        ],
    },
}
event = calendar.events().insert(calendarId='primary', body=event).execute()
```

4. **Список календарей:**
```python
calendar_list = calendar.calendarList().list().execute()
for cal in calendar_list.get('items', []):
    print(f"{cal['summary']} ({cal['id']})")
```

5. **Удалить событие:**
```python
calendar.events().delete(calendarId='primary', eventId=event_id).execute()
```

## Форматы времени
- Полное: `2025-12-22T10:00:00+03:00`
- Весь день: `2025-12-22` (без времени)
- TimeZone: свой пояс или `UTC`

## Примеры
- `/gcalendar today` - что запланировано на сегодня
- `/gcalendar week` - расписание на неделю
- `/gcalendar create "Созвон в 15:00 завтра"` - создать событие
