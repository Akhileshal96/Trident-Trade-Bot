from kiteconnect import KiteConnect
from kite_api_config import api_key, access_token

def get_kite_instance():
    kite = KiteConnect(api_key=api_key)
    kite.set_access_token(access_token)
    return kite
