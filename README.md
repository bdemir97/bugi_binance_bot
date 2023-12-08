## Run

1. Clone the repository.
2. Generate a Binance API key (with Spot access) and put it in your custom `.env`.
3. Run `pip install -r requirements.txt`.
4. Run `python main.py`.

This will run an example bot on trading cryptocurrencies.

## Config

To write custom bots you can:

- Define new indicators in `indicators.py`.
- Define a new strategy in `main.py` (especially inside `is_it_time_to_sell`
  and `is_it_time_to_buy` functions).
- Config your bot settings in `config.py`.

## Last Transaction

Last Transaction is written into file last_transaction.txt to keep track of the trade order. 
If you run for the first time, write MINAUSDT(your parity),SELL,10.0000(your starting budget)

## Telegram Config

1. Create a Telegram bot using [@botfather](https://t.me/botfather).
2. Get your Telegram user ID, using [@userinfobot](https://t.me/userinfobot).
3. Send a message to bot on your phone first.
4. Set `TELEGRAM_API_KEY`, `SEND_TELEGRAM_MESSAGE` and `TELEGRAM_USER_ID_LIST` in `config.py` .

## To-do

- Add more indicators to `indicators.py`.
- Fine tune buying and selling strategies.

