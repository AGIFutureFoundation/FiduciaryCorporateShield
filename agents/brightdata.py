# Brightdata proxy helper. This simple helper configures requests/httpx to
# use a Brightdata proxy. You can provide BRIGHTDATA_PROXY as a full proxy URL
# (including credentials), or provide username/password/host/port variants.

import os
from typing import Optional
import httpx
import requests

BRIGHTDATA_PROXY = os.getenv("BRIGHTDATA_PROXY")  # e.g. "http://user:pass@proxy.brighthost:22225"

def requests_session_with_brightdata(proxy_url: Optional[str] = None) -> requests.Session:
    """
    Returns a requests.Session that routes traffic through Brightdata proxy.
    """
    proxy = proxy_url or BRIGHTDATA_PROXY
    session = requests.Session()
    if proxy:
        session.proxies = {"http": proxy, "https": proxy}
    return session

def httpx_client_with_brightdata(proxy_url: Optional[str] = None, timeout: int = 30) -> httpx.Client:
    """
    Returns an httpx.Client configured to use the Brightdata proxy.
    Note: For httpx, we set 'proxies' mapping.
    """
    proxy = proxy_url or BRIGHTDATA_PROXY
    if proxy:
        proxies = {
            "http://": proxy,
            "https://": proxy,
        }
        return httpx.Client(proxies=proxies, timeout=timeout)
    return httpx.Client(timeout=timeout)
