from config import CANDLE_LENGTH
from datetime import datetime, timedelta

def calculate_ema(symbol, binance_spot_api, window):
    end_time = datetime.now()
    start_time = end_time - timedelta(days=window)

    klines = binance_spot_api.get_historical_klines(
        symbol=symbol,
        interval=CANDLE_LENGTH,
        start_str=str(int(start_time.timestamp() * 1000)),
        end_str=str(int(end_time.timestamp() * 1000)))
    
    close_prices = [candle[4] for candle in klines]

    ema = [close_prices[0]]
    multiplier = 2 / (window + 1)
    for i in range(1, len(close_prices)):
        ema_value = (close_prices[i] - ema[i - 1]) * multiplier + ema[i - 1]
        ema.append(ema_value)

    return ema

def calculate_dema(symbol, binance_spot_api, window):
    ema = calculate_ema(symbol, binance_spot_api, window)
    dema = 2 * ema - calculate_ema(ema, window)
    
    return dema[-1]