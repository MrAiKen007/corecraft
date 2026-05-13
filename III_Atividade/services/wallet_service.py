from bitcoin_rpc import list_wallet_dir, list_wallets, load_wallet, get_wallet_info, list_unspent
import services.state as state

def get_wallets_info():
    available = list_wallet_dir()
    wallet_names = [w['name'] for w in available.get('wallets', [])] if available else []
    loaded = list_wallets() or []
    
    return {
        "available_wallets": wallet_names,
        "loaded_wallets": loaded,
        "selected_wallet": state.selected_wallet
    }

def select_active_wallet(wallet_name):
    available = list_wallet_dir()
    wallet_names = [w['name'] for w in available.get('wallets', [])] if available else []
    
    if wallet_name not in wallet_names:
        return None

    loaded = list_wallets() or []
    if wallet_name not in loaded:
        load_wallet(wallet_name)
    
    state.selected_wallet = wallet_name
    info = get_wallet_info(wallet=state.selected_wallet)
    return info

def get_wallet_status():
    if not state.selected_wallet:
        return None
    
    info = get_wallet_info(wallet=state.selected_wallet)
    utxos = list_unspent(wallet=state.selected_wallet)
    
    return {
        "wallet": state.selected_wallet,
        "balance": info.get("balance", 0) if info else 0,
        "utxos": len(utxos) if utxos else 0
    }
