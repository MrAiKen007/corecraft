import zmq
import zmq.asyncio
import time
import asyncio
import hashlib
import services.state as state

def calculate_txid(raw_hex):
    """Calcula o TXID real a partir do hex da transação bruta."""
    try:
        raw_bytes = bytes.fromhex(raw_hex)
        first_sha = hashlib.sha256(raw_bytes).digest()
        second_sha = hashlib.sha256(first_sha).digest()
        # O TXID é o hash reverso (little-endian)
        return second_sha[::-1].hex()
    except Exception:
        return raw_hex[:64]

async def zmq_listener():
    context = zmq.asyncio.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://127.0.0.1:28332")
    
    socket.setsockopt_string(zmq.SUBSCRIBE, "hashtx")
    socket.setsockopt_string(zmq.SUBSCRIBE, "rawtx")
    socket.setsockopt_string(zmq.SUBSCRIBE, "hashblock")

    print("--- ZMQ Listener Ativado: Calculando TXIDs reais... ---")
    while True:
        try:
            topic, body, seq = await socket.recv_multipart()
            topic = topic.decode()
            hex_data = body.hex()
            
            current_ts = int(time.time())
            state.stats["last_event_time"] = current_ts

            if topic == 'hashblock':
                evento = {"hash": hex_data, "ts": current_ts}
                state.ultimo_bloco.appendleft(evento)
                state.stats["blocks_count"] += 1
                
            elif topic == 'hashtx':
                txid = hex_data
                print(f"-> ZMQ: Nova transação (hashtx): {txid[:10]}...")
                evento = {"txid": txid, "ts": current_ts}
                state.ultima_transacao.appendleft(evento)
                state.stats["tx_count"] += 1
                
            elif topic == 'rawtx':
                # Cálculo do TXID real para evitar erro -5
                txid = calculate_txid(hex_data)
                print(f"-> ZMQ: Nova transação (rawtx -> txid calculado): {txid[:10]}...")
                evento = {"txid": txid, "ts": current_ts}
                state.ultima_transacao.appendleft(evento)
                state.stats["tx_count"] += 1
                
        except Exception as e:
            print(f"Erro no ZMQ: {e}")
            await asyncio.sleep(1)
