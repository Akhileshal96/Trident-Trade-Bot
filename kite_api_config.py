import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("KITE_API_KEY")
access_token = os.getenv("KITE_ACCESS_TOKEN")
