# telegram_alerts.py
import requests
from kite_api_config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from risk_manager import get_risk_status

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    requests.post(url, data=data)

def handle_command(command):
    status = get_risk_status()
    if command == "/status":
        return (
            f"📊 *TridentBot Status*\n"
            f"Trades today: {status['daily_trades']}\n"
            f"Loss today: ₹{status['daily_loss']:.2f}\n"
            f"Trade Allowed: {'✅ Yes' if status['can_trade'] else '❌ No'}"
        )
    elif command == "/todaypnl":
        return f"💼 *Today's Realized Loss*: ₹{status['daily_loss']:.2f}"
    else:
        return "🤖 Unknown command."
