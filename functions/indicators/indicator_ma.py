from config import CANDLE_LENGTH
from datetime import datetime, timedelta

def calculate_ma(symbol: str, ma_period: int, binance_spot_api):
    end_time = datetime.now()
    start_time = end_time - timedelta(days=ma_period)

    klines = binance_spot_api.get_historical_klines(
        symbol=symbol, 
        interval=CANDLE_LENGTH, 
        start_str=str(int(start_time.timestamp() * 1000)),
        end_str=str(int(end_time.timestamp() * 1000)))
    closes = [float(kline[4]) for kline in klines]

    return sum(closes[(ma_period*-1):]) / ma_period