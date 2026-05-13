# CoreCraft | Bitcoin Event Monitor (Aula 02) 🚀

Este projeto é uma evolução do monitor de estado do Bitcoin Core. Ele combina dados estáticos via **RPC** com um fluxo de eventos em tempo real via **ZMQ**, criando um painel inteligente que observa a rede Bitcoin de forma dinâmica.

## Objetivos da Atividade
- **Monitoramento em Tempo Real**: Capturar eventos de novos blocos (`hashblock`) e transações (`rawtx`) via ZeroMQ.
- **Processamento Orientado a Eventos**: Estruturar os dados recebidos em memória utilizando filas limitadas (`deque`).
- **Comparação de Estado**: Identificar divergências entre o que o nó reporta via RPC (`getbestblockhash`) e o que foi observado no fluxo ZMQ.
- **Acessibilidade Externa**: Disponibilizar a aplicação via internet utilizando túneis seguros.

## Tecnologias Utilizadas
- **Backend**: Python + FastAPI (Assíncrono)
- **Mensageria**: ZeroMQ (ZMQ) para eventos do Bitcoin Core
- **Comunicação**: JSON-RPC para consulta de estado
- **Frontend**: HTML5, CSS3 (Glassmorphism) e JavaScript Vanilla
- **Túnel**: Cloudflare Tunnel (`cloudflared`)

## Funcionalidades Implementadas

### 1. Camada de Eventos (Backend)
- Registro automático de eventos ZMQ em estruturas de dados `deque`.
- Mantém os últimos 10 blocos e as últimas 50 transações em memória.
- Cálculo de taxa de eventos (Transações por Segundo - TPS).

### 2. Endpoints da API
- `GET /api/events/summary`: Retorna estatísticas resumidas da atividade ZMQ.
- `GET /api/events/latest`: Lista os hashes dos blocos e transações mais recentes.
- `GET /api/events/state-comparison`: Compara o estado do RPC com o ZMQ para detectar lags.
- `GET /api/mempool/summary`: Resumo da mempool (legado Aula 01).
- `GET /api/blockchain/lag`: Status de sincronização do nó (legado Aula 01).

### 3. Painel Visual (Frontend)
- **Atividade de Eventos**: Card dinâmico com contagem de eventos e TPS.
- **Últimos Eventos**: Lista em tempo real com scroll para acompanhar o fluxo da rede.
- **Indicador de Divergência**: Alerta visual proeminente que aparece caso o ZMQ e o RPC percam a sincronia.

## Como Executar

### Pré-requisitos
1.  **Bitcoin Core** rodando com as seguintes configurações no `bitcoin.conf`:
    ```ini
    server=1
    zmqpubrawtx=tcp://127.0.0.1:28332
    zmqpubhashblock=tcp://127.0.0.1:28332
    ```
2.  **Dependências do Python**:
    ```bash
    pip install fastapi uvicorn pyzmq requests
    ```

### Execução Local
1.  Navegue até a pasta:
    ```bash
    cd II_Atividade
    ```
2.  Inicie o servidor:
    ```bash
    python main.py
    ```
3.  Acesse: `http://localhost:8000`

### Acesso Externo (Cloudflare Tunnel)
Para disponibilizar o painel na internet:
```bash
cloudflared tunnel --url http://localhost:8000
```
