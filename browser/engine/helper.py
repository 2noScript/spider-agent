import sys
from browser.logging import configure_logging
import asyncio


logger = configure_logging(name=__name__)


def get_host_os():
    platform = sys.platform
    if platform == "darwin":
        return "macos"
    if platform == "win32":
        return "windows"
    return "linux"


def build_proxy_config(config):
    proxy = config.get("proxy", {})

    host = proxy.get("host")
    port = proxy.get("port")
    username = proxy.get("username")
    password = proxy.get("password")

    if not host or not port:
        logger.info("no proxy configured")
        return None

    logger.info("info", "proxy configured", {"host": host, "port": port})

    return {
        "server": f"http://{host}:{port}",
        "username": username,
        "password": password,
    }





async def with_timeout(coro, ms: int, label: str):
    try:
        return await asyncio.wait_for(coro, timeout=ms / 1000)
    except asyncio.TimeoutError:
        raise Exception(f"{label} timed out after {ms}ms")