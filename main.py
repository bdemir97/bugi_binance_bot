import logging, sys, time
from binance.client import Client

from functions.function_buy_sell import buy, sell
from functions.function_checkers import sell_decision, buy_decision, binance_status
from functions.function_telegram import send_message

from config import MONGODB, BINANCE_API_KEY, BINANCE_SECRET_KEY, BINANCE_API_TIMEOUT, INITIAL_CAPITAL1, INITIAL_CAPITAL2, SYMBOL1, SYMBOL2, INITIAL_PRICE1

def init_bot():
    global binance_spot_api
        
    binance_spot_api = Client(api_key=BINANCE_API_KEY, api_secret=BINANCE_SECRET_KEY, requests_params={'timeout': BINANCE_API_TIMEOUT})
    
    logging.info('Initiating bot...')
    send_message(f"*Komplete Trading Bot* started running!\n"
                 f"*Initial capitals:* {round(INITIAL_CAPITAL1,3)} {SYMBOL1} & {round(INITIAL_CAPITAL2,3)} {SYMBOL2}")
    
def main():
    logging.basicConfig(level=logging.INFO, format='%(levelname)s %(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M', handlers=[logging.FileHandler("application.log"), logging.StreamHandler(sys.stdout)])
    init_bot()

    while True:
        if not binance_status(binance_spot_api):
            time.sleep(1)
            continue
        
        try:
            collection = MONGODB.trade_history.last_transaction

            try:
                last_transaction = collection.find().sort('_id', -1).limit(1).next()
                type = last_transaction['type']
                wallet = str(last_transaction['wallet'])
                last_price = last_transaction['price']
            except StopIteration:
                if INITIAL_CAPITAL2 > 0:
                    type = "SELL"
                    wallet = INITIAL_CAPITAL2
                else:
                    type = "BUY"
                    wallet = INITIAL_CAPITAL1
                last_price = INITIAL_PRICE1

            if type == "SELL":
                if buy_decision(SYMBOL1, SYMBOL2, binance_spot_api, last_price):
                    buy(binance_spot_api, SYMBOL1, SYMBOL2, wallet, MONGODB)
            if type == "BUY":
                if sell_decision(SYMBOL1, SYMBOL2, binance_spot_api, last_price):
                    sell(binance_spot_api, SYMBOL1, SYMBOL2, wallet, MONGODB)

        except Exception as e:
            print(f"An error occurred: {e}")
        
        time.sleep(10)
        
if __name__ == '__main__':
    main()
