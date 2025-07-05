import csv
from datetime import datetime

LOG_FILE = "trades.csv"

def log_trade(trade_data):
    fieldnames = ['timestamp', 'symbol', 'ltp', 'sl', 'tp', 'direction', 'order_id']
    trade_data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        file_exists = False
        try:
            with open(LOG_FILE, 'r') as f:
                file_exists = True
        except FileNotFoundError:
            pass

        with open(LOG_FILE, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow(trade_data)

    except Exception as e:
        print(f"Logging Error: {e}")
