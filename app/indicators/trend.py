import pandas as pd


def trend_indicators(closes: pd.Series) -> dict:
    latest = float(closes.iloc[-1])
    mas = {f"ma{window}": float(closes.rolling(window).mean().iloc[-1]) if len(closes) >= window else None for window in (20, 50, 200)}
    above = {f"price_above_ma{window}": None if mas[f"ma{window}"] is None else latest > mas[f"ma{window}"] for window in (20, 50, 200)}
    available = [value for value in above.values() if value is not None]
    classification = "BULLISH" if available and all(available) else "BEARISH" if available and not any(available) else "NEUTRAL"
    return {**mas, **above, "trend": classification}
