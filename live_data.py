# live_data.py
from kiteconnect import KiteTicker
import json
from kite_api import get_kite_instance
from kite_api_config import SIGNAL_THRESHOLD
from strategy_engine import evaluate_signals
from trade_executor import execute_trade
from trade_tracker import track_new_trade, monitor_trades
from risk_manager import within_trading_hours, can_trade
from telegram_alerts import send_telegram_message
import pandas as pd

kite = get_kite_instance()

from get_tokens import get_token_map_nifty100
symbol_to_token = get_token_map_nifty100()

symbols = fetch_symbol_list()  # Use your dynamic method to get stock symbols

watch_tokens = [symbol_to_token[symbol] for symbol in watchlist]
token_to_symbol = {v: k for k, v in symbol_to_token.items()}
historical_data = {symbol: [] for symbol in watchlist}
tick_data = {}

def on_ticks(ws, ticks):
    for tick in ticks:
        token = tick["instrument_token"]
        ltp = tick["last_price"]
        symbol = token_to_symbol.get(token)

        if not symbol:
            continue

        if not within_trading_hours():
            return

        if not can_trade():
            return

        # Update tick history
        history = historical_data[symbol]
        history.append({
            "close": ltp,
            "high": tick.get("ohlc", {}).get("high", ltp),
            "low": tick.get("ohlc", {}).get("low", ltp)
        })

        if len(history) < 50:
            continue

        df = pd.DataFrame(history[-100:])
        score = evaluate_signals(df)

        if score >= SIGNAL_THRESHOLD:
            trade = execute_trade(symbol, ltp)
            if trade:
                trade["token"] = token
                track_new_trade(trade)
                send_telegram_message(f"📈 *Buy {symbol}* @ ₹{ltp}\nSL: ₹{trade['sl']}, TP: ₹{trade['tp']}")

        monitor_trades({"token": token, "ltp": ltp})

def on_connect(ws, response):
    ws.subscribe(watch_tokens)

def on_close(ws, code, reason):
    print("WebSocket closed:", reason)

if __name__ == "__main__":
    kws = KiteTicker(kite.api_key, kite.access_token)
    kws.on_ticks = on_ticks
    kws.on_connect = on_connect
    kws.on_close = on_close
    kws.connect(threaded=True)
