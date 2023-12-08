from datetime import datetime, timedelta
from config import SHORT_MA, LONG_MA

from .indicator_heikin import calculate_heikin_ashi
from .indicator_rsi import calculate_rsi
from .indicator_ma import calculate_ma

def rsi(symbol,num_days, binance_spot_api):
    end_time = datetime.now()
    start_time = datetime.now() - timedelta(days=num_days)
    return calculate_rsi(symbol, num_days, start_time, end_time, binance_spot_api)

def heikin_today(symbol, binance_spot_api):
    end_time = datetime.now()
    start_time = end_time - timedelta(days=1)
    candle = calculate_heikin_ashi(symbol, start_time, end_time, binance_spot_api)
    return candle.close - candle.open

def heikin_yesterday(symbol, binance_spot_api):
    end_time = datetime.now() - timedelta(days=1)
    start_time = end_time - timedelta(days=1)
    candle = calculate_heikin_ashi(symbol, start_time, end_time, binance_spot_api)
    return candle.close - candle.open

def moving_averages(symbol, binance_spot_api):
    return  calculate_ma(symbol, SHORT_MA, binance_spot_api), calculate_ma(symbol,LONG_MA, binance_spot_api)



