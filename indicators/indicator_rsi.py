from binance.enums import *
from binance.client import Client

def calculate_rsi(symbol, num_days, start_time, end_time):
    klines = Client().get_historical_klines(
        symbol=symbol,
        interval=KLINE_INTERVAL_1DAY,
        startTime=start_time.timestamp() * 1000,
        endTime=end_time.timestamp() * 1000,
        klines_type=HistoricalKlinesType.SPOT
    )
    
    closes = [float(kline[4]) for kline in klines]
    price_changes = [closes[i] - closes[i - 1] for i in range(1, len(closes))]
    gains = [change if change > 0 else 0 for change in price_changes]
    losses = [-change if change < 0 else 0 for change in price_changes]

    avg_gain = sum(gains) / num_days
    avg_loss = sum(losses) / num_days

    rs = avg_gain / avg_loss if avg_loss != 0 else 0
    rsi = 100 - (100 / (1 + rs))
    return rsi




