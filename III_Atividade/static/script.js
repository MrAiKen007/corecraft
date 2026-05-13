let currentWallet = null;

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

        // Aula 03 - Status da Wallet
        fetchWalletStatus();

    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

// Lógica Aula 03 - Wallets
async function initWallets() {
    try {
        const res = await fetch('/api/wallets');
        const data = await res.json();
        const select = document.getElementById('wallet-select');
        
        if (data.available_wallets.length === 0) {
            select.innerHTML = '<option value="">Nenhuma wallet encontrada</option>';
            return;
        }

        select.innerHTML = data.available_wallets.map(w => 
            `<option value="${w}" ${w === data.selected_wallet ? 'selected' : ''}>${w}</option>`
        ).join('');

        currentWallet = data.selected_wallet;
        
        select.addEventListener('change', (e) => {
            selectWallet(e.target.value);
        });

        if (currentWallet) {
            fetchWalletStatus();
        }
    } catch (e) {
        console.error("Erro ao carregar wallets", e);
    }
}

async function selectWallet(wallet) {
    try {
        const res = await fetch('/api/wallet/select', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ wallet })
        });
        const data = await res.json();
        currentWallet = data.selected_wallet;
        fetchWalletStatus();
        fetchData();
    } catch (e) {
        console.error("Erro ao selecionar wallet", e);
    }
}

async function fetchWalletStatus() {
    if (!currentWallet) return;
    try {
        const res = await fetch('/api/wallet/status');
        const data = await res.json();
        if (data.error) return;
        
        document.getElementById('wallet-balance').innerHTML = `${data.balance.toFixed(8)} <small>BTC</small>`;
        document.getElementById('wallet-utxos').textContent = data.utxos;
        document.getElementById('active-wallet-name').textContent = data.wallet;
        document.getElementById('execution-context').textContent = `Contexto: ${data.wallet}`;
    } catch (e) {
        console.error("Erro ao carregar status da wallet", e);
    }
}

function updateMempoolUI(data) {
    if (data.error) return;
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
    if (data.error) return;
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

function updateZmqActivityUI(data) {
    document.getElementById('zmq-tx-count').textContent = data.tx_observed.toLocaleString();
    document.getElementById('zmq-blocks-count').textContent = data.blocks_observed.toLocaleString();
    document.getElementById('zmq-rate').innerHTML = `${data.tx_per_second} <small>tx/s</small>`;
}

async function updateLatestEventsUI(data) {
    const blockList = document.getElementById('latest-blocks-list');
    blockList.innerHTML = data.blocks.map(b => `
        <li>
            <span class="hash-label">${b.hash.substring(0, 16)}...</span>
            <span class="ts">${new Date(b.ts * 1000).toLocaleTimeString()}</span>
        </li>
    `).join('');

    const txList = document.getElementById('latest-txs-list');
    
    // Para cada transação, vamos tentar buscar a interpretação (Aula 03)
    // Nota: Em produção, isso deveria ser otimizado para não fazer 50 fetches por ciclo.
    // Aqui faremos apenas para as 5 primeiras para demonstrar.
    const topTxs = data.txs.slice(0, 5);
    const otherTxs = data.txs.slice(5);

    let html = '';
    
    for (const t of topTxs) {
        try {
            const detailRes = await fetch(`/api/tx/${t.txid}`);
            const detail = await detailRes.json();
            
            html += `
                <li class="event-item status-${detail.status}">
                    <div class="event-main">
                        <span class="txid">${t.txid.substring(0, 16)}...</span>
                        <span class="badge">${detail.status}</span>
                        <span class="wallet-tag"><i class="fas fa-wallet"></i> ${t.wallet}</span>
                    </div>
                    <div class="event-meta">
                        <span class="message">${detail.message}</span>
                        ${detail.warning ? `<span class="warning"><i class="fas fa-exclamation-circle"></i> ${detail.warning}</span>` : ''}
                        <span class="ts">${new Date(t.ts * 1000).toLocaleTimeString()} (${detail.age_seconds}s)</span>
                    </div>
                </li>
            `;
        } catch (e) {
            html += `<li><span>${t.txid.substring(0, 16)}...</span> <span class="ts">${new Date(t.ts * 1000).toLocaleTimeString()}</span></li>`;
        }
    }

    html += otherTxs.map(t => `
        <li class="simple-item">
            <span>${t.txid.substring(0, 16)}...</span>
            <span class="wallet-tag">${t.wallet}</span>
            <span class="ts">${new Date(t.ts * 1000).toLocaleTimeString()}</span>
        </li>
    `).join('');

    txList.innerHTML = html;
}

function updateDivergenceUI(data) {
    const alert = document.getElementById('divergence-alert');
    if (data.divergence) {
        alert.style.display = 'flex';
    } else {
        alert.style.display = 'none';
    }
}

document.getElementById('btn-track-tx').addEventListener('click', trackManualTx);
document.getElementById('btn-send-btc').addEventListener('click', sendBitcoin);

async function sendBitcoin() {
    const address = document.getElementById('send-address').value.trim();
    const amount = parseFloat(document.getElementById('send-amount').value);
    const statusDiv = document.getElementById('send-result');

    if (!address || isNaN(amount)) {
        alert("Preencha o endereço e o valor corretamente.");
        return;
    }

    statusDiv.style.display = 'block';
    statusDiv.className = 'send-status';
    statusDiv.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processando envio...';

    try {
        const res = await fetch('/api/wallet/send', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ address, amount })
        });

        const data = await res.json();

        if (res.ok) {
            statusDiv.className = 'send-status success';
            statusDiv.innerHTML = `<i class="fas fa-check-circle"></i> Sucesso! TXID: ${data.txid.substring(0, 15)}...`;
            document.getElementById('send-address').value = '';
            document.getElementById('send-amount').value = '';
            setTimeout(fetchData, 2000);
        } else {
            statusDiv.className = 'send-status error';
            statusDiv.innerHTML = `<i class="fas fa-times-circle"></i> Erro: ${data.detail}`;
        }
    } catch (e) {
        statusDiv.className = 'send-status error';
        statusDiv.innerHTML = `<i class="fas fa-times-circle"></i> Falha na conexão com o servidor.`;
    }
}
document.getElementById('btn-sync-wallet').addEventListener('click', () => {
    fetchData();
    const icon = document.querySelector('#btn-sync-wallet i');
    icon.classList.add('fa-spin');
    setTimeout(() => icon.classList.remove('fa-spin'), 1000);
});

async function trackManualTx() {
    const txid = document.getElementById('manual-txid').value.trim();
    if (!txid) return;

    const resultDiv = document.getElementById('manual-track-result');
    resultDiv.style.display = 'block';
    resultDiv.innerHTML = '<p>Buscando...</p>';

    try {
        const res = await fetch(`/api/tx/${txid}`);
        const data = await res.json();
        
        resultDiv.innerHTML = `
            <div class="result-header">
                <span class="badge">${data.status}</span>
                <span class="wallet-tag">${data.wallet}</span>
            </div>
            <div class="result-msg">${data.message}</div>
            ${data.warning ? `<div class="warning"><i class="fas fa-exclamation-triangle"></i> ${data.warning}</div>` : ''}
            <div class="stats-list" style="margin-top: 10px; font-size: 0.8rem;">
                <div class="list-item">
                    <span>Confirmações</span>
                    <span class="value">${data.confirmations}</span>
                </div>
                <div class="list-item">
                    <span>Idade</span>
                    <span class="value">${data.age_seconds}s</span>
                </div>
            </div>
        `;
        resultDiv.className = `track-result status-${data.status}`;
        
    } catch (e) {
        resultDiv.innerHTML = '<p style="color: var(--danger);">Erro ao buscar transação.</p>';
    }
}

initWallets();
fetchData();
setInterval(fetchData, 5000);
