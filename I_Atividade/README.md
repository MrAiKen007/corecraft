# CoreCraft - Snapshot Inteligente (Aula 01)

Este projeto é uma evolução da Aula 1, transformando dados brutos do Bitcoin Core em informações interpretadas através de uma primeira camada de inteligência.

## Funcionalidades
- **Mempool Intelligence**: Analisa a mempool e classifica transações por níveis de taxa (Low, Medium, High).
- **Node Sync Status**: Calcula o lag entre headers e blocos processados.
- **API REST**: Implementada com FastAPI.
- **Interface Premium**: Dashboard moderno com Glassmorphism e atualizações em tempo real.

## Como Executar

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

2. Certifique-se de que seu Bitcoin Core está rodando (Regtest ou Mainnet) com RPC habilitado.

3. Inicie o servidor:
   ```bash
   python main.py
   ```

4. Acesse: [http://localhost:8000](http://localhost:8000)
