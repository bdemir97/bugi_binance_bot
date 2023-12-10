from binance.enums import *
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

MONGODB_URI = "mongodb+srv://idemir:Bugra07.@cryptotradebot.w9yryxn.mongodb.net/?retryWrites=true&w=majority"

try:
    MONGODB = MongoClient(MONGODB_URI, server_api=ServerApi('1'))
    config = MONGODB.configuration.config.find().sort('_id', -1).limit(1).next()
    BINANCE_API_KEY = config["BINANCE_API_KEY"]
    BINANCE_SECRET_KEY = config["BINANCE_SECRET_KEY"]
    MAXIMUM_NUMBER_OF_API_CALL_TRIES = config["MAXIMUM_NUMBER_OF_API_CALL_TRIES"]
    BINANCE_API_TIMEOUT = config["BINANCE_API_TIMEOUT"]
    INITIAL_CAPITAL1 = config["INITIAL_CAPITAL1"]
    INITIAL_CAPITAL2 = config["INITIAL_CAPITAL2"]
    INITIAL_SPOT1 = config["INITIAL_SPOT1"]
    INITIAL_SPOT2 = config["INITIAL_SPOT2"]
    INITIAL_PRICE1 = config["INITIAL_PRICE1"]
    SYMBOL1 = config["SYMBOL1"]
    SYMBOL2 = config["SYMBOL2"]
    DECIMAL1 = config["DECIMAL1"]
    DECIMAL2 = config["DECIMAL2"]
    candle_length = config["CANDLE_LENGTH"]
    SEND_TELEGRAM_MESSAGE = config["SEND_TELEGRAM_MESSAGE"]
    TELEGRAM_API_KEY = config["TELEGRAM_API_KEY"]
    TELEGRAM_USER_ID_LIST = config["TELEGRAM_USER_ID_LIST"]
    VOLATILITY_THRESHOLD = config["VOLATILITY_THRESHOLD"]
    RSI_THRESHOLD = config["RSI_THRESHOLD"]
    SHORT_MA = config["SHORT_MA"]
    LONG_MA = config["LONG_MA"]
    SHORT_DEMA = config["SHORT_DEMA"]
    LONG_DEMA = config["LONG_DEMA"]
    COMMISSION_RATE = config["COMMISSION_RATE"]

    if candle_length == "1m":
        CANDLE_LENGTH = KLINE_INTERVAL_1MINUTE
    elif candle_length =="3m":
        CANDLE_LENGTH = KLINE_INTERVAL_3MINUTE
    elif candle_length =="15m":
        CANDLE_LENGTH = KLINE_INTERVAL_15MINUTE
    elif candle_length =="30m":
        CANDLE_LENGTH = KLINE_INTERVAL_30MINUTE
    elif candle_length =="1H":
        CANDLE_LENGTH = KLINE_INTERVAL_1HOUR
    elif candle_length =="4H":
        CANDLE_LENGTH = KLINE_INTERVAL_4HOUR
    else: 
        CANDLE_LENGTH = KLINE_INTERVAL_1DAY
except Exception as e:
    print(e)


