import asyncio
from kite_api import get_kite_instance
from strategy_engine import evaluate_signals
from risk_manager import within_trading_hours, can_trade, register_trade
from trade_executor import execute_trade
from telegram_alerts import send_telegram_message
from trade_tracker import monitor_trades

kite = get_kite_instance()

# Symbols to watch – replace with dynamic if needed
watchlist = ['RELIANCE', 'INFY', 'HDFCBANK', 'TCS', 'SBIN']

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
            await send_telegram_message("⏱️ Market closed. Bot sleeping.")
            await asyncio.sleep(600)
            continue

        if not can_trade():
            await send_telegram_message("⚠️ Risk limits reached. Trading paused.")
            await asyncio.sleep(600)
            continue

        live_prices = get_live_prices()

        for symbol, ltp in live_prices.items():
            df = kite.historical_data(instrument_token=kite.ltp(f"NSE:{symbol}")[f"NSE:{symbol}"]['instrument_token'], interval="5minute", from_date="2023-01-01", to_date="2023-01-02")
            signal_score = evaluate_signals(df)

            if signal_score >= 3:
                trade = execute_trade(symbol, ltp)
                if trade:
                    register_trade(ltp - trade['sl'])  # Estimate loss to track risk

        monitor_trades(live_prices)
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(run_bot())
