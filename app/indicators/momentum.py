import pandas as pd


def _change(closes: pd.Series, periods: int) -> float | None:
    return None if len(closes) <= periods else float((closes.iloc[-1] / closes.iloc[-1 - periods] - 1) * 100)


def momentum_indicators(closes: pd.Series) -> dict:
    delta = closes.diff()
    gain, loss = delta.clip(lower=0), -delta.clip(upper=0)
    avg_gain, avg_loss = gain.rolling(14).mean().iloc[-1], loss.rolling(14).mean().iloc[-1]
    rsi = None if len(closes) < 15 or avg_loss == 0 else float(100 - (100 / (1 + avg_gain / avg_loss)))
    return {"rsi14": rsi, "change_20d_pct": _change(closes, 20), "change_60d_pct": _change(closes, 60)}
