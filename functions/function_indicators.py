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

############## VOLATILITY CALCULATION ####################
def volatility(klines):    
    previous_price = float(klines[0][1])
    current_price = float(klines[-1][4])
    volatility = ((current_price - previous_price) / previous_price) * 100
    
    return volatility

################## SMOOTHED ADX ##########################
def adx(klines, period):
    kline_size = len(klines)
    tr_list = []
    dm_plus_list = []
    dm_minus_list = []
    dx_list = []

    for i in range(1, kline_size):
        high = float(klines[i][2])
        low = float(klines[i][3])
        close_prev = float(klines[i - 1][4])

        # True Range
        tr = max(high - low, abs(high - close_prev), abs(low - close_prev))
        tr_list.append(tr)

        # Directional Movements
        dm_plus = max(high - float(klines[i - 1][2]), 0) if high - float(klines[i - 1][2]) > float(klines[i - 1][3]) - low else 0
        dm_minus = max(float(klines[i - 1][3]) - low, 0) if float(klines[i - 1][3]) - low > high - float(klines[i - 1][2]) else 0

        dm_plus_list.append(dm_plus)
        dm_minus_list.append(dm_minus)

    # Initial Averages
    smoothed_tr = sum(tr_list[:period])
    smoothed_dm_plus = sum(dm_plus_list[:period])
    smoothed_dm_minus = sum(dm_minus_list[:period])

    for i in range(period, len(klines)):
        smoothed_tr = (smoothed_tr - (smoothed_tr / period)) + tr_list[i - 1]
        smoothed_dm_plus = (smoothed_dm_plus - (smoothed_dm_plus / period)) + dm_plus_list[i - 1]
        smoothed_dm_minus = (smoothed_dm_minus - (smoothed_dm_minus / period)) + dm_minus_list[i - 1]

        di_plus = 100 * (smoothed_dm_plus / smoothed_tr)
        di_minus = 100 * (smoothed_dm_minus / smoothed_tr)

        dx = 100 * abs(di_plus - di_minus) / (di_plus + di_minus)
        dx_list.append(dx)

    # Smoothing the DX values for ADX
    adx_list = [dx_list[0]]  
    for dx in dx_list[1:]:
        adx_list.append((adx_list[-1] * (period-1) + dx) / period)

    adx = sum(adx_list) / len(adx_list) 

    return adx, abs(di_plus) - abs(di_minus)

####################### SUPERTREND ############################
def supertrend(klines, period, multiplier): 
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
    