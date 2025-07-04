# risk_manager.py
from datetime import datetime
from kite_api_config import MAX_DAILY_LOSS, MAX_TRADES_PER_DAY

# Daily tracking (reset on bot restart)
daily_loss = 0
daily_trades = 0

def within_trading_hours():
    now = datetime.now().time()
    return now >= datetime.strptime("09:15", "%H:%M").time() and \
           now <= datetime.strptime("15:30", "%H:%M").time()

def can_trade():
    return daily_loss < MAX_DAILY_LOSS and daily_trades < MAX_TRADES_PER_DAY

def record_trade(pnl):
    global daily_loss, daily_trades
    daily_trades += 1
    daily_loss += abs(pnl) if pnl < 0 else 0

def get_risk_status():
    return {
        "daily_loss": daily_loss,
        "daily_trades": daily_trades,
        "can_trade": can_trade()
    }
