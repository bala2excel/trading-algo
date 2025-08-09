import random
import time
import pandas as pd
import os

class MockBroker:
    def get_atm_symbol(self, symbol_initials, option_type="CE"):
        """
        Returns the ATM option symbol for the given option type (CE/PE) and symbol_initials.
        """
        # Get current market price
        ltp = self.get_market_price(symbol_initials)
        # Filter instruments for the correct expiry and option type
        df = self.instruments_df[
            (self.instruments_df['tradingsymbol'].str.startswith(symbol_initials)) &
            (self.instruments_df['instrument_type'] == option_type)
        ]
        if df.empty:
            return None
        # Find closest strike to LTP
        df['strike_diff'] = (df['strike'] - ltp).abs()
        best = df.sort_values('strike_diff').iloc[0]
        return best['tradingsymbol']
    
    def get_market_price(self, symbol):
        # Return last_price from instruments_df or default
        df = self.instruments_df
        row = df[df["tradingsymbol"] == symbol]
        if row.empty:
            return 100.0
        return float(row.iloc[0]["last_price"])
    """
    Simulates broker API for testing and paper trading.
    """
    def __init__(self, **kwargs):
        self.orders = []
        self.price_map = {}
        self.symbols = []
        self.instruments_df = None
        self.download_instruments()

    def authenticate(self):
        return self, {"access_token": "mock_token"}

    def get_orders(self):
        return self.orders

    def get_quote(self, symbol, exchange=None):
        # symbol can be 'NFO:NIFTY25JAN30000CE' or just 'NIFTY25JAN30000CE'
        if exchange and ":" not in symbol:
            symbol = exchange + ":" + symbol
        if ":" in symbol:
            exchange, tradingsymbol = symbol.split(":")
        else:
            tradingsymbol = symbol
            exchange = None
        df = self.instruments_df
        row = df[df["tradingsymbol"] == tradingsymbol]
        if row.empty:
            return {symbol: {"last_price": 100, "instrument_token": 9999999}}
        price = float(row.iloc[0]["last_price"])
        token = int(row.iloc[0]["instrument_token"])
        return {symbol: {"last_price": price, "instrument_token": token}}

    def place_gtt_order(self, symbol, quantity, price, transaction_type, order_type, exchange, product, tag="Unknown"):
        order_id = f"mock_gtt_{int(time.time())}_{random.randint(1000,9999)}"
        order = {
            "order_id": order_id,
            "symbol": symbol,
            "quantity": quantity,
            "order_type": order_type,
            "transaction_type": transaction_type,
            "exchange": exchange,
            "product": product,
            "price": price,
            "tag": tag,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "paper_trade": True,
        }
        self.orders.append(order)
        return order_id

    def place_order(self, symbol, quantity, price, transaction_type, order_type, variety, exchange, product, tag="Unknown"):
        order_id = f"mock_{int(time.time())}_{random.randint(1000,9999)}"
        order = {
            "order_id": order_id,
            "symbol": symbol,
            "quantity": quantity,
            "order_type": order_type,
            "transaction_type": transaction_type,
            "exchange": exchange,
            "product": product,
            "price": price,
            "variety": variety,
            "tag": tag,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "paper_trade": True,
        }
        self.orders.append(order)
        return order_id

    def get_positions(self):
        # Return mock positions
        return [{"symbol": o["symbol"], "quantity": o["quantity"]} for o in self.orders]

    def symbols_to_subscribe(self, symbols):
        self.symbols = symbols

    # Websocket Callbacks (no-op for mock)
    def on_ticks(self, ws, ticks):
        pass
    def on_connect(self, ws, response):
        pass
    def on_order_update(self, ws, data):
        pass
    def on_close(self, ws, code, reason):
        pass
    def on_error(self, ws, code, reason):
        pass
    def on_reconnect(self, ws, attempts_count):
        pass
    def on_noreconnect(self, ws):
        pass

    def download_instruments(self):
        # Load mock instruments from CSV
        csv_path = os.path.join(os.path.dirname(__file__), "mock_instruments.csv")
        self.instruments_df = pd.read_csv(csv_path)

    def get_instruments(self):
        return self.instruments_df

    def connect_websocket(self):
        # No-op for mock
        pass
