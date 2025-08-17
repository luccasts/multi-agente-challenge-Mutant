
from dataclasses import dataclass
from typing import Dict, Tuple
from llm import humanize_reply

@dataclass
class Message:
    user: str
    text: str
    meta: Dict[str, str] | None = None

class BaseAgent:
    name: str = "base"
    def handle(self, msg: Message) -> Tuple[str, Dict]:
        raise NotImplementedError

class SentimentAgent(BaseAgent):
    name = "sentiment"
    def handle(self, msg: Message) -> Tuple[str, Dict]:
        #adição sentimentos sem acento 
        frustrated = any(w in msg.text.lower() for w in ["não aguento", "ridículo", "pior", "horrível","angry","raiva", "nao aguento", "horrivel", "ridiculo"])
        sentiment = "negative" if frustrated else "neutral"
        reply = "Registro de sentimento: " + sentiment
        return reply, {"sentiment": sentiment}

class BillingAgent(BaseAgent):
    name = "billing"
    def __init__(self, tools):
        self.tools = tools
    def handle(self, msg: Message, s_ctx: Dict) -> Tuple[str, Dict]:
        customer = (msg.meta or {}).get("customer", "alice")
        balance_res = self.tools.call("get_balance", customer=customer)
        if not balance_res.get("ok"):
            base = "Não encontrei seu cadastro. Pode confirmar seu nome completo e CPF?"
            return humanize_reply(self.name, "billing_check", base, {**s_ctx, **{"customer": customer}}), {"intent":"billing_check"}
        balance = balance_res["balance"]
        if balance < 0:
            base = f"Você possui um débito de R${abs(balance):.2f}. Posso oferecer parcelamento em 3x sem juros."
            return humanize_reply(self.name, "billing_debt", base, {**s_ctx, **{"balance": balance}}), {"intent":"billing_debt","balance":balance}
        else:
            base = "Seu saldo está em dia. Posso ajudar com mais alguma coisa?"
            return humanize_reply(self.name, "billing_ok", base, {**s_ctx, **{"balance": balance}}), {"intent":"billing_ok","balance":balance}

class SupportAgent(BaseAgent):
    name = "support"
    def __init__(self, tools):
        self.tools = tools
    def handle(self, msg: Message, s_ctx: Dict) -> Tuple[str, Dict]:
        t = msg.text.lower()
        if "segunda via" in t or "2ª via" in t or "boleto" in t:
            email_res = self.tools.call("send_email", to="user@example.com", subject="2ª via", body="Segue sua 2ª via.")
            if email_res.get("ok"):
                base = "Enviei a 2ª via para seu e-mail cadastrado. Se precisar, eu te ajudo a localizar."
                return humanize_reply(self.name, "send_duplicate", base, s_ctx), {"intent":"send_duplicate"}
        
        base = "Pode descrever seu problema com mais detalhes? Assim eu direciono corretamente."
        return humanize_reply(self.name, "support_followup", base, s_ctx), {"intent":"support_followup"}

class RouterAgent(BaseAgent):
    name = "router"
   
    
    def handle(self, msg: Message) -> Tuple[str, Dict]:
        t = msg.text.lower()
        billing_keywords = [
        "boleto", "cobran", "fatura", "parcel", "saldo", "conta", "pagar"
        ]  
        suport_keywords = [
            "suporte", "problem", "erro", "segunda via", "atendimento", "problem 2 via", "ajuda", "não funciona", "nao funciona"
        ]
        if any(k in t for k in billing_keywords):
            return "Encaminhando para cobrança…", {"route":"billing"}
        elif any(k in t for k in suport_keywords):
            return "Encaminhando para suporte…", {"route":"support"}
        else: 
           return "Não entendi sua solicitação.", {"route": "support"}
