# Brightdata proxy helper (async + sync helpers).
import os
from typing import Optional
import httpx
import requests

BRIGHTDATA_PROXY = os.getenv("BRIGHTDATA_PROXY")  # e.g. "http://user:pass@proxy.brighthost:22225"

def requests_session_with_brightdata(proxy_url: Optional[str] = None) -> requests.Session:
    proxy = proxy_url or BRIGHTDATA_PROXY
    session = requests.Session()
    if proxy:
        session.proxies = {"http": proxy, "https": proxy}
    return session

def async_httpx_client_with_brightdata(proxy_url: Optional[str] = None, timeout: int = 30) -> httpx.AsyncClient:
    """
    Returns an httpx.AsyncClient configured to use the Brightdata proxy.
    Use this in async code paths (async with ...).
    """
    proxy = proxy_url or BRIGHTDATA_PROXY
    if proxy:
        proxies = {
            "http://": proxy,
            "https://": proxy,
        }
        return httpx.AsyncClient(proxies=proxies, timeout=timeout)
    return httpx.AsyncClient(timeout=timeout)
