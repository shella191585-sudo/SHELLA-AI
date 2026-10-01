# Market Intelligence Loop

A small, reproducible market-state and risk-analysis system for **BTC/USD**, **gold (GLD proxy)**, and **U.S. stocks (SPY proxy)**. It is not a trading bot and cannot execute trades.

## Quick start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m app.main run --days 260
```

The command downloads daily Yahoo Finance history, writes normalized raw candles to SQLite, calculates indicators, persists a timestamped analysis snapshot, and creates `reports/daily-YYYY-MM-DD.md`. Gold uses the liquid GLD ETF proxy, not fabricated XAU/USD data. Macro fields are explicitly recorded as unavailable in this MVP.

Useful commands:

```bash
python -m app.main evaluate --horizon-days 20
python -m app.main feedback ANALYSIS_ID --rating 4 --note "Useful context"
```

## Design

`data → indicators → (AI narrative + deterministic risk engine) → report/content`.

The LLM client is optional and provider-independent. When `LLM_PROVIDER=disabled` (the default), the application produces a deterministic explanatory narrative; no invented analysis or scores are used. The risk score always comes from `app/risk/engine.py`.

## Data and limitations

Yahoo Finance is used as a convenient public MVP source. Source availability, exact source identifier, input candle values, indicator payload, analysis, reasoning, and confidence are retained in the database. Network failures fail clearly rather than silently supplying made-up data. This is informational software, not investment advice.
