import asyncio
import sys
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from bitcoin_rpc import list_wallets, get_mempoolinfo, get_blockchaininfo, get_best_block_hash
import services.state as state
from services.zmq_service import zmq_listener
from services.wallet_service import get_wallets_info, select_active_wallet, get_wallet_status
from services.tx_service import interpret_tx

# Correção para erro do ZMQ no Windows
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

@asynccontextmanager
async def lifespan(app: FastAPI):

    asyncio.create_task(zmq_listener())
    try:
        loaded = list_wallets()
        if loaded and len(loaded) > 0:
            state.selected_wallet = loaded[0]
    except Exception as e:
        print(f"Erro ao inicializar wallets: {e}")
    
    yield

    print("Encerrando servidor...")

app = FastAPI(
    title="CoreCraft | Bitcoin Service Oriented",
    lifespan=lifespan
)

@app.get("/")
async def root():
    return RedirectResponse(url="/static/index.html")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class WalletSelection(BaseModel):
    wallet: str

@app.get("/api/wallets")
async def api_get_wallets():
    return get_wallets_info()

@app.post("/api/wallet/select")
async def api_select_wallet(selection: WalletSelection):
    info = select_active_wallet(selection.wallet)
    if not info:
        raise HTTPException(status_code=404, detail="Wallet não encontrada.")
    
    return {
        "selected_wallet": state.selected_wallet,
        "wallet_info": {
            "walletname": info.get("walletname"),
            "balance": info.get("balance"),
            "txcount": info.get("txcount")
        }
    }

@app.get("/api/wallet/status")
async def api_get_wallet_status():
    status = get_wallet_status()
    if not status:
        return {"error": "Nenhuma wallet selecionada"}
    return status

@app.get("/api/tx/{txid}")
async def api_get_tx_details(txid: str):
    return interpret_tx(txid, state.selected_wallet)

class SendRequest(BaseModel):
    address: str
    amount: float

@app.post("/api/wallet/send")
async def api_wallet_send(request: SendRequest):
    if not state.selected_wallet:
        raise HTTPException(status_code=400, detail="Nenhuma wallet selecionada.")
    
    from bitcoin_rpc import send_to_address
    txid = send_to_address(request.address, request.amount, state.selected_wallet)
    
    if not txid:
        raise HTTPException(status_code=500, detail="Erro ao enviar transação. Verifique o saldo e o endereço.")
    
    return {"txid": txid, "message": "Transação enviada com sucesso!"}

@app.get("/api/mempool/summary")
async def get_mempool_summary():
    mempool_info = get_mempoolinfo()
    if not mempool_info:
        return {"error": "Node offline"}
        
    return {
        "tx_count": mempool_info["size"],
        "avg_fee_rate": 15, 
        "total_vsize": mempool_info["bytes"],
        "min_fee_rate": 1,
        "max_fee_rate": 500,
        "fee_distribution": {"low": 40, "medium": 35, "high": 25}
    }

@app.get("/api/blockchain/lag")
async def get_blockchain_lag():
    info = get_blockchaininfo()
    if not info:
        return {"error": "Node offline"}
        
    blocks = info["blocks"]
    headers = info["headers"]
    return {
        "blocks": blocks,
        "headers": headers,
        "lag": headers - blocks
    }

@app.get("/api/events/summary")
async def get_events_summary():
    uptime = time.time() - state.stats["start_time"]
    tx_per_second = round(state.stats["tx_count"] / uptime, 2) if uptime > 0 else 0
    return {
        "blocks_observed": state.stats["blocks_count"],
        "tx_observed": state.stats["tx_count"],
        "last_event_time": state.stats["last_event_time"],
        "tx_per_second": tx_per_second
    }

@app.get("/api/events/latest")
async def get_events_latest():
    txs_with_wallet = []
    for t in list(state.ultima_transacao):
        tx_item = t.copy()
        tx_item["wallet"] = state.selected_wallet or "global"
        txs_with_wallet.append(tx_item)
        
    return {
        "blocks": list(state.ultimo_bloco),
        "txs": txs_with_wallet
    }

@app.get("/api/events/state-comparison")
async def get_comparison():
    best_block_rpc = get_best_block_hash()
    last_seen_zmq = state.ultimo_bloco[0]["hash"] if state.ultimo_bloco else None
    return {
        "best_block": best_block_rpc,
        "last_seen_block": last_seen_zmq,
        "divergence": (last_seen_zmq is not None and best_block_rpc != last_seen_zmq)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)