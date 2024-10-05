from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator

def calculate_indicators(df):        
    RSI_period = 14
    EMA_period = 72

    if df is not None and not df.empty:
        df['RSI'] = calculate_rsi(close=df['Adj Close'], window=RSI_period)
        df['EMA'] = calculate_ema(close=df['Adj Close'], window=EMA_period)
    
    return df

def calculate_rsi(close, window):
    return RSIIndicator(close=close, window=window).rsi()

def calculate_ema(close, window):
    return EMAIndicator(close=close, window=window).ema_indicator()

def calculate_fibonacci_retracement(df):
    min_price = df['Adj Close'].min()
    max_price = df['Adj Close'].max()
    
    fibonacci_levels = [0.236, 0.382, 0.5, 0.618, 0.786]
    diff = max_price - min_price
    fibonacci_retracements = {}

    for level in fibonacci_levels:
        retracement = max_price - (diff * level)
        fibonacci_retracements[f'Fib {int(level*100)}%'] = retracement

    return fibonacci_retracements
