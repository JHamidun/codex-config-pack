---
name: "stock-analysis"
description: "Акции и компании через yfinance: цены, инсайдеры, рекомендации аналитиков, SEC. Триггеры: «акции», «биржа», «стоит ли покупать бумагу»."
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


# Stock Analysis

Comprehensive stock and company analysis using Python yfinance library.

## Dependencies

```bash
pip install yfinance pandas openpyxl
```

## Quick Start

```python
import yfinance as yf

# Company info
ticker = yf.Ticker("AAPL")
info = ticker.info  # Full profile
hist = ticker.history(period="1y")  # Price history
recs = ticker.recommendations  # Analyst recommendations
```

## Available Data via yfinance

| Manus API | yfinance Equivalent | Usage |
|-----------|-------------------|-------|
| `get_stock_profile` | `yf.Ticker(sym).info` | Company profile, sector, employees |
| `get_stock_insights` | `yf.Ticker(sym).recommendations` | Analyst ratings, target prices |
| `get_stock_chart` | `yf.Ticker(sym).history()` | OHLCV price data |
| `get_stock_holders` | `yf.Ticker(sym).insider_transactions` | Insider trading activity |
| `get_stock_sec_filing` | `yf.Ticker(sym).sec_filings` | SEC filing history |

## Script

Run analysis via: `python ${CODEX_PACK_ROOT}/library/skills/stock-analysis/scripts/stock_analysis.py`

```bash
# Company overview
python stock_analysis.py profile AAPL

# Price chart data
python stock_analysis.py chart AAPL --period 1y --interval 1d

# Analyst recommendations
python stock_analysis.py recommendations AAPL

# Insider transactions
python stock_analysis.py insiders AAPL

# Full analysis (all data)
python stock_analysis.py full AAPL

# Compare multiple stocks
python stock_analysis.py compare AAPL,MSFT,GOOGL --period 6mo

# Export to Excel
python stock_analysis.py full AAPL --excel output.xlsx
```

## Common Workflows

### Company Overview
```
User: "Tell me about AAPL"
-> profile (business summary, industry, employees)
-> recommendations (analyst outlook)
-> chart (recent performance)
```

### Investment Analysis
```
User: "Is TSLA a good buy?"
-> chart (price trends, 52-week range)
-> recommendations (analyst consensus, target price)
-> profile (business fundamentals)
-> insider_transactions (insider sentiment)
```

### Multi-Stock Comparison
```
User: "Compare AAPL vs MSFT vs GOOGL"
-> chart for each (relative performance)
-> profile for each (market cap, P/E, sector)
-> recommendations for each (ratings comparison)
-> Export side-by-side to Excel
```

## Key Data Points

### Profile: `ticker.info`
- `marketCap`, `sector`, `industry`, `fullTimeEmployees`
- `forwardPE`, `trailingPE`, `dividendYield`
- `fiftyTwoWeekHigh`, `fiftyTwoWeekLow`
- `targetMeanPrice`, `recommendationKey`

### History: `ticker.history(period, interval)`
- Periods: `1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max`
- Intervals: `1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo`
- Returns DataFrame with Open, High, Low, Close, Volume

### Recommendations: `ticker.recommendations`
- Columns: period, strongBuy, buy, hold, sell, strongSell

## When to Use

**Trigger words:** "stock", "share price", "AAPL", "TSLA", "$MSFT", "analyze company", "compare stocks", "insider trading", "SEC filing", "analyst rating", "акции", "курс", "биржа"

## Excel Export Integration

Use with skill `xlsx` for professional reports:

```python
import yfinance as yf
import pandas as pd

ticker = yf.Ticker("AAPL")
hist = ticker.history(period="1y")
hist.to_excel("aapl_history.xlsx", sheet_name="Price History")
```
