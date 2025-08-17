
from prometheus_client import Counter, Histogram
import time
import structlog
import logging
import sys

REQUESTS = Counter("chat_requests_total", "Total chat requests", ["agent", "intent"])
AGENT_HANDOFFS = Counter("agent_handoffs_total", "Agent handoffs between roles", ["from_agent","to_agent"])
LATENCY = Histogram("turn_latency_seconds", "Latency per turn", buckets=(0.05,0.1,0.25,0.5,1,2,5))
# Contador para requisições do roteador, com o rótulo da rota
ROUTER_REQUESTS = Counter("router_requests_total", "Total requests processed by the router", ["route"])
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
log = structlog.get_logger()

class TurnTimer:
    def __init__(self):
        self.start = time.perf_counter()
    def observe(self):
        LATENCY.observe(time.perf_counter() - self.start)
