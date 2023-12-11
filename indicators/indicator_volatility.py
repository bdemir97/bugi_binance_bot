from datetime import datetime, timedelta

def calculate_volatility(symbol, binance_spot_api, candle_length, candle_diff):
    end_time = datetime.now()
    start_time = end_time - timedelta(minutes=candle_diff)

    klines = binance_spot_api.get_historical_klines(
        symbol=symbol,
        interval=candle_length,
        start_str=str(int(start_time.timestamp() * 1000)),
        end_str=str(int(end_time.timestamp() * 1000)))
    
    previous_price = float(klines[0][1])
    current_price = float(klines[-1][4])

    return ((current_price - previous_price) / previous_price) * 100