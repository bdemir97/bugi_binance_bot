import datetime
import logging

from binance.client import Client
from indicators.indicators import heikin_today, heikin_yesterday, calculate_ma, rsi
from config import VOLATILITY_THRESHOLD, RSI_THRESHOLD

def calculate_price_change(symbol):
    current_price = float(Client().get_ticker(symbol=symbol)['lastPrice'])

    end_time = datetime.now()
    start_time = end_time - datetime.timedelta(minutes=5)

    klines = Client().get_historical_klines(
        symbol=symbol,
        interval=Client.KLINE_INTERVAL_5MINUTE,
        startTime=start_time.timestamp() * 1000,
        endTime=end_time.timestamp() * 1000)
    
    previous_price = float(klines[0][1])

    return ((current_price - previous_price) / previous_price) * 100

def sell_decision(symbol1, symbol2):
    symbol = symbol1+symbol2
    price_change_percentage = calculate_price_change(symbol)

    if abs(price_change_percentage) >= VOLATILITY_THRESHOLD:
        logging.info(f'Decided to sell {symbol} based on high volatility (Price change: {price_change_percentage}%)')
        return True
    
    if rsi(symbol, 14) >= RSI_THRESHOLD and heikin_today(symbol) < 0 and heikin_yesterday(symbol) < 0:
        ma_50, ma_200 = calculate_ma(symbol)
        if ma_50 < ma_200:
            logging.info(f'Decided to sell {symbol} based on RSI, Heikin Ashi, and moving average crossover.')
            return True
        else:
            logging.info(f'Decided not to sell {symbol} based on RSI, Heikin Ashi, but moving average still positive.')
    else:
        logging.info(f'Decided not to sell {symbol} based on RSI, Heikin Ashi, and other indicators.')
    return False


def buy_decision(symbol1, symbol2):
    symbol = symbol1+symbol2

    logging.info('Checking to buy for ' + symbol)
    suitable= False  #Define buying strategy here!
    if suitable:
        logging.info('Decided to buy for ' + symbol)
    else:
        logging.info('Decided to not buy for ' + symbol)
    return suitable


def binance_status(binance_spot_api):
    status: bool = binance_spot_api.get_system_status()['status'] == 0
    if status: 
        logging.info('Binance status is okay!')
    else:
        logging.info('Cannot reach to Binance!')

    return status


