from binance.client import Client

from functions.function_buy_sell import buy, sell
from functions.function_checkers import sell_decision, buy_decision, binance_status
from functions.function_telegram import send_message

from config import BINANCE_API_TIMEOUT, SYMBOL1, SYMBOL2, BINANCE_API_KEY, BINANCE_SECRET_KEY
from return_codes import *

import logging, sys, time

csv_file = 'files/trade_history.csv'
txt_file = 'files/last_transaction.txt'

def init_bot():
    global binance_spot_api
    binance_spot_api = Client(api_key=BINANCE_API_KEY, api_secret=BINANCE_SECRET_KEY, requests_params={'timeout': BINANCE_API_TIMEOUT})
    logging.info('Initiating bot...')
    
    send_message("Bugi Binance Bot started running...")


def main():
    logging.basicConfig(level=logging.INFO, format='%(levelname)s %(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M', handlers=[logging.FileHandler("application.log"), logging.StreamHandler(sys.stdout)])
    init_bot()

    for i in range(5):
        if not binance_status(binance_spot_api):
            logging.info("Sleeping for 5 seconds!")    
            time.sleep(5)
            continue
        
        try:
            with open(txt_file, 'r') as file:
                last_transaction = file.read()
            
            last = last_transaction.split(',')
            parity = last[0] #you can check if you are trading with correct parity
            type = last[1]
            wallet = last[2]

            if type == "SELL":
                if buy_decision(SYMBOL1, SYMBOL2):
                    buy(binance_spot_api, SYMBOL1, SYMBOL2, wallet)
            if type == "BUY":
                if sell_decision(SYMBOL1, SYMBOL2):
                    sell(binance_spot_api, SYMBOL1, SYMBOL2, wallet)
        except FileNotFoundError:
            print(f"Txt file not found!")
        except Exception as e:
            print(f"An error occurred: {e}")
        
        time.sleep(5)

if __name__ == '__main__':
    main()
