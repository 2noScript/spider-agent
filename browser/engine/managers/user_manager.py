import time
from typing import Dict, List

from playwright.sync_api import BrowserContext

from browser.engine.core.enum import UserMode
from browser.engine.managers.tab_manager import TabManager


class UserManager:
    def __init__(
        self,
        mode: UserMode,
        browser_id: str,
        context: BrowserContext,
        cookies: List[str],
    ):
        self.mode = mode
        self.browser_id = browser_id
        self.context = context
        self.last_access = time.time()
        self.cookies = cookies
        self.tab_group: Dict[str, Dict[str, TabManager]] = {}

