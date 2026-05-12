import requests
from requests.auth import HTTPBasicAuth

RPC_URL = "http://127.0.0.1:18443"
AUTH = HTTPBasicAuth("teste","teste")

def rpc(method , params=[]):
    payload = {
        "jsonrpc" : "1.0",
        "id" : "Atividade",
        "method" : method,
        "params" : params
    }
    r = requests.post(RPC_URL, json=payload, auth=AUTH)
    return r.json()['result']

def get_blockchaininfo():
    return rpc('getblockchaininfo')

def get_mempoolinfo():
    return rpc('getmempoolinfo')

def get_rawmempoolinfo():
    return rpc('getrawmempool', [True])
