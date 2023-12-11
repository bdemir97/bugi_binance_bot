from .indicator_heikin import calculate_heikin_ashi
from .indicator_rsi import calculate_rsi
from .indicator_ma import calculate_ma
from .indicator_ema import calculate_dema
from .indicator_volatility import calculate_volatility

def rsi(symbol, num_days, binance_spot_api, CANDLE_LENGTH):
    return calculate_rsi(symbol, num_days, binance_spot_api, CANDLE_LENGTH)

def heikin_ashi(symbol, binance_spot_api, CANDLE_LENGTH, HEIKIN_DURATION):
    return calculate_heikin_ashi(symbol, binance_spot_api, CANDLE_LENGTH, HEIKIN_DURATION)

def moving_averages(symbol, binance_spot_api, CANDLE_LENGTH, SHORT_MA, LONG_MA):
    return calculate_ma(symbol, SHORT_MA, binance_spot_api, CANDLE_LENGTH), calculate_ma(symbol, LONG_MA, binance_spot_api, CANDLE_LENGTH)

def dema(symbol, binance_spot_api, CANDLE_LENGTH, SHORT_DEMA, LONG_DEMA):
    return calculate_dema(symbol, binance_spot_api, SHORT_DEMA, CANDLE_LENGTH), calculate_dema(symbol, binance_spot_api, LONG_DEMA, CANDLE_LENGTH)

def volatility(symbol, binance_spot_api, candle_length, candle_diff):
    return calculate_volatility(symbol, binance_spot_api, candle_length, candle_diff)

