from datetime import datetime, timedelta
import logging

from .indicators.indicators import heikin_ashi, moving_averages, rsi, dema
from .function_buy_sell import buy, sell
from config_manager import ConfigManager

def price_change_candle(symbol, binance_spot_api, candle_length, candle_diff):
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

def sell_decision(symbol1, symbol2, binance_spot_api, last_price, wallet):
    config_manager = ConfigManager.get_instance()

    symbol = symbol1+symbol2
    initial1 = float(binance_spot_api.get_asset_balance(asset=symbol1)['free'])
    initial2 = float(binance_spot_api.get_asset_balance(asset=symbol2)['free'])

    price_change_percentage = price_change_candle(symbol, binance_spot_api, config_manager.get("CANDLE_LENGTH"), config_manager.get("PRICE_CHANGE_CALCULATION"))
    
    if price_change_percentage <= (config_manager.get("VOLATILITY_THRESHOLD")*-1):
        logging.info(f'Decided to sell based on high volatility (Price change: {price_change_percentage}%)')
        return sell(binance_spot_api, symbol1, symbol2, wallet, initial1, initial2)
    
    DECISION_ALGORITHM = config_manager.get("DECISION_ALGORITHM")
    if DECISION_ALGORITHM == 1:
        if rsi(symbol, config_manager.get("RSI_DURATION"), binance_spot_api, config_manager.get("CANDLE_LENGTH")) >= config_manager.get("RSI_THRESHOLD_SELL"):
            if heikin_ashi(symbol, binance_spot_api, config_manager.get("CANDLE_LENGTH"),config_manager.get("HEIKIN_DURATION")) < 0:
                logging.info(f'Decided to sell based on RSI and Heikin Ash.')
                return sell(binance_spot_api, symbol1, symbol2, wallet, initial1, initial2)
            else:
                logging.info(f'RSI signaling sell but Heikin Ash decided to not sell.')    
        #else:
        #    logging.info(f'Decided not to sell based on RSI. Heikin Ashi not checked.')

    elif DECISION_ALGORITHM == 2:
        if rsi(symbol, config_manager.get("RSI_DURATION"), binance_spot_api, config_manager.get("CANDLE_LENGTH")) >= config_manager.get("RSI_THRESHOLD_SELL"):
            if heikin_ashi(symbol, binance_spot_api, config_manager.get("CANDLE_LENGTH"),config_manager.get("HEIKIN_DURATION")) < 0:
                ma_short, ma_long = moving_averages(symbol, binance_spot_api, config_manager.get("CANDLE_LENGTH"), config_manager.get("SHORT_MA"), config_manager.get("LONG_MA"))
                if ma_short < ma_long:
                    logging.info(f'Decided to sell based on RSI, Heikin Ashi, and MA.')
                    return sell(binance_spot_api, symbol1, symbol2, wallet, initial1, initial2)
                else:
                    logging.info(f'Decided not to sell based on MA.')
            else:
                logging.info(f'RSI signaling sell but Heikin Ash decided to not sell. MA not checked.')    
        #else:
        #    logging.info(f'Decided not to sell based on RSI. Heikin Ashi and MA not checked.')

    elif DECISION_ALGORITHM == 3:
        dema_short, dema_long = dema(symbol, binance_spot_api, config_manager.get("CANDLE_LENGTH"), config_manager.get("SHORT_DEMA"), config_manager.get("LONG_DEMA"))
        if dema_short < dema_long:
            price = float(binance_spot_api.get_ticker(symbol=symbol)['lastPrice'])
            change_wrt_last = ((price - last_price) / price) * 100
            if change_wrt_last > config_manager.get("COMMISSION_RATE"):
                logging.info(f'Decided to sell based on DEMA and commission rate.')
                return sell(binance_spot_api, symbol1, symbol2, wallet, initial1, initial2)
            elif change_wrt_last < (config_manager.get("VOLATILITY_THRESHOLD")*-1):
                logging.info(f'Decided to sell based on DEMA and volatility.')
                return sell(binance_spot_api, symbol1, symbol2, wallet, initial1, initial2)
            else:
                logging.info(f'DEMA signaling sell but decided not to sell based on % change.')
        #else:
        #    logging.info(f'Decided not to sell based on DEMA. Commission and volatility not checked.')

    else:
        ma_short, ma_long = moving_averages(symbol, binance_spot_api, config_manager.get("CANDLE_LENGTH"), config_manager.get("SHORT_MA"), config_manager.get("LONG_MA"))
        if ma_short < ma_long:
            price = float(binance_spot_api.get_ticker(symbol=symbol)['lastPrice'])
            change_wrt_last = ((price - last_price) / price) * 100
            if change_wrt_last > config_manager.get("COMMISSION_RATE"):
                logging.info(f'Decided to sell based on MA and commission rate.')
                return sell(binance_spot_api, symbol1, symbol2, wallet, initial1, initial2)
            elif change_wrt_last < (config_manager.get("VOLATILITY_THRESHOLD")*-1):
                logging.info(f'Decided to sell based on MA and volatility.')
                return sell(binance_spot_api, symbol1, symbol2, wallet, initial1, initial2)
            else:
                logging.info(f'MA signaling sell but decided not to sell based on % changes.')
        #else:
        #    logging.info(f'Decided not to sell based on MA. Commission and volatility not checked.')

    return


def buy_decision(symbol1, symbol2, binance_spot_api, last_price, wallet):
    config_manager = ConfigManager.get_instance()
    symbol = symbol1+symbol2

    initial1 = float(binance_spot_api.get_asset_balance(asset=symbol1)['free'])
    initial2 = float(binance_spot_api.get_asset_balance(asset=symbol2)['free'])

    price_change_percentage = price_change_candle(symbol, binance_spot_api, config_manager.get("CANDLE_LENGTH"), config_manager.get("PRICE_CHANGE_CALCULATION"))

    if price_change_percentage >= config_manager.get("VOLATILITY_THRESHOLD"):
        logging.info(f'Decided to buy based on high volatility (Price change: {price_change_percentage}%)')
        return buy(binance_spot_api, symbol1, symbol2, wallet, initial1, initial2)
    
    DECISION_ALGORITHM = config_manager.get("DECISION_ALGORITHM")
    if DECISION_ALGORITHM == 1:
        if rsi(symbol, config_manager.get("RSI_DURATION"), binance_spot_api, config_manager.get("CANDLE_LENGTH")) <= config_manager.get("RSI_THRESHOLD_BUY"):
            if heikin_ashi(symbol, binance_spot_api, config_manager.get("CANDLE_LENGTH"),config_manager.get("HEIKIN_DURATION")) > 0:
                logging.info(f'Decided to buy based on RSI and Heikin Ash.')
                return buy(binance_spot_api, symbol1, symbol2, wallet, initial1, initial2)
            else:
                logging.info(f'RSI signaling buy but Heikin Ash decided to not buy.')    
        #else:
        #    logging.info(f'Decided not to buy based on RSI. Heikin Ashi not checked.')

    elif DECISION_ALGORITHM == 2:
        if rsi(symbol, config_manager.get("RSI_DURATION"), binance_spot_api, config_manager.get("CANDLE_LENGTH")) <= config_manager.get("RSI_THRESHOLD_BUY"):
            if heikin_ashi(symbol, binance_spot_api, config_manager.get("CANDLE_LENGTH"),config_manager.get("HEIKIN_DURATION")) > 0:
                ma_short, ma_long = moving_averages(symbol, binance_spot_api, config_manager.get("CANDLE_LENGTH"), config_manager.get("SHORT_MA"), config_manager.get("LONG_MA"))
                if ma_short > ma_long:
                    logging.info(f'Decided to buy based on RSI, Heikin Ashi, and MA.')
                    return buy(binance_spot_api, symbol1, symbol2, wallet, initial1, initial2)
                else:
                    logging.info(f'Decided not to buy based on MA.')
            else:
                logging.info(f'RSI signaling buy but Heikin Ash decided to not buy. MA not checked.')    
        #else:
        #    logging.info(f'Decided not to buy based on RSI. Heikin Ashi and MA not checked.')
    
    elif DECISION_ALGORITHM == 3:
        dema_short, dema_long = dema(symbol, binance_spot_api, config_manager.get("CANDLE_LENGTH"), config_manager.get("SHORT_DEMA"), config_manager.get("LONG_DEMA"))
        if dema_short > dema_long:
            price = float(binance_spot_api.get_ticker(symbol=symbol)['lastPrice'])
            change_wrt_last = ((price - last_price) / price) * 100
            if change_wrt_last < (config_manager.get("COMMISSION_RATE")*-1):
                logging.info(f'Decided to buy based on DEMA and commission rate.')
                return buy(binance_spot_api, symbol1, symbol2, wallet, initial1, initial2)
            elif change_wrt_last > (config_manager.get("VOLATILITY_THRESHOLD")):
                logging.info(f'Decided to buy based on DEMA and volatility.')
                return buy(binance_spot_api, symbol1, symbol2, wallet, initial1, initial2)
            else:
                logging.info(f'DEMA signaling buy but decided not to buy based on % change.')
        #else:
        #    logging.info(f'Decided not to buy based on DEMA. Commission and volatility not checked.')
    
    else:
        ma_short, ma_long = moving_averages(symbol, binance_spot_api, config_manager.get("CANDLE_LENGTH"), config_manager.get("SHORT_MA"), config_manager.get("LONG_MA"))
        if ma_short > ma_long:
            price = float(binance_spot_api.get_ticker(symbol=symbol)['lastPrice'])
            change_wrt_last = ((price - last_price) / price) * 100
            if change_wrt_last < (config_manager.get("COMMISSION_RATE")*-1):
                logging.info(f'Decided to buy based on MA and commission rate.')
                return buy(binance_spot_api, symbol1, symbol2, wallet, initial1, initial2)
            elif change_wrt_last > (config_manager.get("VOLATILITY_THRESHOLD")):
                logging.info(f'Decided to buy based on MA and volatility.')
                return buy(binance_spot_api, symbol1, symbol2, wallet, initial1, initial2)
            else:
                logging.info(f'MA signaling buy but decided not to buy based on % changes.')
        #else:
        #    logging.info(f'Decided not to buy based on MA. Commission and volatility not checked.')

    return


def binance_status(binance_spot_api):
    status: bool = binance_spot_api.get_system_status()['status'] == 0
    if not status: 
        logging.info('Cannot reach to Binance!')

    return status


