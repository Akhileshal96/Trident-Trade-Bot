import pandas as pd

def get_token_map_nifty100():
    url = "https://api.kite.trade/instruments"
    df = pd.read_csv(url)

    df = df[(df['exchange'] == 'NSE') & (df['instrument_type'] == 'EQ')]

    nifty100_symbols = [
        "RELIANCE", "INFY", "TCS", "HDFCBANK", "ICICIBANK", "KOTAKBANK",
        "ITC", "LT", "SBIN", "AXISBANK", "HCLTECH", "WIPRO", "ASIANPAINT",
        "ULTRACEMCO", "SUNPHARMA", "MARUTI", "TITAN", "BAJAJFINSV", "NESTLEIND",
        "HINDUNILVR"
    ]

    df = df[df['tradingsymbol'].isin(nifty100_symbols)]
    token_map = dict(zip(df['tradingsymbol'], df['instrument_token']))
    return token_map
