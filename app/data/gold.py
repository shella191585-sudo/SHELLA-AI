from .yahoo import YahooFinanceProvider


class GoldProvider(YahooFinanceProvider):
    """GLD is a transparent, liquid gold proxy for this MVP."""
    asset = "GOLD"
    symbol = "GLD"
