from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
import uvicorn

from agents import EchoAgent  # simple example; additional agents can be registered

app = FastAPI(title="FiduciaryCorporateShield Agents API", version="0.1.0")

# Simple in-memory registry
AGENTS: Dict[str, object] = {
    "echo": EchoAgent(),
}

class RunRequest(BaseModel):
    input: str

class RunResponse(BaseModel):
    output: str
    reversed: str
    meta: dict

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/agents")
async def list_agents():
    return {"agents": list(AGENTS.keys())}

@app.post("/agents/{agent_name}/run", response_model=RunResponse)
async def run_agent(agent_name: str, req: RunRequest):
    agent = AGENTS.get(agent_name)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    result = await agent.run(req.input)
    # Normalize result into expected RunResponse fields for this simple example
    return {"output": result.get("output", ""), "reversed": result.get("reversed", ""), "meta": result.get("meta", {})}

if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, log_level="info")
