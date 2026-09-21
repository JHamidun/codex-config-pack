---
name: "init-project"
description: "Инициализация нового проекта с выбранным стеком"
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


# 🚀 Init Project: $ARGUMENTS

Создаю новый проект с полной автоматизацией!

## Supported Stacks:

### Backend:
- **django** - Django 5.x (Python)
- **fastapi** - FastAPI (Python async)
- **flask** - Flask (Python micro)
- **express** - Express.js (Node.js)
- **nest** - Nest.js (Node.js TypeScript)
- **gin** - Gin (Go)
- **fiber** - Fiber (Go)
- **actix** - Actix-web (Rust)
- **spring** - Spring Boot (Java)
- **laravel** - Laravel (PHP)
- **rails** - Ruby on Rails

### Frontend:
- **react** - React + Vite
- **next** - Next.js 14 (App Router)
- **vue** - Vue 3 + Vite
- **nuxt** - Nuxt 3
- **svelte** - SvelteKit
- **angular** - Angular 17+
- **remix** - Remix

### Full-Stack:
- **mern** - MongoDB + Express + React + Node
- **t3** - T3 Stack (Next.js + tRPC + Prisma)
- **django-react** - Django + React
- **rails-react** - Rails + React

## Process:

### 1. Parse Arguments
```bash
STACK=$(echo "$ARGUMENTS" | awk '{print $1}')
PROJECT_NAME=$(echo "$ARGUMENTS" | awk '{print $2}')
```

### 2. Create Project Structure
Based on selected stack, create:
- Directory structure
- Configuration files
- Package manifests
- Git repository
- Docker setup

### 3. Install Dependencies
Run appropriate package manager:
- Python: pip / poetry
- Node.js: npm / yarn / pnpm
- Go: go mod
- Rust: cargo
- Java: maven / gradle

### 4. Setup Development Tools

**Linting & Formatting:**
- Python: black, flake8, mypy
- JavaScript/TypeScript: ESLint, Prettier
- Go: golangci-lint
- Rust: rustfmt, clippy
- Java: Checkstyle

**Git Hooks:**
- Pre-commit: format + lint
- Pre-push: tests
- Commit-msg: conventional commits

### 5. Database Setup (if applicable)
- Create docker-compose.yml with DB service
- Add connection configuration
- Create initial migrations
- Add seed data

### 6. Testing Framework
- Unit tests setup
- Integration tests
- E2E tests (if frontend)
- Coverage configuration

### 7. CI/CD Pipeline
Create `.github/workflows/ci.yml`:
```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup
        # Stack-specific setup
      - name: Lint
        run: # Stack-specific linting
      - name: Test
        run: # Stack-specific tests
      - name: Build
        run: # Stack-specific build
```

### 8. Documentation
Create README.md with:
- Project overview
- Tech stack
- Setup instructions
- Development workflow
- Deployment guide
- API documentation (if applicable)

### 9. Docker Configuration
**Dockerfile:**
```dockerfile
# Multi-stage build for production
FROM base-image AS builder
# Build steps...

FROM base-image AS runtime
# Runtime configuration
```

**docker-compose.yml:**
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "PORT:PORT"
    environment:
      - ENV_VAR
    depends_on:
      - db
  db:
    image: postgres:15
    # DB configuration
```

### 10. Environment Configuration
Create `.env.example`:
```bash
# Application
APP_NAME=project-name
APP_ENV=development
DEBUG=true

# Database
DATABASE_URL=postgres://...

# API Keys
API_KEY=your_key_here
```

## Stack-Specific Templates:

### Django Template
```
project-name/
├── manage.py
├── requirements.txt
├── requirements-dev.txt
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── pytest.ini
├── .github/workflows/
├── project/
│   ├── settings/
│   │   ├── base.py
│   │   ├── dev.py
│   │   └── prod.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   └── core/
│       ├── models.py
│       ├── views.py
│       ├── serializers.py
│       └── tests/
└── static/
```

### FastAPI Template
```
project-name/
├── pyproject.toml
├── requirements.txt
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models/
│   ├── schemas/
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── users.py
│   │   └── items.py
│   ├── services/
│   ├── utils/
│   └── tests/
│       ├── test_api.py
│       └── conftest.py
└── alembic/
```

### MERN Template
```
project-name/
├── package.json
├── .env.example
├── docker-compose.yml
├── client/
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── utils/
│   │   ├── api/
│   │   ├── types/
│   │   ├── App.tsx
│   │   └── main.tsx
│   └── tests/
└── server/
    ├── package.json
    ├── tsconfig.json
    ├── src/
    │   ├── controllers/
    │   ├── models/
    │   ├── routes/
    │   ├── middleware/
    │   ├── utils/
    │   ├── types/
    │   └── server.ts
    └── tests/
```

### Next.js 14 Template
```
project-name/
├── package.json
├── next.config.js
├── tsconfig.json
├── tailwind.config.ts
├── .env.local
├── Dockerfile
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   ├── globals.css
│   ├── api/
│   │   └── [...route]/route.ts
│   └── (routes)/
│       ├── dashboard/
│       └── auth/
├── components/
│   ├── ui/
│   └── shared/
├── lib/
│   ├── utils.ts
│   ├── db.ts
│   └── api.ts
├── public/
└── __tests__/
```

## Output:

После выполнения команды:

```bash
✅ Project created: project-name
📁 Stack: [selected-stack]
🔧 Configuration complete
📦 Dependencies installed
🧪 Tests configured
🐳 Docker ready
📝 Documentation generated

Next steps:
1. cd project-name
2. Copy .env.example to .env and configure
3. [stack-specific start command]
4. Open http://localhost:[PORT]

Development:
- Run tests: [test command]
- Format code: [format command]
- Build: [build command]
```

## Examples:

```bash
/init-project django my-blog
/init-project next ecommerce-store
/init-project fastapi api-service
/init-project mern social-network
/init-project gin microservice
```

**Let's build! 🚀**