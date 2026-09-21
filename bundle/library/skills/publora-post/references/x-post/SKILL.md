---
name: "x-post"
description: "Post to X (Twitter) with auto-threading, images, and videos via Publora MCP"
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


# X/Twitter Post

Create and schedule posts to X (Twitter) using the Publora MCP server. Supports text posts, images (up to 4), videos, and automatic thread splitting for long-form content.

## Prerequisites

**Plans:** Pro ($2.99/account/month), Premium ($9.99/account/month)

**Important:** X/Twitter is NOT available on the free Starter plan due to Twitter API costs.

### Getting Started

1. **Create account** at [publora.com/register](https://publora.com/register)
2. **Choose Pro or Premium plan** (X/Twitter requires paid plan)
3. **Connect X/Twitter** via OAuth in [Publora Dashboard](https://publora.com/dashboard)
4. **Get API key** at [publora.com/settings/api](https://publora.com/settings/api)
5. **Configure MCP** in Claude Desktop (`${CODEX_PACK_ROOT}/library/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "publora": {
      "type": "http",
      "url": "https://mcp.publora.com",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      }
    }
  }
}
```

### REST API Fallback

If MCP is unavailable, use the REST API directly:

**Base URL:** `https://api.publora.com/api/v1`

**Authentication:** `x-publora-key` header

```bash
# Get connected platforms
curl -X GET "https://api.publora.com/api/v1/platform-connections" \
  -H "x-publora-key: $PUBLORA_API_KEY"

# Create a post
curl -X POST "https://api.publora.com/api/v1/create-post" \
  -H "x-publora-key: $PUBLORA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "platforms": ["twitter-123456789"],
    "content": "Your tweet content",
    "scheduledTime": "2026-03-25T10:00:00Z"
  }'
```

**Platform ID Format:** `twitter-{id}` (e.g., `twitter-123456789`)

📖 **Docs:** [docs.publora.com](https://docs.publora.com)

### Plan Limits

| Plan | Posts/month | Price |
|------|-------------|-------|
| Starter | **Not available** | Free |
| Pro | 100/account | $2.99/account/month |
| Premium | 500/account | $9.99/account/month |

## Platform Limits

| Feature | API Limit | Notes |
|---------|-----------|-------|
| Characters | 280 | Emojis count as 2 characters |
| Images | Up to 4 | Auto-converted to PNG (max 1000px width) |
| Video duration | **2 minutes** | API limit (native app allows 2:20) |
| Video size | 512 MB | MP4, MOV formats |
| Threading | Automatic | Content over 280 chars split with `(1/N)` markers |

## Character Counting

X has specific character counting rules that Publora handles automatically:

- Standard characters = 1
- **Emojis = 2 characters**
- URLs counted by literal length
- Thread markers reserve 10 characters per tweet

## Auto-Threading

When content exceeds 280 characters, Publora automatically creates a connected thread:

1. Content split at paragraph breaks, then sentence boundaries, then word boundaries
2. Each part numbered with `(1/N)`, `(2/N)` format
3. Tweets connected via X's `reply_to_id` parameter

### Manual Thread Breaks

Use `---` on its own line to force a thread break:

```
This is my first tweet in the thread.

---

This is my second tweet in the thread.

---

And this is my third tweet!
```

## Available Tools

### create_post
Create a new X/Twitter post or thread.

**Parameters:**
- `platforms`: Array with your X connection ID (e.g., `["twitter-12345678"]`)
- `content`: Post text (auto-threads if over 280 chars)
- `scheduledTime`: ISO 8601 datetime (**required** - for immediate posting, use current time + 1 minute)

### get_upload_url
Get presigned URL for media uploads.

**Parameters:**
- `postGroupId`: Post ID to attach media to
- `fileName`: File name (e.g., "image.png", "video.mp4")
- `contentType`: `image/png`, `image/jpeg`, `video/mp4`
- `type`: `"image"` or `"video"`

### list_posts / update_post / delete_post
Manage scheduled and draft posts.

## Examples

### Simple Tweet
```
Post this to X:
"Just shipped our new API documentation. Check it out!"
```

### Tweet with Images
```
Post this to Twitter with screenshots of the new dashboard:
"Before and after our redesign. What do you think?"
```
Note: Up to 4 images allowed. All images auto-converted to PNG.

### Long-Form Thread
```
Create a Twitter thread:
"Thread: 5 lessons from building our startup

---

1. Ship early, iterate fast. We launched with a buggy MVP and improved based on real feedback.

---

2. Talk to users daily. Our best features came from customer conversations.

---

3. Focus beats features. We killed 3 products to focus on the one that worked."
```

### Scheduled Tweet
```
Schedule this for tomorrow at 9 AM:
"Monday motivation: Start before you're ready."
```

## Important Restrictions

1. **Pro plan required**: X/Twitter is excluded from the free Starter plan due to Twitter API costs.

2. **2-minute video limit**: The X API limits videos to 2 minutes, even though the native app allows longer videos.

3. **Image auto-conversion**: All images are converted to PNG (max 1000px width) before upload. Animated GIFs lose animation.

4. **No image+video mix**: A tweet can have images OR video, not both.

5. **Media on first tweet only**: In threads, images/video attach to the first tweet only.

## Best Practices

### Content
1. **Hook in first line**: Most engagement happens on the first tweet
2. **Optimal thread length**: 3-7 tweets for best engagement
3. **Emoji awareness**: Remember emojis count as 2 characters

### Timing
- **Best times**: 8-10 AM, 12-1 PM, 5-6 PM in target timezone
- **Frequency**: 3-5 tweets per day for growth
- **Threads**: Post in morning for maximum visibility

### Engagement
- Reply to comments within the first hour
- Quote tweet your own threads for visibility
- Use relevant hashtags (1-2 per tweet)

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| "X/Twitter requires Pro plan" | Using Starter plan | Upgrade to Pro at publora.com/settings |
| "Content too long" | Over 280 chars and threading failed | Add manual `---` breaks |
| "Video too long" | Over 2 minutes | Trim video to under 2 minutes |
| "Too many images" | More than 4 images | Reduce to 4 or fewer |
| "Rate limit exceeded" | X API limit reached | Wait and retry |
