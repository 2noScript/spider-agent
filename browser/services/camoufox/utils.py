from urllib.parse import urlparse
from browser.logging import configure_logging


logger = configure_logging(name=__name__)

def build_proxy_config(proxy_str: str):
    """
    Build Playwright proxy config from a proxy string.

    Supported formats:
    - http://user:pass@host:port
    - http://host:port
    - socks5://host:port
    - host:port (default to http)
    """

    if not proxy_str:
        logger.info("no proxy configured")
        return None

    # Add default scheme if missing
    if "://" not in proxy_str:
        proxy_str = f"http://{proxy_str}"

    parsed = urlparse(proxy_str)

    host = parsed.hostname
    port = parsed.port
    username = parsed.username
    password = parsed.password
    scheme = parsed.scheme or "http"

    if not host or not port:
        logger.info("invalid proxy format")
        return None

    logger.info("proxy configured", {"host": host, "port": port})

    return {
        "server": f"{scheme}://{host}:{port}",
        "username": username,
        "password": password,
    }