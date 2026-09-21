---
name: "onboarding-ux"
description: "Паттерны первого запуска: welcome, tour, empty-states. Триггеры: «первый запуск», «setup wizard», «TTV». НЕ активация trial→onboarding-cro-ru."
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


# Onboarding UX

Цель — дать пользователю **первое полезное действие за <60 секунд**. Любой экран, который не приближает к этому, — кандидат на удаление.

## Паттерны (от лучшего к худшему)

### 1. Get-to-value first
Не показывай туториал, не спрашивай данные — пусти в продукт сразу с примером данных. Покажи возможности через готовый кейс.

### 2. Inline coachmarks
Подсказки появляются у элемента **в момент**, когда он впервые становится видимым. Не отдельный туториал, а тонкие сноски прямо в интерфейсе. Закрываются один раз.

### 3. Empty state с задачей
Не просто «Тут пока ничего нет». Дай конкретное действие: «Создайте первый проект» с кнопкой.

### 4. Прогрессивный сбор данных
Не спрашивай 8 полей в форме. 1-2 минимума. Остальное — собирай по мере использования.

### 5. Опциональный тур
Только если пользователь сам ткнул «Show me how». Не auto-play.

## Что НЕ делать

- ❌ **3+ welcome-слайда** перед началом работы. Удаляй.
- ❌ **Modal с туториалом**, который надо закрыть. Не работает.
- ❌ **Пустые поля «расскажите о себе»** на старте. Не заполнят.
- ❌ **Подсветка одного элемента на всём экране** — лекторская, давит.
- ❌ **«Пропустить»** мелким серым в углу — верный признак, что онбординг не нужен.

## Empty states — отдельный жанр

Каждый раздел приложения должен иметь empty state, не тупо «Нет данных». Структура:

```
┌────────────────────────────┐
│        [иконка / иллюстр]  │
│                            │
│  Заголовок: что тут будет  │
│  Подзаголовок: зачем оно   │
│                            │
│      [ Главное действие ]  │
│      или вторичная ссылка  │
└────────────────────────────┘
```

См. `states-checklist` для полного списка состояний.

## Прогрессия

Первая сессия пользователя — не одна целевая точка. Это серия побед:

1. **Первая минута** — видит value (не просто понимает интерфейс).
2. **Первая сессия** — выполняет первое полезное действие.
3. **Первый день** — возвращается.
4. **Первая неделя** — приглашает кого-то / интегрирует.

Дизайнь под каждую вешку отдельно.

## Реализация в прототипе

```jsx
function App() {
  const [seen, setSeen] = useState(() => JSON.parse(localStorage.onboarding || '{}'));
  const mark = (k) => {
    const next = { ...seen, [k]: true };
    setSeen(next); localStorage.onboarding = JSON.stringify(next);
  };

  return <>
    {!seen.firstVisit && <FirstVisitBanner onClose={() => mark('firstVisit')} />}
    {!seen.composer  && hasOpenedComposer && <ComposerHint onSeen={() => mark('composer')} />}
    <Workspace />
  </>;
}
```

Никаких мегамодалок. Маленькие подсказки в нужный момент.

## Чеклист онбординга

- [ ] Понятно, что это за продукт, за 5 секунд?
- [ ] Первое полезное действие <60 секунд?
- [ ] Нет 3+ welcome-экранов?
- [ ] Empty states содержательные, не «Тут пока пусто»?
- [ ] Подсказки появляются in-context, не как modal?
- [ ] Можно закрыть всё и вернуться позже?
- [ ] Возвращающийся пользователь не видит онбординга снова?
- [ ] Есть способ найти помощь, если запутался?

## Антипаттерны для прототипа

В прототипе часто соблазн «нарисовать туториал», потому что это видимая работа. **Но если туториал нужен — продукт плох.** Лучше потрать время на то, чтобы сделать UX, который не нуждается в туториале.

Если туториал всё-таки нужен — сделай его максимально невидимым. Ты ведь хочешь, чтобы человек **пользовался** продуктом, а не **изучал** его.

## Legacy reference

Прежняя расширенная версия скилла (дерево @2026-04-30) сохранена целиком в `references/legacy-onboarding-ux.md`. Секции там: 4 типа онбординга, Структура экранов, Permissions — когда просить, Time-to-value (TTV), Progressive disclosure, Empty states которые учат, Specific onboarding patterns, Skip vs обязательное, Antipattern: «You must complete this», Метрики (для тех кто меряет), Антипаттерны.
