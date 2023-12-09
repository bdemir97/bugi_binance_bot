import logging
from datetime import datetime
from .function_telegram import send_message
from config import SYMBOL1, SYMBOL2, INITIAL_CAPITAL1, INITIAL_CAPITAL2

def log_info(message):
    logging.info(message)
    send_message(message)

def log_error(message):
    logging.error(message)
    send_message(message)

def log_trade(mongodb, type, status, amount1, price, initial1, initial2, final1, final2, pnl1, pnl2, commission_paid, comission_asset):
    mongodb.trade_history.trades.insert_one({
        "type": type,
        "symbol1": SYMBOL1,
        "symbol2": SYMBOL2,
        "status": status,
        "amount1": amount1,
        "price": price,
        "initial1": initial1,
        "initial2": initial2,
        "final1": final1,
        "final2": final2,
        "pnl1": pnl1,
        "pnl2": pnl2,
        "commission_paid": commission_paid,
        "comission_asset": comission_asset,
        "initial_capital1": INITIAL_CAPITAL1,
        "initial_capital2": INITIAL_CAPITAL2,
        "datetime": datetime.now()
        })
    
    sum_pnl2 = pnl2 + (pnl1*price)
    if type == "BUY":
        balance = str(round(final1 - initial1, 3)) + " " + SYMBOL1
    else:
        balance = str(round(final2 - initial2, 3)) + " " + SYMBOL2

    log_info(f"{type} Order Filled!\n"
             f"{round(amount1, 3)} {SYMBOL1} @{price}\n"
             f"Commission Paid: {round(commission_paid, 3)} {comission_asset}\n"
             f"**BALANCE:** {balance}\n"
             f"**P&L:** {round(sum_pnl2, 3)} {SYMBOL2}")

def log_last(mongodb, parity, type, wallet):
    last_transaction = mongodb.trade_history.last_transaction.find().sort('_id', -1).limit(1).next()

    result = mongodb.trade_history.last_transaction.replace_one({'_id': last_transaction['_id']}, {"parity": parity,"type": type,"wallet": wallet})
    print(result)
