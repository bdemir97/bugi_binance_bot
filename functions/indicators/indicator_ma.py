from binance.enums import *
from datetime import datetime, timedelta

def calculate_ma(symbol: str, ma_period: int, binance_spot_api):
    end_time = datetime.now()
    start_time = end_time - timedelta(days=ma_period)

    klines = binance_spot_api.get_historical_klines(
        symbol=symbol, 
        interval=KLINE_INTERVAL_3MINUTE, 
        start_str=str(int(start_time.timestamp() * 1000)),
        end_str=str(int(end_time.timestamp() * 1000)))
    closes = [float(kline[4]) for kline in klines]

    return sum(closes) / len(closes)