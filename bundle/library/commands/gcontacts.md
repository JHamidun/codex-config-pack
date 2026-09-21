---
name: "gcontacts"
description: "Google Контакты (People API): список, поиск, детали, создание. Триггеры: «найди контакт», «телефон из контактов»."
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


# Google Contacts Operations

/gcontacts - Работа с Google Контактами

## Описание
Просмотр, поиск и создание контактов через Google People API.

## Использование
```
/gcontacts list [количество]     - Список контактов
/gcontacts search <запрос>       - Поиск контактов
/gcontacts get <resourceName>    - Детали контакта
/gcontacts create <имя> <email>  - Создать контакт
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
people = build('people', 'v1', credentials=creds)
```

2. **Список контактов:**
```python
results = people.people().connections().list(
    resourceName='people/me',
    pageSize=100,
    personFields='names,emailAddresses,phoneNumbers,organizations'
).execute()
connections = results.get('connections', [])

for person in connections:
    names = person.get('names', [{}])
    name = names[0].get('displayName', 'Без имени') if names else 'Без имени'
    emails = [e['value'] for e in person.get('emailAddresses', [])]
    phones = [p['value'] for p in person.get('phoneNumbers', [])]
    print(f"{name} | {', '.join(emails)} | {', '.join(phones)}")
```

3. **Поиск контактов:**
```python
results = people.people().searchContacts(
    query='Иван',
    readMask='names,emailAddresses,phoneNumbers',
    pageSize=10
).execute()
for result in results.get('results', []):
    person = result.get('person', {})
    name = person.get('names', [{}])[0].get('displayName', '')
    print(name)
```

4. **Создать контакт:**
```python
contact = people.people().createContact(body={
    'names': [{'givenName': 'Иван', 'familyName': 'Петров'}],
    'emailAddresses': [{'value': 'user@example.com'}],
    'phoneNumbers': [{'value': '+1234567890'}],
    'organizations': [{'name': 'Company', 'title': 'Manager'}]
}).execute()
print(f"Создан: {contact['resourceName']}")
```

5. **Детали контакта:**
```python
person = people.people().get(
    resourceName='people/c1234567890',
    personFields='names,emailAddresses,phoneNumbers,organizations,addresses,birthdays'
).execute()
```

## personFields (доступные поля)
- `names` - ФИО
- `emailAddresses` - email
- `phoneNumbers` - телефоны
- `organizations` - компании
- `addresses` - адреса
- `birthdays` - дни рождения
- `urls` - ссылки
- `biographies` - заметки

## Примеры
- `/gcontacts list 20` - первые 20 контактов
- `/gcontacts search "Company"` - поиск по Company
- `/gcontacts create "John Doe" "user@example.com"` - новый контакт
