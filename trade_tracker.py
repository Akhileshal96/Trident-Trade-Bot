# trade_tracker.py
from kite_api import get_kite_instance
from telegram_alerts import send_telegram_message
from trade_logger import log_trade
from risk_manager import record_trade

open_trades = []

def track_new_trade(trade):
    open_trades.append(trade)

def monitor_trades(live_data):
    kite = get_kite_instance()
    closed = []

    for trade in open_trades:
        symbol = trade["symbol"]
        token = live_data["token"]
        ltp = live_data["ltp"]

        if token != trade.get("token"):
            continue

        if trade["status"] == "open":
            if ltp <= trade["sl"]:
                exit_price = ltp
                pnl = (exit_price - trade["entry"]) * trade["qty"]
                record_trade(pnl)
                log_trade(trade, exit_price, pnl)
                send_telegram_message(f"📉 *SL Hit*: {symbol} exited @ ₹{exit_price}\nPNL: ₹{pnl:.2f} ❌")
                trade["status"] = "closed"
                closed.append(trade)

            elif ltp >= trade["tp"]:
                exit_price = ltp
                pnl = (exit_price - trade["entry"]) * trade["qty"]
                record_trade(pnl)
                log_trade(trade, exit_price, pnl)
                send_telegram_message(f"🎯 *TP Hit*: {symbol} exited @ ₹{exit_price}\nPNL: ₹{pnl:.2f} ✅")
                trade["status"] = "closed"
                closed.append(trade)

    for trade in closed:
        open_trades.remove(trade)
