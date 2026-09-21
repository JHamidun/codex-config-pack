---
name: "translate"
description: "Перевод через DeepL Pro: текст, formality, документы docx/pptx/pdf/xlsx. Триггеры: «переведи», «перевод документа». Массовый Google-перевод → /gtranslate."
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


# Translate

/translate - Professional translation via DeepL Pro API

## Usage
```
/translate <text>                    - Auto-detect -> English (configurable)
/translate <text> EN                 - Translate to English
/translate <text> DE formal          - Translate to formal German
/translate file <path> <target_lang> - Translate document
/translate usage                     - Check API usage/limits
```

## Instructions for Claude

Uses DeepL Pro API. Full reference: `${CODEX_PACK_ROOT}/library/skills/deepl-pro/SKILL.md`

### Quick translate

```python
import deepl
import os
from dotenv import load_dotenv

load_dotenv(os.path.expanduser('${CODEX_PACK_ROOT}/library/.credentials.master.env'))
translator = deepl.Translator(os.getenv('DEEPL_API_KEY'))

# Text translation
result = translator.translate_text("Hello world", target_lang="RU")
print(result.text)  # "Привет мир"

# With formality
result = translator.translate_text("How are you?", target_lang="DE", formality="more")

# Batch
results = translator.translate_text(["Hello", "Goodbye"], target_lang="FR")
for r in results:
    print(r.text)
```

### Translate document

```python
# Supports: .docx, .pptx, .pdf, .txt, .html, .xlsx
with open("report.docx", "rb") as in_file:
    with open("report_de.docx", "wb") as out_file:
        translator.translate_document(in_file, out_file, target_lang="DE")
```

### Check usage

```python
usage = translator.get_usage()
print(f"Characters: {usage.character.count}/{usage.character.limit}")
```

## Language codes

**Common:** RU, EN-US, EN-GB, DE, FR, ES, IT, PT-BR, ZH-HANS, JA, KO, TR, PL, UK

**Formality** (DE, FR, ES, RU, IT, NL, PL, PT, JA): `more`, `less`, `prefer_more`, `prefer_less`

## Important

- Use `api.deepl.com` (NOT `api-free.deepl.com`)
- DEEPL_API_KEY from `${CODEX_PACK_ROOT}/library/.credentials.master.env`
