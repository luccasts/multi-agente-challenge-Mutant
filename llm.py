
import os
import google.generativeai as genai

_MODEL = "gemini-1.5-flash"

def _client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY não definido no ambiente.")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(model_name=_MODEL)

def humanize_reply(agent: str, intent: str, raw_message: str, ctx: dict) -> str:
    content = f"""
    Você é um assistente conversacional educado e conciso, falando PT-BR.
    Limite: 1 a 3 frases.
    Agente: {agent}
    Intenção: {intent}
    Resposta-base (para reescrever de modo humano): {raw_message}
    Contexto adicional: {ctx} 
    Regras: empático, claro, proponha próximo passo simples. Se o sentimento no contexto for 'negative', use um tom mais empático e tranquilizador.
    """
    #Implementação de uma regra mais abrangente.
    model = _client()
    out = model.generate_content(content)
    return (out.text or raw_message).strip()
