---
name: "real-data"
description: "Прототип на настоящих данных: CSV/JSON/SQLite или локальный API-мок вместо фейков. Триггеры: «подключи к API», «прототип с моими данными»."
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


# Real data

Подменяет фейковые данные на настоящие, не вынуждая пользователя поднимать бэк.

## Способы

### 1. JSON-файл напрямую

Самое простое. Никакого сервера.

```js
// data.json
[{"id":1,"name":"Alpha"}, {"id":2,"name":"Beta"}]

// в HTML
const data = await fetch('data.json').then(r => r.json());
```

Через `live.mjs` (`live-preview` скилл) — работает из коробки.

### 2. CSV

```js
import Papa from 'https://esm.sh/papaparse';
const text = await fetch('users.csv').then(r => r.text());
const { data } = Papa.parse(text, { header: true, dynamicTyping: true });
```

### 3. SQLite в браузере (sql.js)

```js
import initSqlJs from 'https://esm.sh/sql.js';
const SQL = await initSqlJs({ locateFile: f => `https://esm.sh/sql.js/dist/${f}` });
const buf = await fetch('app.db').then(r => r.arrayBuffer());
const db = new SQL.Database(new Uint8Array(buf));
const rows = db.exec('SELECT * FROM users LIMIT 10')[0];
```

Подходит, если у пользователя уже есть `.db`.

### 4. Локальный API-мок через json-server

```bash
npm i -g json-server
json-server --watch db.json --port 3001
```

`db.json`:
```json
{ "users": [{"id":1,"name":"Alpha"}], "posts": [...] }
```

Прототип:
```js
fetch('http://localhost:3001/users').then(...)
fetch('http://localhost:3001/users/1', { method: 'PATCH', body: '...' })
```

Поддерживает GET / POST / PUT / PATCH / DELETE — почти настоящий REST.

### 5. Postgres / реальный бэк через прокси

Если у пользователя есть бэк на `internal.company.com`, который недоступен с прототипа:

```js
// proxy.mjs
import http from 'node:http';
http.createServer((req, res) => {
  const target = 'https://internal.company.com' + req.url;
  fetch(target, { method: req.method, headers: req.headers })
    .then(r => r.body.pipeTo(new WritableStream({ write: c => res.write(c), close: () => res.end() })));
}).listen(3002);
```

Прототип бьёт `localhost:3002/api/...` — реально дёргает `internal.company.com/api/...`.

## Скрипт-мост

`templates/data-bridge.mjs` — один файл, который покрывает все варианты:

```bash
node data-bridge.mjs --csv users.csv --port 3001
# поднимает HTTP-сервер с GET /users (из CSV)
```

```js
import http from 'node:http';
import fs from 'node:fs/promises';
import Papa from 'papaparse';

const args = parse(process.argv.slice(2));
const port = +(args.port || 3001);
let data = {};

if (args.csv) {
  const t = await fs.readFile(args.csv, 'utf8');
  data[path(args.csv)] = Papa.parse(t, { header: true, dynamicTyping: true }).data;
}
if (args.json) {
  data = { ...data, ...JSON.parse(await fs.readFile(args.json, 'utf8')) };
}

http.createServer((req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  const url = new URL(req.url, `http://localhost`);
  const key = url.pathname.split('/')[1];
  if (data[key]) {
    res.writeHead(200, { 'content-type': 'application/json' });
    res.end(JSON.stringify(data[key]));
  } else { res.writeHead(404); res.end(); }
}).listen(port);

console.log(`data-bridge :${port} →`, Object.keys(data));

function path(p) { return p.split('/').pop().split('.')[0]; }
function parse(argv) { /* как в других скриптах */ }
```

## Когда что использовать

| Объём | Сложность | Решение |
|---|---|---|
| < 100 записей, read-only | низкая | JSON-файл напрямую |
| 100–10000 записей, read-only | низкая | CSV + Papa |
| Нужен mutation (CRUD) | средняя | json-server |
| Сложная схема, joins | высокая | sql.js |
| Реальный бэк | высокая | proxy |

## Privacy

- Если данные содержат PII — не коммить в репо. `.gitignore` для `data/`.
- Для демо-показа клиенту — обфусцируй (фамилии → анаграммы, телефоны → +7 (XXX) XXX-XX-XX).

## Legacy reference

Прежняя расширенная версия скилла (дерево @2026-04-30) сохранена целиком в `references/legacy-real-data.md`. Секции там: 4 уровня connection, Уровень 1: Static JSON, Уровень 2: Public API, Уровень 3: Read-only proxy, Smart placeholders (gap), CSV → JSON, Данные с обновлением, Правила для demo, Stack, Антипаттерны.
