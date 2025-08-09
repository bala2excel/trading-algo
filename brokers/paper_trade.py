import csv
import os
from datetime import datetime

class PaperTradeLogger:
    def __init__(self, csv_file='artifacts/paper_trades.csv'):
        self.csv_file = csv_file
        os.makedirs(os.path.dirname(self.csv_file), exist_ok=True)
        self.header = ['timestamp', 'symbol', 'side', 'quantity', 'price', 'order_type', 'exchange', 'product', 'tag']
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(self.header)

    def log_trade(self, symbol, side, quantity, price, order_type, exchange, product, tag):
        with open(self.csv_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().isoformat(), symbol, side, quantity, price, order_type, exchange, product, tag
            ])
