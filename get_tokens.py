import json

def build_token_maps(instruments_file='instruments.json'):
    symbol_to_token = {}
    token_to_symbol = {}

    with open(instruments_file, 'r') as f:
        instruments = json.load(f)

    for instrument in instruments:
        if instrument['exchange'] == 'NSE' and instrument['tradingsymbol'].isalpha():
            token = instrument['instrument_token']
            symbol = instrument['tradingsymbol']
            symbol_to_token[symbol] = token
            token_to_symbol[str(token)] = symbol

    with open('symbol_to_token.json', 'w') as f:
        json.dump(symbol_to_token, f)

    with open('token_to_symbol.json', 'w') as f:
        json.dump(token_to_symbol, f)
