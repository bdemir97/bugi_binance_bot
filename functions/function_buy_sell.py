from binance.enums import *
from binance.exceptions import (BinanceRequestException, BinanceAPIException, BinanceOrderException,
                               BinanceOrderMinAmountException, BinanceOrderMinPriceException,
                               BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException,
                               BinanceOrderInactiveSymbolException)

from config_manager import ConfigManager
from .function_utils import get_local_timestamp, round_down
from .function_log import *

def sell(binance_spot_api, symbol1, symbol2, wallet, initial1, initial2):
    config_manager = ConfigManager.get_instance()

    symbol = symbol1+symbol2

    quantity = round_down(float(wallet),config_manager.get("DECIMAL1"))
    order_id = 's' + get_local_timestamp()

    try:
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
        wallet1 = config_manager.get("INITIAL_CAPITAL1") + (final1 - config_manager.get("INITIAL_SPOT1"))
        wallet2 = config_manager.get("INITIAL_CAPITAL2") + (final2 - config_manager.get("INITIAL_SPOT2"))
        pnl1 = wallet1 - config_manager.get("INITIAL_CAPITAL1")
        pnl2 = wallet2 - config_manager.get("INITIAL_CAPITAL2")

        log_trade("SELL", sell_order_response["status"], qty, price, initial1, initial2, wallet1, wallet2, final1, final2, pnl1, pnl2, commission, comissionAsset)
        log_last(symbol,"SELL",wallet2,price)

    except (BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException,
            BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException,
            BinanceOrderInactiveSymbolException) as ex:
        log_error('Error on creating the sell order! ' + str(ex.message))

def buy(binance_spot_api, symbol1, symbol2, wallet, initial1, initial2):
    config_manager = ConfigManager.get_instance()

    symbol = symbol1+symbol2

    quoteOrderQty = round_down(float(wallet),config_manager.get("DECIMAL2"))
    order_id = 's' + get_local_timestamp()

    try:
        buy_order_response = binance_spot_api.create_order( symbol=symbol, side=SIDE_BUY, type=ORDER_TYPE_MARKET, quoteOrderQty=quoteOrderQty, newClientOrderId=order_id)
        
        price = qty = commission = count = 0
        comissionAsset = ""
        for fill in buy_order_response['fills']:
            price += float(fill['price'])
            qty += float(fill['qty'])
            commission += float(fill['commission'])
            comissionAsset = fill["commissionAsset"]
            count += 1

        price = round(price/count,4)
        final1 = float(binance_spot_api.get_asset_balance(asset=symbol1)['free'])
        final2 = float(binance_spot_api.get_asset_balance(asset=symbol2)['free'])
        wallet1 = config_manager.get("INITIAL_CAPITAL1") + (final1 - config_manager.get("INITIAL_SPOT1"))
        wallet2 = config_manager.get("INITIAL_CAPITAL2") + (final2 - config_manager.get("INITIAL_SPOT2"))
        pnl1 = wallet1 - config_manager.get("INITIAL_CAPITAL1")
        pnl2 = wallet2 - config_manager.get("INITIAL_CAPITAL2")

        log_trade("BUY", buy_order_response["status"], qty, price, initial1, initial2, wallet1, wallet2, final1, final2, pnl1, pnl2, commission, comissionAsset)
        log_last(symbol,"BUY",wallet1,price)

    except (BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException,
            BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException,
            BinanceOrderInactiveSymbolException) as ex:
        log_error('Error occurred for the buy order! '+ str(ex.message))