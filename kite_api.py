# kite_api.py
from kiteconnect import KiteConnect
import os

def get_kite_instance():
    api_key = os.getenv("KITE_API_KEY")
    access_token = None

    import os
access_token = os.getenv("ACCESS_TOKEN")

    kite = KiteConnect(api_key=api_key)
    kite.set_access_token(access_token)
    return kite
