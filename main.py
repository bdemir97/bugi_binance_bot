import logging, sys, time
from binance.client import Client
from functions.function_checkers import sell_decision, buy_decision, binance_status
from functions.function_telegram import send_message
from config_manager import ConfigManager

def init_bot(config_manager):
    global binance_spot_api
    binance_api_key = config_manager.get("BINANCE_API_KEY")
    binance_secret_key = config_manager.get("BINANCE_SECRET_KEY")
    binance_api_timeout = config_manager.get("BINANCE_API_TIMEOUT")
        
    binance_spot_api = Client(api_key=binance_api_key, api_secret=binance_secret_key, requests_params={'timeout': binance_api_timeout})
    
    logging.info('Initiating bot...')
    #send_message(f"*Komplete Trading Bot* started running!\n"
    #             f"*Initial capitals:* {round(INITIAL_CAPITAL1,3)} {SYMBOL1} & {round(INITIAL_CAPITAL2,3)} {SYMBOL2}")

def check_for_config_update(config_manager):
    try:
        mongodb = config_manager.get("MONGO_DB")
        latest_config = mongodb.configuration.config.find().sort('_id', -1).limit(1).next()
        if latest_config["CURRENT_VERSION"] != config_manager.get("CURRENT_VERSION"):
            logging.info("Configurations has changed. Updating configurations.")
            config_manager.update_config()
            send_message(f"Configurations has changed. Continuing with new configurations!\n"
                         f"*Initial capitals:* {round(config_manager.get('INITIAL_CAPITAL1'),3)} {config_manager.get('SYMBOL1')} & {round(config_manager.get('INITIAL_CAPITAL2'),3)} {config_manager.get('SYMBOL2')}")

    except Exception as e:
        logging.error(f"Error checking for config updates: {e}")

def main():
    logging.basicConfig(level=logging.INFO, format='%(levelname)s %(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M', handlers=[logging.FileHandler("application.log"), logging.StreamHandler(sys.stdout)])
    config_manager = ConfigManager.get_instance()
    init_bot(config_manager)

    while True:
        check_for_config_update(config_manager)

        if not binance_status(binance_spot_api):
            time.sleep(1)
            continue
        
        try:
            mongodb = config_manager.get("MONGO_DB")
            collection = mongodb.trade_history.last_transaction

            try:
                last_transaction = collection.find().sort('_id', -1).limit(1).next()
                transaction_type = last_transaction['type']
                wallet = str(last_transaction['wallet'])
                last_price = last_transaction['price']
            except StopIteration:
                initial_capital1 = config_manager.get("INITIAL_CAPITAL1")
                initial_capital2 = config_manager.get("INITIAL_CAPITAL2")
                initial_price1 = config_manager.get("INITIAL_PRICE1")
                if initial_capital2 > 0:
                    transaction_type = "SELL"
                    wallet = initial_capital2
                else:
                    transaction_type = "BUY"
                    wallet = initial_capital1
                last_price = initial_price1

            symbol1 = config_manager.get("SYMBOL1")
            symbol2 = config_manager.get("SYMBOL2")
            if transaction_type == "SELL":
                buy_decision(symbol1, symbol2, binance_spot_api, last_price, wallet)
            if transaction_type == "BUY":
                sell_decision(symbol1, symbol2, binance_spot_api, last_price, wallet)

        except Exception as e:
            print(f"An error occurred: {e}")

        time.sleep(config_manager.get("SLEEP_DURATION"))
        
if __name__ == '__main__':
    main()
