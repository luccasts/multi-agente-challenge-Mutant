
from typing import Dict, Any
from agents import Message, RouterAgent, BillingAgent, SupportAgent, SentimentAgent
from monitor import REQUESTS, AGENT_HANDOFFS, ROUTER_REQUESTS, log, TurnTimer

class Orchestrator:
    def __init__(self, tools):
        self.router = RouterAgent()
        self.sentiment = SentimentAgent()
        self.billing = BillingAgent(tools)
        self.support = SupportAgent(tools)

    def turn(self, user: str, text: str, meta: Dict[str,str] | None = None) -> Dict[str, Any]:
        timer = TurnTimer()
        msg = Message(user=user, text=text, meta=meta)

        s_reply, s_ctx = self.sentiment.handle(msg)
        log.info("sentiment", reply=s_reply, ctx=s_ctx)

        r_reply, r_ctx = self.router.handle(msg)
        route = r_ctx.get("route","support")
        log.info("route", reply=r_reply, route=route)
        # Incremente o novo contador, usando a rota como rótulo
        ROUTER_REQUESTS.labels(route=route).inc()
        AGENT_HANDOFFS.labels(from_agent="router", to_agent=route).inc()

        #Caminhos do agente  de domínio(billing ou support)
        if route == "billing":
            reply, ctx = self.billing.handle(msg, s_ctx)
            intent = ctx.get("intent","unknown")
            REQUESTS.labels(agent="billing", intent=intent).inc()
            timer.observe()
            return {"agent":"billing","reply":reply,"context":{**s_ctx, **ctx}}
        
        else:
            reply, ctx = self.support.handle(msg, s_ctx)
            intent = ctx.get("intent","unknown")
            REQUESTS.labels(agent="support", intent=intent).inc()
            timer.observe()
            return {"agent":"support","reply":reply,"context":{**s_ctx, **ctx}}
