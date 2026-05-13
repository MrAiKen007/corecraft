import time
from bitcoin_rpc import get_transaction, get_raw_transaction, get_mempool_entry
import services.state as state

def interpret_tx(txid, wallet_name=None):
    # Tenta buscar detalhes na wallet primeiro
    tx_data = get_transaction(txid, wallet=wallet_name)
    
    if not tx_data:
        # Se não estiver na wallet, tenta o node global
        tx_data = get_raw_transaction(txid)
        if not tx_data:
            return {
                "txid": txid,
                "wallet": wallet_name or "global",
                "status": "unknown",
                "confirmed": False,
                "confirmations": 0,
                "block_hash": None,
                "age_seconds": 0,
                "message": "Transação não localizada.",
                "warning": "Transação não localizada na wallet selecionada ou no node."
            }

    confirmations = tx_data.get("confirmations", 0)
    
    if txid in state.tracked_transactions:
        added_at = state.tracked_transactions[txid]["added_at"]
    else:
        added_at = tx_data.get("time", time.time())
    
    age_seconds = int(time.time() - added_at)

    status = "unknown"
    message = ""
    warning = None

    if confirmations > 0:
        status = "confirmed"
        message = "Transação confirmada em bloco."
    else:
        mempool_entry = get_mempool_entry(txid)
        if mempool_entry:
            status = "mempool"
            message = "Transação aceita na mempool, aguardando inclusão em bloco."
            if age_seconds > 120:
                warning = "Transação está na mempool há mais de 2 minutos."
        else:
            status = "broadcast"
            message = "Transação enviada ao node, aguardando aceitação na mempool."

    return {
        "txid": txid,
        "wallet": wallet_name or "global",
        "status": status,
        "confirmed": confirmations > 0,
        "confirmations": confirmations,
        "block_hash": tx_data.get("blockhash"),
        "age_seconds": age_seconds,
        "message": message,
        "warning": warning
    }
