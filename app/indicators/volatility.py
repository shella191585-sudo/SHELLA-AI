import pandas as pd


def volatility_indicators(frame: pd.DataFrame) -> dict:
    closes = frame["close"].astype(float)
    returns = closes.pct_change()
    realized = None if len(returns.dropna()) < 20 else float(returns.tail(20).std(ddof=1) * (252 ** 0.5) * 100)
    high_low = frame["high"].astype(float) - frame["low"].astype(float)
    atr = None if len(high_low) < 14 else float(high_low.tail(14).mean())
    rolling_peak = closes.cummax()
    drawdown = (closes / rolling_peak - 1) * 100
    return {"realized_vol_20d_pct": realized, "atr14": atr, "max_drawdown_pct": float(drawdown.min()), "volatility": "HIGH" if realized is not None and realized >= 35 else "NORMAL"}
