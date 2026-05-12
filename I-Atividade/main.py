from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from services.mempool import get_mempool_stats
from services.blockchain import get_blockchain_lag
import os

app = FastAPI(title="Bitcoin Snapshot Inteligente")

@app.get("/api/mempool/summary")
async def mempool_summary():
    return get_mempool_stats()

@app.get("/api/blockchain/lag")
async def blockchain_lag():
    return get_blockchain_lag()

@app.get("/")
async def read_index():
    return FileResponse('static/index.html')

if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
