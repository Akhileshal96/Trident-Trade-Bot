# trade_executor.py
from kite_api import get_kite_instance
from kite_api_config import TRADE_CAPITAL
import json

with open("symbol_to_token.json", "r") as f:
    SYMBOL_TO_TOKEN = json.load(f)

def execute_trade(symbol, ltp):
    kite = get_kite_instance()

    capital_per_trade = TRADE_CAPITAL
    qty = int(capital_per_trade // ltp)

    if qty <= 0:
        print(f"[⚠️] Quantity zero for {symbol}, skipping trade.")
        return None

    try:
        order_id = kite.place_order(
            variety=kite.VARIETY_REGULAR,
            exchange=kite.EXCHANGE_NSE,
            tradingsymbol=symbol,
            transaction_type=kite.TRANSACTION_TYPE_BUY,
            quantity=qty,
            order_type=kite.ORDER_TYPE_MARKET,
            product=kite.PRODUCT_MIS
        )

        print(f"[✅] Buy order placed for {symbol} (Qty: {qty})")
        return {
            "symbol": symbol,
            "qty": qty,
            "entry": ltp,
            "sl": round(ltp * 0.98, 2),
            "tp": round(ltp * 1.02, 2),
            "status": "open"
        }

    except Exception as e:
        print(f"[❌] Trade failed: {e}")
        return None
