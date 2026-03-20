import os
from pathlib import Path
from typing import List
from dotenv import load_dotenv

# Load .env file
load_dotenv()


class FastAPISettings:
    # Project name
    title: str = "SPIDER AGENT"
    # Project description
    description: str = "All free"
    # Project version
    version: str = "0.0.1"
    # Swagger docs URL
    docs_url: str = "/docs"
    # Whether to enable debug mode
    debug: bool = False
    # Whether to automatically reload the project when changes to the project code are detected
    reload_on_file_change: bool = os.getenv("RELOAD_ON_FILE_CHANGE", False)
    # FastAPI service IP
    ip: str = "0.0.0.0"
    # FastAPI service port
    port: int = 80


class LogSettings:
    # Log level
    """
    CRITICAL = 50
    FATAL = CRITICAL
    ERROR = 40
    WARNING = 30
    WARN = WARNING
    INFO = 20
    DEBUG = 10
    NOTSET = 0
    """
    level: int = 10
    #  Log file directory
    log_dir: str = "./log_files"
    #  Log file prefix
    log_file_prefix: str = "app"
    #  Log file encoding
    encoding: str = "utf-8"
    backup_count: int = 7


class HealthCheckSettings:
    router: str = "/health"
    router_tags: List[str] = ["Health-Check"]


class BrowserSettings:
    router: str = "/browser"
    router_tags: List[str] = ["Browser-Driver"]


class AiHelperSettings:
    google_api_key: str = os.getenv("GOOGLE_API_KEY")
    open_api_key: str = os.getenv("OPENAI_API_KEY")


class EngineSettings:
    cookies_dir = os.getenv("CAMOFOX_COOKIES_DIR") or str(
        Path.home() / ".camofox" / "cookies"
    )
    handler_timeout_s = int(os.getenv("HANDLER_TIMEOUT_S", "30"))
    max_concurrent_per_user = int(os.getenv("MAX_CONCURRENT_PER_USER", "3"))
    session_timeout_s = int(os.getenv("SESSION_TIMEOUT_S", "600"))
    tab_inactivity_s = int(os.getenv("TAB_INACTIVITY_S", "300"))
    max_sessions = int(os.getenv("MAX_SESSIONS", "50"))
    max_tabs_per_session = int(os.getenv("MAX_TABS_PER_SESSION", "10"))
    max_tabs_global = int(os.getenv("MAX_TABS_GLOBAL", "10"))
    navigate_timeout_s = int(os.getenv("NAVIGATE_TIMEOUT_S", "25"))
    buildrefs_timeout_s = int(os.getenv("BUILDREFS_TIMEOUT_S", "12"))
    browser_idle_timeout_s = int(os.getenv("BROWSER_IDLE_TIMEOUT_S", "300"))
