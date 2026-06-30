# Template Runpod integration for inference via HTTP.
# Uses httpx for async HTTP calls. Expects RUNPOD_API_KEY and RUNPOD_MODEL_ID
# in environment variables. This file is intentionally minimal — adapt to your
# Runpod model input/output schema.

import os
from typing import Dict, Any, Optional

import httpx

RUNPOD_API_KEY = os.getenv("RUNPOD_API_KEY")
RUNPOD_MODEL_ID = os.getenv("RUNPOD_MODEL_ID")  # e.g. "rp-model-xxxx"

RUNPOD_BASE = "https://api.runpod.io/v2"

class RunpodClient:
    def __init__(self, api_key: Optional[str] = None, model_id: Optional[str] = None):
        self.api_key = api_key or RUNPOD_API_KEY
        self.model_id = model_id or RUNPOD_MODEL_ID
        if not self.api_key or not self.model_id:
            raise ValueError("RUNPOD_API_KEY and RUNPOD_MODEL_ID must be set in the environment")

    async def infer(self, prompt: str, timeout: int = 60) -> Dict[str, Any]:
        """
        Call Runpod inference endpoint for the configured model.
        Adapt the request payload to the model's expected schema.
        """
        url = f"{RUNPOD_BASE}/pods/{self.model_id}/infer"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        json_payload = {
            "input": prompt,
            # Add model-specific fields here if required
        }

        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.post(url, headers=headers, json=json_payload)
            resp.raise_for_status()
            return resp.json()
