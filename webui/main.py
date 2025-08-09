from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import threading
import queue
import os
import yaml
import time
import asyncio

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
config_file = os.path.join(os.path.dirname(__file__), "../strategy/configs/survivor.yml")

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
    while status["running"]:
        # Simulate order placement every 5 seconds
        order = {
            "order_id": f"paper_{int(time.time())}",
            "symbol": "NIFTY25JAN30000CE",
            "quantity": 50,
            "market_price": 100 + int(time.time()) % 10,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "paper_trade": True,
        }
        order_queue.put(order)
        # Put order in thread-safe queue for async publishing
        thread_order_queue.put(order)
        time.sleep(5)
