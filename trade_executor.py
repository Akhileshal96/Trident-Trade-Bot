from kite_api import get_kite_instance
from telegram_alerts import send_telegram_message
from trade_logger import log_trade
from trade_tracker import track_new_trade

kite = get_kite_instance()

def execute_trade(symbol, ltp, direction='BUY', quantity=1, sl_points=2, tp_points=5):
    try:
        # Place order (mock or live)
        order = kite.place_order(
            variety=kite.VARIETY_REGULAR,
            exchange=kite.EXCHANGE_NSE,
            tradingsymbol=symbol,
            transaction_type=direction,
            quantity=quantity,
            product=kite.PRODUCT_MIS,
            order_type=kite.ORDER_TYPE_MARKET
        )

        sl = ltp - sl_points if direction == 'BUY' else ltp + sl_points
        tp = ltp + tp_points if direction == 'BUY' else ltp - tp_points

        trade = {
            "symbol": symbol,
            "ltp": ltp,
            "sl": sl,
            "tp": tp,
            "direction": direction,
            "order_id": order['order_id']
        }

        log_trade(trade)
        track_new_trade(trade)
        send_telegram_message(f"✅ Trade Executed: {symbol} ({direction}) @ ₹{ltp}")

        return trade

    except Exception as e:
        send_telegram_message(f"❌ Failed to place trade for {symbol}: {e}")
        return None
