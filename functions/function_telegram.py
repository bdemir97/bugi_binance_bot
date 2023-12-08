import logging, requests, time
from config import SEND_TELEGRAM_MESSAGE, TELEGRAM_USER_ID_LIST, TELEGRAM_API_KEY

def send_message(message):
    if not SEND_TELEGRAM_MESSAGE:
        logging.info('Sending telegram messages is disabled!')
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage"

    for TELEGRAM_USER_ID in TELEGRAM_USER_ID_LIST:
        for attempt in range(5):
            try:
                payload = {"chat_id": TELEGRAM_USER_ID, "text": message}
                response = requests.post(url, json=payload)
                response.raise_for_status() 
                break 
            except Exception as e:
                if attempt < 4: 
                    time.sleep(0.5)  
                else:
                    logging.error(f"Message could not be sent to telegram after 5 attempts.")
    
    return

    