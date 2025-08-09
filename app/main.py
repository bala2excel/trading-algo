from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import threading
import queue
import os
import yaml
import time
import asyncio
from brokers.zerodha import ZerodhaBroker
from brokers.mock import MockBroker
from strategy.survivor import SurvivorStrategy

# from app.brokers.zerodha import ZerodhaBroker
# from app.brokers.mock import MockBroker
# from app.strategy.survivor import SurvivorStrategy

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

order_queue = queue.Queue()
async_order_queue = asyncio.Queue()
status = {"running": False}
config_file = os.path.join(os.path.dirname(__file__), "./strategy/configs/survivor.yml")

# Thread-safe queue for cross-thread order publishing
thread_order_queue = queue.Queue()

# Background task to move orders from thread_order_queue to async_order_queue
async def order_publisher():
    while True:
        try:
            order = thread_order_queue.get(timeout=1)
            await async_order_queue.put(order)
        except queue.Empty:
            await asyncio.sleep(0.1)

@app.on_event("startup")
async def startup_event():
    # Start the background publisher
    asyncio.create_task(order_publisher())

# Load config
with open(config_file, "r") as f:
    config = yaml.safe_load(f)["default"]

@app.get("/parameters")
def get_parameters():
    return config

@app.post("/parameters")
def set_parameters(new_config: dict):
    config.update(new_config)
    with open(config_file, "w") as f:
        yaml.safe_dump({"default": config}, f)
    return JSONResponse({"success": True, "config": config})

@app.get("/status")
def get_status():
    return status

@app.post("/start")
def start_algo():
    if not status["running"]:
        status["running"] = True
        threading.Thread(target=run_algo, daemon=True).start()
    return {"running": status["running"]}

@app.post("/stop")
def stop_algo():
    status["running"] = False
    return {"running": status["running"]}

@app.websocket("/ws/orders")
async def websocket_orders(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            try:
                # Use asyncio.Queue for non-blocking async
                order = await asyncio.wait_for(async_order_queue.get(), timeout=1)
                await ws.send_json(order)
            except asyncio.TimeoutError:
                await asyncio.sleep(0.5)
    except WebSocketDisconnect:
        pass

# Dummy algo runner for demo (replace with real integration)
def run_algo():
    # Load broker credentials from environment
    paper_trade = os.getenv("PAPER_TRADE", "true").lower() == "true"
    if paper_trade:
        broker = MockBroker()
        class DummyOrderManager:
            def add_order(self, order_details):
                pass
        order_manager = DummyOrderManager()
    else:
        broker = ZerodhaBroker(
            api_key=os.getenv("BROKER_API_KEY"),
            api_secret=os.getenv("BROKER_API_SECRET"),
            user_id=os.getenv("BROKER_ID"),
            password=os.getenv("BROKER_PASSWORD"),
            totp_key=os.getenv("BROKER_TOTP_KEY"),
        )
        from app.orders import OrderTracker
        order_manager = OrderTracker()
    strategy = SurvivorStrategy(broker, config, order_manager)

    # Dynamically select ATM symbol for simulation/live trading
    symbol_initials = config.get("symbol_initials", "NIFTY25JAN30")
    option_type = "CE"  # Default to CE, can be made configurable
    symbol = broker.get_atm_symbol(symbol_initials, option_type)
    if not symbol:
        # Fallback to first available instrument
        symbol = symbol_initials
    interval = config.get("interval", 5)

    while status["running"]:
        if paper_trade:
            # Simulate tick data from mock instruments
            market_price = broker.get_market_price(symbol)
            tick_data = {"last_price": market_price}
            strategy.on_ticks_update(tick_data)
        else:
            # For live, get real quote and pass to strategy
            market_price = broker.get_market_price(symbol)
            tick_data = {"last_price": market_price}
            strategy.on_ticks_update(tick_data)
        time.sleep(interval)
