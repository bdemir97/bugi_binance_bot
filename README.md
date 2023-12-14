# Crypto Trading Bot

**Created By: Bugra Demir**

## Configuration

The algorithm's behavior is determined by parameters defined in the config table within the database. Key parameters include:

- `CURRENT_VERSION`: A boolean used for the bot to check for changes in the configuration. When making adjustments to configurations, update this number.

- `DECISION_ALGORITHM`:
    1. ADX and RSI
    2. To be added

- `SYMBOL1` & `SYMBOL2`: The trading pair (e.g., MINA and USDT).

- `CANDLE_INTERVAL`: The interval of the candlesticks for trading up to 30 minutes as integer (1 / 3 / 5 / 15 / 30).

- **Thresholds & Periods:** Including Volatility, Heikin Ashi, RSI Buy and Sell, ADX, MA Crossovers and Supertrend.

- **Restarting the Bot:**
    1. `INITIAL_CAPITAL1` & `INITIAL_CAPITAL2`: Amounts of Symbol1 & Symbol2 for trading.
    2. `INITIAL_SPOT1` & `INITIAL_SPOT2`: Amounts of Symbol1 & Symbol2 in your spot wallet.
    3. `INITIAL_PRICE`: The value of the trading pair at the time you start the bot.
    4. Clear the last_transaction table.

- **API Keys:**
    - `BINANCE_API_KEY` and `BINANCE_SECRET_KEY`: Credentials to access your Binance wallet through the API.
    - `MONGODB_URI`: URI to access MongoDB tables.

**Last Transaction:** Recorded in the last_transaction table in the database to track trade orders.

## Telegram Configuration

1. Create a Telegram bot using [@botfather](https://t.me/botfather).
2. Obtain your Telegram user ID using [@userinfobot](https://t.me/userinfobot).
3. Send a message to the bot on your phone first.
4. Set `TELEGRAM_API_KEY`, `SEND_TELEGRAM_MESSAGE`, and `TELEGRAM_USER_ID_LIST` in the config database table.

## To-Do

- Add more indicators to `indicators.py`.
- Fine-tune parameters and buying/selling strategies.