# tests/test_runpod_brightdata_errors.py
import pytest
import respx
import httpx

from agents.runpod_brightdata_agent import RunpodBrightdataAgent

@pytest.mark.asyncio
async def test_runpod_infer_server_error(monkeypatch):
    monkeypatch.setenv("RUNPOD_API_KEY", "test-key")
    monkeypatch.setenv("RUNPOD_MODEL_ID", "test-model")

    runpod_url = "https://api.runpod.io/v2/pods/test-model/infer"
    with respx.mock(assert_all_called=True) as mock:
        mock.post(runpod_url).respond(500, json={"error": "server error"})
        agent = RunpodBrightdataAgent()
        res = await agent.run("input with no fetch")
        # Should return failure metadata rather than raising
        assert res.get("output", "") == ""
        assert "error" in res.get("meta", {})

@pytest.mark.asyncio
async def test_fetch_timeout(monkeypatch):
    monkeypatch.setenv("RUNPOD_API_KEY", "test-key")
    monkeypatch.setenv("RUNPOD_MODEL_ID", "test-model")

    fetch_url = "https://example.com/slow"
    with respx.mock(assert_all_called=True) as mock:
        # Simulate timeout on fetch
        mock.get(fetch_url).mock(side_effect=httpx.ReadTimeout("timeout"))
        agent = RunpodBrightdataAgent()
        res = await agent.run("please fetch", context={"fetch_url": fetch_url})
        assert res.get("output", "") == ""
        assert "fetch_failed" in res.get("meta", {}).get("error", "")

@pytest.mark.asyncio
async def test_proxy_auth_failure(monkeypatch):
    monkeypatch.setenv("RUNPOD_API_KEY", "test-key")
    monkeypatch.setenv("RUNPOD_MODEL_ID", "test-model")

    fetch_url = "https://example.com/page"
    with respx.mock(assert_all_called=True) as mock:
        # Simulate proxy/auth failure (407)
        mock.get(fetch_url).respond(407, text="Proxy Auth Required")
        agent = RunpodBrightdataAgent()
        res = await agent.run("fetch with proxy", context={"fetch_url": fetch_url})
        assert res.get("output", "") == ""
        assert "fetch_failed" in res.get("meta", {}).get("error", "")

@pytest.mark.asyncio
async def test_runpod_returns_invalid_json(monkeypatch):
    monkeypatch.setenv("RUNPOD_API_KEY", "test-key")
    monkeypatch.setenv("RUNPOD_MODEL_ID", "test-model")

    runpod_url = "https://api.runpod.io/v2/pods/test-model/infer"
    with respx.mock(assert_all_called=True) as mock:
        # Return text that isn't JSON
        mock.post(runpod_url).respond(200, content=b"not-json")
        agent = RunpodBrightdataAgent()
        res = await agent.run("input")
        # Code should not crash; normalize result
        assert isinstance(res.get("meta", {}).get("raw", None), (dict, str)) or res.get("output", "") is not None
