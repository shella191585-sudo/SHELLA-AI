from .yahoo import YahooFinanceProvider


class StocksProvider(YahooFinanceProvider):
    asset = "US_STOCKS"
    symbol = "SPY"
