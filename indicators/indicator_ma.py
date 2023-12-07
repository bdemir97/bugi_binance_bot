from binance.enums import *
from binance.client import Client
from datetime import datetime, timedelta

def calculate_ma(symbol: str, ma_period: int):
    end_time = datetime.now()
    start_time = end_time - timedelta(days=ma_period)

    klines = Client().get_historical_klines(symbol=symbol, interval=KLINE_INTERVAL_1DAY, startTime=start_time.timestamp() * 1000, endTime=end_time.timestamp() * 1000)
    closes = [float(kline[4]) for kline in klines]

    return sum(closes) / len(closes)