from binance.enums import *
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from binance.client import Client
from datetime import datetime, timedelta

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
            
            CANDLE_INTERVAL = config["CANDLE_INTERVAL"]
            if CANDLE_INTERVAL == 1:
                KLINE_INTERVAL = KLINE_INTERVAL_1MINUTE
            elif CANDLE_INTERVAL == 3:
                KLINE_INTERVAL = KLINE_INTERVAL_3MINUTE
            elif CANDLE_INTERVAL == 5:
                KLINE_INTERVAL = KLINE_INTERVAL_5MINUTE
            elif CANDLE_INTERVAL == 15:
                KLINE_INTERVAL = KLINE_INTERVAL_15MINUTE
            elif CANDLE_INTERVAL == 30:
                KLINE_INTERVAL = KLINE_INTERVAL_30MINUTE
            
            candle_per_day = 1440 / CANDLE_INTERVAL
            KLINE_VOLATILITY = int(config["VOLATILITY_PERIOD"] / CANDLE_INTERVAL)
            KLINE_HEIKIN = int(config["HEIKIN_PERIOD"] / CANDLE_INTERVAL)
            KLINE_RSI = int((config["RSI_PERIOD"]+1) * candle_per_day)
            KLINE_ADX_SHORT = int(config["ADX_SHORT"] * candle_per_day)
            KLINE_ADX_LONG = int(config["ADX_LONG"] * candle_per_day)
            KLINE_MA_SHORT = int(config["MA_SHORT"] * candle_per_day)
            KLINE_MA_MID = int(config["MA_MID"] * candle_per_day)
            KLINE_MA_LONG = int(config["MA_LONG"] * candle_per_day)
            KLINE_STREND = int(config["STREND_PERIOD"] * candle_per_day)
            
            BINANCE_API = Client(api_key=config["BINANCE_API_KEY"], api_secret=config["BINANCE_SECRET_KEY"], requests_params={'timeout': config["BINANCE_API_TIMEOUT"]})
            MAX_PERIOD = max(config["ADX_LONG"], config["MA_LONG"], config["STREND_PERIOD"], config["RSI_PERIOD"])
            end_time = datetime.now()
            start_time = datetime.now() - timedelta(days=MAX_PERIOD)
            KLINES = BINANCE_API.get_historical_klines(
                symbol=config["SYMBOL1"]+config["SYMBOL2"],
                interval=KLINE_INTERVAL,
                start_str=str(int(start_time.timestamp() * 1000)),
                end_str=str(int(end_time.timestamp() * 1000)))

            exchange_info = BINANCE_API.get_exchange_info()
            symbol_info = next(item for item in exchange_info['symbols'] if item['symbol'] == "MINAUSDT")
            MIN_TRADE = symbol_info['filters'][6]["minNotional"]
            MAX_TRADE = symbol_info['filters'][6]["maxNotional"]
            SYMBOL1_PRECISION = symbol_info['filters'][1]["stepSize"].split('.')[1].find("1")+1
            SYMBOL2_PRECISION = symbol_info['quotePrecision']

            self.config = {
                "MONGODB_URI": MONGODB_URI,
                "MONGO_DB": mongodb,
                "CURRENT_VERSION": config["CURRENT_VERSION"],

                "SEND_TELEGRAM_MESSAGE": config["SEND_TELEGRAM_MESSAGE"],
                "TELEGRAM_API_KEY": config["TELEGRAM_API_KEY"],
                "TELEGRAM_USER_ID_LIST": config["TELEGRAM_USER_ID_LIST"],

                "BINANCE_API_KEY": config["BINANCE_API_KEY"],
                "BINANCE_SECRET_KEY": config["BINANCE_SECRET_KEY"],
                "MAXIMUM_NUMBER_OF_API_CALL_TRIES": config["MAXIMUM_NUMBER_OF_API_CALL_TRIES"],
                "BINANCE_API_TIMEOUT": config["BINANCE_API_TIMEOUT"],
                "BINANCE_API": BINANCE_API,
                "KLINES": KLINES,
                "KLINES_LEN": len(KLINES),

                "INITIAL_CAPITAL1": config["INITIAL_CAPITAL1"],
                "INITIAL_CAPITAL2": config["INITIAL_CAPITAL2"],
                "INITIAL_SPOT1": config["INITIAL_SPOT1"],
                "INITIAL_SPOT2": config["INITIAL_SPOT2"],
                "INITIAL_PRICE1": config["INITIAL_PRICE1"],
                "SYMBOL1": config["SYMBOL1"],
                "SYMBOL2": config["SYMBOL2"],
                "MIN_TRADE": MIN_TRADE,
                "MAX_TRADE": MAX_TRADE,
                "SYMBOL1_PRECISION": SYMBOL1_PRECISION,
                "SYMBOL2_PRECISION": SYMBOL2_PRECISION,

                "CANDLE_INTERVAL": config["CANDLE_INTERVAL"],
                "KLINE_INTERVAL": KLINE_INTERVAL,
                "RSI_THRESHOLD_BUY": config["RSI_THRESHOLD_BUY"],
                "RSI_THRESHOLD_SELL": config["RSI_THRESHOLD_SELL"],
                "RSI_PERIOD": config["RSI_PERIOD"],
                "KLINE_RSI": KLINE_RSI,
                "HEIKIN_PERIOD": config["HEIKIN_PERIOD"],
                "KLINE_HEIKIN": KLINE_HEIKIN,
                "MA_SHORT": config["MA_SHORT"],
                "MA_MID": config["MA_MID"],
                "MA_LONG": config["MA_LONG"],
                "KLINE_MA_SHORT": KLINE_MA_SHORT,
                "KLINE_MA_MID": KLINE_MA_MID,
                "KLINE_MA_LONG": KLINE_MA_LONG,
                "VOLATILITY_THRESHOLD": config["VOLATILITY_THRESHOLD"],
                "VOLATILITY_PERIOD": config["VOLATILITY_PERIOD"],
                "KLINE_VOLATILITY": KLINE_VOLATILITY,
                "ADX_SHORT": config["ADX_SHORT"],
                "ADX_LONG": config["ADX_LONG"],
                "KLINE_ADX_SHORT": KLINE_ADX_SHORT,
                "KLINE_ADX_LONG": KLINE_ADX_LONG,
                "STREND_PERIOD": config["STREND_PERIOD"],
                "STREND_MULT": config["STREND_MULT"],
                "KLINE_STREND": KLINE_STREND,
                "MAX_PERIOD": MAX_PERIOD,

                "COMMISSION_RATE": config["COMMISSION_RATE"],
                "DECISION_ALGORITHM": config["DECISION_ALGORITHM"],
                "SLEEP_DURATION": config["SLEEP_DURATION"]
            }
        except Exception as e:
            print(e)
            self.config = {}

    def get(self, key):
        return self.config.get(key)

    def update_config(self):
        self.load_config()
    
    def update_klines(self):
        latest_kline = self.config["BINANCE_API"].get_historical_klines(
            symbol=self.config["SYMBOL1"] + self.config["SYMBOL2"],
            interval=self.config["KLINE_INTERVAL"],
            limit=1,
            end_str=str(int(datetime.now().timestamp() * 1000)))[0]

        if self.config["KLINES"][-1][0] != latest_kline[0]:
            self.config["KLINES"].append(latest_kline)
        
        if len(self.config["KLINES"]) > self.config["KLINES_LEN"]:
            self.config["KLINES"] = self.config["KLINES"][-self.config["KLINES_LEN"]:]
    
    