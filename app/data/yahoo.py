from datetime import date, datetime, timedelta, timezone

import pandas as pd
import requests

from .base import MarketDataProvider, validate_normalized


class YahooFinanceProvider(MarketDataProvider):
    """Small Yahoo chart API adapter. All provider-specific details stay here."""

    source = "yahoo_finance_chart"

    def get_price_history(self, symbol: str, start: date, end: date) -> pd.DataFrame:
        start_dt = datetime.combine(start, datetime.min.time(), tzinfo=timezone.utc)
        end_dt = datetime.combine(end + timedelta(days=1), datetime.min.time(), tzinfo=timezone.utc)
        response = requests.get(
            f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}",
            params={"period1": int(start_dt.timestamp()), "period2": int(end_dt.timestamp()), "interval": "1d"},
            timeout=20,
        )
        response.raise_for_status()
        result = response.json()["chart"]["result"]
        if not result:
            raise ValueError(f"No Yahoo data returned for {symbol}")
        item = result[0]
        quote = item["indicators"]["quote"][0]
        frame = pd.DataFrame(quote)
        frame["timestamp"] = pd.to_datetime(item["timestamp"], unit="s", utc=True)
        frame["symbol"] = symbol
        frame["source"] = self.source
        return validate_normalized(frame)
