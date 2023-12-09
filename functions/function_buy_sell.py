from binance.enums import *
from binance.exceptions import (BinanceRequestException, BinanceAPIException, BinanceOrderException,
                               BinanceOrderMinAmountException, BinanceOrderMinPriceException,
                               BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException,
                               BinanceOrderInactiveSymbolException)
from config import INITIAL_CAPITAL1, INITIAL_CAPITAL2, DECIMAL1, DECIMAL2

from .function_utils import get_local_timestamp, round_down
from .function_log import *

def sell(binance_spot_api, symbol1, symbol2, wallet, mongodb):
    symbol = symbol1+symbol2

    initial1 = float(binance_spot_api.get_asset_balance(asset=symbol1)['free'])
    initial2 = float(binance_spot_api.get_asset_balance(asset=symbol2)['free'])

    quantity = round_down(float(wallet),DECIMAL1)
    sell_price = float(binance_spot_api.get_symbol_ticker(symbol=symbol)['price'])
    order_id = 's' + get_local_timestamp()

    try:
        log_info(f'Trying to sell {round(quantity,3)} {symbol1} at price {sell_price}')
        sell_order_response = binance_spot_api.create_order( symbol=symbol, side=SIDE_SELL, type=ORDER_TYPE_MARKET, quantity=quantity, newClientOrderId=order_id)
        
        price = qty = commission = count = 0
        comissionAsset = ""
        for fill in sell_order_response['fills']:
            price += float(fill['price'])
            qty += float(fill['qty'])
            commission += float(fill['commission'])
            comissionAsset = fill["commissionAsset"]
            count += 1

        price = round(price/count,4)
        final1 = float(binance_spot_api.get_asset_balance(asset=symbol1)['free'])
        final2 = float(binance_spot_api.get_asset_balance(asset=symbol2)['free'])
        change2 = final2 - initial2
        pnl1 = final1 - INITIAL_CAPITAL1
        pnl2 = final2 - INITIAL_CAPITAL2


        log_trade(mongodb, "SELL", sell_order_response["status"], qty, price, initial1, initial2, final1, final2, pnl1, pnl2, commission, comissionAsset)
        log_last(mongodb,symbol,"SELL",change2)

    except (BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException,
            BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException,
            BinanceOrderInactiveSymbolException) as ex:
        log_error('Error on creating the sell order! ' + str(ex.message))

def buy(binance_spot_api, symbol1, symbol2, wallet, mongodb):
    symbol = symbol1+symbol2

    initial1 = float(binance_spot_api.get_asset_balance(asset=symbol1)['free'])
    initial2 = float(binance_spot_api.get_asset_balance(asset=symbol2)['free'])

    quoteOrderQty = round_down(float(wallet),DECIMAL2)
    buy_price = float(binance_spot_api.get_symbol_ticker(symbol=symbol)['price'])
    order_id = 's' + get_local_timestamp()

    try:
        log_info(f'Trying to buy {round(quoteOrderQty,3)} {symbol2} worth of {symbol1} at price {buy_price}')
        buy_order_response = binance_spot_api.create_order( symbol=symbol, side=SIDE_BUY, type=ORDER_TYPE_MARKET, quoteOrderQty=quoteOrderQty, newClientOrderId=order_id)
        
        price = qty = commission = 0
        comissionAsset = ""
        for fill in buy_order_response['fills']:
            price += float(fill['price'])
            qty += float(fill['qty'])
            commission += float(fill['commission'])
            comissionAsset = fill["commissionAsset"]

        final1 = float(binance_spot_api.get_asset_balance(asset=symbol1)['free'])
        final2 = float(binance_spot_api.get_asset_balance(asset=symbol2)['free'])
        change1 = final1 - initial1
        pnl1 = final1 - INITIAL_CAPITAL1
        pnl2 = final2 - INITIAL_CAPITAL2

        log_trade(mongodb, "BUY", buy_order_response["status"], qty, price, initial1, initial2, final1, final2, pnl1, pnl2, commission, comissionAsset  )
        log_last(mongodb,symbol,"BUY",change1)

    except (BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException,
            BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException,
            BinanceOrderInactiveSymbolException) as ex:
        log_error('Error occurred for the buy order! '+ str(ex.message))