import asyncio
import json
import logging
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Set

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

import config
from cme_fetcher import (
    get_all_quotes,
    get_quote_by_symbol,
    get_history_by_symbol,
    get_contracts_info,
    get_quikstrike_most_actives,
    start_cme_market_loop,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Active WebSocket clients
connected_clients: Set[WebSocket] = set()


async def broadcast_market_updates():
    """Broadcasts quotes to all connected WebSocket clients every 10 seconds."""
    while True:
        await asyncio.sleep(config.UPDATE_INTERVAL_SECONDS)
        if connected_clients:
            quotes = get_all_quotes()
            payload = json.dumps({"type": "quotes_update", "data": quotes})
            dead_clients = set()
            for ws in list(connected_clients):
                try:
                    await ws.send_text(payload)
                except Exception:
                    dead_clients.add(ws)
            for dead in dead_clients:
                connected_clients.discard(dead)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: start background market loops
    loop_task = asyncio.create_task(start_cme_market_loop())
    broadcast_task = asyncio.create_task(broadcast_market_updates())
    logger.info("FastAPI CME Metals Mini App backend started!")
    yield
    # Shutdown
    loop_task.cancel()
    broadcast_task.cancel()


app = FastAPI(title="CME Metals Mini App API", lifespan=lifespan)

# Allow CORS for Telegram WebApp
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"


# API Routes
@app.get("/api/quotes")
async def api_get_quotes():
    """Returns current prices and stats for all CME contracts."""
    return {"status": "ok", "quotes": get_all_quotes()}


@app.get("/api/quote/{symbol}")
async def api_get_quote(symbol: str):
    """Returns data for a single instrument."""
    quote = get_quote_by_symbol(symbol)
    if not quote:
        raise HTTPException(status_code=404, detail="Instrument not found")
    return {"status": "ok", "quote": quote}


@app.get("/api/contracts")
async def api_get_contracts():
    """Returns specifications and expiration schedules for all contracts."""
    return {"status": "ok", "contracts": get_contracts_info()}


@app.get("/api/contracts/{symbol}")
async def api_get_contract_by_symbol(symbol: str):
    """Returns specs and expirations for specific instrument."""
    quote = get_quote_by_symbol(symbol)
    if not quote:
        raise HTTPException(status_code=404, detail="Instrument not found")
    return {
        "status": "ok",
        "symbol": quote["symbol"],
        "name": quote["name"],
        "specs": quote.get("specs", {}),
        "expirations": quote.get("expirations", []),
    }


@app.get("/api/options/most-actives")
async def api_get_options_most_actives(min_oi: int = 1000, symbol: str = "GC"):
    """Returns CME QuikStrike Most Actives filtered by Open Interest."""
    return {"status": "ok", "data": get_quikstrike_most_actives(min_oi=min_oi, symbol=symbol)}


@app.get("/api/history/{symbol}")
async def api_get_history(symbol: str, limit: int = 100):
    """Returns OHLC candles for TradingView Lightweight Charts."""
    history = get_history_by_symbol(symbol, limit=limit)
    if not history:
        raise HTTPException(status_code=404, detail="Symbol not found")
    return {"status": "ok", "symbol": symbol.upper(), "candles": history}


@app.get("/api/health")
async def api_health():
    return {"status": "healthy", "service": "cme-metals-miniapp"}


# WebSocket live stream
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)
    try:
        # Send initial snapshot immediately
        await websocket.send_text(json.dumps({
            "type": "initial_snapshot",
            "data": get_all_quotes()
        }))
        while True:
            # Keep connection open and receive client messages (pings, subscriptions)
            data = await websocket.receive_text()
            try:
                msg = json.loads(data)
                if msg.get("action") == "ping":
                    await websocket.send_text(json.dumps({"type": "pong"}))
            except Exception:
                pass
    except WebSocketDisconnect:
        connected_clients.discard(websocket)
    except Exception as e:
        logger.warning(f"WebSocket error: {e}")
        connected_clients.discard(websocket)


# Serve Static Frontend Files
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

    @app.get("/")
    async def serve_index():
        return FileResponse(FRONTEND_DIR / "index.html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host=config.API_HOST, port=config.API_PORT, reload=True)
