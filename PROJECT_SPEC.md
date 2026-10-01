# Market Intelligence Loop

This implementation follows the MVP specification: daily BTC/USD, gold (GLD), and SPY observations are normalized, persisted, transformed into a small indicator set, assessed by a deterministic risk engine, and rendered into reproducible reports and draft X posts. It is research tooling only and never places trades.

The database stores inputs, indicators, narrative analysis, scores, future outcomes, and user feedback separately so later evaluation can improve rules or prompts without rewriting history.
