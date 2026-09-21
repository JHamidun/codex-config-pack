---
name: "gchat"
description: "Google Chat: пространства, чтение и отправка сообщений, карточки (Chat API). Триггеры: «гугл чат», «напиши в google chat»."
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


# Google Chat Operations

/gchat - Работа с Google Chat

## Описание
Просмотр пространств, чтение и отправка сообщений через Google Chat API.

## Использование
```
/gchat spaces                    - Список пространств (чатов)
/gchat messages <space_id>       - Сообщения из пространства
/gchat send <space_id> <текст>   - Отправить сообщение
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
chat = build('chat', 'v1', credentials=creds)
```

2. **Список пространств:**
```python
results = chat.spaces().list(pageSize=50).execute()
for space in results.get('spaces', []):
    stype = space.get('type', '')
    name = space.get('displayName', space.get('name'))
    print(f"{space['name']} | {stype} | {name}")
```

3. **Сообщения из пространства:**
```python
results = chat.spaces().messages().list(
    parent='spaces/AAAA_bbbb',
    pageSize=25,
    orderBy='createTime desc'
).execute()
for msg in results.get('messages', []):
    sender = msg.get('sender', {}).get('displayName', 'Unknown')
    text = msg.get('text', '')
    created = msg.get('createTime', '')
    print(f"[{created}] {sender}: {text}")
```

4. **Отправить сообщение:**
```python
result = chat.spaces().messages().create(
    parent='spaces/AAAA_bbbb',
    body={'text': 'Привет! Это сообщение из Claude Code.'}
).execute()
print(f"Отправлено: {result['name']}")
```

5. **Сообщение с карточкой:**
```python
result = chat.spaces().messages().create(
    parent='spaces/AAAA_bbbb',
    body={
        'cardsV2': [{
            'cardId': 'status-card',
            'card': {
                'header': {'title': 'Статус деплоя', 'subtitle': 'Production'},
                'sections': [{
                    'widgets': [{
                        'decoratedText': {
                            'topLabel': 'Статус',
                            'text': 'Успешно развёрнуто'
                        }
                    }]
                }]
            }
        }]
    }
).execute()
```

6. **Участники пространства:**
```python
members = chat.spaces().members().list(
    parent='spaces/AAAA_bbbb',
    pageSize=100
).execute()
for m in members.get('memberships', []):
    print(f"{m.get('member', {}).get('displayName', '')} | {m.get('role', '')}")
```

## Типы пространств
- `ROOM` - именованное пространство (группа)
- `DM` - личное сообщение
- `GROUP_CHAT` - групповой чат

## Примеры
- `/gchat spaces` - все мои чаты
- `/gchat messages spaces/AAAA_bbbb` - последние сообщения
- `/gchat send spaces/AAAA_bbbb "Деплой завершён"` - написать в чат
