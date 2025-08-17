
from fastapi import FastAPI
from pydantic import BaseModel
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Response as FResponse
from pathlib import Path

from mcp_tools import MCPRegistry
from orchestrator import Orchestrator

class ChatIn(BaseModel):
    user: str = "user"
    text: str
    meta: dict | None = None

tools = MCPRegistry()
orch = Orchestrator(tools)

app = FastAPI(title="AI Multi-Agent + Gemini Chat")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/public", StaticFiles(directory="public"), name="public")

@app.get("/", response_class=HTMLResponse)
def index():
    with open("public/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/chat")
def chat(inp: ChatIn):
    out = orch.turn(inp.user, inp.text, inp.meta)
    return out

@app.get("/metrics")
def metrics():
    data = generate_latest()
    return FResponse(content=data, media_type=CONTENT_TYPE_LATEST)

@app.get("/public/logo-mutant")
def logo_mutant():
    png = Path("assets/mutant.png").read_bytes()
    return FResponse(content=png, media_type="image/png")

@app.get("/public/logo-unirios")
def logo_unirios():
    png = Path("assets/unirios.png").read_bytes()
    return FResponse(content=png, media_type="image/png")
