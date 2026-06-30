# Runpod + Brightdata integration guide

This document describes the template integration files included in the scaffold and how to adapt them to your accounts.

Files:
- agents/runpod_agent.py — lightweight client for Runpod inference API.
- agents/brightdata.py — proxy helpers for Brightdata.
- agents/runpod_brightdata_agent.py — example Agent combining both parts.

Setup:
1. Obtain a Runpod API key and a model/pod id. Put them into environment variables:
   export RUNPOD_API_KEY=sk-...
   export RUNPOD_MODEL_ID=rp-model-...

2. (Optional) Configure Brightdata proxy:
   export BRIGHTDATA_PROXY="http://user:pass@proxy.brighthost:22225"

3. Run the API locally:
   uvicorn api.main:app --reload --port 8000

Adapting to your model:
- Runpod models can expect different request payloads. Inspect your model docs and adapt RunpodClient.infer() payload and response parsing.
- Add streaming or chunked response handling if your model supports streaming.

CI and Secrets:
- In CI, add RUNPOD_API_KEY and BRIGHTDATA_PROXY as repository secrets and avoid printing them in logs.
- For tests, prefer mocking Runpod/HTTP responses instead of real network calls. The scaffold includes a simple unit test for the EchoAgent as an example.

Notes:
- Brightdata proxy usage may have legal/usage constraints. Ensure scraping or data retrieval complies with target site terms and privacy requirements.
- For heavy production use, add retry/backoff, circuit breakers, rate limiting, and observability (tracing/metrics).
