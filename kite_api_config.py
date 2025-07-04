# kite_api_config.py
import os
from dotenv import load_dotenv

load_dotenv()

KITE_API_KEY = os.getenv("KITE_API_KEY")
KITE_API_SECRET = os.getenv("KITE_API_SECRET")
KITE_REDIRECT_URI = os.getenv("KITE_REDIRECT_URI")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

TRADE_CAPITAL = float(os.getenv("TRADE_CAPITAL", 5000))
SIGNAL_THRESHOLD = int(os.getenv("SIGNAL_THRESHOLD", 3))

MAX_DAILY_LOSS = float(os.getenv("MAX_DAILY_LOSS", 2000))
MAX_TRADES_PER_DAY = int(os.getenv("MAX_TRADES_PER_DAY", 5))
