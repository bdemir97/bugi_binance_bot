import logging

from .function_indicators import rsi, heikin_ashi, sma, ema, volatility, adx, supertrend
from .function_buy_sell import buy, sell
import concurrent.futures

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
    STREND_PERIOD = config_manager.get("STREND_PERIOD")
    STREND_MULT = config_manager.get("STREND_MULT")
    DECISION_ALGORITHM = config_manager.get("DECISION_ALGORITHM")

    volatile_percent = volatility(KLINES[-VOLATILITY_PERIOD:])
    
    if volatile_percent <= -VOLATILITY_THRESHOLD:
        logging.info(f'Decided to sell based on high volatility (Price change: {round(volatile_percent,2)}%)')
        return sell(wallet, initial1, initial2)
    
    last_trade_change = (float(KLINES[-1][4])/last_price-1)*100
    if -last_trade_change >= LAST_TRADE_THRESHOLD:
        logging.info(f'Decided to sell since price passed last trade (Price change: {round(last_trade_change,2)}%)')
        return sell(wallet, initial1, initial2)

    if DECISION_ALGORITHM == 1:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            rsi_future = executor.submit(rsi, KLINES[-(RSI_PERIOD+1):])
            heikin_ashi_future = executor.submit(heikin_ashi, KLINES[-(RSI_PERIOD+1):])
            adx_future = executor.submit(adx, KLINES[-(ADX_PERIOD*2):])
            strend_future = executor.submit(supertrend, KLINES[-STREND_PERIOD:], STREND_PERIOD, STREND_MULT)

            curr_rsi = rsi_future.result()
            curr_heikin = heikin_ashi_future.result()
            curr_adx = adx_future.result()
            curr_strend = strend_future.result()

        sell_count = 0
        msg = ""
        if curr_rsi >= RSI_THRESHOLD: 
            sell_count += 1
            msg += f"RSI({round(curr_rsi,3)}): SELL | "
        else: msg += f"RSI({round(curr_rsi,3)}): NOT SELL | "

        if curr_heikin < 0: 
            sell_count += 1
            msg += f"HEIKIN: SELL | "
        else: msg += f"HEIKIN: NOT SELL | "

        if curr_adx > ADX_THRESHOLD: 
            sell_count += 1
            msg += f"ADX({round(curr_adx,3)}): SELL | "
        else: msg += f"ADX({round(curr_adx,3)}): NOT SELL | "

        if curr_strend < 0: 
            sell_count += 1
            msg += f"SUPERTREND: SELL"
        else: msg += f"SUPERTREND: NOT SELL"

        signal_rate = sell_count/4
        if signal_rate > 0.5:
            logging.info(f'Decided to sell! {msg}')
            return buy(wallet, initial1, initial2)
        
        if signal_rate == 0.5:
            logging.info(f'Half voted for sell! {msg}')

    #logging.info(f'{msg}.')
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
    STREND_PERIOD = config_manager.get("STREND_PERIOD")
    STREND_MULT = config_manager.get("STREND_MULT")
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
        with concurrent.futures.ThreadPoolExecutor() as executor:
            rsi_future = executor.submit(rsi, KLINES[-(RSI_PERIOD+1):])
            heikin_ashi_future = executor.submit(heikin_ashi, KLINES[-(RSI_PERIOD+1):])
            adx_future = executor.submit(adx, KLINES[-(ADX_PERIOD*2):])
            strend_future = executor.submit(supertrend, KLINES[-STREND_PERIOD:], STREND_PERIOD, STREND_MULT)

            curr_rsi = rsi_future.result()
            curr_heikin = heikin_ashi_future.result()
            curr_adx = adx_future.result()
            curr_strend_p, curr_strend = strend_future.result()

        buy_count = 0
        msg = ""
        if curr_rsi <= RSI_THRESHOLD: 
            buy_count += 1
            msg += f"RSI({round(curr_rsi,3)}): BUY | "
        else: msg += f"RSI({round(curr_rsi,3)}): NOT BUY | "

        if curr_heikin > 0: 
            buy_count += 1
            msg += f"HEIKIN: BUY | "
        else: msg += f"HEIKIN: NOT BUY | "

        if curr_adx > ADX_THRESHOLD: 
            buy_count += 1
            msg += f"ADX({round(curr_adx,3)}): BUY | "
        else: msg += f"ADX({round(curr_adx,3)}): NOT BUY | "

        if curr_strend > 0: 
            buy_count += 1
            msg += f"SUPERTREND({round(curr_strend_p,3)}): BUY"
        else: msg += f"SUPERTREND({round(curr_strend_p,3)}): NOT BUY"

        signal_rate = buy_count/4
        if signal_rate > 0.5:
            logging.info(f'Decided to buy! {msg}.')
            return buy(wallet, initial1, initial2)
        
        if signal_rate == 0.5:
            logging.info(f'Half voted to buy! {msg}.')

    #logging.info(f'{msg}.')
    return


def binance_status(config_manager):
    BINANCE_API = config_manager.get("BINANCE_API")
    status: bool = BINANCE_API.get_system_status()['status'] == 0
    if not status: 
        logging.info('Cannot reach to Binance!')

    return status


