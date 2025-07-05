from telethon.sync import TelegramClient, events import os from dotenv import load_dotenv

load_dotenv() api_id = int(os.getenv("TELEGRAM_API_ID")) api_hash = os.getenv("TELEGRAM_API_HASH") bot_token = os.getenv("BOT_TOKEN")

bot = TelegramClient('trident_session', api_id, api_hash).start(bot_token=bot_token)

from token_handler import *  # ✅ Must come after bot is defined

import asyncio from kite_api import get_kite_instance from strategy_engine import evaluate_signals from risk_manager import within_trading_hours, can_trade, register_trade from trade_executor import execute_trade from telegram_alerts import send_telegram_message from trade_tracker import monitor_trades

kite = get_kite_instance()

Symbols to watch – replace with dynamic if needed

watchlist = ['RELIANCE', 'INFY', 'HDFCBANK', 'TCS', 'SBIN']

Mock function – replace with WebSocket stream for production

def get_live_prices(): prices = {} for symbol in watchlist: try: quote = kite.ltp(f"NSE:{symbol}") prices[symbol] = quote[f"NSE:{symbol}"]['last_price'] except: continue return prices

async def run_bot(): await send_telegram_message("🤖 Trident Bot Started")

while True:
    if not within_trading_hours():
        await send_telegram_message("❌ Market closed. Bot sleeping.")
        await asyncio.sleep(600)
        continue

    if not can_trade():
        await send_telegram_message("⚠️ Risk limits reached. Trading halted.")
        await asyncio.sleep(600)
        continue

    live_prices = get_live_prices()

    for symbol, ltp in live_prices.items():
        df = kite.historical_data(instrument_token=kite.ltp(f"NSE:{symbol}")[f"NSE:{symbol}"]['instrument_token'], interval="5minute", from_date=None, to_date=None, continuous=False)
        signal_score = evaluate_signals(df)
        if signal_score >= 4:
            trade = execute_trade(symbol, ltp)
            if trade:
                register_trade(ltp - trade['sl'])

    monitor_trades(live_prices)
    await asyncio.sleep(60)

if name == "main": asyncio.run(run_bot())

