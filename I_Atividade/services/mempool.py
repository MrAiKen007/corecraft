from rpc import get_mempoolinfo, get_rawmempoolinfo

def get_mempool_stats():

    info = get_mempoolinfo()
    txs = get_rawmempoolinfo()

    total_vsize = 0
    fee_rates = []

    low = 0
    medium = 0
    high = 0

    for txid, tx in txs.items():

        # vsize
        vsize = tx['vsize']
        total_vsize += vsize

        # fee em BTC
        fee_btc = tx['fees']['base']

        # converter BTC -> satoshis
        fee_sats = fee_btc * 100_000_000

        # sat/vB
        fee_rate = fee_sats / vsize

        fee_rates.append(fee_rate)

        # distribuição
        if fee_rate < 10:
            low += 1

        elif fee_rate < 50:
            medium += 1

        else:
            high += 1

    if not fee_rates:
        return {
            "tx_count": info.get('size', 0),
            "total_vsize": 0,
            "avg_fee_rate": 0,
            "min_fee_rate": 0,
            "max_fee_rate": 0,
            "fee_distribution": {"low": 0, "medium": 0, "high": 0}
        }

    result = {
        "tx_count": info['size'],
        "total_vsize": total_vsize,
        "avg_fee_rate": round(sum(fee_rates) / len(fee_rates), 2),
        "min_fee_rate": round(min(fee_rates), 2),
        "max_fee_rate": round(max(fee_rates), 2),
        "fee_distribution": {
            "low": low,
            "medium": medium,
            "high": high
        }
    }

    return result



if __name__ == '__main__':

    stats = get_mempool_stats()

    print(stats)