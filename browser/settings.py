import os
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
    router_tags: List[str] = ["Browser"]