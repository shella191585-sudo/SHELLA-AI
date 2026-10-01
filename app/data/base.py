from abc import ABC, abstractmethod
from datetime import date

import pandas as pd

REQUIRED_COLUMNS = ["timestamp", "symbol", "open", "high", "low", "close", "volume", "source"]


class MarketDataProvider(ABC):
    @abstractmethod
    def get_price_history(self, symbol: str, start: date, end: date) -> pd.DataFrame:
        """Return daily OHLCV with the normalized REQUIRED_COLUMNS schema."""


def validate_normalized(frame: pd.DataFrame) -> pd.DataFrame:
    missing = set(REQUIRED_COLUMNS).difference(frame.columns)
    if missing:
        raise ValueError(f"Market data missing normalized fields: {sorted(missing)}")
    result = frame[REQUIRED_COLUMNS].copy()
    result["timestamp"] = pd.to_datetime(result["timestamp"], utc=True)
    result = result.sort_values("timestamp").drop_duplicates(["timestamp", "symbol"])
    if result.empty or result["close"].isna().any():
        raise ValueError("Market data has no valid close prices")
    return result
