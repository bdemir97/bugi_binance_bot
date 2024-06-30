from binance.enums import *
from binance.client import Client
import matplotlib.pyplot as plt
import pandas as pd
import ta
from html2image import Html2Image # type: ignore
from io import BytesIO
import requests

##############################################################################################
SEND_TELEGRAM_MESSAGE = True
TELEGRAM_API_KEY = "7456951608:AAE-hkF40LHVDrN12MS8IzX32rRXtSux7LM"
BINANCE_API_KEY = "UBteOn74fmRvhAlHl5pfOLHDvoTTZkMtYWWUe5NtfX9Pvvqxr1UuTG5z3zBCQwoA"
BINANCE_SECRET_KEY = "7Limv3m5FmSozmp52mXAbOlaahOltY7jIxHynMsn4kX4g2MmfTi3vQyymdKqPrCn"
KLINE_INTERVAL = KLINE_INTERVAL_4HOUR
KLINE_LIMIT = 100 

SYMBOLS = ["RNDRUSDT", "AVAXUSDT", "ACHUSDT", "LEVERUSDT", "MINAUSDT"]
TELEGRAM_CHAT_ID = "-1002249210693"
TELEGRAM_THREAD_IDS = ["12", "10", "8", "6", "4"]
##############################################################################################

def draw_table_as_image(data, output_path):
    df = pd.DataFrame(data)
    
    # Use the first row as column names
    column_names = df.iloc[0].tolist()
    df = df[1:].reset_index(drop=True)

    # Generate HTML content manually
    table_headers = "".join([f"<th class='{ 'left-align' if idx == 0 else 'notes-align' if idx == len(column_names) - 1 else ''}'>{col}</th>" for idx, col in enumerate(column_names)])
    table_rows = ""
    for row in df.itertuples(index=False):
        table_rows += "<tr>" + "".join([f"<td class='{ 'left-align' if idx == 0 else ''} { 'last-column' if idx == len(row) - 1 else '' }'>{cell}</td>" for idx, cell in enumerate(row)]) + "</tr>"

    html_content = f"""
    <html>
    <head>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Montserrat">
    <style>
        body {{
            background-color: white;
            font-family: 'Montserrat', sans-serif;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 10px auto;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
            overflow: hidden;
            font-size: 10px;
        }}
        th {{
            background-color: #858585;
            color: #ece9f7;
            padding: 8px;
            text-align: center;
            font-weight: bold;
        }}
        td {{
            background-color: white;
            color: #333;
            text-align: center;
            padding: 8px;
        }}
        .left-align {{
            text-align: left !important;
            padding-left: 24px;
        }}
        .notes-align {{
            text-align: left !important;
        }}
        tr:nth-child(even) td {{
            background-color: #f2f2f2;
        }}
        .last-column {{
            font-size: 8px;
            text-align: left
        }}
        .pill {{
            display: inline-block;
            padding: 5px 10px;
            width: 60px;
            height: 20px;
            border-radius: 15px;
            font-size: 7px;
            font-weight: bold;
            text-align: center;
            line-height: 10px; /* Vertically center text */
            box-sizing: border-box;
        }}
        .strong-green-pill {{ background-color: #5f9c61; color: #90d693;}}
        .green-pill {{ background-color: #90d693; color: #013220;}}
        .red-pill {{ background-color: #f2978f; color: #911104;}}
        .strong-red-pill {{ background-color: #911104; color: #f2978f;}}
        .yellow-pill {{ background-color: #f7e58d; color: #706102;}}
        .gray-pill {{ background-color: #e0e0e0; color: #555555;}}
    </style>
    </head>
    <body>
    <table>
        <thead>
            <tr>{table_headers}</tr>
        </thead>
        <tbody>
            {table_rows}
        </tbody>
    </table>
    </body>
    </html>
    """
    
    # Calculate the height of the table
    row_height = 37  
    num_rows = len(df) + 1  
    table_height = row_height * num_rows

    # Save HTML to image
    hti = Html2Image()
    hti.screenshot(html_str=html_content, save_as=output_path, size=(620, table_height))

def send_message(signals, thread_id):
    data = [
        [signals['current']['Header'], signals['prev_4']['Time'], signals['prev_3']['Time'], signals['prev_2']['Time'], signals['prev']['Time'], signals['current']['Time'], "Notes"],
        [signals['current']['Price_H'],  signals['prev_4']['Price'], signals['prev_3']['Price'], signals['prev_2']['Price'], signals['prev']['Price'], signals['current']['Price'], ""],
        [signals['current']['MA7_H'],  signals['prev_4']['MA7'], signals['prev_3']['MA7'], signals['prev_2']['MA7'], signals['prev']['MA7'], signals['current']['MA7'], signals['current']['MA7_N']],
        [signals['current']['MA25_H'],  signals['prev_4']['MA25'], signals['prev_3']['MA25'], signals['prev_2']['MA25'], signals['prev']['MA25'], signals['current']['MA25'], signals['current']['MA25_N']],
        [signals['current']['RSI_H'],  signals['prev_4']['RSI'], signals['prev_3']['RSI'], signals['prev_2']['RSI'], signals['prev']['RSI'], signals['current']['RSI'],""],
        [signals['current']['MACD_H'],  signals['prev_4']['MACD'], signals['prev_3']['MACD'], signals['prev_2']['MACD'], signals['prev']['MACD'], signals['current']['MACD'],""],
        [signals['current']['BOLL_H'],  signals['prev_4']['Bollinger'], signals['prev_3']['Bollinger'], signals['prev_2']['Bollinger'], signals['prev']['Bollinger'], signals['current']['Bollinger'], signals['current']['BOLL_N']],
        [signals['current']['STOCH_H'],  signals['prev_4']['Stochastic'], signals['prev_3']['Stochastic'], signals['prev_2']['Stochastic'], signals['prev']['Stochastic'], signals['current']['Stochastic'], signals['current']['STOCH_N']],
        [signals['current']['VOL_H'],  signals['prev_4']['Volume'], signals['prev_3']['Volume'], signals['prev_2']['Volume'], signals['prev']['Volume'], signals['current']['Volume'], signals['current']['VOL_N']],
        [signals['current']['ICHI_H'],  signals['prev_4']['Ichimoku'], signals['prev_3']['Ichimoku'], signals['prev_2']['Ichimoku'], signals['prev']['Ichimoku'], signals['current']['Ichimoku'], signals['current']['ICHI_N']],
        [signals['current']['SUP_RES_H'],  signals['prev_4']['Support_Resistance'], signals['prev_3']['Support_Resistance'], signals['prev_2']['Support_Resistance'], signals['prev']['Support_Resistance'], signals['current']['Support_Resistance'], signals['current']['SUP_RES_N']],
    ]
    
    # Draw the table as an image
    output_path = 'table.png'
    draw_table_as_image(data, output_path)

    # Read the image into a buffer
    with open(output_path, "rb") as f:
        buf = BytesIO(f.read())

    # Send image to Telegram
    url = f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendPhoto"
    files = {'photo': buf}
    data = {'chat_id': TELEGRAM_CHAT_ID, "message_thread_id": thread_id}

    response = requests.post(url, files=files, data=data)

    # Output
    print(f"Request URL: {url}")
    print(f"Request files: {files}")
    print(f"Request data: {data}")
    print(f"Response status code: {response.status_code}")
    #print(f"Response content: {response.content}")

    buf.close()
    
    return response

def generate_signals(df, symbol):
    def get_signal(df, idx):
        signals = {}
        
        close_price = df['Close'].iloc[idx]
        prev_price = df['Close'].iloc[idx-1]
        precision = len(str(close_price).split('.')[1])
        
        def format_value(value, precision):
            return f"{value:.{precision}f}"
        def format_volume(value):
            return f"{value / 1_000_000:.1f}M"
        def format_percentage(value):
            return f"{value:.1f}%"
        def format_number(value):
            return f"{value:.1f}"
        def format_price(value):
            return f"{value:.{precision}f}$"
        def format_value_as_percentage(reference, value):
            return f"{((value - reference) / reference * 100):.1f}%"
        
        def pill_class(value, condition):
            if condition == 2:
                p_class = "strong-green-pill"
            elif condition == 1:
                p_class = "green-pill"
            elif condition == 0:
                p_class = "yellow-pill"
            elif condition == -1:
                p_class = "red-pill"
            elif condition == -2:
                p_class = "strong-red-pill"
            else:
                p_class = "gray-pill"
            return f'<span style="font-weight: bold;" class="pill {p_class}">{value}</span>'
        
        #Current Price
        signals['Price'] = pill_class(format_price(close_price), 100)
        
        #Time
        dt = pd.to_datetime(df['Close Time'].iloc[idx], unit='ms')
        rounded_dt = (dt + pd.Timedelta(minutes=30)).floor('h')
        signals['Time'] = rounded_dt.strftime('%H:00')
        
        # MA7
        ma7 = df['ma7'].iloc[idx]
        
        if close_price > ma7:
            if close_price > prev_price:
                signals['MA7'] = pill_class(format_price(ma7), 2)
            else:
                signals['MA7'] = pill_class(format_price(ma7), 1)
        elif close_price < ma7:
            if close_price < prev_price:
                signals['MA7'] = pill_class(format_price(ma7), -2)
            else:
                signals['MA7'] = pill_class(format_price(ma7), -1)
        elif abs(close_price - ma7) / ma7 <= 0.01:
            signals['MA7'] = pill_class(format_price(ma7), 0)            
        else:
            signals['MA7'] = pill_class(format_price(ma7), 100)              

        # MA25  
        ma25 = df['ma25'].iloc[idx]
        
        if close_price > ma25:
            if close_price > prev_price:
                signals['MA25'] = pill_class(format_price(ma25), 2)
            else:
                signals['MA25'] = pill_class(format_price(ma25), 1)
        elif close_price < ma25:
            if close_price < prev_price:
                signals['MA25'] = pill_class(format_price(ma25), -2)
            else:
                signals['MA25'] = pill_class(format_price(ma25), -1)
        elif abs(close_price - ma25) / ma25 <= 0.01:
            signals['MA25'] = pill_class(format_price(ma25), 0)            
        else:
            signals['MA25'] = pill_class(format_price(ma25), 100)     

        # RSI
        rsi = df['rsi'].iloc[idx]
        prev_rsi = df['rsi'].iloc[idx-1]
        
        if rsi < 30:
            if rsi > prev_rsi:
                signals['RSI'] = pill_class(format_number(rsi), 2)
            else:
                signals['RSI'] = pill_class(format_number(rsi), -2)
        elif 30 <= rsi <= 50:
            signals['RSI'] = pill_class(format_number(rsi), 1)
        elif 50 <= rsi <= 70:
            signals['RSI'] = pill_class(format_number(rsi), -1)
        elif rsi > 70:
            if rsi > prev_rsi:
                signals['RSI'] = pill_class(format_number(rsi), 2)
            else:
                signals['RSI'] = pill_class(format_number(rsi), -2)
        elif abs(rsi - 50) / 50 <= 0.05:
            signals['RSI'] = pill_class(format_number(rsi), 0)
        else:
            signals['RSI'] = pill_class(format_number(rsi), 100)

        # MACD
        macd = df['macd'].iloc[idx]
        prev_macd = df['macd'].iloc[idx-1]
        macd_signal = df['macd_signal'].iloc[idx]
        
        if macd > macd_signal:
            if macd > prev_macd:
                signals['MACD'] = pill_class("", 2)
            else:
                signals['MACD'] = pill_class("", 1)
        elif macd < macd_signal:
            if macd < prev_macd:
                signals['MACD'] = pill_class("", -2)
            else:
                signals['MACD'] = pill_class("", -1)
        elif abs(macd - macd_signal) / macd_signal <= 0.005:
            signals['MACD'] = pill_class("", 0)            
        else:
            signals['MACD'] = pill_class("", 100)     
            
        # Bollinger Bands
        bb_low = df['bb_low'].iloc[idx]
        bb_high = df['bb_high'].iloc[idx]
        bb_mid = df['bb_mid'].iloc[idx]

        if close_price < bb_low:
            if close_price > prev_price:
                signals['Bollinger'] = pill_class("", 2)
            else:
                signals['Bollinger'] = pill_class("", -2)
        elif close_price > bb_high:
            if close_price > prev_macd:
                signals['Bollinger'] = pill_class("", 2)
            else:
                signals['Bollinger'] = pill_class("", -2)
        elif abs(close_price - bb_mid) / bb_mid <= 0.05:
            signals['Bollinger'] = pill_class("", 0)   
        elif close_price > bb_mid:
            signals['Bollinger'] = pill_class("", 1)            
        else:
            signals['Bollinger'] = pill_class("", -1)     

        # Stochastic Oscillator
        d_line = df['d%'].iloc[idx]
        k_line = df['k%'].iloc[idx] 
        prev_k_line = df['k%'].iloc[idx-1]
        
        if k_line < 20:
            if k_line > d_line and k_line > prev_k_line:
                signals['Stochastic'] = pill_class(format_number(k_line), 2)
            elif k_line < d_line and k_line < prev_k_line:
                signals['Stochastic'] = pill_class(format_number(k_line), -2)
            else:
                signals['Stochastic'] = pill_class(format_number(k_line), 100)    
        elif k_line > 80:
            if k_line < d_line and k_line < prev_k_line:
                signals['Stochastic'] = pill_class(format_number(k_line), -2)
            elif k_line > d_line and k_line > prev_k_line:
                signals['Stochastic'] = pill_class(format_number(k_line), 2)
            else:
                signals['Stochastic'] = pill_class(format_number(k_line), 100)    
        elif 20 <= k_line <= 80:
            signals['Stochastic'] = pill_class(format_number(k_line), 0) 
        elif abs(k_line - d_line) / d_line <= 0.05 and 20 <= k_line <= 80:
            signals['Stochastic'] = pill_class(format_number(k_line), 100)          
        else:
            signals['Stochastic'] = pill_class(format_number(k_line), 100)     

        # Volume
        vol = df['Volume'].iloc[idx]
        avg_vol = df['avg_volume'].iloc[idx]
        #lowest_high = df['lowest_volumes'].max()

        if vol > 1.5 * avg_vol:
            signals['Volume'] = pill_class(format_volume(vol), 2)
        elif 1.0 * avg_vol < vol <= 1.5 * avg_vol:
            signals['Volume'] = pill_class(format_volume(vol), 1)
        elif 0.5 * avg_vol <= vol <= 1.0 * avg_vol:
            signals['Volume'] = pill_class(format_volume(vol), 0)
        elif 0.2 * avg_vol <= vol < 0.5 * avg_vol:
            signals['Volume'] = pill_class(format_volume(vol), -1)
        else:
            signals['Volume'] = pill_class(format_volume(vol), -2)

        # Ichimoku Cloud
        red_line = df['red_line'].iloc[idx]
        blue_line = df['blue_line'].iloc[idx]
        cloud_a = df['cloud_a'].iloc[idx]
        cloud_b = df['cloud_b'].iloc[idx]
        
        if close_price > max(cloud_a, cloud_b):
            if red_line > blue_line:
                signals['Ichimoku'] = pill_class("", 2)
            else:
                signals['Ichimoku'] = pill_class("", 1)
        elif close_price < min(cloud_a, cloud_b):
            if red_line < blue_line:
                signals['Ichimoku'] = pill_class("", -2)
            else:
                signals['Ichimoku'] = pill_class("", -1)
        elif min(cloud_a, cloud_b) <= close_price <= max(cloud_a, cloud_b):
            signals['Ichimoku'] = pill_class("", 100)   
        elif red_line > blue_line and close_price < min(cloud_a, cloud_b):
            signals['Ichimoku'] = pill_class("", 0)            
        else:
            signals['Ichimoku'] = pill_class("", 100)     

        # Support and Resistance
        support = df['support'].iloc[idx-1]
        resistance = df['resistance'].iloc[idx-1]
        s_text = f"S:{format_price(support)}"
        r_text = f"R:{format_price(resistance)}"
        
        if close_price > resistance * 1.03:
            signals['Support_Resistance'] = pill_class(r_text, 2)
        elif resistance < close_price <= resistance * 1.03:
            signals['Support_Resistance'] = pill_class(r_text, 1)
        elif close_price < support * 0.97:
            signals['Support_Resistance'] = pill_class(s_text, -2)
        elif support * 0.97 <= close_price < support:
            signals['Support_Resistance'] = pill_class(s_text, -1)
        elif abs(close_price - support) / support <= 0.03:
            signals['Support_Resistance'] = pill_class(s_text, 0)
        elif abs(close_price - resistance) / resistance <= 0.03:
            signals['Support_Resistance'] = pill_class(r_text, 0)
        else:
            signals['Support_Resistance'] = pill_class(r_text, 100)
        
        #Header and notes
        if idx == -1:
            signals['Header'] = f'{symbol}'
            signals['Price_H'] = f"Close Price"
            
            signals['MA7_H'] = f"MA7"
            signals['MA7_N'] = f"%Diff: {format_value_as_percentage(ma7, close_price)}"

            signals['MA25_H'] = f"MA25"
            signals['MA25_N'] = f"%Diff: {format_value_as_percentage(ma25, close_price)}"
            
            signals['RSI_H'] = f"RSI"
            
            signals['MACD_H'] = f"MACD"
            
            signals['BOLL_H'] = f"Bollinger"
            signals['BOLL_N'] = f"H: {format_value_as_percentage(bb_high, close_price)} L: {format_value_as_percentage(bb_low, close_price)}"

            signals['STOCH_H'] = f"Stochastic"
            signals['STOCH_N'] = f"K: {format_number(k_line)} D: {format_number(d_line)}"

            signals['VOL_H'] = f"Volume"
            signals['VOL_N'] = f"%Diff: {format_value_as_percentage(avg_vol, vol)}"

            signals['ICHI_H'] = f"Ichimoku"
            signals['ICHI_N'] = f"B: {format_value_as_percentage(cloud_b, close_price)} A: {format_value_as_percentage(cloud_a, close_price)}"

            signals['SUP_RES_H'] = f"Support/Resistance"
            signals['SUP_RES_N'] = f"S: {format_value_as_percentage(support, close_price)} R: {format_value_as_percentage(resistance, close_price)}"

        return signals

    current_idx = -1
    prev_idx = -2
    prev_2_idx = -3
    prev_3_idx = -4
    prev_4_idx = -5

    current_signals = get_signal(df, current_idx)
    prev_signals = get_signal(df, prev_idx)
    prev_2_signals = get_signal(df, prev_2_idx)
    prev_3_signals = get_signal(df, prev_3_idx)
    prev_4_signals = get_signal(df, prev_4_idx)

    return {
        'current': current_signals,
        'prev': prev_signals,
        'prev_2': prev_2_signals,
        'prev_3': prev_3_signals,
        'prev_4': prev_4_signals
    }

def calculate_indicators(df):
    df['Close'] = pd.to_numeric(df['Close'])
    df['High'] = pd.to_numeric(df['High'])
    df['Low'] = pd.to_numeric(df['Low'])
    df['Volume'] = pd.to_numeric(df['Volume'])

    # Moving Averages
    df['ma7'] = df['Close'].rolling(window=7).mean()
    df['ma25'] = df['Close'].rolling(window=25).mean()

    # Relative Strength Index (RSI)
    rsi_series = ta.momentum.RSIIndicator(df['Close']).rsi()
    df['rsi'] = rsi_series.ewm(span=1, adjust=False).mean()

    # MACD
    macd = ta.trend.MACD(df['Close'], window_fast=9, window_slow=21, window_sign=7)
    df['macd'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()

    # Bollinger Bands
    bb = ta.volatility.BollingerBands(close=df['Close'], window=21, window_dev=2)
    df['bb_high'] = bb.bollinger_hband()
    df['bb_low'] = bb.bollinger_lband()
    df['bb_mid'] = bb.bollinger_mavg()

    # Stochastic Oscillator
    stoch = ta.momentum.StochasticOscillator(df['High'], df['Low'], df['Close'], window=14, smooth_window=3)
    df['k%'] = stoch.stoch()
    df['d%'] = stoch.stoch_signal()

    # Volume
    df['lowest_volumes'] = df['Volume'].nsmallest(15)
    df['avg_volume'] = df['Volume'].iloc[-11:-1].mean()

    # Ichimoku Cloud
    red_high = df['High'].rolling(window=9).max()
    red_low = df['Low'].rolling(window=9).min()
    df['red_line'] = (red_high + red_low) / 2 

    blue_high = df['High'].rolling(window=22).max()
    blue_low = df['Low'].rolling(window=22).min()
    df['blue_line'] = (blue_high + blue_low) / 2 

    df['cloud_a'] = ((df['red_line'] + df['blue_line']) / 2).shift(30) 
    cloud_b_high = df['High'].rolling(window=48).max()
    cloud_b_low = df['Low'].rolling(window=48).min()
    df['cloud_b'] = ((cloud_b_high + cloud_b_low) / 2).shift(30)
    
    # Support and Resistance Levels (based on highest high and lowest low in lookback period)
    df['support'] = df['Close'].iloc[-75:-1].min()
    df['resistance'] = df['Close'].iloc[-75:-1].max()

    return df

def fetch_data(binance_api, symbol):
    klines = binance_api.get_historical_klines(symbol=symbol, interval=KLINE_INTERVAL,limit=KLINE_LIMIT)
    klines.pop()
    
    columns = ['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore']
    df = pd.DataFrame(klines, columns=columns)

    return df

def main():
    binance_api = Client(api_key=BINANCE_API_KEY, api_secret=BINANCE_SECRET_KEY, requests_params={'timeout': 60})

    for i in range(len(SYMBOLS)):
        df = fetch_data(binance_api, SYMBOLS[i])
        calc_df = calculate_indicators(df)
        signals = generate_signals(calc_df, SYMBOLS[i])
        print(send_message(signals, TELEGRAM_THREAD_IDS[i]))
        
if __name__ == '__main__':
    main()