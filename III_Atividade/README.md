# CoreCraft | Bitcoin Snapshot

**III_Atividade** é um dashboard inteligente e interativo para monitoramento e interação com o **Bitcoin Core**. Desenvolvido para a Mentoria Aula 03, o sistema evoluiu de um simples visualizador para uma aplicação robusta orientada a serviços, capaz de gerenciar múltiplas wallets e interpretar o estado da rede em tempo real.

![Dashboard Preview](https://img.shields.io/badge/Bitcoin-Node_Insight-orange?style=for-the-badge&logo=bitcoin)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![ZMQ](https://img.shields.io/badge/ZeroMQ-Distributed-blue?style=for-the-badge&logo=zeromq)

## Funcionalidades Principais

### 1. Gestão de Múltiplas Wallets

- **Seleção Dinâmica:** Liste, carregue (`loadwallet`) e alterne entre diferentes wallets do Bitcoin Core diretamente pela interface.
- **Estado em Tempo Real:** Visualize saldo, quantidade de UTXOs e o contexto da wallet ativa.
- **Envio Direto:** Realize transações de envio de BTC (`sendtoaddress`) com feedback imediato de sucesso e TXID.

### 2. Monitoramento de Eventos (ZMQ)

- **Baixa Latência:** Captura instantânea de novas transações e blocos via ZeroMQ.
- **Cálculo de TXID Inteligente:** Sistema capaz de derivar o TXID real a partir de dados brutos (`rawtx`) usando hashing SHA-256 duplo.
- **Histórico Vivo:** Lista persistente dos últimos eventos detectados na rede.

### 3. Inteligência de Mempool & Sync

- **Análise de Fees:** Distribuição de taxas em categorias (Baixa, Média, Alta) e cálculo de média de sat/vB.
- **Lag de Sincronização:** Monitoramento visual da diferença entre blocos processados e headers sincronizados.

### 4. Interpretação de Transações

- **Camada de Tradução:** Converte estados crus do Bitcoin Core em mensagens amigáveis (Broadcast, Mempool, Confirmada).
- **Rastreamento Manual:** Insira qualquer TXID para obter uma análise instantânea do status e avisos de latência.

## Tecnologias Utilizadas

- **Backend:** FastAPI (Python) - Arquitetura orientada a serviços.
- **Comunicação Node:** RPC (JSON-RPC) e ZMQ (ZeroMQ).
- **Frontend:** Vanilla HTML5, CSS3 (Glassmorphism UI) e JavaScript (Async/Await).
- **Segurança:** Autenticação básica via RPC e isolamento de serviços.

## Como Executar

### Pré-requisitos

- **Bitcoin Core** instalado e rodando.
- **Python 3.10+** instalado.
- **Dependências Python:** `pip install fastapi uvicorn requests pyzmq pydantic`

### Configuração do Bitcoin Core (`bitcoin.conf`)

Certifique-se de que o seu node permite conexões RPC e envia eventos ZMQ:

```text
server=1
rpcuser=bitcoin
rpcpassword=sua_senha_aqui
rpcport=38332
zmqpubhashtx=tcp://127.0.0.1:28332
zmqpubhashblock=tcp://127.0.0.1:28332
```

### Execução

1. Clone o repositório.
2. Configure as credenciais no arquivo `bitcoin_rpc.py`.
3. Inicie o servidor:

   ```bash
   python main.py
   ```

4. Acesse no navegador: `http://localhost:8000`

---
