from rpc import get_blockchaininfo

def get_blockchain_lag():
    info = get_blockchaininfo()
    blocks = info.get('blocks', 0)
    headers = info.get('headers', 0)
    lag = headers - blocks
    
    return {
        "blocks": blocks,
        "headers": headers,
        "lag": lag
    }

if __name__ == '__main__':
    print(get_blockchain_lag())
