---
name: "scaffold"
description: "Каркас проекта по шаблону: fastapi, react, nextjs, telegram-bot, cli — папки, конфиги, Dockerfile. Триггеры: «каркас проекта». Полная инициализация → /init-project."
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


# Project Scaffolding

**Аргументы:** $ARGUMENTS (тип проекта: fastapi, react, nextjs, telegram-bot, cli)

## Задача

Создай структуру нового проекта по выбранному шаблону.

## Доступные шаблоны

### fastapi
```
project/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app
│   ├── config.py            # Settings
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   └── __init__.py
│   │   └── deps.py          # Dependencies
│   ├── models/
│   │   └── __init__.py
│   ├── schemas/
│   │   └── __init__.py
│   └── services/
│       └── __init__.py
├── tests/
│   └── __init__.py
├── .env.example
├── .gitignore
├── requirements.txt
├── Dockerfile
└── README.md
```

### react
```
project/
├── src/
│   ├── components/
│   ├── hooks/
│   ├── pages/
│   ├── services/
│   ├── utils/
│   ├── App.tsx
│   └── index.tsx
├── public/
├── tests/
├── .env.example
├── .gitignore
├── package.json
├── tsconfig.json
├── vite.config.ts
└── README.md
```

### nextjs
```
project/
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── api/
│   ├── components/
│   ├── lib/
│   └── types/
├── public/
├── .env.example
├── .gitignore
├── next.config.js
├── package.json
├── tailwind.config.js
└── README.md
```

### telegram-bot
```
project/
├── bot/
│   ├── __init__.py
│   ├── main.py              # Entry point
│   ├── config.py            # Settings
│   ├── handlers/
│   │   ├── __init__.py
│   │   ├── start.py
│   │   └── commands.py
│   ├── keyboards/
│   │   └── __init__.py
│   ├── services/
│   │   └── __init__.py
│   └── utils/
│       └── __init__.py
├── tests/
├── .env.example
├── .gitignore
├── requirements.txt
├── Dockerfile
└── README.md
```

### cli
```
project/
├── src/
│   ├── __init__.py
│   ├── cli.py               # Click/Typer CLI
│   ├── commands/
│   │   └── __init__.py
│   └── utils/
│       └── __init__.py
├── tests/
├── .gitignore
├── pyproject.toml
└── README.md
```

## Действия

1. Спроси название проекта если не указано
2. Создай директории и файлы по шаблону
3. Заполни базовые файлы рабочим кодом
4. Инициализируй git репозиторий
5. Установи зависимости (опционально)

## Базовые файлы для каждого шаблона

### .gitignore (Python)
```
__pycache__/
*.py[cod]
.env
.venv/
venv/
*.egg-info/
dist/
build/
.pytest_cache/
.coverage
```

### .gitignore (Node)
```
node_modules/
.env
.env.local
dist/
build/
.next/
coverage/
```

### .env.example
```
# Copy to .env and fill values
DEBUG=true
DATABASE_URL=
API_KEY=
```

## После создания

Выведи инструкции для запуска:
```bash
cd project-name
# Для Python:
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
# Для Node:
npm install
npm run dev
```
