# 🤖 Atendimento Conversacional Inteligente

### Projeto de Desafio para a Mutant

Este kit oferece **duas frentes de frontend** para você escolher:

- **Web Chat (FastAPI + HTML/JS)** em `/` (como no kit anterior)
- **Chat em Streamlit** (`streamlit_app.py`) com logos da **Mutant** e **UniRios**

Inclui também: **multiagentes**, **MCP** (SQLite + email fake), **Gemini Flash** para respostas humanizadas e **métricas Prometheus**.

---

### 🏛️ Arquitetura e Componentes

A arquitetura é composta pelos seguintes elementos:

- **Orquestrador (`orchestrator.py`):** Atua como a "cola" do sistema, controlando o fluxo da conversa. Ele executa os agentes em sequência: Sentimento → Roteamento → Agente de Domínio.
- **Agentes:**
  - `SentimentAgent`: Analisa o sentimento do usuário (negativo ou neutro) com base em palavras-chave.
  - `RouterAgent`: Encaminha a mensagem para o agente de domínio correto (`Billing` ou `Support`) com base em palavras-chave.
  - `BillingAgent`: Lida com questões de cobrança, consultando o saldo via MCP e tratando erros de cliente não encontrado.
  - `SupportAgent`: Lida com questões de suporte, como o envio de 2ª via de boleto via MCP.
- **Métricas (`monitor.py`):** Utiliza Prometheus para expor métricas de contagem de requisições, handoffs e latência, garantindo a observabilidade completa do sistema.
- **MCP (`mcp_tools.py`):** Simula a consulta a um banco de dados (SQLite) e o envio de e-mails, funcionando como um "cérebro" para as ações dos agentes.
- **LLM (`llm.py`):** Utiliza o modelo Gemini Flash para humanizar as respostas geradas pelos agentes, tornando a conversa mais natural e empática, especialmente ao lidar com sentimentos negativos.

---

### ⚙️ Requisitos

- Python 3.10+
- API Key do Gemini (Google AI Studio): defina `GEMINI_API_KEY` no ambiente.

### 📥 Instalação

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export GEMINI_API_KEY="<SUA_CHAVE_AQUI>"            # PowerShell: $env:GEMINI_API_KEY="<SUA_CHAVE_AQUI>"
```

## Executar a API (com web chat e métricas)

```bash
uvicorn main:app --reload
# Chat web: http://127.0.0.1:8000
# Métricas: http://127.0.0.1:8000/metrics
```

## Executar o Chat em Streamlit

```bash
streamlit run streamlit_app.py
# A página abrirá no navegador com as logos Mutant e UniRios
```

## Estrutura

```
.
├── agents.py
├── orchestrator.py
├── mcp_tools.py
├── monitor.py
├── llm.py
├── main.py                 # API FastAPI + web chat (pasta public/)
├── public/
│   └── index.html
├── streamlit_app.py        # Chat Streamlit com logos
├── assets/
│   ├── mutant.png
│   └── unirios.png
├── requirements.txt
└── README.md
```

---

#### Cenário 1: Consulta de Fatura com Tratamento de Erro

- **Prompt do usuário:** `Qual o meu saldo, por favor?`
- **O que acontece:** O `RouterAgent` direciona a conversa para o `BillingAgent`, que consulta o saldo da cliente "alice". O sistema retorna o valor correto.
- **Captura de tela:**
  ![Exemplo de consulta de fatura](https://i.imgur.com/HtaTMuI.png)

- **Prompt do usuário:** `Eu queria saber o saldo da Ana.`
- **O que acontece:** O `BillingAgent` tenta consultar a conta "Lucas", mas o MCP não a encontra. O sistema trata o erro e pede para que o usuário confirme os dados.
- **Captura de tela:**
  ![Exemplo de tratamento de erro](https://i.imgur.com/RqoEFAi.png)

#### Cenário 2: Envio de 2ª Via do Boleto

- **Prompt do usuário:** `Estou com raiva, me mande a 2ª via da minha fatura!`
- **O que acontece:** O `SentimentAgent` detecta o sentimento negativo. O `RouterAgent` direciona a conversa para o `SupportAgent`, que "envia" a 2ª via. A resposta é humanizada pelo Gemini para ser mais empática e tranquilizadora.
- **Captura de tela:**
  ![Exemplo de resposta empática](https://i.imgur.com/HEgSkU2.png)

#### Cenário 3: Observabilidade com Métricas Prometheus

- **Como acessar:** Enquanto o Streamlit está rodando, abra uma nova aba do navegador em: `http://localhost:8000/metrics`
- **O que você verá:** Um dashboard com as métricas do sistema.
- **Captura de tela:**
  ![Exemplo do dashboard de métricas](https://i.imgur.com/JGxtaxg.png)
  _Os contadores `chat_requests_total`, `agent_handoffs_total` e `router_requests_total` estarão preenchidos com os dados das suas interações._

---

### 📹 Vídeo de Demonstração

Assista a um tour completo pelo projeto e veja as métricas em ação.

- **Link do Vídeo:** <LINK_DO_YOUTUBE>
