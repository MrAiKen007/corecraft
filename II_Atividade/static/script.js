async function fetchData() {
    try {
        // Aula 01 - Mempool e Lag
        const mempoolRes = await fetch('/api/mempool/summary');
        const mempoolData = await mempoolRes.json();
        updateMempoolUI(mempoolData);

        const lagRes = await fetch('/api/blockchain/lag');
        const lagData = await lagRes.json();
        updateSyncUI(lagData);

        // Aula 02 - ZMQ Atividade
        const zmqSummaryRes = await fetch('/api/events/summary');
        const zmqSummaryData = await zmqSummaryRes.json();
        updateZmqActivityUI(zmqSummaryData);

        const zmqLatestRes = await fetch('/api/events/latest');
        const zmqLatestData = await zmqLatestRes.json();
        updateLatestEventsUI(zmqLatestData);

        const compareRes = await fetch('/api/events/state-comparison');
        const compareData = await compareRes.json();
        updateDivergenceUI(compareData);

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
    } else {
        statusText.textContent = `Sincronização Ativa (${data.lag} blocos de lag)`;
        statusText.style.color = 'var(--warning)';
    }
}

// Lógica Aula 02 - ZMQ
function updateZmqActivityUI(data) {
    document.getElementById('zmq-tx-count').textContent = data.tx_observed.toLocaleString();
    document.getElementById('zmq-blocks-count').textContent = data.blocks_observed.toLocaleString();
    document.getElementById('zmq-rate').innerHTML = `${data.tx_per_second} <small>tx/s</small>`;
}

function updateLatestEventsUI(data) {
    const blockList = document.getElementById('latest-blocks-list');
    blockList.innerHTML = data.blocks.map(b => `
        <li>
            <span>${b.hash.substring(0, 20)}...</span>
            <span class="ts">${new Date(b.ts * 1000).toLocaleTimeString()}</span>
        </li>
    `).join('');

    const txList = document.getElementById('latest-txs-list');
    txList.innerHTML = data.txs.map(t => `
        <li>
            <span>${t.txid.substring(0, 20)}...</span>
            <span class="ts">${new Date(t.ts * 1000).toLocaleTimeString()}</span>
        </li>
    `).join('');
}

function updateDivergenceUI(data) {
    const alert = document.getElementById('divergence-alert');
    if (data.divergence) {
        alert.style.display = 'flex';
    } else {
        alert.style.display = 'none';
    }
}

fetchData();
setInterval(fetchData, 5000);
