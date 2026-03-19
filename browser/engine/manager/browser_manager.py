from playwright.sync_api import Browser
from typing import Dict, Optional
from browser.engine.manager.user_manager import SessionManager


class BrowserManager:
    def __init__(self):
        self.ins: Dict[str, Optional[Browser]] = {}
        self.sessions: Dict[str, Optional[SessionManager]] = {}

    async def ensure_browser():
        pass

    def clear_browser_idle_timer(self):
        if self._idle_task:
            self._idle_task.cancel()
            self._idle_task = None

    def schedule_browser_idle_shutdown(self):
        pass
