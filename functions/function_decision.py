from .function_indicators import rsi, heikin_ashi, adx, supertrend, ichimoku_cloud, ichimoku_cloud_v2
from .function_buy_sell import buy, sell
import concurrent.futures, logging

def sell_decision(config_manager, wallet):
    config_manager.update_klines()

    SYMBOL1 = config_manager.get("SYMBOL1")
    SYMBOL2 = config_manager.get("SYMBOL2")
    BINANCE_API = config_manager.get("BINANCE_API")

    initial1 = float(BINANCE_API.get_asset_balance(asset=SYMBOL1)['free'])
    initial2 = float(BINANCE_API.get_asset_balance(asset=SYMBOL2)['free'])

    KLINES = config_manager.get("KLINES")
    
    DECISION_ALGORITHM = config_manager.get("DECISION_ALGORITHM")

    if DECISION_ALGORITHM == 1:
        RSI_THRESHOLD = config_manager.get("RSI_THRESHOLD_SELL")
        RSI_PERIOD = config_manager.get("RSI_PERIOD")
        ADX_PERIOD = config_manager.get("ADX_PERIOD")
        ADX_THRESHOLD = config_manager.get("ADX_THRESHOLD")
        STREND_PERIOD = config_manager.get("STREND_PERIOD")
        STREND_MULT = config_manager.get("STREND_MULT")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            rsi_future = executor.submit(rsi, KLINES[-(RSI_PERIOD*3+1):])
            heikin_ashi_future = executor.submit(heikin_ashi, KLINES[-(RSI_PERIOD+1):])
            adx_future = executor.submit(adx, KLINES[-(ADX_PERIOD*3+1):])
            strend_future = executor.submit(supertrend, KLINES[-STREND_PERIOD:], STREND_PERIOD, STREND_MULT)

            curr_rsi = rsi_future.result()
            curr_heikin = heikin_ashi_future.result()
            curr_adx = adx_future.result()
            curr_strend_p, curr_strend = strend_future.result()

        reversal_count = trend_count = 0
        msg = ""
        if curr_rsi >= RSI_THRESHOLD: 
            reversal_count += 1
            msg += f"Rsi({round(curr_rsi,3)})(+) "
        else: msg += f"Rsi({round(curr_rsi,3)})(-) "

        if curr_heikin < 0: 
            trend_count += 1
            msg += f"Heikin:(+) "
        else: msg += f"Heikin:(-) "

        if curr_adx > ADX_THRESHOLD: 
            trend_count += 1
            msg += f"Adx({round(curr_adx,3)}):(+) "
        else: msg += f"Adx({round(curr_adx,3)}):(-) "

        if curr_strend < 0: 
            trend_count += 1
            msg += f"STrend({round(curr_strend_p,3)}):(+) "
        else: msg += f"STrend({round(curr_strend_p,3)}):(-) "

        if reversal_count >= 1 and trend_count >= 2:
            logging.info(f'Decided to sell! {msg}.')
            return sell(wallet, initial1, initial2)
        
        if reversal_count >= 1 and trend_count < 2:
            logging.info(f'Trend to sell not reversed yet! {msg}.')

    elif DECISION_ALGORITHM == 4:
        CLOUD_PERIOD = config_manager.get("CLOUD_PERIOD")
        if ichimoku_cloud(KLINES[-CLOUD_PERIOD:], config_manager) == -1:
            return sell(wallet, initial1, initial2)
    
    elif DECISION_ALGORITHM == 5:
        CLOUD_PERIOD = config_manager.get("CLOUD_PERIOD")
        if ichimoku_cloud_v2(KLINES[-CLOUD_PERIOD:], config_manager) == -1:
            return sell(wallet, initial1, initial2)

    #logging.info(f'{msg}.')
    return

def buy_decision(config_manager, wallet):
    config_manager.update_klines()

    SYMBOL1 = config_manager.get("SYMBOL1")
    SYMBOL2 = config_manager.get("SYMBOL2")
    BINANCE_API = config_manager.get("BINANCE_API")
    initial1 = float(BINANCE_API.get_asset_balance(asset=SYMBOL1)['free'])
    initial2 = float(BINANCE_API.get_asset_balance(asset=SYMBOL2)['free'])

    KLINES = config_manager.get("KLINES")
    DECISION_ALGORITHM = config_manager.get("DECISION_ALGORITHM")
    
    if DECISION_ALGORITHM == 1:
        RSI_THRESHOLD = config_manager.get("RSI_THRESHOLD_BUY")
        RSI_PERIOD = config_manager.get("RSI_PERIOD")
        ADX_PERIOD = config_manager.get("ADX_PERIOD")
        ADX_THRESHOLD = config_manager.get("ADX_THRESHOLD")
        STREND_PERIOD = config_manager.get("STREND_PERIOD")
        STREND_MULT = config_manager.get("STREND_MULT")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            rsi_future = executor.submit(rsi, KLINES[-(RSI_PERIOD*3+1):])
            heikin_ashi_future = executor.submit(heikin_ashi, KLINES[-(RSI_PERIOD+1):])
            adx_future = executor.submit(adx, KLINES[-(ADX_PERIOD*3+1):])
            strend_future = executor.submit(supertrend, KLINES[-STREND_PERIOD:], STREND_PERIOD, STREND_MULT)

            curr_rsi = rsi_future.result()
            curr_heikin = heikin_ashi_future.result()
            curr_adx = adx_future.result()
            curr_strend_p, curr_strend = strend_future.result()

        reversal_count = trend_count = 0
        msg = ""
        if curr_rsi <= RSI_THRESHOLD: 
            reversal_count += 1
            msg += f"Rsi({round(curr_rsi,3)})(+) "
        else: msg += f"Rsi({round(curr_rsi,3)})(-) "

        if curr_heikin > 0: 
            trend_count += 1
            msg += f"Heikin:(+) "
        else: msg += f"Heikin:(-) "

        if curr_adx > ADX_THRESHOLD: 
            trend_count += 1
            msg += f"Adx({round(curr_adx,3)}):(+) "
        else: msg += f"Adx({round(curr_adx,3)}):(-) "

        if curr_strend > 0: 
            trend_count += 1
            msg += f"STrend({round(curr_strend_p,3)}):(+) "
        else: msg += f"STrend({round(curr_strend_p,3)}):(-) "

        if reversal_count >= 1 and trend_count >= 2:
            logging.info(f'Decided to buy! {msg}.')
            return buy(wallet, initial1, initial2)
        
        if reversal_count >= 1 and trend_count < 2:
            logging.info(f'Trend to buy not reversed yet! {msg}.')

    elif DECISION_ALGORITHM == 4:
        CLOUD_PERIOD = config_manager.get("CLOUD_PERIOD")
        if ichimoku_cloud(KLINES[-CLOUD_PERIOD:], config_manager) == 1:
            return buy(wallet, initial1, initial2)
    
    elif DECISION_ALGORITHM == 5:
        CLOUD_PERIOD = config_manager.get("CLOUD_PERIOD")
        if ichimoku_cloud_v2(KLINES[-CLOUD_PERIOD:], config_manager) == 1:
            return buy(wallet, initial1, initial2)

    #logging.info(f'{msg}.')
    return

def binance_status(config_manager):
    BINANCE_API = config_manager.get("BINANCE_API")
    status: bool = BINANCE_API.get_system_status()['status'] == 0
    if not status: 
        logging.info('Cannot reach to Binance!')

    return status


