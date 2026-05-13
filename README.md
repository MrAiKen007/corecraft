# Evolução do Dashboard Bitcoin Node Insight

Este repositório documenta a trajetória de desenvolvimento do sistema de monitoramento e interação com o Bitcoin Core, dividida em três atividades principais de evolução técnica.

## Estrutura das Atividades

### [I_Atividade](./I_Atividade) - Fundação e Integração RPC
A primeira etapa focou na comunicação básica com o protocolo JSON-RPC do Bitcoin Core.
- **Conectividade:** Implementação da camada inicial de requisições RPC.
- **Dashboard Base:** Interface simples para exibição de informações do estado da blockchain (blocks, headers, chain).
- **Integração:** Backend em Python consumindo dados diretamente do Node.

### [II_Atividade](./II_Atividade) - Monitoramento em Tempo Real (ZMQ)
A segunda etapa introduziu a reatividade ao sistema, utilizando o protocolo ZeroMQ para capturar eventos da rede sem necessidade de polling constante.
- **ZMQ Integration:** Assinatura de tópicos `hashtx` e `hashblock`.
- **Inteligência de Mempool:** Análise de ocupação (vsize) e cálculo de taxas (fees) dinâmicas.
- **Dashboards Dinâmicos:** Exibição de listas em tempo real das últimas transações e blocos minerados.

### [III_Atividade](./III_Atividade) - Arquitetura de Serviços e Gestão de Wallets
A etapa final e mais avançada, transformando o projeto em uma aplicação modular e interativa.
- **SOA (Service-Oriented Architecture):** Refatoração da lógica para serviços independentes (`tx_service`, `wallet_service`, `zmq_service`).
- **Gestão Multi-Wallet:** Sistema completo para listar, carregar e selecionar dinamicamente diferentes wallets do Node.
- **Terminal de Transações:** Implementação de formulário para envio de Bitcoin (`sendtoaddress`) diretamente pela interface.
- **Interpretação Inteligente:** Camada de tradução de estados técnicos para mensagens legíveis (Broadcast -> Mempool -> Confirmed).
- **Cálculo de Hash Real:** Sistema robusto para derivar o TXID real a partir de dados brutos (`rawtx`), garantindo precisão no rastreamento.

---
*Repositório focado no aprendizado prático de desenvolvimento sobre o Bitcoin Core.*