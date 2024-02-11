import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator
from ta.trend import ADXIndicator

############ RSI 14 SMA 14-2 #############################
def rsi(klines):
    columns = ['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore']
    df = pd.DataFrame(klines, columns=columns)
    df['Close'] = pd.to_numeric(df['Close'])
    
    rsi_indicator = RSIIndicator(df['Close'])
    return rsi_indicator.rsi().iloc[-1]

#################### HEIKIN ASHI #########################
def heikin_ashi(klines):
    columns = ['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore']
    df = pd.DataFrame(klines, columns=columns)
    df['High'] = pd.to_numeric(df['High'])
    df['Low'] = pd.to_numeric(df['Low'])
    df['Close'] = pd.to_numeric(df['Close'])
    df['Open'] = pd.to_numeric(df['Open'])

    
    df['HA_Close'] = (df['Open'] + df['High'] + df['Low'] + df['Close']) / 4
    df['HA_Open'] = ((df['Open'].shift(1) + df['Close'].shift(1)) / 2).fillna((df['Open'] + df['Close']) / 2)

    if df['HA_Close'].iloc[-1] > df['HA_Open'].iloc[-1]:
            return 1
    elif df['HA_Close'].iloc[-1] < df['HA_Open'].iloc[-1]:
            return -1
    return 0

############## SMA #############################
def sma(klines):
    columns = ['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore']
    df = pd.DataFrame(klines, columns=columns)
    df['Close'] = pd.to_numeric(df['Close'])

    sma = df['Close'].rolling(window=len(klines)).mean().iloc[-1]

    return sma

############## EMA #############################
def ema(klines):
    columns = ['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore']
    df = pd.DataFrame(klines, columns=columns)
    df['Close'] = pd.to_numeric(df['Close'])

    ema = df['Close'].ewm(span=len(klines), adjust=False).mean().iloc[-1]

    return ema

############## VOLATILITY CALCULATION ####################
def volatility(klines):    
    previous_price = float(klines[0][1])
    current_price = float(klines[-1][4])
    volatility = ((current_price - previous_price) / previous_price) * 100
    
    return volatility

################## SMOOTHED ADX ##########################
def adx(klines):
    columns = ['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore']
    df = pd.DataFrame(klines, columns=columns)
    df['High'] = pd.to_numeric(df['High'])
    df['Low'] = pd.to_numeric(df['Low'])
    df['Close'] = pd.to_numeric(df['Close'])

    adx_indicator = ADXIndicator(df['High'], df['Low'], df['Close'])
    adx = adx_indicator.adx().iloc[-1]
    #dplus = adx_indicator.adx_pos().iloc[-1]
    #dminus = adx_indicator.adx_neg().iloc[-1]

    return adx #, abs(dplus) - abs(dminus)

####################### SUPERTREND ############################

def calculate_atr(df, period):
    high_low = df['High'] - df['Low']
    high_close = np.abs(df['High'] - df['Close'].shift())
    low_close = np.abs(df['Low'] - df['Close'].shift())
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = np.max(ranges, axis=1)
    atr = true_range.rolling(period).mean()
    return atr

def supertrend(klines, period, multiplier): 
    columns = ['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore']
    df = pd.DataFrame(klines, columns=columns)
    df['High'] = pd.to_numeric(df['High'])
    df['Low'] = pd.to_numeric(df['Low'])
    df['Close'] = pd.to_numeric(df['Close'])
    
    hl2 = (df['High'] + df['Low']) / 2
    atr = calculate_atr(df, period=period)
    
    supertrend = pd.Series([float('nan')] * len(df))
    for i in range(1, len(df)):
        if df['Close'][i] > supertrend[i - 1]:
            supertrend[i] = hl2[i] - (multiplier * atr[i])
        else:
            supertrend[i] = hl2[i] + (multiplier * atr[i])
        
        if supertrend[i] > supertrend[i - 1]:
            if df['Close'][i] > supertrend[i - 1]:
                supertrend[i] = max(supertrend[i], supertrend[i - 1])
        else:
            if df['Close'][i] < supertrend[i - 1]:
                supertrend[i] = min(supertrend[i], supertrend[i - 1])
    
    if df['Close'].iloc[-1] > supertrend.iloc[-1]:
            return supertrend.iloc[-1],1
    if df['Close'].iloc[-1] < supertrend.iloc[-1]:
            return supertrend.iloc[-1],-1

    return supertrend.iloc[-1],0

############## ICHIMOKU CLOUD ################
    
def ichimoku_cloud(klines, config_manager):
    current_price = (float(klines[-1][3]) + float(klines[-1][2]))/2
    ichimoku_data = pd.DataFrame(klines, columns=["timestamp", "open", "high", "low", "close", "volume", "close_time", "quote_asset_volume","number_of_trades", "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"])

    tenkan_sen = (ichimoku_data['high'].rolling(window=config_manager.get("TENKAN_PERIOD")).max() + ichimoku_data['low'].rolling(window=config_manager.get("TENKAN_PERIOD")).min()) / 2 
    kijun_sen = (ichimoku_data['high'].rolling(window=config_manager.get("KIJUN_PERIOD")).max() + ichimoku_data['low'].rolling(window=config_manager.get("KIJUN_PERIOD")).min()) / 2 
    senkou_a = (tenkan_sen + kijun_sen) / 2 
    senkou_b = (ichimoku_data['high'].rolling(window=config_manager.get("SENKOU_PERIOD")).max() + ichimoku_data['low'].rolling(window=config_manager.get("SENKOU_PERIOD")).min()) / 2
    chikou = ichimoku_data['close'].shift(config_manager.get("KIJUN_PERIOD"))

    line = 0; cloud = 0; ichi_slope = 1; lag = 0
    #if the tenkan_sen is above then sell signal, or buy signal
    if tenkan_sen.iloc[-1] > kijun_sen.iloc[-1]: line = -1  
    elif tenkan_sen.iloc[-1] < kijun_sen.iloc[-1]: line = 1  
    
    #If the "current close price" vs. "open price x bar ago" has slope larger than y% then don't let trade
    if abs(float(klines[-1][4])/float(klines[-config_manager.get("SLOPE_DISTANCE")][1])-1) > config_manager.get("ICHIMOKU_SLOPE"): ichi_slope = 0  

    #if senkou_a is above then buy signal, else sell signal
    if senkou_a.iloc[-1] > senkou_b.iloc[-1]: cloud = 1  
    elif senkou_a.iloc[-1] < senkou_b.iloc[-1]: cloud = -1  

    #if % difference between "middle of the cloud" vs. "lagging chikou line" is larger than x% 
    senkou_avg = (senkou_a.iloc[-1]+senkou_b.iloc[-1])/2
    if abs(float(chikou.iloc[-1])/senkou_avg-1) >= config_manager.get("CHIKOU_DISTANCE"): lag = 1

    #if "price is above the cloud" & "tenkan_sen passed kijun_sen" & "senkou_a passed senkou_b" & "no extreme slope change" then sell
    if current_price > senkou_a.iloc[-1] and line == -1 and cloud == 1 and lag == 1 and ichi_slope == 1: 
         return -1
    #else if "price is below the cloud" & "kijun_sen passed tenkan_sen" & "senkou_b passed senkou_a" & "no extreme slope change" then buy
    elif current_price < senkou_a.iloc[-1] and line == 1 and cloud == -1 and lag == 1 and ichi_slope == 1: 
         return 1
    
    return 0
    