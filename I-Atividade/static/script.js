async function fetchData() {
    try {
        const mempoolRes = await fetch('/api/mempool/summary');
        const mempoolData = await mempoolRes.json();
        updateMempoolUI(mempoolData);

        const lagRes = await fetch('/api/blockchain/lag');
        const lagData = await lagRes.json();
        updateSyncUI(lagData);

    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

function updateMempoolUI(data) {
    document.getElementById('tx-count').textContent = data.tx_count.toLocaleString();
    document.getElementById('avg-fee').innerHTML = `${data.avg_fee_rate} <small>sat/vB</small>`;
    document.getElementById('total-vsize').innerHTML = `${(data.total_vsize / 1024 / 1024).toFixed(2)} <small>MB</small>`;
    
    document.getElementById('mempool-range').textContent = `Min: ${data.min_fee_rate} | Max: ${data.max_fee_rate} sat/vB`;

    const total = data.fee_distribution.low + data.fee_distribution.medium + data.fee_distribution.high;
    
    updateBar('low', data.fee_distribution.low, total);
    updateBar('medium', data.fee_distribution.medium, total);
    updateBar('high', data.fee_distribution.high, total);
}

function updateBar(type, count, total) {
    const percentage = total > 0 ? (count / total * 100) : 0;
    const bar = document.getElementById(`bar-${type}`);
    const val = document.getElementById(`val-${type}`);
    
    bar.style.width = `${percentage}%`;
    val.textContent = `${count} (${percentage.toFixed(1)}%)`;
}

function updateSyncUI(data) {
    document.getElementById('lag-display').textContent = data.lag;
    document.getElementById('sync-blocks').textContent = data.blocks.toLocaleString();
    document.getElementById('sync-headers').textContent = data.headers.toLocaleString();

    const statusText = document.getElementById('sync-status-text');
    if (data.lag === 0) {
        statusText.textContent = 'Node Totalmente Sincronizado';
        statusText.style.color = 'var(--success)';
    } else if (data.lag < 10) {
        statusText.textContent = `Sincronização Próxima (${data.lag} blocos)`;
        statusText.style.color = 'var(--warning)';
    } else {
        statusText.textContent = `Atrás por ${data.lag} blocos`;
        statusText.style.color = 'var(--danger)';
    }
}

fetchData();

setInterval(fetchData, 10000);
