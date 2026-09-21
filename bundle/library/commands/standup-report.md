---
name: "standup-report"
description: "Сводный отчёт по standup updates за период"
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


# 📊 Standup Report: $ARGUMENTS

Создай сводный отчёт за: **$ARGUMENTS**

## Process:

### 1. Collect Data

**Git Activity:**
```bash
git log --since="1 week ago" --pretty=format:"%h - %an: %s"
git shortlog -s -n --since="1 week ago"
```

**GitHub PRs** (если GitHub MCP доступен):
- Merged PRs
- Open PRs
- PR reviews

**Linear/Jira Updates** (если MCP настроен):
- Completed issues
- In progress issues
- Blocked issues

**Slack Activity** (опционально):
- Daily standup messages
- Важные обсуждения

### 2. Aggregate Metrics

**Velocity:**
- Story points completed
- Issues closed
- PRs merged

**Quality:**
- Bug count (opened vs closed)
- Code review turnaround time
- Test coverage changes

**Blockers:**
- Current blockers
- Resolved blockers
- Dependencies

### 3. Create Report

**Используй xlsx skill** для dashboard:

**Sheet 1: Summary**
| Metric | This Period | Last Period | Change |
|--------|-------------|-------------|--------|
| Story Points | 34 | 28 | +21% ✅ |
| PRs Merged | 12 | 15 | -20% ⚠️ |
| Bugs Fixed | 8 | 5 | +60% ✅ |

**Sheet 2: Team Activity**
| Member | Commits | PRs | Issues | Status |
|--------|---------|-----|--------|--------|
| Developer 1 | 45 | 3 | 5 | ✅ On track |
| Developer 2 | 32 | 2 | 4 | ✅ On track |

**Sheet 3: Completed Features**
- Feature A (PROJ-123) - Deployed ✅
- Feature B (PROJ-124) - In review 🔍
- Feature C (PROJ-125) - Blocked ⚠️

### 4. Executive Summary (pptx skill)

**Slide 1: Highlights**
- Top achievements
- Key metrics
- Important decisions

**Slide 2: Team Progress**
- Velocity trend (chart)
- Completed features
- Upcoming work

**Slide 3: Issues & Blockers**
- Current blockers
- Mitigation plans
- Help needed

### 5. Distribution

**Email format:**
```
Subject: Weekly Update - [Date Range]

Hi team,

Here's our weekly summary:

🎯 HIGHLIGHTS:
- Shipped feature X to production
- Resolved 8 bugs
- Completed Sprint 23 with 34 points

📊 METRICS:
- Velocity: 34 pts (+21% vs last week)
- PRs Merged: 12
- Test Coverage: 85% (+2%)

⚠️ BLOCKERS:
- Waiting for API access from Partner team
- Database migration pending approval

📋 NEXT WEEK:
- Start Sprint 24
- Focus on Feature Y
- Tech debt cleanup

Dashboard: [link to Excel]

Best,
[Your name]
```

**Slack post** (#general or #updates):
```
📊 *Weekly Update - Week 45*

*Highlights:*
✅ Shipped feature X
✅ 34 story points completed
✅ 8 bugs resolved

*Metrics:* Velocity +21%, Coverage 85%
*Next:* Sprint 24, Feature Y

📈 Full dashboard: [link]
```

## Output:

1. **Excel Dashboard** (detailed metrics)
2. **PowerPoint Summary** (exec-ready)
3. **Email/Slack formatted** update
4. **Notion page** (если MCP настроен)

## Examples:

```
/standup-report week
/standup-report last week
/standup-report this month
/standup-report Q4 2024
```

**Создаю standup report! 📊**
