from binance.enums import *
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

class ConfigManager:
    _instance = None

    @staticmethod
    def get_instance():
        if ConfigManager._instance is None:
            ConfigManager()
        return ConfigManager._instance

    def __init__(self):
        if ConfigManager._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            ConfigManager._instance = self
            self.load_config()

    def load_config(self):
        MONGODB_URI = "mongodb+srv://idemir:Bugra07.@cryptotradebot.w9yryxn.mongodb.net/?retryWrites=true&w=majority"
        try:
            mongodb = MongoClient(MONGODB_URI, server_api=ServerApi('1'))
            config = mongodb.configuration.config.find().sort('_id', -1).limit(1).next()
            
            if config["CANDLE_LENGTH"] == "1m":
                CANDLE_LENGTH = KLINE_INTERVAL_1MINUTE
            elif config["CANDLE_LENGTH"] =="3m":
                CANDLE_LENGTH = KLINE_INTERVAL_3MINUTE
            elif config["CANDLE_LENGTH"] =="15m":
                CANDLE_LENGTH = KLINE_INTERVAL_15MINUTE
            elif config["CANDLE_LENGTH"] =="30m":
                CANDLE_LENGTH = KLINE_INTERVAL_30MINUTE
            elif config["CANDLE_LENGTH"] =="1H":
                CANDLE_LENGTH = KLINE_INTERVAL_1HOUR
            elif config["CANDLE_LENGTH"] =="4H":
                CANDLE_LENGTH = KLINE_INTERVAL_4HOUR
            else: 
                CANDLE_LENGTH = KLINE_INTERVAL_1DAY

            self.config = {
                "MONGODB_URI": MONGODB_URI,
                "MONGO_DB": mongodb,
                "CURRENT_VERSION": config["CURRENT_VERSION"],
                "BINANCE_API_KEY": config["BINANCE_API_KEY"],
                "BINANCE_SECRET_KEY": config["BINANCE_SECRET_KEY"],
                "MAXIMUM_NUMBER_OF_API_CALL_TRIES": config["MAXIMUM_NUMBER_OF_API_CALL_TRIES"],
                "BINANCE_API_TIMEOUT": config["BINANCE_API_TIMEOUT"],
                "INITIAL_CAPITAL1": config["INITIAL_CAPITAL1"],
                "INITIAL_CAPITAL2": config["INITIAL_CAPITAL2"],
                "INITIAL_SPOT1": config["INITIAL_SPOT1"],
                "INITIAL_SPOT2": config["INITIAL_SPOT2"],
                "INITIAL_PRICE1": config["INITIAL_PRICE1"],
                "SYMBOL1": config["SYMBOL1"],
                "SYMBOL2": config["SYMBOL2"],
                "DECIMAL1": config["DECIMAL1"],
                "DECIMAL2": config["DECIMAL2"],
                "CANDLE_LENGTH": CANDLE_LENGTH,
                "SEND_TELEGRAM_MESSAGE": config["SEND_TELEGRAM_MESSAGE"],
                "TELEGRAM_API_KEY": config["TELEGRAM_API_KEY"],
                "TELEGRAM_USER_ID_LIST": config["TELEGRAM_USER_ID_LIST"],
                "VOLATILITY_THRESHOLD": config["VOLATILITY_THRESHOLD"],
                "RSI_THRESHOLD_BUY": config["RSI_THRESHOLD_BUY"],
                "RSI_THRESHOLD_SELL": config["RSI_THRESHOLD_SELL"],
                "RSI_DURATION": config["RSI_DURATION"],
                "HEIKIN_DURATION": config["RSI_DURATION"],
                "SHORT_MA": config["SHORT_MA"],
                "LONG_MA": config["LONG_MA"],
                "SHORT_DEMA": config["SHORT_DEMA"],
                "LONG_DEMA": config["LONG_DEMA"],
                "COMMISSION_RATE": config["COMMISSION_RATE"],
                "DECISION_ALGORITHM": config["DECISION_ALGORITHM"],
                "SLEEP_DURATION": config["SLEEP_DURATION"],
                "PRICE_CHANGE_CALCULATION": config["PRICE_CHANGE_CALCULATION"]
            }
        except Exception as e:
            print(e)
            self.config = {}

    def get(self, key):
        return self.config.get(key)

    def update_config(self):
        self.load_config()
        