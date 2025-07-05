from datetime import datetime, time

# Time window (example: 9:20 AM to 3:15 PM)
TRADING_START = time(9, 20)
TRADING_END = time(15, 15)

# Risk configuration (can be externalized to a config file or .env)
MAX_TRADES_PER_DAY = 10
MAX_DAILY_LOSS = -1500  # INR
MAX_RISK_PER_TRADE = 500  # INR

trades_today = []
cumulative_pnl = 0

def within_trading_hours():
    now = datetime.now().time()
    return TRADING_START <= now <= TRADING_END

def can_trade():
    if len(trades_today) >= MAX_TRADES_PER_DAY:
        return False
    if cumulative_pnl <= MAX_DAILY_LOSS:
        return False
    return True

def register_trade(pnl):
    global cumulative_pnl
    trades_today.append(pnl)
    cumulative_pnl += pnl

def reset_day():
    global trades_today, cumulative_pnl
    trades_today = []
    cumulative_pnl = 0
