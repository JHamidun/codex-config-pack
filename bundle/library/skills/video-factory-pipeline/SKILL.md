---
name: "video-factory-pipeline"
description: "Гонит ролик по стадиям: бриф → сценарий → звук → раскадровка → промпты → генерация кадров → монтаж → контроль, и отдельно тренд → аватар → YouTube. Триггеры «сделай ролик», «ролик под ключ», «сделай видео и выложи». НЕ монтаж готового футажа → video-editor; НЕ одна AI-сцена → video-generation."
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


# Video Factory Pipeline — стадии видеофабрики

Стадии конвейера лежат здесь целиком (`references/stage-*.md`) — это полные промпты
ролей. В паке им соответствуют агенты `vf-brief` … `vf-qc` и оркестратор `video-factory`:
агент даёт короткое описание роли, файл стадии — её рабочий текст со всеми ограничителями.
Гонит конвейер агент `video-factory` (или сама сессия, если ролик короткий).

**Что понадобится:** ffmpeg в PATH + ключ хотя бы одного генератора видео. Стадия 6 —
единственная платная, и она платная всерьёз (посекундная тарификация движка). Конвейер B
сверх этого требует HeyGen, ElevenLabs и OAuth к YouTube — список с порядком цен
в шапке `references/youtube-pipeline.md`.

## Здесь ДВА разных конвейера — не перепутай

Имя «видеофабрика» носили две несовместимые программы. Свели их в один навык, но
объединять их нельзя: у них разные входы, разные артефакты и разная цена ошибки.

| | **Конвейер A — сборка ролика** | **Конвейер B — тренд → YouTube** |
|---|---|---|
| Вход | задача владельца («ролик про X, вертикальный, 40 секунд») | тема или `auto` |
| Ищет тему сам | нет | да, фаза 1 |
| Артефакт | конверт `production.json` | папка с `script.json`, `scene_*.mp4` |
| Аватар HeyGen | только маршрут `avatar` | да, ядро стиля Avatar/Mixed |
| Публикует наружу | **нет** | **да, на YouTube** |
| Стадии | 8, `references/stage-*.md` | 6 фаз, `references/youtube-pipeline.md` |
| Кто исполняет | агенты `vf-*` | агент `video-factory` |
| Запуск программой | `skills/video-montage/workflows/video-factory.js` | нет, ведёт агент |

Развилка одной фразой: «собери рилс из вот этого» → **A**; «найди тему и выложи» → **B**.

---

## Конвейер A: карта стадий

```
задача владельца + workdir
        │
  1 бриф          →  brief, route            барьер: от него зависит всё
        │
        ├──────────────────────────┐         ПАРАЛЛЕЛЬНО
        ▼                          ▼
  2 сценарист  → structure,   3 звукорежиссёр → audio
                 script          (карта трека нужна стадии 4!)
        └──────────────┬───────────┘
                       ▼                     барьер: раскадровке нужны
  4 раскадровщик  →  shots                   и сценарий, и сетка долей
                       │
  5 промптер      →  shots[].prompt / negative
                       │
  6 оператор      →  shots[].output, status  ← ЕДИНСТВЕННАЯ ПЛАТНАЯ СТАДИЯ
                       │                       кадры идут независимо, волнами по 4
  7 монтажёр      →  edit, edit.output
                       │
  8 контроль      →  qa                      verdict: pass / revise / fail
                       │
              revise → назад на 5–6 по qa.revise_targets (только помеченные кадры)
              fail   → назад на 4 (переделка с раскадровки)
```

| # | Стадия | Агент | Пишет в конверт | Промпт |
|---|--------|-----------|-----------------|--------|
| 1 | бриф | `vf-brief` | `brief`, `route` | `references/stage-1-brief.md` |
| 2 | сценарист | `vf-screenwriter` | `structure`, `script` | `references/stage-2-screenwriter.md` |
| 3 | звукорежиссёр | `vf-sound` | `audio` | `references/stage-3-sound.md` |
| 4 | раскадровщик | `vf-storyboard` | `shots` | `references/stage-4-storyboard.md` |
| 5 | промптер | `vf-prompter` | `shots[].prompt`, `.negative` | `references/stage-5-prompter.md` |
| 6 | оператор | `vf-operator` | `shots[].output/status/attempts` | `references/stage-6-operator.md` |
| 7 | монтажёр | `vf-editor` | `edit` | `references/stage-7-editor.md` |
| 8 | контроль | `vf-qc` | `qa` | `references/stage-8-qc.md` |

> **Порядок в списке ≠ очередь исполнения.** Звук (3) стартует сразу после брифа,
> параллельно сценаристу: карта трека (`audio.cut_grid`, дропы) нужна раскадровщику на
> стадии 4, иначе он положит кадры мимо долей и монтаж придётся пересобирать.

## Общий документ

Все стадии пишут в один конверт — `production.json`
(схема: `${CODEX_PACK_ROOT}/library/skills/video-montage/schemas/production.schema.json`).
Каждая стадия дописывает **свой** раздел и не трогает чужие. Это не бюрократия, а условие
параллельности и перезапуска поодиночке: провалился один кадр из двенадцати — считается
заново он один, остальные лежат с отметкой `status: ready` и **второй раз не оплачиваются**.

Полная архитектура, таблица маршрутов и обоснования правил —
`${CODEX_PACK_ROOT}/library/skills/video-montage/references/pipeline-architecture.md`.

## Как запускать конвейер A

**Через готовую программу** (умеет resume, волны по 4, барьеры):

```
Workflow({
  scriptPath: '${CODEX_PACK_ROOT}/library/skills/video-montage/workflows/video-factory.js',
  args: { brief: 'как за день собрали лендинг вайбкодингом',
          seconds: 35, platform: 'reels', goal: 'watch',
          workdir: './work/video-factory/lending-35s' }
})
```

Обрыв не страшен: `Workflow({scriptPath, resumeFromRunId})` продолжит с места.

**Стадиями вручную** — каждая стадия отдельный `general-purpose` субагент на `fable`.
Промпт стадии берётся **целиком** из соответствующего `references/stage-*.md` и
дополняется конкретикой запуска:

```
Task(subagent_type="general-purpose", model: inherit-current-codex-model, prompt=f"""
{содержимое references/stage-4-storyboard.md}

---
## Запуск
- КОНВЕРТ: {workdir}/production.json
- РАБОЧАЯ ПАПКА: {workdir}
- СХЕМА: ${CODEX_PACK_ROOT}/library/skills/video-montage/schemas/production.schema.json
- Пишешь ТОЛЬКО свой раздел конверта, чужие не трогаешь.
""")
```

Параллелить можно **только** 2 и 3 (у них разные разделы конверта) и кадры внутри
стадии 6. Остальное — строго последовательно: у стадий общий файл.

## Деньги — стадия 6 и только она

Одна стадия конвейера тратит настоящие деньги (Veo 3.1, Sora 2, Nano Banana). Её
ограничители перенесены дословно и ослаблению не подлежат:

- `direct_video.py` без `--yes` печатает план и цену и останавливается — **сначала
  посмотреть, потом запускать**;
- черновой прогон дешёвым движком (`veo-lite`/`veo-fast`) на весь ролик — правило, а не
  экономия; тяжёлым переснимаются только финальные кадры;
- приёмка кадра **сразу после генерации**, глазами по контактному листу, а не после
  двенадцатого — брак виден на первом и повторится в остальных за те же деньги;
- одна правка за попытку; после 10–15 неудач упрощается сам кадр, а не формулировки;
- `status: ready` при перезапуске не пересчитывается — проверить перед запуском, чтобы
  не заплатить дважды;
- `meta.cost_notes` после каждой партии: сколько кадров, каким движком, сколько попыток.

Конвейер B тратит деньги в фазах 3–4 (аватар HeyGen, озвучка ElevenLabs — порядок цен
в шапке `references/youtube-pipeline.md`) и требует **подтверждения владельца на шаге 0**,
до первого платного вызова.

## Правила, которые конвейер соблюдает сам

Из каталога приёмов (`${CODEX_PACK_ROOT}/library/skills/video-montage/scripts/techniques.json`, 79 записей
с источником и статусом доказательности):

- **Крючок не длиннее трёх секунд.** Растянутый крючок — главная причина отвала.
- **Событие каждые 3–7 секунд**, чаще к концу блока.
- **Склейки притянуты к долям**, на дропе склейка обязательна.
- **Плотность склеек следует за энергией трека**, а не равномерна по нему.
- **Два-три вида переходов на ролик.** Разнообразие переходов читается как неумение.
- **Длительность перехода — либо 0,15–0,25 с, либо 0,6–1,0 с.** Середина выглядит ошибкой темпа.
- **Шрифт подбирается под роль и проверяется на кириллицу** по таблице символов, а не по названию.
- **Пороги без первоисточника не применяются.** «60/80% досмотра», «теряешь треть за три
  секунды», «внимание восемь секунд» в контроль качества не заложены — источников нет.

## Контроль качества: почему без усреднения

Оценки по измерениям **не усредняются**: любой `fail` в отдельной проверке делает общий
вердикт `fail`. Разбор чужих оценщиков показал типичную поломку — шесть измерений
усредняются, и план с полностью проваленным измерением получает хорошую общую оценку за
счёт остальных; ролик, где все кадры одинаковы, проходил такую проверку как «сильный».
На переделку уходят только помеченные кадры (`qa.revise_targets`), не весь ролик: лишний
кадр «на всякий случай» — это реальные деньги.

## Смежное

- Монтаж готового футажа (без конвейера) → навык `video-editor`.
- Одна AI-сцена, выбор движка → навык `video-generation`.
- Инструменты и приёмка ролика (`review_cut.py`, `techniques.py`, `reel_structure.py`) →
  навык `video-montage`.
- Промо-ролик продукта на Remotion → навык `video-shotcraft`.
