---
name: "bot-debug"
description: "Telegram bot debugging helper с анализом логов и common issues"
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


# 🐛 Bot Debug: $ARGUMENTS

Проанализируй и помоги отладить Telegram бота: **$ARGUMENTS**

## Process:

### 1. Identify Problem Type

**Автоматически определи тип проблемы:**
- 🔴 **Bot not responding** - Бот не отвечает на команды
- 🟡 **Scene stuck** - Застревание в conversation handler
- 🟠 **Commands as text** - Команды обрабатываются как обычный текст
- 🔵 **Middleware issues** - Проблемы с порядком middleware
- 🟣 **Database errors** - Ошибки подключения к БД
- ⚫ **Memory leaks** - Утечки памяти в long-polling
- 🟢 **Deployment issues** - Проблемы с Docker/webhook

### 2. Analyze Code

**Используй telegram-bot-toolkit skill:**
```
"Используй telegram-bot-toolkit: analyze bot code в $ARGUMENTS"
```

**Проверь:**
- Handler order (commands BEFORE conversation handler)
- Middleware sequence (logging → auth → commands → conversation)
- Scene management (per_user=True, fallbacks present)
- Callback query handling (query.answer() called)
- Error handlers (error_handler registered)

### 3. Check Common Bugs

#### Bug #1: Bot застревает в scene
**Symptoms:** /start не работает when in conversation

**Check:**
```python
# WRONG:
states={
    SCENE: [
        MessageHandler(filters.TEXT, handler)  # catches commands!
    ]
}

# CORRECT:
states={
    SCENE: [
        MessageHandler(filters.TEXT & ~filters.COMMAND, handler)
    ]
}
# OR:
fallbacks=[CommandHandler('start', start)]
```

#### Bug #2: Commands обрабатываются как text
**Symptoms:** /help, /settings не работают

**Check middleware order:**
```python
# Commands MUST be in lower group than conversation
app.add_handler(CommandHandler('help', help), group=1)
app.add_handler(conversation_handler, group=2)
```

#### Bug #3: Callback queries timeout
**Symptoms:** "Query is too old" errors

**Check:**
```python
async def button_handler(update, context):
    query = update.callback_query
    await query.answer()  # MUST be first!
    # ... rest of logic
```

#### Bug #4: Memory leak
**Symptoms:** Memory grows over time

**Check:**
```python
# Clean up user_data periodically
async def cleanup(context):
    for user_id in list(context.application.user_data.keys()):
        if is_inactive(user_id):
            del context.application.user_data[user_id]
```

### 4. Analyze Logs

**If logs provided:**
- Parse error messages
- Identify stack traces
- Find root cause
- Suggest specific fix

**Log patterns to look for:**
```
ERROR:... ConversationHandler... - Scene handling issue
ERROR:... Conflict: terminated by other getUpdates - Multiple instances
ERROR:... Network error - Connection issues
WARNING:... Callback query is too old - query.answer() missing
```

### 5. Debug Strategy

**Quick checks:**
```bash
# 1. Check if bot is running
ps aux | grep python | grep bot

# 2. Check logs
tail -f logs/bot.log

# 3. Test connection
curl https://api.telegram.org/bot<TOKEN>/getMe

# 4. Check handlers order
# Add logging to see handler execution
```

**Test scenarios:**
```python
# 1. Test /start command
# 2. Test conversation flow
# 3. Test callback buttons
# 4. Test error handling
# 5. Test concurrent users
```

### 6. Fix Recommendations

**Generate fix based on problem type:**

**For scene issues:**
```python
# Add ~filters.COMMAND to text handlers
# Add proper fallbacks
# Use per_user=True in ConversationHandler
```

**For middleware issues:**
```python
# Reorder handlers: logging(-1) → auth(0) → commands(1) → conversation(2)
```

**For database issues:**
```python
# Check connection string
# Add retry logic
# Use connection pooling
```

**For deployment:**
```python
# Check environment variables
# Verify webhook URL
# Test health endpoints
```

### 7. Testing Plan

**Create test checklist:**
- [ ] Bot responds to /start
- [ ] Conversation flow works
- [ ] Commands work in conversation
- [ ] Callbacks respond immediately
- [ ] Error messages показываются
- [ ] Database operations succeed
- [ ] Multiple users don't interfere
- [ ] Memory stable over time

### 8. Prevention

**Best practices для избежания проблем:**
```python
# 1. Always use ~filters.COMMAND
states={
    SCENE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handler)]
}

# 2. Always answer callbacks
await query.answer()

# 3. Always register error handler
app.add_error_handler(error_handler)

# 4. Always log important events
logger.info(f"User {user_id} started conversation")

# 5. Always clean up user_data
# Schedule periodic cleanup
```

## Output Format:

### Problem Analysis
**Issue Type:** [type]
**Root Cause:** [detailed explanation]
**Affected:** [what's not working]

### Solution
**Quick Fix:** [immediate action]
```python
# Code changes needed
```

**Long-term Fix:** [proper solution]
```python
# Better implementation
```

### Testing
**Test Steps:**
1. [step 1]
2. [step 2]
3. [step 3]

**Expected Result:** [what should happen]

### Prevention
**Best Practices:** [how to avoid in future]

## Examples:

```
/bot-debug Bot застревает после /start command в your-project/backend/bot
```

```
/bot-debug Commands /help и /settings не работают, обрабатываются как text
```

```
/bot-debug Callback buttons показывают "query is too old" error
```

```
/bot-debug src/handlers/onboarding.py - users can't exit onboarding flow
```

## Integration:

**Automatically uses:**
- telegram-bot-toolkit skill для patterns
- Read tool для анализа кода
- Grep для поиска problems в логах

---

**Начинай debugging! 🐛**
