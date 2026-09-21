---
name: "sdat"
description: "Сдача практических заданий Академии Hamidun прямо из Claude Code. Использовать, когда ученик говорит «сдать задание», «сдай задание N», «отправь задание на проверку», «проверь моё задание», «submit homework», «сдать дз». Скилл берёт персональный токен ученика из ${CODEX_PACK_ROOT}/library/hamidun.env, собирает артефакт (код, текст, ссылку на репозиторий) и отправляет его в LMS на автопроверку — вердикт (зачтено / нужна доработка) и фидбек приходят в Telegram/на почту и в кабинет academy.hamidun.com. "
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


# Сдать задание (Академия Hamidun)

Ученик сдаёт домашние и задания «на звонке» тем же агентом, в котором работает.
Скилл вызывает `scripts/submit.py` (без внешних зависимостей — только стандартная
библиотека Python 3). Сдача уходит в LMS `POST /api/submit`, автопроверку делает
проверяющий-агент, вердикт приходит ученику в Telegram/на почту.

## Перед первой сдачей — токен

Ученику нужен персональный токен сдачи (формат `hs_...`). Он лежит в кабинете:
**academy.hamidun.com → раздел «Эфиры» → блок «Сдача заданий через Claude Code»**.
Токен надо один раз положить строкой в `${CODEX_PACK_ROOT}/library/hamidun.env`:

```
HAMIDUN_SUBMIT_TOKEN=hs_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Если файла нет — создай его. Токен персональный, привязан к участнику потока;
он один и тот же для всех заданий. Если токена нет — скажи ученику, где его взять
(текст выше), и не пытайся угадывать.

## Как действовать (для агента)

1. **Определи номер задания.** Из фразы ученика («сдать задание 3» → номер 3).
   Если номер не назван — запусти `list` (см. ниже) и спроси, какое из заданий сдаём.
2. **Собери артефакт** — что именно ученик сделал:
   - **код/текст** → `--type text` c `--content-file <файл>` (предпочтительно) или
     `--content "..."`. Если работа — это файл(ы) в проекте, отправь текст самого
     значимого файла или короткое связное описание сделанного + ключевой код.
   - **репозиторий/gist/ссылка** → `--type link --url https://...`. Хорошо для
     больших проектов (артефакт > 2 МБ текстом не принимается — только ссылкой).
   - Всегда добавляй короткое человеческое описание того, что сделано, если
     задание это подразумевает — проверяющий читает и описание, и артефакт.
3. **Покажи ученику, что именно отправляешь**, и отправь.
4. **Покажи ответ сервера** дословно: принято / уже на проверке / уже зачтено.
   Напомни: вердикт и фидбек придут в Telegram/на почту и в кабинет — здесь мы
   только отправили работу, оценивает её проверяющий асинхронно (пара минут).
5. Если пришёл `needs_work` (ученик вернулся дорабатывать) — поправь по фидбеку и
   сдай снова: та же команда, попытка увеличится автоматически.

## Команды

Показать список заданий и их статусы (что сдавать, что уже зачтено):

```bash
python "${CODEX_PACK_ROOT}/library/skills/sdat/scripts/submit.py" list
```

Сдать задание текстом из файла:

```bash
python "${CODEX_PACK_ROOT}/library/skills/sdat/scripts/submit.py" submit \
  --assignment 3 --type text --content-file ./solution.md
```

Сдать ссылкой на репозиторий (для больших работ):

```bash
python "${CODEX_PACK_ROOT}/library/skills/sdat/scripts/submit.py" submit \
  --assignment 3 --type link --url https://github.com/user/repo
```

Пересдать уже зачтённое задание (по умолчанию зачтённое не трогается):

```bash
python "${CODEX_PACK_ROOT}/library/skills/sdat/scripts/submit.py" submit \
  --assignment 3 --type text --content-file ./solution_v2.md --resubmit
```

На Windows используй `python` (или `py`) и путь
`%USERPROFILE%\.claude\skills\sdat\scripts\submit.py`.

## Флаги submit

| Флаг | Значение |
|------|----------|
| `--assignment, -a` | номер задания (или его uuid) — обязателен |
| `--type, -t` | `text` (по умолч.) · `link` · `file` |
| `--content, -c` | текст артефакта прямо в аргументе |
| `--content-file` | файл, чьё содержимое отправить как текст (filename проставится) |
| `--file, -f` | то же, что `--content-file`, но всегда ставит имя файла |
| `--url, -u` | ссылка (для `--type link`) |
| `--filename` | метка имени файла |
| `--resubmit` | пересдать даже если уже зачтено |

## Тонкости

- **Токен из окружения** тоже подхватывается: если задан `HAMIDUN_SUBMIT_TOKEN`
  в env — файл не обязателен. Файл `${CODEX_PACK_ROOT}/library/hamidun.env` — рекомендованный способ.
- **Другой домен** (стенд/тест) — переменная `HAMIDUN_ACADEMY_URL`.
- **Лимит текста 2 МБ.** Большие проекты — только ссылкой (`--type link`).
- **Только текстовые артефакты.** `--type file` / `--content-file` читают файл
  строгим UTF-8. Бинарники (PDF, скриншоты, архивы, `.docx`, `.zip`) сдавать
  нельзя — скилл честно откажет (а не отправит кашу с ложным «принято»). Такой
  артефакт залей на gist/GitHub/облако и сдай ссылкой (`--type link --url ...`).
- **Дубли не плодятся:** если сдача уже на проверке (`pending`), сервер вернёт ту
  же сдачу, а не создаст новую. Уже зачтённое требует `--resubmit`.
- **Приватность:** скилл шлёт ТОЛЬКО на academy.hamidun.com и ТОЛЬКО работу
  ученика. Никаких токенов/ключей из окружения в артефакт не подкладывай.
