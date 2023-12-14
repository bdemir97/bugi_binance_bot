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
    VOLATILITY_PERIOD = config_manager.get("VOLATILITY_PERIOD")
    VOLATILITY_THRESHOLD = config_manager.get("VOLATILITY_THRESHOLD")
    LAST_TRADE_THRESHOLD = config_manager.get("LAST_TRADE_THRESHOLD")
    RSI_THRESHOLD = config_manager.get("RSI_THRESHOLD_SELL")
    RSI_PERIOD = config_manager.get("RSI_PERIOD")
    ADX_PERIOD = config_manager.get("ADX_PERIOD")
    ADX_THRESHOLD = config_manager.get("ADX_THRESHOLD")
    DECISION_ALGORITHM = config_manager.get("DECISION_ALGORITHM")

    volatile_percent = volatility(KLINES[-VOLATILITY_PERIOD:])
    
    if volatile_percent <= -VOLATILITY_THRESHOLD:
        logging.info(f'Decided to sell based on high volatility (Price change: {round(volatile_percent,2)}%)')
        return sell(wallet, initial1, initial2)
    
    last_trade_change = (KLINES[-1][4]/last_price-1)*100
    if -last_trade_change >= LAST_TRADE_THRESHOLD:
        logging.info(f'Decided to sell since price passed last trade (Price change: {round(last_trade_change,2)}%)')
        return sell(wallet, initial1, initial2)

    if DECISION_ALGORITHM == 1:
        curr_adx, adx_trend = adx(KLINES[-(ADX_PERIOD*2+1):], ADX_PERIOD)
        if curr_adx > ADX_THRESHOLD and adx_trend < 0:
            curr_rsi = rsi(KLINES[-(RSI_PERIOD+1):])
            if curr_rsi >= RSI_THRESHOLD:
                logging.info(f'Decided to sell based on ADX ({round(curr_adx,2)}) and RSI ({round(curr_rsi,2)}).')
                return sell(wallet, initial1, initial2)
            else:
                logging.info(f'ADX ({round(curr_adx,2)}) signaling to sell but RSI ({round(curr_rsi,2)}) decided to not sell.')    
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
    VOLATILITY_PERIOD = config_manager.get("VOLATILITY_PERIOD")
    VOLATILITY_THRESHOLD = config_manager.get("VOLATILITY_THRESHOLD")
    LAST_TRADE_THRESHOLD = config_manager.get("LAST_TRADE_THRESHOLD")
    RSI_THRESHOLD = config_manager.get("RSI_THRESHOLD_BUY")
    RSI_PERIOD = config_manager.get("RSI_PERIOD")
    ADX_PERIOD = config_manager.get("ADX_PERIOD")
    ADX_THRESHOLD = config_manager.get("ADX_THRESHOLD")
    DECISION_ALGORITHM = config_manager.get("DECISION_ALGORITHM")

    volatile_percent = volatility(KLINES[-VOLATILITY_PERIOD:])

    if volatile_percent >= VOLATILITY_THRESHOLD:
        logging.info(f'Decided to buy based on high volatility (Price change: {round(volatile_percent,2)}%)')
        return buy(wallet, initial1, initial2)
    
    last_trade_change = (float(KLINES[-1][4])/last_price-1)*100
    if last_trade_change >= LAST_TRADE_THRESHOLD:
        logging.info(f'Decided to buy since price passed last trade (Price change: {round(last_trade_change,2)}%)')
        return buy(wallet, initial1, initial2)
    
    if DECISION_ALGORITHM == 1:
        curr_adx, adx_trend = adx(KLINES[-(ADX_PERIOD*2+1):], ADX_PERIOD)
        if curr_adx > ADX_THRESHOLD and adx_trend > 0:
            curr_rsi = rsi(KLINES[-(RSI_PERIOD+1):])
            if curr_rsi <= RSI_THRESHOLD:
                logging.info(f'Decided to buy based on ADX ({round(curr_adx,2)}) and RSI ({round(curr_rsi,2)}).')
                return buy(wallet, initial1, initial2)
            else:
                logging.info(f'ADX ({round(curr_adx,2)}) signaling to buy but RSI ({round(curr_rsi,2)}) decided to not buy.')    
        #else:
        #    logging.info(f'Decided not to buy based on ADX ({round(curr_adx,2)}). RSI ({round(curr_rsi,2)}) not checked.')

    return


def binance_status(config_manager):
    BINANCE_API = config_manager.get("BINANCE_API")
    status: bool = BINANCE_API.get_system_status()['status'] == 0
    if not status: 
        logging.info('Cannot reach to Binance!')

    return status


