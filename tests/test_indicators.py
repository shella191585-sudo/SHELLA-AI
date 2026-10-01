import pandas as pd

from app.indicators.momentum import momentum_indicators
from app.indicators.trend import trend_indicators
from app.indicators.volatility import volatility_indicators


def test_indicators_for_rising_series():
    closes = pd.Series(range(1, 251), dtype=float)
    trend = trend_indicators(closes)
    assert trend["trend"] == "BULLISH" and trend["price_above_ma200"] is True
    assert momentum_indicators(closes)["change_20d_pct"] > 0
    frame = pd.DataFrame({"close": closes, "high": closes + 1, "low": closes - 1})
    assert volatility_indicators(frame)["atr14"] == 2.0
