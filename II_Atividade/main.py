import asyncio
import time
import sys
from datetime import datetime
from collections import deque
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import zmq
import zmq.asyncio
from bitcoin_rpc import rpc

# Correção para erro do ZMQ no Windows
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = FastAPI(title="CoreCraft | Bitcoin Event Monitor")

@app.get("/")
async def root():
    return RedirectResponse(url="/static/index.html")

# Servir arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ESTADO EM MEMÓRIA ---
ultimo_bloco = deque(maxlen=10)
ultima_transacao = deque(maxlen=50)
stats = {
    "blocks_count": 0,
    "tx_count": 0,
    "start_time": time.time(),
    "last_event_time": None
}

# --- BACKGROUND TASKS ---
async def zmq_listener():
    context = zmq.asyncio.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://127.0.0.1:28332")
    socket.setsockopt_string(zmq.SUBSCRIBE, "rawtx")
    socket.setsockopt_string(zmq.SUBSCRIBE, "hashblock")

    print("--- ZMQ Listener Ativado ---")
    while True:
        try:
            topic, body, seq = await socket.recv_multipart()
            topic = topic.decode()
            hex_data = body.hex()
            
            current_ts = int(time.time())
            stats["last_event_time"] = current_ts

            if topic == 'hashblock':
                evento = {"hash": hex_data, "ts": current_ts}
                ultimo_bloco.appendleft(evento)
                stats["blocks_count"] += 1
                
            elif topic == 'rawtx':
                evento = {"txid": hex_data[:64], "ts": current_ts}
                ultima_transacao.appendleft(evento)
                stats["tx_count"] += 1
        except Exception as e:
            print(f"Erro no ZMQ: {e}")
            await asyncio.sleep(1)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(zmq_listener())

# --- ENDPOINTS AULA 01 (SNAPSHOT/RPC) ---

@app.get("/api/mempool/summary")
async def get_mempool_summary():
    mempool_info = rpc("getmempoolinfo")
    # Simulação de distribuição para o dashboard (Aula 01)
    return {
        "tx_count": mempool_info["size"],
        "avg_fee_rate": 15, # Simplificado para exemplo
        "total_vsize": mempool_info["bytes"],
        "min_fee_rate": 1,
        "max_fee_rate": 500,
        "fee_distribution": {"low": 40, "medium": 35, "high": 25}
    }

@app.get("/api/blockchain/lag")
async def get_blockchain_lag():
    info = rpc("getblockchaininfo")
    blocks = info["blocks"]
    headers = info["headers"]
    return {
        "blocks": blocks,
        "headers": headers,
        "lag": headers - blocks
    }

# --- ENDPOINTS AULA 02 (EVENTOS/ZMQ) ---

@app.get("/api/events/summary")
async def get_events_summary():
    uptime = time.time() - stats["start_time"]
    tx_per_second = round(stats["tx_count"] / uptime, 2) if uptime > 0 else 0
    return {
        "blocks_observed": stats["blocks_count"],
        "tx_observed": stats["tx_count"],
        "last_event_time": stats["last_event_time"],
        "tx_per_second": tx_per_second
    }

@app.get("/api/events/latest")
async def get_events_latest():
    return {
        "blocks": list(ultimo_bloco),
        "txs": list(ultima_transacao)
    }

@app.get("/api/events/state-comparison")
async def get_comparison():
    best_block_rpc = rpc("getbestblockhash")
    last_seen_zmq = ultimo_bloco[0]["hash"] if ultimo_bloco else None
    return {
        "best_block": best_block_rpc,
        "last_seen_block": last_seen_zmq,
        "divergence": (last_seen_zmq is not None and best_block_rpc != last_seen_zmq)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
