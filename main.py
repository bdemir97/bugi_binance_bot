from binance.client import Client

from functions.function_buy_sell import buy, sell
from functions.function_checkers import sell_decision, buy_decision, binance_status
from functions.function_telegram import send_message
from functions.function_update_balance import update_account_usdt_balance

from config import BINANCE_API_TIMEOUT, SYMBOL, BINANCE_API_KEY, BINANCE_SECRET_KEY
from return_codes import *

import logging, sys, asyncio, time

global binance_spot_api
global account_free_usdt_balance
global last_account_free_usdt_balances_list
global account_locked_usdt_balance
global last_account_locked_usdt_balances_list


def init_bot():
    global binance_spot_api
    binance_spot_api = Client(api_key=BINANCE_API_KEY, api_secret=BINANCE_SECRET_KEY, requests_params={'timeout': BINANCE_API_TIMEOUT})
    logging.info('Initiating bot...')
    asyncio.run(send_message('Bugi Binance Bot is started!'))

def main():
    logging.basicConfig(level=logging.INFO, format='%(levelname)s %(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M', handlers=[logging.FileHandler("application.log"), logging.StreamHandler(sys.stdout)])
    init_bot()

    while True:
        if not binance_status():
            logging.info("Sleeping for 5 seconds!")    
            time.sleep(5)
            continue
        update_account_usdt_balance(binance_spot_api)
        
        if sell_decision(SYMBOL):
            sell(binance_spot_api, SYMBOL)
        if buy_decision(SYMBOL):
            buy(binance_spot_api, SYMBOL)
    
        return

if __name__ == '__main__':
    main()
