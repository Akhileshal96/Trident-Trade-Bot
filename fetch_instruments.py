# fetch_instruments.py
import json
from kite_api import get_kite_instance

kite = get_kite_instance()

def fetch_and_save_instruments():
    instruments = kite.instruments("NSE")
    symbol_to_token = {}
    token_to_symbol = {}

    for item in instruments:
        symbol = item['tradingsymbol']
        token = item['instrument_token']
        symbol_to_token[symbol] = token
        token_to_symbol[token] = symbol

    with open("symbol_to_token.json", "w") as f:
        json.dump(symbol_to_token, f)
    with open("token_to_symbol.json", "w") as f:
        json.dump(token_to_symbol, f)

    print("[✅] Instruments saved to JSON files.")

if __name__ == "__main__":
    fetch_and_save_instruments()
