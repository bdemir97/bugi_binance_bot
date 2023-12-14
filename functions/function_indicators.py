from datetime import datetime

############ RSI 14 SMA 14-2 #############################
def rsi(klines):
    period = len(klines)
    closes = [float(kline[4]) for kline in klines][-period:]
    
    price_changes = [closes[i]-closes[i-1] for i in range(1, period)]
    
    gains = [change if change > 0 else 0 for change in price_changes]
    losses = [-change if change < 0 else 0 for change in price_changes]

    avg_gain = sum(gains) / (period-1)
    avg_loss = sum(losses) / (period-1)

    rs = avg_gain / avg_loss if avg_loss != 0 else 0
    rsi = 100 - (100 / (1 + rs))

    return rsi

#################### HEIKIN ASHI #########################
def heikin_ashi(klines):
    opens = [float(kline[1]) for kline in klines]
    closes = [float(kline[4]) for kline in klines]
    highs = [float(kline[2]) for kline in klines]
    lows = [float(kline[3]) for kline in klines]
    
    heikin_open = (opens[-2] + closes[-1]) / 2
    heikin_close = (opens[-2] + highs[-2] + lows[-1] + closes[-1]) / 4

    return heikin_close - heikin_open

############## MOVING AVERAGE CROSSOVER ###################
def ma(klines):
    closes = [float(kline[4]) for kline in klines]
    ma = sum(closes) / len(closes)

    return ma

############## VOLATILITY CALCULATION ################
def volatility(klines):    
    previous_price = float(klines[0][1])
    current_price = float(klines[-1][4])
    volatility = ((current_price - previous_price) / previous_price) * 100
    
    return volatility

####################### ADX ############################
def adx(klines, period):  #period = adx_period * 1440 / candle_interval
    high_prices = [float(kline[2]) for kline in klines]
    low_prices = [float(kline[3]) for kline in klines]
    close_prices = [float(kline[4]) for kline in klines]
    
    true_range = []
    for i in range(1, len(klines)):
        tr1 = max(high_prices[i] - low_prices[i], abs(high_prices[i] - close_prices[i - 1]))
        tr2 = abs(low_prices[i] - close_prices[i - 1])
        true_range.append(max(tr1, tr2))

    positive_dm = [max(high_prices[i] - high_prices[i - 1], 0) if high_prices[i] - high_prices[i - 1] > low_prices[i - 1] - low_prices[i] else 0 for i in range(1, len(klines))]
    negative_dm = [max(low_prices[i - 1] - low_prices[i], 0) if low_prices[i - 1] - low_prices[i] > high_prices[i] - high_prices[i - 1] else 0 for i in range(1, len(klines))]

    atr = [0] * len(true_range)
    atr[period] = sum(true_range[:period + 1]) / period
    for i in range(period + 1, len(true_range)):
        atr[i] = (atr[i - 1] * (period - 1) + true_range[i]) / period

    positive_di = [100 * sum(positive_dm[:i]) / atr[i] for i in range(1, len(klines) - 1)]
    negative_di = [100 * sum(negative_dm[:i]) / atr[i] for i in range(1, len(klines) - 1)]
    dx = [100 * abs(positive_di[i] - negative_di[i]) / (positive_di[i] + negative_di[i]) for i in range(len(positive_di))]

    adx = [0] * len(dx)
    adx[period] = sum(dx[:period + 1]) / period
    for i in range(period + 1, len(dx)):
        adx[i] = (adx[i - 1] * (period - 1) + dx[i]) / period

    return adx

####################### SUPERTREND ############################
def supertrend(klines, period, multiplier): #period = strend_period * 1440 / candle_interval
    high_prices = [float(kline[2]) for kline in klines]
    low_prices = [float(kline[3]) for kline in klines]
    close_prices = [float(kline[4]) for kline in klines]

    atr = [0] * period
    for i in range(period, len(klines)):
        tr1 = high_prices[i] - low_prices[i]
        tr2 = abs(high_prices[i] - close_prices[i - 1])
        tr3 = abs(low_prices[i] - close_prices[i - 1])
        true_range = max(tr1, tr2, tr3)
        atr.append((atr[-1] * (period - 1) + true_range) / period)

    supertrend = [0] * period
    for i in range(period, len(klines)):
        upper_band = (high_prices[i] + low_prices[i]) / 2 + multiplier * atr[i]
        lower_band = (high_prices[i] + low_prices[i]) / 2 - multiplier * atr[i]

        if close_prices[i - 1] <= supertrend[-1]:
            supertrend.append(min(upper_band, close_prices[i]))
        else:
            supertrend.append(max(lower_band, close_prices[i]))

    return supertrend
    