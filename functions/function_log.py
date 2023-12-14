import logging
from datetime import datetime
from .function_telegram import send_message
from config_manager import ConfigManager

def log_info(message):
    logging.info(message)
    send_message(message)

def log_error(message):
    logging.error(message)
    send_message(message)

def log_trade(type, status, amount1, price, initial1, initial2, wallet1, wallet2, final1, final2, pnl1, pnl2, commission_paid, comission_asset):
    config_manager = ConfigManager.get_instance()
    config_manager.get("MONGO_DB").trade_history.trades.insert_one({
        "type": type,
        "symbol1": config_manager.get("SYMBOL1"),
        "symbol2": config_manager.get("SYMBOL2"),
        "status": status,
        "amount1": amount1,
        "price": price,
        "initial1": initial1,
        "initial2": initial2,
        "wallet1": wallet1,
        "wallet2": wallet2,
        "final1": final1,
        "final2": final2,
        "pnl1": pnl1,
        "pnl2": pnl2,
        "commission_paid": commission_paid,
        "comission_asset": comission_asset,
        "initial_capital1": config_manager.get("INITIAL_CAPITAL1"),
        "initial_capital2": config_manager.get("INITIAL_CAPITAL2"),
        "datetime": datetime.now(),
        "decision_algorithm":config_manager.get("DECISION_ALGORITHM"),
        "config_version":config_manager.get("CURRENT_VERSION")
        })
    
    real_pnl = pnl2 + (pnl1*price)
    act_pnl = pnl2 + ((wallet1*price) - (config_manager.get("INITIAL_CAPITAL1")*config_manager.get("INITIAL_AVG_PRICE")))

    log_info(f"*{type}* {round(amount1, 3)} {config_manager.get('SYMBOL1')} @{price}\n"
             f"Commission: {round(commission_paid, 3)} {comission_asset}\n"
             f"*Balance:* {round(wallet1,3)} {config_manager.get('SYMBOL1')} | {round(wallet2,3)} {config_manager.get('SYMBOL2')}\n"
             f"*Actual P&L:* {round(act_pnl, 3)} {config_manager.get('SYMBOL2')}\n"
             f"*Realized P&L:* {round(real_pnl, 3)} {config_manager.get('SYMBOL2')}")

def log_last(parity, type, wallet, price):
    config_manager = ConfigManager.get_instance()
    last_transaction = config_manager.get("MONGO_DB").trade_history.last_transaction.find_one({}, sort=[('_id', -1)])

    if last_transaction:
        config_manager.get("MONGO_DB").trade_history.last_transaction.replace_one({'_id': last_transaction['_id']}, {"parity": parity, "type": type, "wallet": wallet, "price": price})
    else:
        config_manager.get("MONGO_DB").trade_history.last_transaction.insert_one({"parity": parity, "type": type, "wallet": wallet, "price": price})
