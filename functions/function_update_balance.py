from config import MAXIMUM_NUMBER_OF_API_CALL_TRIES
from binance.exceptions import BinanceRequestException, BinanceAPIException
from return_codes import *
import logging

def update_account_usdt_balance(binance_spot_api):
    global account_free_usdt_balance
    global last_account_free_usdt_balances_list
    last_account_free_usdt_balances_list = []
    global account_locked_usdt_balance
    global last_account_locked_usdt_balances_list
    last_account_locked_usdt_balances_list = []
    for i in range(MAXIMUM_NUMBER_OF_API_CALL_TRIES):
        try:
            asset_balance_response = binance_spot_api.get_asset_balance('USDT')
            if asset_balance_response is None:
                return ASSET_BALANCE_NOT_FOUND
            account_free_usdt_balance = float(asset_balance_response['free'])
            logging.info('Free USDT balance: ' + str(account_free_usdt_balance))
            last_account_free_usdt_balances_list.append(account_free_usdt_balance)

            account_locked_usdt_balance = float(asset_balance_response['locked'])
            logging.info('Locked USDT balance: ' + str(account_locked_usdt_balance))
            last_account_locked_usdt_balances_list.append(account_locked_usdt_balance)
            return SUCCESSFUL
        except (BinanceRequestException, BinanceAPIException) as ex:
            logging.error('ERROR in update_account_usdt_balance')
            logging.exception(ex)
            return ERROR
