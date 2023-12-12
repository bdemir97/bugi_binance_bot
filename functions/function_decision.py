import logging

from .function_indicators import rsi, heikin_ashi, ma, volatility, adx, supertrend
from .function_buy_sell import buy, sell

def sell_decision(config_manager, wallet, last_price):
    config_manager.update_klines()

    SYMBOL1 = config_manager.get("SYMBOL1")
    SYMBOL2 = config_manager.get("SYMBOL2")
    BINANCE_API = config_manager.get("BINANCE_API")

    initial1 = float(BINANCE_API.get_asset_balance(asset=SYMBOL1)['free'])
    initial2 = float(BINANCE_API.get_asset_balance(asset=SYMBOL2)['free'])

    KLINES = config_manager.get("KLINES")
    KLINE_VOLATILITY = config_manager.get("KLINE_VOLATILITY")
    VOLATILITY_THRESHOLD = config_manager.get("VOLATILITY_THRESHOLD")
    KLINE_RSI = config_manager.get("KLINE_RSI")
    RSI_THRESHOLD = config_manager.get("RSI_THRESHOLD_SELL")
    KLINE_HEIKIN = config_manager.get("KLINE_HEIKIN")
    DECISION_ALGORITHM = config_manager.get("DECISION_ALGORITHM")

    volatile_percent = volatility(KLINES[-KLINE_VOLATILITY:])
    
    if volatile_percent <= -VOLATILITY_THRESHOLD:
        logging.info(f'Decided to sell based on high volatility (Price change: {round(volatile_percent,2)}%)')
        return sell(wallet, initial1, initial2)
    
    if DECISION_ALGORITHM == 1:
        curr_rsi = rsi(KLINES[-KLINE_RSI:])
        if curr_rsi >= RSI_THRESHOLD:
            curr_heikin = heikin_ashi(KLINES[-KLINE_HEIKIN:])
            if curr_heikin < 0:
                logging.info(f'Decided to sell based on RSI ({round(curr_rsi,2)}) and Heikin Ash ({round(curr_heikin,2)}).')
                return sell(wallet, initial1, initial2)
            else:
                logging.info(f'RSI ({round(curr_rsi,2)}) signaling sell but Heikin Ash ({round(curr_heikin,2)}) decided to not sell.')    
        #else:
        #    logging.info(f'Decided not to sell based on RSI ({round(curr_rsi,2)}). Heikin Ashi ({round(curr_heikin,2)}) not checked.')

    return


def buy_decision(config_manager, wallet, last_price):
    config_manager.update_klines()

    SYMBOL1 = config_manager.get("SYMBOL1")
    SYMBOL2 = config_manager.get("SYMBOL2")
    BINANCE_API = config_manager.get("BINANCE_API")
    initial1 = float(BINANCE_API.get_asset_balance(asset=SYMBOL1)['free'])
    initial2 = float(BINANCE_API.get_asset_balance(asset=SYMBOL2)['free'])

    KLINES = config_manager.get("KLINES")
    KLINE_VOLATILITY = config_manager.get("KLINE_VOLATILITY")
    VOLATILITY_THRESHOLD = config_manager.get("VOLATILITY_THRESHOLD")
    KLINE_RSI = config_manager.get("KLINE_RSI")
    RSI_THRESHOLD = config_manager.get("RSI_THRESHOLD_BUY")
    KLINE_HEIKIN = config_manager.get("KLINE_HEIKIN")
    DECISION_ALGORITHM = config_manager.get("DECISION_ALGORITHM")

    volatile_percent = volatility(KLINES[-KLINE_VOLATILITY:])

    if volatile_percent >= VOLATILITY_THRESHOLD:
        logging.info(f'Decided to buy based on high volatility (Price change: {round(volatile_percent,2)}%)')
        return buy(wallet, initial1, initial2)
    
    if DECISION_ALGORITHM == 1:
        curr_rsi = rsi(KLINES[-KLINE_RSI:])
        if curr_rsi <= RSI_THRESHOLD:
            curr_heikin = heikin_ashi(KLINES[-KLINE_HEIKIN:])
            if curr_heikin > 0:
                logging.info(f'Decided to buy based on RSI ({round(curr_rsi,2)}) and Heikin Ash ({round(curr_heikin,2)}).')
                return buy(wallet, initial1, initial2)
            else:
                logging.info(f'RSI ({round(curr_rsi,2)}) signaling buy but Heikin Ash ({round(curr_heikin,2)}) decided to not buy.')    
        #else:
        #    logging.info(f'Decided not to buy based on RSI ({round(curr_rsi,2)}). Heikin Ashi ({round(curr_heikin,2)}) not checked.')

    return


def binance_status(config_manager):
    BINANCE_API = config_manager.get("BINANCE_API")
    status: bool = BINANCE_API.get_system_status()['status'] == 0
    if not status: 
        logging.info('Cannot reach to Binance!')

    return status


