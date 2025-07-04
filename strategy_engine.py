# strategy_engine.py
import numpy as np

def ema(data, period):
    return data.ewm(span=period, adjust=False).mean()

def rsi(data, period=14):
    delta = data.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def macd(data):
    ema12 = data.ewm(span=12, adjust=False).mean()
    ema26 = data.ewm(span=26, adjust=False).mean()
    macd_line = ema12 - ema26
    signal_line = macd_line.ewm(span=9, adjust=False).mean()
    return macd_line, signal_line

def evaluate_signals(df):
    close = df['close']

    ema_vals = ema(close, 20)
    rsi_vals = rsi(close, 14)
    macd_vals, macdsignal_vals = macd(close)

    latest_close = close.iloc[-1]
    latest_ema = ema_vals.iloc[-1]
    latest_rsi = rsi_vals.iloc[-1]
    latest_macd = macd_vals.iloc[-1]
    latest_macdsignal = macdsignal_vals.iloc[-1]

    score = 0

    # EMA Signal
    if latest_close > latest_ema:
        score += 1

    # RSI Signal
    if latest_rsi > 50:
        score += 1

    # MACD Signal
    if latest_macd > latest_macdsignal:
        score += 1

    return score
