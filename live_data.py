import asyncio
import os
from dotenv import load_dotenv
from kite_api import get_kite_instance
from strategy_engine import evaluate_signals
from risk_manager import within_trading_hours, can_trade, register_trade
from trade_executor import execute_trade
from telegram_alerts import send_telegram_message
from trade_tracker import monitor_trades
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

# Load environment variables
load_dotenv()

# Telegram API credentials
TELEGRAM_API_ID = int(os.getenv("TELEGRAM_API_ID"))
TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH")
TELEGRAM_SESSION = os.getenv("TELETHON_SESSION")

# Start Telethon client (used if needed for advanced interactions)
telethon_client = TelegramClient(StringSession(TELEGRAM_SESSION), TELEGRAM_API_ID, TELEGRAM_API_HASH)
telethon_client.start()

kite = get_kite_instance()

# Symbols to watch – replace with dynamic if needed
watchlist = ["RELIANCE", "INFY", "HDFCBANK", "TCS", "SBIN"]

# Mock function – replace with WebSocket stream for production
def get_live_prices():
    prices = {}
    for symbol in watchlist:
        try:
            quote = kite.ltp(f"NSE:{symbol}")
            prices[symbol] = quote[f"NSE:{symbol}"]['last_price']
        except:
            continue
    return prices

async def run_bot():
    await send_telegram_message("🤖 Trident Bot Started")

    while True:
        if not within_trading_hours():
            await send_telegram_message("⏰ Market closed. Bot sleeping.")
            await asyncio.sleep(600)
            continue

        if not can_trade():
            await send_telegram_message("⚠️ Risk limits reached. Trading paused.")
            await asyncio.sleep(600)
            continue

        live_prices = get_live_prices()

        for symbol, ltp in live_prices.items():
            df = kite.historical_data(instrument_token=kite.ltp(f"NSE:{symbol}")[f"NSE:{symbol}"]['instrument_token'], interval="5minute", from_date=None, to_date=None)
            signal_score = evaluate_signals(df)
            if signal_score >= 4:
                trade = execute_trade(symbol, ltp)
                if trade:
                    register_trade(ltp - trade['sl'])

        monitor_trades(live_prices)
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(run_bot())
