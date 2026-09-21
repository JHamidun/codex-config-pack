---
name: "states-checklist"
description: "Чек-лист состояний экрана перед сдачей прототипа: empty, loading, error, partial, success. Триггеры: «happy path только», «8 состояний UI»."
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


# States checklist

Дизайнеры рисуют «успешное» состояние и забывают остальные. **80% пользовательского опыта живёт в нестандартных состояниях.**

## Минимальный набор для любого экрана с данными

| Состояние | Когда показать | Что должно быть |
|---|---|---|
| **Loading** | Данные ещё не пришли | Skeleton (не спиннер), не блокировать UI |
| **Empty (cold)** | Никогда не было данных (новый юзер) | Объяснение + onboarding-кнопка |
| **Empty (clean)** | Данные были, сейчас 0 (всё прочитано / выполнено) | Похвала + нейтральная иллюстрация |
| **Empty (filtered)** | Применён фильтр, под него ничего нет | «Очистить фильтр» |
| **Error (network)** | Запрос упал | «Не удалось загрузить» + Retry |
| **Error (forbidden)** | 403 | Что произошло + куда пойти |
| **Error (not found)** | 404 на конкретный ресурс | Ссылка на список |
| **Partial** | Загрузилась часть | Показать что есть + индикатор «загружается ещё» |
| **Stale** | Данные устарели | «Обновить» + timestamp |
| **Offline** | Сеть пропала | Баннер + что доступно офлайн |

## Минимальный набор для форм

- Default (пустая, до фокуса)
- Focused (поле в фокусе)
- Filled (введено)
- Validating (асинхронная проверка)
- Error (с конкретным сообщением)
- Success (после отправки)
- Disabled
- Read-only (если применимо)

## Минимальный набор для кнопок

- Default
- Hover
- Active (нажата)
- Focus-visible
- Disabled
- Loading (асинхронное действие)
- Success-flash (200ms после успеха)

## Чек-лист (использовать как linter перед сдачей)

Для каждого экрана прототипа:
- [ ] Что видит юзер, который только что зарегистрировался (cold empty)?
- [ ] Что видит, если очистил всё / выполнил всё (clean empty)?
- [ ] Что видит, если выключил wifi на 3 секунды (loading + error)?
- [ ] Что видит, если ввёл неправильные данные в форму?
- [ ] Что видит, если кликнул на ссылку, которая ведёт в удалённый объект?
- [ ] Что видит на slow-3g (skeleton нужен)?
- [ ] Что видит, если у него отключены картинки (alt-текст осмыслен)?

## Шаблоны компонентов

`templates/states.html` — готовая страница с примерами всех состояний для копирования.

```html
<!-- Skeleton -->
<div class="skeleton">
  <div class="line w-3/4"></div>
  <div class="line w-1/2"></div>
  <div class="line w-2/3"></div>
</div>

<!-- Empty (cold) -->
<div class="empty">
  <div class="empty-icon"><!-- placeholder --></div>
  <h2>Здесь будут ваши проекты</h2>
  <p>Начните с создания первого проекта.</p>
  <button>Создать проект</button>
</div>

<!-- Error -->
<div class="error" role="alert">
  <h3>Не удалось загрузить</h3>
  <p>Проверьте подключение и повторите.</p>
  <button>Повторить</button>
  <button class="secondary">Подробности</button>
</div>
```

CSS skeleton-анимации:

```css
.skeleton .line {
  height: 12px; border-radius: 6px;
  background: linear-gradient(90deg, #eee 0%, #f5f5f5 50%, #eee 100%);
  background-size: 200% 100%;
  animation: shimmer 1.4s infinite;
}
@keyframes shimmer {
  0%   { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
@media (prefers-reduced-motion) {
  .skeleton .line { animation: none; background: #eee; }
}
```

## Правила

- **Skeleton, не спиннер**, на загрузке списков и страниц. Спиннер — только для action-кнопок (200ms-3s).
- **Не показывай loading младше 200ms** — мерцание раздражает. Дебаунс.
- **После 5 секунд** — добавь «занимает дольше обычного» сообщение.
- **Empty-state не должен быть пустым** — это тоже экран, заполни смыслом.
- **Error-сообщения — конкретны**, без «Произошла ошибка».

## Legacy reference

Прежняя расширенная версия скилла (дерево @2026-04-30) сохранена целиком в `references/legacy-states-checklist.md`. Секции там: 8 обязательных состояний, Чеклист на экран, Empty state design, Error state design, Loading state — когда что показывать, Disabled vs read-only vs locked, Куда сложить варианты состояний, Антипаттерны.
