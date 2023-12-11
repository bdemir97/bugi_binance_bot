from datetime import datetime, timedelta

def calculate_heikin_ashi(symbol, binance_spot_api, candle_length, HEIKIN_DURATION):
    end_time = datetime.now()
    start_time = end_time - timedelta(minutes=HEIKIN_DURATION)

    klines = binance_spot_api.get_historical_klines(
        symbol=symbol,
        interval=candle_length,
        start_str=str(int(start_time.timestamp() * 1000)),
        end_str=str(int(end_time.timestamp() * 1000)))
    opens = [float(kline[1]) for kline in klines]
    closes = [float(kline[4]) for kline in klines]
    highs = [float(kline[2]) for kline in klines]
    lows = [float(kline[3]) for kline in klines]
    
    heikin_open = (opens[-1] + closes[-1]) / 2
    heikin_close = (opens[-1] + highs[-1] + lows[-1] + closes[-1]) / 4
    #heikin_high = max(highs[-1], heikin_open, heikin_close)
    #heikin_low = min(lows[-1], heikin_open, heikin_close)

    return heikin_close - heikin_open

