import logging

from .function_indicators import rsi, heikin_ashi, ma, volatility, adx, supertrend
from .function_buy_sell import buy, sell

def sell_decision(config_manager, wallet, last_price):
    config_manager.update_klines()

    SYMBOL1 = config_manager.get("SYMBOL1")
    SYMBOL2 = config_manager.get("SYMBOL2")
    SYMBOL = SYMBOL1+SYMBOL2
    BINANCE_API = config_manager.get("BINANCE_API")

    initial1 = float(BINANCE_API.get_asset_balance(asset=SYMBOL1)['free'])
    initial2 = float(BINANCE_API.get_asset_balance(asset=SYMBOL2)['free'])

    KLINES = config_manager.get("KLINES")
    KLINE_VOLATILITY = config_manager.get("KLINE_VOLATILITY")
    VOLATILITY_THRESHOLD = config_manager.get("VOLATILITY_THRESHOLD")
    KLINE_RSI = config_manager.get("KLINE_RSI")
    RSI_PERIOD = config_manager.get("RSI_PERIOD")
    RSI_THRESHOLD = config_manager.get("RSI_THRESHOLD_SELL")
    KLINE_HEIKIN = config_manager.get("KLINE_HEIKIN")
    DECISION_ALGORITHM = config_manager.get("DECISION_ALGORITHM")

    volatile_percent = volatility(KLINES[-KLINE_VOLATILITY:])
    
    if volatile_percent <= -VOLATILITY_THRESHOLD:
        logging.info(f'Decided to sell based on high volatility (Price change: {round(volatility,2)}%)')
        return sell(wallet, initial1, initial2)
    
    if DECISION_ALGORITHM == 1:
        if rsi(KLINES[-KLINE_RSI:], RSI_PERIOD) >= RSI_THRESHOLD:
            if heikin_ashi(KLINES[-KLINE_HEIKIN:]) < 0:
                logging.info(f'Decided to sell based on RSI and Heikin Ash.')
                return sell(wallet, initial1, initial2)
            else:
                logging.info(f'RSI signaling sell but Heikin Ash decided to not sell.')    
        #else:
        #    logging.info(f'Decided not to sell based on RSI. Heikin Ashi not checked.')

    return


def buy_decision(config_manager, wallet, last_price):
    config_manager.update_klines()

    SYMBOL1 = config_manager.get("SYMBOL1")
    SYMBOL2 = config_manager.get("SYMBOL2")
    SYMBOL = SYMBOL1+SYMBOL2
    BINANCE_API = config_manager.get("BINANCE_API")
    initial1 = float(BINANCE_API.get_asset_balance(asset=SYMBOL1)['free'])
    initial2 = float(BINANCE_API.get_asset_balance(asset=SYMBOL2)['free'])

    KLINES = config_manager.get("KLINES")
    KLINE_VOLATILITY = config_manager.get("KLINE_VOLATILITY")
    VOLATILITY_THRESHOLD = config_manager.get("VOLATILITY_THRESHOLD")
    KLINE_RSI = config_manager.get("KLINE_RSI")
    RSI_PERIOD = config_manager.get("RSI_PERIOD")
    RSI_THRESHOLD = config_manager.get("RSI_THRESHOLD_SELL")
    KLINE_HEIKIN = config_manager.get("KLINE_HEIKIN")
    DECISION_ALGORITHM = config_manager.get("DECISION_ALGORITHM")

    volatile_percent = volatility(KLINES[-KLINE_VOLATILITY:])

    if volatile_percent >= VOLATILITY_THRESHOLD:
        logging.info(f'Decided to buy based on high volatility (Price change: {round(volatility,2)}%)')
        return buy(wallet, initial1, initial2)
    
    if DECISION_ALGORITHM == 1:
        if rsi(KLINES[-KLINE_RSI:], RSI_PERIOD) <= RSI_THRESHOLD:
            if heikin_ashi(KLINES[-KLINE_HEIKIN:]) > 0:
                logging.info(f'Decided to buy based on RSI and Heikin Ash.')
                return buy(wallet, initial1, initial2)
            else:
                logging.info(f'RSI signaling buy but Heikin Ash decided to not buy.')    
        #else:
        #    logging.info(f'Decided not to buy based on RSI. Heikin Ashi not checked.')

    return


def binance_status(binance_spot_api):
    status: bool = binance_spot_api.get_system_status()['status'] == 0
    if not status: 
        logging.info('Cannot reach to Binance!')

    return status


