---
name: "animations"
description: "Таймлайн-анимации в HTML (React): плеер, скраббер, ease. Триггеры: «анимация в HTML», «motion design», «интро», «transitions для презентации»."
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


# Animations

Минималистичный движок таймлайн-анимаций. Один HTML, React + inline JSX, без сторонних либ кроме Babel.

## Что даёт `templates/anim-engine.jsx`

- `<Stage duration={...}>` — корневой контейнер. Авто-скейлит канвас под viewport, рисует скраббер и play/pause.
- `<Sprite start={s} end={s} ...>` — обёртка с временными границами. Внутри читает `useTime()` и рендерит детей.
- `useTime()` — текущая позиция таймлайна в секундах.
- `useSprite()` — нормализованная позиция внутри спрайта (0..1).
- `Easing` — `linear`, `easeIn`, `easeOut`, `easeInOut`, `expo`, `back`, `bounce`.
- `interpolate(t, [from, to], easing)` — линейная интерполяция чисел или массивов чисел (для transform).
- `entryFade`, `entryRise`, `exitFade` — готовые входы/выходы.

## Структура сцены

```jsx
<Stage duration={8} width={1920} height={1080}>
  <Sprite start={0} end={3}>
    {() => {
      const p = useSprite();
      const y = interpolate(p, [40, 0], Easing.easeOut);
      const o = interpolate(p, [0, 1], Easing.easeOut);
      return <h1 style={{ transform: `translateY(${y}px)`, opacity: o }}>Hello</h1>;
    }}
  </Sprite>

  <Sprite start={2} end={5}>
    {() => <SecondScene />}
  </Sprite>
</Stage>
```

## Принципы

- **Всё происходит в долях секунды.** Не в кадрах. 24/30/60 fps — забота браузера.
- **Перекрытия — благо.** Последние 0.3s одного спрайта пересекаются с первыми 0.3s следующего — глаз не цепляется за стыки.
- **Easing — не декорация.** `easeOut` для входов («падает и тормозит»), `easeIn` для выходов («ускоряется и улетает»), `easeInOut` для одновременных движений, `linear` для камер и пэннингов.
- **Не анимируй всё.** Один-два элемента в кадре движутся, остальные стоят. Иначе каша.
- **Сохраняй позицию плеера.** Если делаешь длинную анимацию для итераций — пиши текущее время в `localStorage`, чтоб рефреш не сбрасывал.

## Экспорт в видео

Если попросят MP4/GIF, дёргай `export-png` для покадрового рендера через Playwright + ffmpeg для склейки.

## Что НЕ делать

- Не имитируй keyframes-CSS через JS-таймауты. Используй `requestAnimationFrame` (он внутри Stage).
- Не используй GSAP / Framer Motion / Popmotion, если задачу решает встроенный движок. Бандл-вес и сложность не оправданы.
- Не пытайся синхронизировать анимацию со звуком через `setTimeout`. Используй `audio.currentTime` как источник правды.
