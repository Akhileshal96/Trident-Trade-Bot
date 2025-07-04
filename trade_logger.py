# trade_logger.py
import csv
import os
from datetime import datetime

def log_trade(trade, exit_price, pnl):
    file_path = "trades.csv"
    file_exists = os.path.exists(file_path)

    with open(file_path, mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Date", "Time", "Symbol", "Entry", "SL", "TP", "Exit", "Qty", "PNL"])

        now = datetime.now()
        writer.writerow([
            now.strftime("%Y-%m-%d"),
            now.strftime("%H:%M:%S"),
            trade["symbol"],
            trade["entry"],
            trade["sl"],
            trade["tp"],
            exit_price,
            trade["qty"],
            round(pnl, 2)
        ])
