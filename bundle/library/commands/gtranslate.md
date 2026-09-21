---
name: "gtranslate"
description: "Google Cloud Translation v2: перевод текста и батчей, определение языка. Триггеры: «переведи через google», «определи язык». Качественный перевод → /translate."
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


# Google Cloud Translation Operations

/gtranslate - Работа с Google Cloud Translation API

## Описание
Перевод текста, определение языка и список поддерживаемых языков через Translation API v2.

## Использование
```
/gtranslate translate <текст> <язык>  - Перевести текст
/gtranslate detect <текст>            - Определить язык
/gtranslate languages                 - Поддерживаемые языки
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
translate = build('translate', 'v2', credentials=creds)
```

2. **Перевести текст:**
```python
result = translate.translations().list(
    q='Hello, how are you?',
    target='ru'
).execute()
for t in result.get('translations', []):
    print(f"Перевод: {t['translatedText']}")
    print(f"Исходный язык: {t.get('detectedSourceLanguage', 'указан')}")
```

3. **Перевести с указанием исходного языка:**
```python
result = translate.translations().list(
    q='Привет, мир!',
    source='ru',
    target='en'
).execute()
print(result['translations'][0]['translatedText'])
```

4. **Перевести несколько текстов:**
```python
result = translate.translations().list(
    q=['Привет', 'Как дела?', 'Спасибо'],
    target='pt'
).execute()
for t in result['translations']:
    print(t['translatedText'])
```

5. **Определить язык:**
```python
result = translate.detections().list(
    q='Bonjour le monde'
).execute()
for detection in result['detections']:
    for d in detection:
        print(f"Язык: {d['language']} | confidence: {d['confidence']:.2f}")
```

6. **Список поддерживаемых языков:**
```python
result = translate.languages().list(target='ru').execute()
for lang in result['languages']:
    code = lang['language']
    name = lang.get('name', '')
    print(f"{code}: {name}")
```

## Популярные коды языков
- `ru` - русский
- `en` - английский
- `pt` - португальский
- `es` - испанский
- `de` - немецкий
- `fr` - французский
- `zh` - китайский
- `ja` - японский
- `ar` - арабский
- `ko` - корейский

## Примеры
- `/gtranslate translate "Meeting at 3pm" ru` - перевести на русский
- `/gtranslate detect "Guten Morgen"` - определить язык
- `/gtranslate languages` - все поддерживаемые языки
