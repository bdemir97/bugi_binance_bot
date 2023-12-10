from datetime import datetime

def calculate_rsi(symbol, num_days, start_time: datetime, end_time: datetime, binance_spot_api, candle_length):
    klines = binance_spot_api.get_historical_klines(
        symbol=symbol,
        interval=candle_length,
        start_str=str(int(start_time.timestamp() * 1000)),
        end_str=str(int(end_time.timestamp() * 1000)))
    
    closes = [float(kline[4]) for kline in klines]
    price_changes = [closes[i] - closes[i - 1] for i in range(1, len(closes))]
    gains = [change if change > 0 else 0 for change in price_changes]
    losses = [-change if change < 0 else 0 for change in price_changes]

    avg_gain = sum(gains) / num_days
    avg_loss = sum(losses) / num_days

    rs = avg_gain / avg_loss if avg_loss != 0 else 0
    rsi = 100 - (100 / (1 + rs))
    return rsi




