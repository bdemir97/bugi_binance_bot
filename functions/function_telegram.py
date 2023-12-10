import logging, requests, time
from config_manager import ConfigManager

def send_message(message):
    config_manager = ConfigManager.get_instance()
    if not config_manager.get("SEND_TELEGRAM_MESSAGE"):
        logging.info('Sending telegram messages is disabled!')
        return

    url = f"https://api.telegram.org/bot{config_manager.get('TELEGRAM_API_KEY')}/sendMessage"

    for TELEGRAM_USER_ID in config_manager.get("TELEGRAM_USER_ID_LIST"):
        for attempt in range(5):
            try:
                payload = {"chat_id": TELEGRAM_USER_ID, "text": message, "parse_mode": "Markdown"}
                response = requests.post(url, json=payload)
                response.raise_for_status() 
                break 
            except Exception as e:
                if attempt < 4: 
                    time.sleep(0.1)  
                else:
                    logging.error(f"Message could not be sent to telegram after 5 attempts.")
    
    return

    