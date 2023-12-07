from binance.enums import *
from binance.client import Client
from binance.enums import *
from binance.client import Client

def calculate_heikin_ashi(symbol, start_time, end_time):
    klines = Client().get_historical_klines(
        symbol=symbol,
        interval=KLINE_INTERVAL_1DAY,
        startTime=start_time.timestamp() * 1000,
        endTime=end_time.timestamp() * 1000,
        klines_type=HistoricalKlinesType.SPOT
    )
    opens = [float(kline[1]) for kline in klines]
    closes = [float(kline[4]) for kline in klines]
    highs = [float(kline[2]) for kline in klines]
    lows = [float(kline[3]) for kline in klines]
    
    heikin_open = (opens[-1] + closes[-1]) / 2
    heikin_close = (opens[-1] + highs[-1] + lows[-1] + closes[-1]) / 4
    heikin_high = max(highs[-1], heikin_open, heikin_close)
    heikin_low = min(lows[-1], heikin_open, heikin_close)

    return {
        "open": heikin_open,
        "high": heikin_high,
        "low": heikin_low,
        "close": heikin_close
    }

