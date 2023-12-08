import logging, csv
from .function_telegram import send_message

csv_file = 'files/trade_history.csv'
txt_file = 'files/last_transaction.txt'

def log_info(message):
    logging.info(message)
    send_message(message)

def log_error(message):
    logging.error(message)
    send_message(message)

def log_trade(response):
    with open(csv_file, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([response])

def log_last(response):
    with open(txt_file, 'w') as file:
        file.write(response)