import logging, csv

from binance.enums import *
from binance.exceptions import (BinanceRequestException, BinanceAPIException, BinanceOrderException,
                               BinanceOrderMinAmountException, BinanceOrderMinPriceException,
                               BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException,
                               BinanceOrderInactiveSymbolException)

from .function_telegram import send_message
from .function_utils import get_local_timestamp

csv_file = 'trade_history.csv'

def log_info(message):
    logging.info(message)
    with open(csv_file, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["INFO", message])
    send_message(message)

def log_error(message):
    logging.error(message)
    with open(csv_file, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["ERROR", message])
    send_message(message)

def sell(binance_spot_api, symbol):
    logging.info('Trying to sell ' + symbol + "!")
    volume = binance_spot_api.get_asset_balance(symbol)
    sell_price = binance_spot_api.get_symbol_ticker(symbol=symbol)['price']
    quantity = volume / sell_price
    order_id = 's' + get_local_timestamp()
    try:
        log_info('Creating sell order with [' + 'symbol: ' + symbol + ', ' + 'side: ' + str(SIDE_SELL) + ', ' + 'time: ' + str(TIME_IN_FORCE_GTC) + ', ' +
                 'quantity: ' + str(quantity) + ', ' + 'price: ' + str(sell_price) + ', ' + 'newClientOrderId: ' + order_id + ', ' + ']')
        sell_order_response = binance_spot_api.create_order( symbol=symbol, side=SIDE_SELL, type=ORDER_TYPE_MARKET, timeInForce=TIME_IN_FORCE_GTC,
                                                             quantity=quantity, price=str(sell_price), newClientOrderId=order_id)
        log_info('Sell order response: ' + str(sell_order_response))
    except (BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException,
            BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException,
            BinanceOrderInactiveSymbolException) as ex:
        log_error('ERROR on creating the sell order!', str(ex))

def buy(binance_spot_api, symbol):
    logging.info('Trying to buy ' + symbol + "!")
    volume = binance_spot_api.get_asset_balance(symbol)
    buy_price = binance_spot_api.get_symbol_ticker(symbol=symbol)['price']
    quantity = volume / buy_price
    order_id = 's' + get_local_timestamp()
    try:
        log_info('Creating buy order with [' + 'symbol: ' + symbol + ', ' + 'side: ' + str(SIDE_BUY) + ', ' + 'time: ' + str(TIME_IN_FORCE_GTC) + ', ' +
                 'quantity: ' + str(quantity) + ', ' + 'price: ' + str(buy_price) + ', ' + 'newClientOrderId: ' + order_id + ', ' + ']')
        buy_order_response = binance_spot_api.create_order( symbol=symbol, side=SIDE_BUY, type=ORDER_TYPE_MARKET, timeInForce=TIME_IN_FORCE_GTC,
                                                            quantity=quantity, price=str(buy_price), newClientOrderId=order_id)
        log_info('Buy order response: ' + str(buy_order_response))
    except (BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException,
            BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException,
            BinanceOrderInactiveSymbolException) as ex:
        log_error('ERROR on creating the buy order!', str(ex))