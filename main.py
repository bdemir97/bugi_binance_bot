import logging, sys, time
from functions.function_decision import sell_decision, buy_decision, binance_status
from functions.function_telegram import send_message
from config_manager import ConfigManager

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
    logging.info("Initiated the trading bot!")
    #send_message(f"*Komplete Trading Bot* started running!\n"
    #             f"*Initial capitals:* {round(config_manager.get('INITIAL_CAPITAL1'),3)} {config_manager.get('SYMBOL1')} & {round(config_manager.get('INITIAL_CAPITAL2'),3)} {config_manager.get('SYMBOL2')}")

    while True:
        check_for_config_update(config_manager)

        if not binance_status(config_manager):
            time.sleep(1)
            continue
        
        try:
            mongodb = config_manager.get("MONGO_DB")
            collection = mongodb.trade_history.last_transaction

            try:
                last_transaction = collection.find().sort('_id', -1).limit(1).next()
                last_transaction_type = last_transaction['type']
                wallet = str(last_transaction['wallet'])
                last_price = last_transaction['price']
            except StopIteration:
                initial_capital1 = config_manager.get("INITIAL_CAPITAL1")
                initial_capital2 = config_manager.get("INITIAL_CAPITAL2")
                if initial_capital2 > 0:
                    last_transaction_type = "SELL"
                    wallet = initial_capital2
                else:
                    last_transaction_type = "BUY"
                    wallet = initial_capital1
                last_price = float(config_manager.get("KLINES")[-1][4])

            if last_transaction_type == "SELL":
                buy_decision(config_manager, wallet, last_price)
            if last_transaction_type == "BUY":
                sell_decision(config_manager, wallet, last_price)

        except Exception as e:
            print(f"An error occurred: {e}. Sleeping for 5 minutes!")
            time.sleep(300)

        time.sleep(config_manager.get("SLEEP_DURATION"))
        
if __name__ == '__main__':
    main()
