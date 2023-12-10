from datetime import datetime, timedelta

from .indicator_heikin import calculate_heikin_ashi
from .indicator_rsi import calculate_rsi
from .indicator_ma import calculate_ma
from .indicator_ema import calculate_dema

def rsi(symbol, num_days, binance_spot_api, CANDLE_LENGTH):
    end_time = datetime.now()
    start_time = datetime.now() - timedelta(days=num_days)
    return calculate_rsi(symbol, num_days, start_time, end_time, binance_spot_api, CANDLE_LENGTH)

def heikin_ashi(symbol, binance_spot_api, CANDLE_LENGTH, HEIKIN_DURATION):
    end_time = datetime.now()
    start_time = end_time - timedelta(minutes=HEIKIN_DURATION)
    candle = calculate_heikin_ashi(symbol, start_time, end_time, binance_spot_api, CANDLE_LENGTH)
    return candle['close'] - candle['open']

def moving_averages(symbol, binance_spot_api, CANDLE_LENGTH, SHORT_MA, LONG_MA):
    return calculate_ma(symbol, SHORT_MA, binance_spot_api, CANDLE_LENGTH), calculate_ma(symbol, LONG_MA, binance_spot_api, CANDLE_LENGTH)

def dema(symbol, binance_spot_api, CANDLE_LENGTH, SHORT_DEMA, LONG_DEMA):
    return calculate_dema(symbol, binance_spot_api, SHORT_DEMA, CANDLE_LENGTH), calculate_dema(symbol, binance_spot_api, LONG_DEMA, CANDLE_LENGTH)



