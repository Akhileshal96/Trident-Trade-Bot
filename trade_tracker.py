import time
from telegram_alerts import send_telegram_message

open_trades = []

def track_new_trade(trade):
    open_trades.append(trade)

def monitor_trades(live_prices):
    global open_trades
    still_open = []

    for trade in open_trades:
        symbol = trade['symbol']
        ltp = live_prices.get(symbol)
        if not ltp:
            continue

        if trade['direction'] == 'BUY':
            if ltp >= trade['tp']:
                send_telegram_message(f"🎯 TP Hit: {symbol} @ ₹{ltp}")
                continue
            elif ltp <= trade['sl']:
                send_telegram_message(f"🛑 SL Hit: {symbol} @ ₹{ltp}")
                continue
        else:  # SELL trade
            if ltp <= trade['tp']:
                send_telegram_message(f"🎯 TP Hit (SELL): {symbol} @ ₹{ltp}")
                continue
            elif ltp >= trade['sl']:
                send_telegram_message(f"🛑 SL Hit (SELL): {symbol} @ ₹{ltp}")
                continue

        still_open.append(trade)

    open_trades = still_open
