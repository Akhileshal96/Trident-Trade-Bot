from telethon import events
from kiteconnect import KiteConnect
import os

api_key = os.getenv("KITE_API_KEY")
api_secret = os.getenv("KITE_API_SECRET")

kite = KiteConnect(api_key=api_key)
user_states = {}

@bot.on(events.NewMessage(pattern='/token'))
async def send_login_link(event):
    user_id = event.sender_id
    login_url = kite.login_url()
    user_states[user_id] = 'awaiting_token'
    await event.respond(f"🔗 Please login using this link:\n{login_url}\n\nAfter login, copy the `request_token` from the browser URL and paste it here.")

@bot.on(events.NewMessage())
async def receive_token(event):
    user_id = event.sender_id
    message = event.raw_text.strip()

    if user_states.get(user_id) == 'awaiting_token':
        try:
            data = kite.generate_session(message, api_secret=api_secret)
            access_token = data["access_token"]
            with open("access_token.txt", "w") as f:
                f.write(access_token)
            await event.respond("✅ Token saved and session refreshed.")
            user_states[user_id] = None
        except Exception as e:
            await event.respond(f"❌ Error: {str(e)}\nMake sure the token is correct.")