# Trading Algo Web UI

## Features
- Edit strategy parameters
- Start/Stop algorithm
- Live order feed (paper & live trades)

## How to Run

### Backend (FastAPI)
1. Install dependencies:
   ```bash
   pip install fastapi uvicorn pyyaml
   ```
2. Start backend:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

### Frontend (React)
1. Install dependencies:
   ```bash
   npm install
   ```
2. Start frontend:
   ```bash
   npm run dev
   ```

Open [http://localhost:5173](http://localhost:5173) in your browser.

---

**Note:**
- The backend emits paper trades via websocket (`/ws/orders`).
- Replace the dummy `run_algo` in `main.py` with your real strategy integration.
- The UI will show all order placements live.
