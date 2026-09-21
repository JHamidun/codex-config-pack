---
name: "claude-in-html"
description: "Вызов LLM прямо из HTML-артефакта — прототипы с живой AI-фичей: чат, саммари, классификация. Триггеры: «встрой Claude в HTML», «AI inside prototype»."
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


# Claude in HTML

Прототип может вызвать модель напрямую из браузера через Anthropic SDK или fetch к своему бэку. В Claude Code пользователь сам управляет ключом.

## Минимальная реализация

```html
<script type="module">
  import Anthropic from "https://esm.sh/@anthropic-ai/sdk";

  // Один раз — спросить и сохранить ключ.
  let key = localStorage.getItem('anthropic_key');
  if (!key) {
    key = prompt('Anthropic API key (sk-ant-...) — сохранится локально');
    if (key) localStorage.setItem('anthropic_key', key);
  }

  const client = new Anthropic({ apiKey: key, dangerouslyAllowBrowser: true });

  window.askClaude = async function (userText) {
    const r = await client.messages.create({
      model: 'claude-haiku-4-5',
      max_tokens: 512,
      messages: [{ role: 'user', content: userText }],
    });
    return r.content[0].text;
  };
</script>
```

## Стриминг (для чат-прототипа)

```js
const stream = await client.messages.stream({
  model: 'claude-haiku-4-5',
  max_tokens: 1024,
  messages: history,
});
for await (const event of stream) {
  if (event.type === 'content_block_delta') {
    chatBox.append(event.delta.text);
  }
}
```

## Системные промпты для роли

Когда прототип симулирует продуктовую фичу — задай system, объясняющий, что это.

```js
client.messages.create({
  model: 'claude-haiku-4-5',
  max_tokens: 256,
  system: 'Ты — помощник в приложении доставки еды. Отвечай коротко, на русском, без эмодзи.',
  messages: [...]
});
```

## Где взять ключ — UX

Не спрашивай через `prompt()` каждый раз. Сделай нормальный onboarding-экран:

1. При первом запуске — экран «Чтобы попробовать AI-фичу, вставьте API key».
2. Объясни, что ключ хранится **только в браузере** (localStorage), никуда не отправляется.
3. Дай ссылку на console.anthropic.com где взять ключ.
4. Кнопка «Use without AI» — прототип работает со статикой.

## Деградация

**Всегда** имей фолбэк, если ключа нет или запрос упал:

```js
window.askClaude = async function (userText) {
  try {
    if (!localStorage.getItem('anthropic_key')) return mockResponse(userText);
    // ... real call
  } catch (e) {
    console.warn('Claude недоступен, fallback', e);
    return mockResponse(userText);
  }
};

function mockResponse(text) {
  return `[mock] я бы ответил на: "${text.slice(0, 60)}..."`;
}
```

## Безопасность

- `dangerouslyAllowBrowser: true` означает, что ключ светится в браузере. Это **только** для локальных прототипов.
- Никогда не вшивай свой ключ в HTML и не публикуй такой файл.
- Если делишься прототипом — пользователь должен ввести **свой** ключ. Никогда не свой.

## Альтернатива: свой бэк

Если у пользователя есть бэкенд, лучший паттерн — свой endpoint, который проксирует запрос с серверным ключом. Браузер дёргает `/api/claude`, бэк делает реальный вызов. Безопаснее, но требует разворачивания. Для большинства локальных прототипов overkill.
