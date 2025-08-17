
import streamlit as st
from orchestrator import Orchestrator
from mcp_tools import MCPRegistry

st.set_page_config(page_title="Mutant x UniRios — Chat Multi-Agente", page_icon="🤖", layout="wide")

col1, col2, col3 = st.columns([1,1,6])
with col1:
    st.image("public/assets/mutant.png", use_column_width=True)
with col2:
    st.image("public/assets/unirios.png", use_column_width=True)
with col3:
    st.markdown("### Atendimento • Multi-Agente + Gemini\n##### Router → Billing/Support • MCP • Métricas")

st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = [{"role":"assistant","content":"Olá! Posso ajudar com sua fatura ou enviar a 2ª via do boleto."}]

tools = MCPRegistry()
orch = Orchestrator(tools)

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

prompt = st.chat_input("Digite sua mensagem...")
if prompt:
    st.session_state.messages.append({"role":"user","content":prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    out = orch.turn(user="user", text=prompt, meta={"customer":"alice"})
    reply = out.get("reply","(sem resposta)")
    agent = out.get("agent","?")
    with st.chat_message("assistant"):
        st.markdown(f"{reply}\n\n`[agente: {agent}]`")
    st.session_state.messages.append({"role":"assistant","content":f"{reply}\n\n`[agente: {agent}]`"})
