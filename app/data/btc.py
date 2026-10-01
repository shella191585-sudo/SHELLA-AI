from .yahoo import YahooFinanceProvider


class BtcProvider(YahooFinanceProvider):
    asset = "BTC"
    symbol = "BTC-USD"
