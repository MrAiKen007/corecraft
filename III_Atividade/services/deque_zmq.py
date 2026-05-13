from collections import deque
from datetime import datetime
from bitcoin_zmq import socket

ultimo_bloco = deque(maxlen=10)
ultima_trasacao = deque(maxlen=50)

def registra_bloco(hash_bloco: str):
    evento = {
        "hash": hash_bloco,
        "timestamp": datetime.now().isoformat()
    }
    ultimo_bloco.append(evento)

def registra_transacao(hash_transacao: str):
    evento = {
        "hash": hash_transacao,
        "timestamp": datetime.now().isoformat()
    }
    ultima_trasacao.append(evento)

while True:
    topic, body, seq = socket.recv_multipart()
    
    topic = topic.decode()

    if topic == 'hashblock':
        registra_bloco(body.decode())
    elif topic == 'rawtransaction':
        registra_transacao(body.decode())

    print("\n")
    print("Últimos 10 blocos:")
    for bloco in ultimo_bloco:
        print(f"- {bloco['hash']} ({bloco['timestamp']})")
    print("\n")
    print("Últimas 50 transações:")
    for transacao in ultima_trasacao:
        print(f"- {transacao['hash']} ({transacao['timestamp']})")
    print("\n")
