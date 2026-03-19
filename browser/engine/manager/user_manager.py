import time

from playwright.sync_api import Browser, BrowserContext
from typing import Dict, List, Optional
from browser.engine.enum import UserMode
from browser.engine.manager.tab_manager import TabManager

# UserManager
# ├── mode: UserMode
# ├── browser_id: str
# ├── context: BrowserContext
# ├── last_access: float
# ├── cookies: List[str]
# └── tab_group: Dict[str, Dict[str, TabManager]]
#      ├── sessionKey_1
#      │    ├── tabId_1 → TabManager
#      │    ├── tabId_2 → TabManager
#      │    └── tabId_3 → TabManager
#      │
#      ├── sessionKey_2
#      │    ├── tabId_1 → TabManager
#      │    └── tabId_2 → TabManager
#      │
#      └── sessionKey_3
#           └── tabId_1 → TabManager

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
        self.tab_group: Dict[str,Dict[str,TabManager]]
        
