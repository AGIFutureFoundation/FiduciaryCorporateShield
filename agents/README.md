# agents/

This directory contains minimal Agent interface and an example agent.

Usage (local):
1. Create and activate a virtualenv:
   python -m venv .venv
   source .venv/bin/activate

2. Install dependencies:
   pip install -r requirements.txt

3. Run the API:
   python -m api.main

Endpoints:
- GET /health
- GET /agents
- POST /agents/{agent_name}/run
  Body: {"input": "text"}
  Response: For the example EchoAgent -> {"output": "...", "reversed": "...", "meta": {...}}

Notes:
- Replace EchoAgent with a real LLM-backed agent by implementing the Agent interface.
- Keep secrets out of code; integrate remote LLMs via environment variables or secret managers.
