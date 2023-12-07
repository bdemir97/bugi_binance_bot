import logging
import telegram
from config import SEND_TELEGRAM_MESSAGE, TELEGRAM_USER_ID_LIST, TELEGRAM_API_KEY

telegram_bot = telegram.Bot(token=TELEGRAM_API_KEY)

async def send_message(message):
    if not SEND_TELEGRAM_MESSAGE:
        logging.info('Sending telegram messages is disabled!')
        return
    for TELEGRAM_USER_ID in TELEGRAM_USER_ID_LIST:
        try:
            await telegram_bot.send_message(chat_id=TELEGRAM_USER_ID, text=message)
        except telegram.error.TelegramError as ex:
            logging.error("Error in sending telegram message!")
            logging.exception(ex)