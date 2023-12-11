# Crypto Trading Bot

**Created By: Bugra Demir**

## Configuration

The algorithm's behavior is determined by parameters defined in the config table within the database. Key parameters include:

- `CURRENT_VERSION`: A number used for the bot to check for changes in the configuration. When making adjustments to configurations, update this number.

- `DECISION_ALGORITHM`:
    1. RSI & Heikin Ashi
    2. RSI & Heikin Ashi & MA Crossover
    3. DEMA Crossover (with commission rate & volatility check)
    4. MA Crossover (with commission rate & volatility check)

- `SYMBOL1` & `SYMBOL2`: The trading pair (e.g., MINA/USDT).

- `CANDLE_LENGTH`: The interval of the candlesticks for trading (1m / 3m / 5m / 15m / 30m / 1H / 4H / 1D).

- **Thresholds:** Including Volatility, RSI Buy and Sell, MA Crossovers, DEMA Crossovers, Commission Rate, Price Change %, etc.

- **Restarting the Bot:**
    1. `INITIAL_CAPITAL1` & `INITIAL_CAPITAL2`: Amounts of Symbol1 & Symbol2 for trading.
    2. `INITIAL_SPOT1` & `INITIAL_SPOT2`: Amounts of Symbol1 & Symbol2 in your spot wallet.
    3. `INITIAL_PRICE`: The value of the trading pair at the time you start the bot.
    4. Clear the last_transaction table.

- **API Keys:**
    - `BINANCE_API_KEY` and `BINANCE_SECRET_KEY`: Credentials to access your Binance wallet through the API.
    - `MONGODB_URI`: URI to access MongoDB tables.

**Last Transaction:** Recorded in the last_transaction table in the database to track trade orders.

`DECIMAL1` & `DECIMAL2`:** Check the minimum required amount to trade for each pair to avoid NOTIONAL errors from the API.

## Telegram Configuration

1. Create a Telegram bot using [@botfather](https://t.me/botfather).
2. Obtain your Telegram user ID using [@userinfobot](https://t.me/userinfobot).
3. Send a message to the bot on your phone first.
4. Set `TELEGRAM_API_KEY`, `SEND_TELEGRAM_MESSAGE`, and `TELEGRAM_USER_ID_LIST` in the config database table.

## To-Do

- Add more indicators to `indicators.py`.
- Fine-tune parameters and buying/selling strategies.