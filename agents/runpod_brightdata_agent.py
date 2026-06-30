# Example Agent that uses Runpod for model inference and Brightdata for optional web
# retrieval when the agent needs to fetch external content before calling the model.

from typing import Dict, Any, Optional
from .agent_base import Agent
from .runpod_agent import RunpodClient
from .brightdata import async_httpx_client_with_brightdata

class RunpodBrightdataAgent(Agent):
    @property
    def name(self) -> str:
        return "runpod_brightdata"

    async def _fetch_with_proxy(self, url: str) -> str:
        """
        Fetches a URL using Brightdata proxy (if configured). Returns raw text.
        """
        # use async client configured for proxy
        async with async_httpx_client_with_brightdata() as client:
            resp = await client.get(url)
            resp.raise_for_status()
            return resp.text

    async def run(self, input: str, context: Dict[str, Any] | None = None) -> Dict[str, Any]:
        """
        Example flow:
        - optional: if 'fetch_url' present in context, fetch content via Brightdata proxy
        - build a prompt combining input + fetched content
        - call Runpod model with prompt
        - return normalized output
        """
        rp = RunpodClient()
        fetch_url = (context or {}).get("fetch_url")
        fetched = ""
        if fetch_url:
            try:
                fetched = await self._fetch_with_proxy(fetch_url)
            except Exception as e:
                # return partial failure metadata — caller can decide retry/backoff
                return {"output": "", "meta": {"error": f"fetch_failed: {str(e)}"}}

        prompt_pieces = [f"User input:\n{input}"]
        if fetched:
            prompt_pieces.append(f"\nFetched content:\n{fetched[:40_000]}")  # limit safety
        prompt = "\n\n".join(prompt_pieces)

        # Call Runpod inference
        try:
            result = await rp.infer(prompt)
        except Exception as e:
            return {"output": "", "meta": {"error": f"runpod_infer_failed: {str(e)}"}}

        # Normalize: many Runpod models return a dict with 'output' or 'response'
        # adapt this to your model's actual return shape
        text = ""
        if isinstance(result, dict):
            text = result.get("output") or result.get("response") or result.get("result") or str(result)
        else:
            text = str(result)

        return {"output": text, "meta": {"raw": result}}
