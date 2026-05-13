import requests
from requests.auth import HTTPBasicAuth

NODE_URL = "http://127.0.0.1:38332"
AUTH = HTTPBasicAuth("bitcoin", "senha_forte_aqui")

def rpc(method, params=[], wallet=None):
    """
    Executa uma chamada RPC básica. 
    Melhorado para capturar erros detalhados do Bitcoin Core.
    """
    url = NODE_URL
    if wallet:
        url = f"{NODE_URL}/wallet/{wallet}"
    
    payload = {
        "jsonrpc": "1.0",
        "id": "CoreCraft",
        "method": method,
        "params": params
    }
    
    try:
        r = requests.post(url, json=payload, auth=AUTH, timeout=10)
        data = r.json()
        
        if data.get('error'):
            err = data['error']
            print(f"Erro RPC ({method}): [{err.get('code')}] {err.get('message')}")
            return None
            
        return data['result']
    except Exception as e:
        print(f"Erro na conexão HTTP ({method}): {e}")
        return None

def get_blockchaininfo():
    return rpc('getblockchaininfo')

def get_mempoolinfo():
    return rpc('getmempoolinfo')

def get_rawmempoolinfo():
    return rpc('getrawmempool', [True])

def get_best_block_hash():
    return rpc("getbestblockhash")

def list_wallet_dir():
    return rpc("listwalletdir")

def list_wallets():
    return rpc("listwallets")

def load_wallet(name):
    return rpc("loadwallet", [name])

def get_wallet_info(wallet=None):
    return rpc("getwalletinfo", wallet=wallet)

def list_unspent(wallet=None):
    return rpc("listunspent", wallet=wallet)

def get_transaction(txid, wallet=None):
    return rpc("gettransaction", [txid], wallet=wallet)

def get_raw_transaction(txid):
    return rpc("getrawtransaction", [txid, True])

def get_mempool_entry(txid):
    return rpc("getmempoolentry", [txid])

def send_to_address(address, amount, wallet=None):
    return rpc("sendtoaddress", [address, amount], wallet=wallet)