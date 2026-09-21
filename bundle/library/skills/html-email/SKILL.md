---
name: "html-email"
description: "HTML-письма: табличная разметка, inline CSS, Outlook-safe, dark-mode. Триггеры: «newsletter html», «MJML», «transactional email». НЕ обычная веб-страница."
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


# HTML email

HTML-письма — это не HTML 2026 года, это HTML 1999-го. Outlook рендерит через Word. Gmail обрезает CSS. Apple Mail почти нормальный.

## Правила, которые не меняются

1. **Табличная разметка.** Не CSS Grid, не Flex — `<table>` с явным `width`.
2. **Inline CSS.** Никаких `<style>` снаружи (Gmail обрезает).
3. **Шрифты — system или Web-safe.** Никаких Google Fonts (не загрузятся в большинстве клиентов).
4. **Изображения с alt.** Многие клиенты картинки блокируют по умолчанию.
5. **Ширина 600px.** Стандарт.
6. **Без JavaScript.** Никогда.

## Скелет

```html
<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width">
  <title>Заголовок</title>
</head>
<body style="margin:0;padding:0;background:#f4f4f4;font-family:-apple-system,Segoe UI,Helvetica,Arial,sans-serif;">

  <!-- Preheader: текст-предпросмотр в inbox, скрыт в письме -->
  <div style="display:none;font-size:1px;line-height:1px;max-height:0;max-width:0;opacity:0;overflow:hidden;">
    Превью текста в inbox — первые 80 символов.
  </div>

  <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background:#f4f4f4;">
    <tr>
      <td align="center" style="padding:32px 16px;">

        <!-- Конверт -->
        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="600" style="max-width:600px;background:#fff;border-radius:8px;">

          <!-- Header -->
          <tr>
            <td style="padding:32px 32px 16px;text-align:center;">
              <img src="https://example.com/logo.png" width="120" alt="Brand" style="display:block;margin:0 auto;">
            </td>
          </tr>

          <!-- Body -->
          <tr>
            <td style="padding:16px 32px;color:#111;font-size:16px;line-height:1.5;">
              <h1 style="font-size:24px;line-height:1.2;margin:0 0 16px;color:#111;">Здравствуйте, Иван!</h1>
              <p style="margin:0 0 16px;">Спасибо за регистрацию. Подтвердите email, нажав кнопку ниже.</p>
            </td>
          </tr>

          <!-- CTA -->
          <tr>
            <td style="padding:8px 32px 32px;">
              <table role="presentation" cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <td bgcolor="#111111" style="border-radius:6px;">
                    <a href="https://example.com/verify?t=abc" style="display:inline-block;padding:14px 28px;color:#fff;text-decoration:none;font-weight:600;font-size:15px;">Подтвердить email</a>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="padding:24px 32px;border-top:1px solid #eee;color:#666;font-size:12px;line-height:1.5;text-align:center;">
              Если кнопка не работает, скопируйте ссылку:<br>
              <a href="https://example.com/verify?t=abc" style="color:#666;word-break:break-all;">https://example.com/verify?t=abc</a>
            </td>
          </tr>

        </table>

        <p style="color:#999;font-size:11px;margin:16px 0 0;">
          Получено по адресу user@example.com.
          <a href="https://example.com/unsub" style="color:#999;">Отписаться</a>.
        </p>

      </td>
    </tr>
  </table>

</body>
</html>
```

## Outlook-specific

Outlook 2007–2019 рендерит через Word, ломает практически всё. Особое внимание:

- Кнопки делай через VML или табличный bullet-proof button (выше).
- `border-radius` Outlook не понимает — будет квадратная.
- `padding` на `<a>` Outlook игнорирует — нужен `padding` на `<td>`, обёртывающий `<a>`.

Для VML-кнопок (если важна закруглённость в Outlook) ищи bulletproof email button generators.

## Dark mode

Apple Mail и iOS Mail инвертируют светлые письма. Можно подсказать:

```html
<meta name="color-scheme" content="light dark">
<meta name="supported-color-schemes" content="light dark">
```

И в CSS:

```css
@media (prefers-color-scheme: dark) {
  body, .container { background: #1a1a1a !important; color: #eee !important; }
  a { color: #88aaff !important; }
}
```

`!important` нужен, потому что inline-стили перевешивают media query.

## Тестирование

- **Litmus** или **Email on Acid** — платно, но самые точные.
- **Gmail (web + mobile)** — отправь себе.
- **Apple Mail** — отправь.
- **Outlook 365** (web и desktop) — отправь.
- Не доверяй визуализаторам в Mailchimp/SendGrid — они не точные.

## Размер

- HTML <100KB. Gmail обрезает то, что больше **102KB** — превратится в `[Message clipped]`.
- Картинки внешними URL, не base64 (раздувает).

## Что НЕ делать

- ❌ `<form>` внутри письма — не сработает в Gmail.
- ❌ Шрифты с Google Fonts — не загрузятся в Outlook, Yahoo.
- ❌ CSS-сетка / flex — Outlook не понимает.
- ❌ Анимированные SVG — большинство клиентов не покажет.
- ❌ Видео `<video>` — никто не покажет.

## Подробности

Расширенный материал вынесен в `references/legacy-html-email.md` — открывай, когда короткого канона выше не хватает. Секции там: Что НЕ работает в email, Что работает, Каркас, Правила, Bulletproof button, Mobile responsive, Тестирование, MJML alternative, Антипаттерны.
