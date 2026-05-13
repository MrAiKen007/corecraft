import time
from collections import deque

ultimo_bloco = deque(maxlen=10)
ultima_transacao = deque(maxlen=50)
selected_wallet = None
# tracked_transactions: txid -> {"wallet": "...", "added_at": float}
tracked_transactions = {} 

stats = {
    "blocks_count": 0,
    "tx_count": 0,
    "start_time": time.time(),
    "last_event_time": None
}
