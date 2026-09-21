---
name: "gmeet"
description: "Google Meet (REST API v2): создание встреч, инфо, записи и участники конференций. Триггеры: «создай встречу meet», «ссылка на мит». Zoom → skill zoom; Телемост → yandex."
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


# Google Meet Operations

/gmeet - Работа с Google Meet

## Описание
Создание и управление видеовстречами через Google Meet REST API.

## Использование
```
/gmeet create [название]         - Создать встречу
/gmeet list                      - Записи конференций
/gmeet get <space_name>          - Информация о встрече
```

## Инструкции для Claude

1. **Загрузи credentials:**
```python
import os
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

with open(os.path.expanduser('${CODEX_PACK_ROOT}/library/google_oauth_token.json'), 'r') as f:
    token_data = json.load(f)
creds = Credentials.from_authorized_user_info(token_data)
meet = build('meet', 'v2', credentials=creds)
```

2. **Создать встречу:**
```python
# Открытая встреча (любой с ссылкой может войти)
space = meet.spaces().create(body={
    'config': {
        'accessType': 'OPEN',
        'entryPointAccess': 'ALL'
    }
}).execute()
print(f"Ссылка: {space.get('meetingUri')}")
print(f"ID: {space.get('name')}")
print(f"Код: {space.get('meetingCode')}")

# Ограниченная встреча (нужно подтверждение)
space = meet.spaces().create(body={
    'config': {
        'accessType': 'TRUSTED',
        'entryPointAccess': 'ALL'
    }
}).execute()
```

3. **Информация о встрече:**
```python
space = meet.spaces().get(name='spaces/abc123').execute()
print(f"URI: {space.get('meetingUri')}")
print(f"Config: {space.get('config')}")
```

4. **Записи конференций:**
```python
# Список прошедших конференций
records = meet.conferenceRecords().list(
    pageSize=25
).execute()
for record in records.get('conferenceRecords', []):
    print(f"{record['name']} | start: {record.get('startTime')} | end: {record.get('endTime')}")
```

5. **Участники конференции:**
```python
participants = meet.conferenceRecords().participants().list(
    parent='conferenceRecords/abc123',
    pageSize=50
).execute()
for p in participants.get('participants', []):
    print(f"{p.get('signedinUser', {}).get('displayName', 'Anonymous')}")
```

## Типы доступа
- `OPEN` - любой с ссылкой
- `TRUSTED` - только приглашённые / с подтверждением
- `RESTRICTED` - только приглашённые из организации

## Примеры
- `/gmeet create` - быстро создать ссылку на встречу
- `/gmeet list` - прошедшие конференции
- `/gmeet get spaces/abc123` - детали встречи
