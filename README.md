Created By Bugra Demir

## Config
There are parameters defined in config table in DB to determine the algorithm. Some of these parameters are:
CURRENT_VERSION: A number for bot to check if there any changes in config. If you want to do a change in configurations, you have to change this number too.
DECISION_ALGORITHM: 
    0: RSI & Heikin Ashi, 
    1: RSI & Hekini Ashi & MA Crossover
    2: DEMA Crossover (w/ commission rate & volatility check)
    Else: MA Crossover (w/ commission rate & volatility check)
SYMBOL1 & SYMBOL2: The parity to trade(for example MINAUSDT is MINA and USDT)
CANDLE_LENGTH: A interval of the candle sticks you want to do the trade (1m / 3m / 5m / 15m / 30m / 1H / 4H / 1D)
Thresholds such as: Volatility, RSI Buy and Sell, MA Crossovers, DEMA Crossovers, Commission Rate, Price Change % etc...
If you want to re-start the bot, you need to enter:
    INITIAL_CAPITAL1 & 2:The amounts of Symbol1 & Symbol2 you want to trade with
    INITIAL_SPOT1 & 2:The amounts of Symbol1 & Symbol2 you have in your spot wallet
    INITIAL_PRICE: The value of parity at the time you start the bot
    Also you need to clear the last_transaction table
BINANCE_API_KEY and BINANCE_SECRET_KEY to access your wallet through API
MONGODB_URI to access mongodb tables

Last Transaction is written into file last_transaction table in db, to keep track of the trade order. 
DECIMAL1 & 2: Check the minimum required amount to trade for each parity, otherwise you will get NOTIONAL Error from API.

## Telegram Config
1. Create a Telegram bot using [@botfather](https://t.me/botfather).
2. Get your Telegram user ID, using [@userinfobot](https://t.me/userinfobot).
3. Send a message to bot on your phone first.
4. Set `TELEGRAM_API_KEY`, `SEND_TELEGRAM_MESSAGE` and `TELEGRAM_USER_ID_LIST` in config DB table.

## To-do
- Add more indicators to `indicators.py`.
- Fine tune buying and selling strategies.

