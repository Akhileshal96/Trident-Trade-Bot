import os
from telethon.sync import TelegramClient
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")
ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID"))  # Your Telegram user ID

client = TelegramClient('session', API_ID, API_HASH)

async def send_telegram_message(message):
    await client.start()
    try:
        await client.send_message(ADMIN_USER_ID, message)
    finally:
        await client.disconnect()
