# trading-algo
Code for certain trading strategies
1. Survivor Algo is Live

## Disclaimer:
This algorithm is provided for **educational** and **informational purposes** only. Trading in financial markets involves substantial risk, and you may lose all or more than your initial investment. By using this algorithm, you acknowledge that all trading decisions are made at your own risk and discretion. The creators of this algorithm assume no liability or responsibility for any financial losses or damages incurred through its use. **Always do your own research and consult with a qualified financial advisor before trading.**


## Setup

### 1. Install Dependencies

To insall uv, use:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
or


```bash
pip install uv
```

This uses `uv` for dependency management. Install dependencies:
```bash
uv sync
```

Or if you prefer using pip:

```bash
pip install -r requirements.txt  # You may need to generate this from pyproject.toml

### 4. Paper Trading Mode

You can run the strategy in paper trading mode to simulate trades without executing real orders. This is useful for backtesting and P&L analysis.

**Enable paper trading:**
1. Edit your `.env` file and set:
   ```bash
   PAPER_TRADE=true
   ```
2. Run the strategy as usual. All trades will be simulated and logged with market price for P&L calculation.

**Log format for paper trades:**
```
[PAPER TRADE] ORDER | Symbol: <symbol> | Qty: <quantity> | Price: <market_price> | Type: <BUY/SELL> | Time: <timestamp> | OrderID: <paper_xxx>
```

### 5. Web UI for Live Management

The project includes a web-based UI for managing strategy parameters, starting/stopping the algorithm, and viewing live order placements (including paper trades).

#### Backend (FastAPI)
1. Install backend dependencies:
   ```bash
   cd webui
   pip install -r requirements.txt  # or use 'uv sync' if using uv
   ```
2. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

#### Frontend (React)
1. Install frontend dependencies:
   ```bash
   cd webui
   npm install
   ```
2. Start the React development server:
   ```bash
   npm start
   ```

#### Usage
- Open your browser and go to `http://localhost:3000` to access the UI.
- You can edit parameters, start/stop the algorithm, and view live order placements (including paper trades) in real time.

#### Websocket Order Feed
- All paper and live trades are emitted via websocket to the UI for live monitoring.

---
```

1. Copy the sample environment file:
   ```bash
   cp .sample.env .env
2. Edit `.env` and fill in your broker credentials:
   ```bash
### 7. Core Components

- `brokers/`: Broker implementations (Fyers, Zerodha)
- `dispatcher.py`: Data routing and queue management
- `orders.py`: Order management utilities
- `logger.py`: Logging configuration
- `strategy/`: Place your trading strategies here
- `webui/`: FastAPI backend and React frontend for live management
   BROKER_TOTP_ENABLE=false # or true
   BROKER_ID=<YOUR_BROKER_ID>
   BROKER_TOTP_REDIDRECT_URI=<YOUR_TOTP_REDIRECT_URI>
   BROKER_TOTP_KEY=<YOUR_TOTP_KEY>
   BROKER_TOTP_PIN=<YOUR_TOTP_PIN>
   BROKER_PASSWORD=<YOUR_BROKER_PASSWORD>  # Required for Zerodha
   ```

### 3. Running Strategies

Strategies should be placed in the `strategy/` folder.

#### Running the Survivor Strategy


**Basic usage (using default config):**

For more details, check the individual broker implementations, example strategies in the `strategy/` folder, and the web UI in `webui/`.
```bash
cd strategy/
python survivor.py
```

**With custom parameters:**
```bash
cd strategy/
python survivor.py \
    --symbol-initials NIFTY25JAN30 \
    --pe-gap 25 --ce-gap 25 \
    --pe-quantity 50 --ce-quantity 50 \
    --min-price-to-sell 15
```

**View current configuration:**
```bash
cd strategy/
python survivor.py --show-config
```

### 4. Available Brokers

- **Fyers**: Supports REST API for historical data, quotes, and WebSocket for live data
- **Zerodha**: Supports KiteConnect API with order management and live data streaming

### 5. Core Components

- `brokers/`: Broker implementations (Fyers, Zerodha)
- `dispatcher.py`: Data routing and queue management
- `orders.py`: Order management utilities
- `logger.py`: Logging configuration
- `strategy/`: Place your trading strategies here

### Example Usage

```python
from brokers.fyers import FyersBroker
from brokers.zerodha import ZerodhaBroker

# Initialize broker based on environment
if os.getenv('BROKER_NAME') == 'fyers':
    broker = FyersBroker(symbols=['NSE:SBIN-EQ'])
else:
    broker = ZerodhaBroker(without_totp=True) # Only available for Zerodha

# Get historical data, place orders, etc.
```

For more details, check the individual broker implementations and example strategies in the `strategy/` folder.
