---
name: "gtasks"
description: "Google Tasks: списки задач, создание/завершение, дедлайны. Триггеры: «задачи google», «добавь задачу в google». Todoist → /gtd."
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


# Google Tasks Operations

/gtasks - Работа с Google Tasks

## Описание
Управление задачами и списками задач через Google Tasks API.

## Использование
```
/gtasks lists                     - Списки задач
/gtasks tasks <list_id>           - Задачи из списка
/gtasks create <список> <задача>  - Создать задачу
/gtasks complete <list_id> <id>   - Завершить задачу
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
tasks = build('tasks', 'v1', credentials=creds)
```

2. **Списки задач:**
```python
results = tasks.tasklists().list(maxResults=20).execute()
for tl in results.get('items', []):
    print(f"{tl['id']}: {tl['title']}")
```

3. **Задачи из списка:**
```python
results = tasks.tasks().list(
    tasklist='list_id_here',
    showCompleted=False,
    showHidden=False,
    maxResults=50
).execute()
for task in results.get('items', []):
    due = task.get('due', 'без срока')
    notes = task.get('notes', '')
    print(f"[{task['status']}] {task['title']} | {due}")
```

4. **Создать задачу:**
```python
task = tasks.tasks().insert(
    tasklist='list_id_here',
    body={
        'title': 'Подготовить отчёт',
        'notes': 'Детали задачи',
        'due': '2026-03-15T00:00:00.000Z'
    }
).execute()
print(f"Создана: {task['id']}")
```

5. **Завершить задачу:**
```python
task = tasks.tasks().get(tasklist='list_id', task='task_id').execute()
task['status'] = 'completed'
tasks.tasks().update(
    tasklist='list_id',
    task='task_id',
    body=task
).execute()
```

6. **Создать новый список:**
```python
new_list = tasks.tasklists().insert(
    body={'title': 'Проект YourProduct'}
).execute()
print(f"Список: {new_list['id']}")
```

## Статусы задач
- `needsAction` - не выполнена
- `completed` - завершена

## Примеры
- `/gtasks lists` - все списки задач
- `/gtasks tasks MTxxxxxxxx` - задачи конкретного списка
- `/gtasks create default "Позвонить клиенту"` - задача в дефолтный список
- `/gtasks complete MTxx task_id` - отметить выполненной
