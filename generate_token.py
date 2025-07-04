# generate_token.py
from kiteconnect import KiteConnect
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("KITE_API_KEY")
api_secret = os.getenv("KITE_API_SECRET")
redirect_uri = os.getenv("KITE_REDIRECT_URI")

kite = KiteConnect(api_key=api_key)
print("[🔑] Login URL:")
print(kite.login_url())

request_token = input("Paste request token here: ").strip()
data = kite.generate_session(request_token, api_secret=api_secret)
access_token = data["access_token"]

with open("access_token.txt", "w") as f:
    f.write(access_token)

print("[✅] Access token saved to access_token.txt")
