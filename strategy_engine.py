# strategy_engine.py
import numpy as np
import talib

def evaluate_signals(df):
    close = df['close'].values
    high = df['high'].values
    low = df['low'].values

    ema = talib.EMA(close, timeperiod=20)
    rsi = talib.RSI(close, timeperiod=14)
    macd, macdsignal, _ = talib.MACD(close)

    latest_close = close[-1]
    latest_ema = ema[-1]
    latest_rsi = rsi[-1]
    latest_macd = macd[-1]
    latest_macdsignal = macdsignal[-1]

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
