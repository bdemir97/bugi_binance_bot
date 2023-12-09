from datetime import datetime, timedelta
import logging

from .indicators.indicators import heikin_today, heikin_yesterday, moving_averages, rsi
from config import VOLATILITY_THRESHOLD, RSI_THRESHOLD, CANDLE_LENGTH, COMMISSION_RATE

def price_change_candle(symbol, binance_spot_api):
    current_price = float(binance_spot_api.get_ticker(symbol=symbol)['lastPrice'])

    end_time = datetime.now()
    start_time = end_time - timedelta(minutes=3)

    klines = binance_spot_api.get_historical_klines(
        symbol=symbol,
        interval=CANDLE_LENGTH,
        start_str=str(int(start_time.timestamp() * 1000)),
        end_str=str(int(end_time.timestamp() * 1000)))
    
    previous_price = float(klines[0][1])

    return ((current_price - previous_price) / previous_price) * 100

def sell_decision(symbol1, symbol2, binance_spot_api, last_price):
    symbol = symbol1+symbol2
    price_change_percentage = price_change_candle(symbol, binance_spot_api)

    if price_change_percentage <= (VOLATILITY_THRESHOLD*-1):
        logging.info(f'Decided to sell {symbol} based on high volatility (Price change: {price_change_percentage}%)')
        return True
    
    """if rsi(symbol, 14) >= RSI_THRESHOLD and heikin_today(symbol) < 0 and heikin_yesterday(symbol) < 0:
        ma_short, ma_long = moving_averages(symbol, binance_spot_api)
        if ma_short < ma_long:
            logging.info(f'Decided to sell {symbol} based on RSI, Heikin Ashi, and moving average crossover.')
            return True
        else:
            logging.info(f'Decided not to sell {symbol} based on RSI, Heikin Ashi, but moving average still positive.')
    else:
        logging.info(f'Decided not to sell {symbol} based on RSI, Heikin Ashi, and other indicators.')"""

    ma_short, ma_long = moving_averages(symbol, binance_spot_api)
    if ma_short < ma_long:
        price = float(binance_spot_api.get_ticker(symbol=symbol)['lastPrice'])
        change_wrt_last = ((price - last_price) / price) * 100
        if change_wrt_last > COMMISSION_RATE | change_wrt_last < (VOLATILITY_THRESHOLD*-1):
            logging.info(f'Decided to sell {symbol} based on moving average crossover.')
            return True
        else:
            logging.info(f'Decided not to sell {symbol} based on %change conditions.')
    else:
        logging.info(f'Decided not to sell {symbol} based on moving averages.')

    return False


def buy_decision(symbol1, symbol2, binance_spot_api, last_price):
    symbol = symbol1+symbol2
    price_change_percentage = price_change_candle(symbol, binance_spot_api)

    if price_change_percentage >= VOLATILITY_THRESHOLD:
        logging.info(f'Decided to buy {symbol} based on high volatility (Price change: {price_change_percentage}%)')
        return True
    
    """if rsi(symbol, 14) >= RSI_THRESHOLD and heikin_today(symbol) < 0 and heikin_yesterday(symbol) < 0:
        ma_short, ma_long = moving_averages(symbol, binance_spot_api)
        if ma_short < ma_long:
            logging.info(f'Decided to buy {symbol} based on RSI, Heikin Ashi, and moving average crossover.')
            return True
        else:
            logging.info(f'Decided not to buy {symbol} based on RSI, Heikin Ashi, but moving average still negative.')
    else:
        logging.info(f'Decided not to buy {symbol} based on RSI, Heikin Ashi, and other indicators.')"""
    
    ma_short, ma_long = moving_averages(symbol, binance_spot_api)
    if ma_short > ma_long:
        price = float(binance_spot_api.get_ticker(symbol=symbol)['lastPrice'])
        change_wrt_last = ((price - last_price) / price) * 100
        if change_wrt_last < (COMMISSION_RATE*-1) | change_wrt_last > (VOLATILITY_THRESHOLD):
            logging.info(f'Decided to buy {symbol} based on moving average crossover.')
            return True
        else:
            logging.info(f'Decided not to buy {symbol} based on %change conditions.')
    else:
        logging.info(f'Decided not to buy {symbol} based on moving averages.')
        
    return False


def binance_status(binance_spot_api):
    status: bool = binance_spot_api.get_system_status()['status'] == 0
    if not status: 
        logging.info('Cannot reach to Binance!')

    return status


