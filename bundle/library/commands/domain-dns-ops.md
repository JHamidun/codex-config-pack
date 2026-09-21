---
name: "domain-dns-ops"
description: "Manage DNS records via Cloudflare API - list, add, update, delete records, check SSL, manage proxy. Use with /domain-dns-ops or \"DNS\", \"домен\"."
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


# Domain & DNS Operations via Cloudflare

Manage DNS records and domain settings through Cloudflare API.

## Setup

API credentials from `${CODEX_PACK_ROOT}/library/.credentials.master.env`:
- `CLOUDFLARE_API_TOKEN` or `CLOUDFLARE_API_KEY` + `CLOUDFLARE_EMAIL`

See `${CODEX_PACK_ROOT}/library/config/cloudflare.md` for zone IDs and config.

## Operations

### List DNS Records
```bash
curl -s -X GET "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" | python -m json.tool
```

### Add DNS Record
```bash
curl -s -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  --data '{
    "type": "A",
    "name": "subdomain.example.com",
    "content": "YOUR_PUBLIC_IP",
    "ttl": 1,
    "proxied": true
  }'
```

### Update DNS Record
```bash
curl -s -X PATCH "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  --data '{"content": "YOUR_PUBLIC_IP"}'
```

### Delete DNS Record
```bash
curl -s -X DELETE "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}" \
  -H "Authorization: Bearer $API_KEY"
```

### Check SSL Status
```bash
curl -s -X GET "https://api.cloudflare.com/client/v4/zones/{zone_id}/ssl/verification" \
  -H "Authorization: Bearer $API_KEY"
```

## Common Record Types

| Type | Use Case | Example |
|------|----------|---------|
| A | IPv4 address | `YOUR_PUBLIC_IP` |
| AAAA | IPv6 address | `2001:db8::1` |
| CNAME | Alias | `other.example.com` |
| MX | Mail server | `mail.example.com` (priority 10) |
| TXT | Verification, SPF, DKIM | `v=spf1 include:...` |
| SRV | Service location | `_sip._tcp` |

## Process

1. User specifies domain operation
2. Load Cloudflare credentials from env
3. Identify zone ID for the domain
4. Execute API call
5. Verify the change
6. Report result

## Safety
- Always confirm before DELETE operations
- Show current state before UPDATE
- Verify DNS propagation after changes: `dig +short subdomain.example.com`
