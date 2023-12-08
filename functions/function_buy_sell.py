import logging

from binance.enums import *
from binance.exceptions import (BinanceRequestException, BinanceAPIException, BinanceOrderException,
                               BinanceOrderMinAmountException, BinanceOrderMinPriceException,
                               BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException,
                               BinanceOrderInactiveSymbolException)

from .function_utils import get_local_timestamp, round_down
from .function_log import *

def sell(binance_spot_api, symbol1, symbol2, wallet):
    symbol = symbol1+symbol2
    logging.info('Trying to sell ' + symbol + "!")

    quantity = float(wallet)
    sell_price = float(binance_spot_api.get_symbol_ticker(symbol=symbol)['price'])
    order_id = 's' + get_local_timestamp()

    try:
        log_info('Creating sell order for ' + symbol + ' at price ' + str(sell_price))
        sell_order_response = binance_spot_api.create_order( symbol=symbol, side=SIDE_SELL, type=ORDER_TYPE_MARKET, quantity=quantity, newClientOrderId=order_id)
        
        fill_response = sell_order_response["fills"][0]
        fill_price = round_down(float(fill_response["price"]),4)
        fill_quantity = round_down(float(fill_response["qty"]),4)
        fill_commission = round_down(float(fill_response["commission"]),4)
        fill_comm_paid = fill_commission
        fill_value = round_down((float(fill_price)*float(fill_quantity))-float(fill_comm_paid),4)
        log_info(f"Sell success!\nParity: {symbol}\nPrice: {fill_price}\nAmount: {fill_quantity} {symbol1}\nCommission Paid: {fill_comm_paid} {symbol2}\nTotal Received: {fill_value}")

        log_trade(f'{sell_order_response["side"]},{sell_order_response["symbol"]},{sell_order_response["status"]},{fill_price},{fill_quantity},{fill_commission},{fill_response["commissionAsset"]}')
        log_last(symbol1+symbol2+","+"SELL"+","+str(fill_value))
    except (BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException,
            BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException,
            BinanceOrderInactiveSymbolException) as ex:
        log_error('Error on creating the sell order! ' + str(ex.message))

def buy(binance_spot_api, symbol1, symbol2, wallet):
    symbol = symbol1+symbol2
    logging.info('Trying to buy ' + symbol + "!")

    quoteOrderQty = float(wallet)
    buy_price = float(binance_spot_api.get_symbol_ticker(symbol=symbol)['price'])
    order_id = 's' + get_local_timestamp()

    try:
        log_info('Creating buy order for ' + symbol + ' at price ' + str(buy_price))
        buy_order_response = binance_spot_api.create_order( symbol=symbol, side=SIDE_BUY, type=ORDER_TYPE_MARKET, quoteOrderQty=quoteOrderQty, newClientOrderId=order_id)
        
        fill_response = buy_order_response["fills"][0]
        fill_price = round_down(float(fill_response["price"]),4)
        fill_quantity = round_down(float(fill_response["qty"]),4)
        fill_commission = round_down(float(fill_response["commission"]),4)
        fill_comm_paid = round_down(float(fill_commission)*float(fill_price),4)
        fill_value = round_down((float(fill_price)*float(fill_quantity))+float(fill_comm_paid),4)
        log_info(f"Buy success!\nParity: {symbol}\nPrice: {fill_price}\nAmount: {fill_quantity} {symbol1}\nCommission Paid: {fill_comm_paid} {symbol2}\nTotal Paid: {fill_value}")

        log_trade(f'{buy_order_response["side"]},{buy_order_response["symbol"]},{buy_order_response["status"]},{fill_price},{fill_quantity},{fill_commission},{fill_response["commissionAsset"]}')
        log_last(symbol1+symbol2+","+"BUY"+","+str(fill_quantity))
    except (BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException,
            BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException,
            BinanceOrderInactiveSymbolException) as ex:
        log_error('Error occurred for the buy order! '+ str(ex.message))