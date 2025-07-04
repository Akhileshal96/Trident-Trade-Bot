# kite_api.py
import os
from kiteconnect import KiteConnect

def get_kite_instance():
    api_key = os.getenv("KITE_API_KEY")
    access_token = os.getenv("ACCESS_TOKEN")

    kite = KiteConnect(api_key=api_key)
    kite.set_access_token(access_token)

    return kite
