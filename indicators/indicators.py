from datetime import datetime, timedelta

from .indicator_heikin import calculate_heikin_ashi
from .indicator_rsi import calculate_rsi
from .indicator_ma import calculate_ma

def rsi(symbol,num_days):
    end_time = datetime.now()
    start_time = datetime.now() - timedelta(days=num_days)
    return calculate_rsi(symbol, num_days, start_time, end_time)

def heikin_today(symbol):
    end_time = datetime.now()
    start_time = end_time - timedelta(days=1)
    candle = calculate_heikin_ashi(symbol, start_time, end_time)
    return candle.close - candle.open

def heikin_yesterday(symbol):
    end_time = datetime.now() - timedelta(days=1)
    start_time = end_time - timedelta(days=1)
    candle = calculate_heikin_ashi(symbol, start_time, end_time)
    return candle.close - candle.open

def moving_averages(symbol):
    return  calculate_ma(symbol, 50), calculate_ma(symbol,200)



