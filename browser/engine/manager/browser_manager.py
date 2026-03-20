import asyncio
from playwright.sync_api import Browser, BrowserContext
from typing import Dict, Optional, Union
from browser.engine.enum import BrowserType
from browser.engine.manager.user_manager import UserManager
import os
import signal


class BrowserManager:
    def __init__(self):
        # 1.(REUSE)
        self.shared_browsers: Dict[BrowserType, Browser] = {}
        # 2. (NEW_BROWSER + PROFILE)
        self.user_browsers: Dict[str, Browser] = {}
        self.users: Dict[str, Optional[UserManager]] = {}

    async def ensure_browser():
        pass

    def clear_browser_idle_timer(self):
        if self._idle_task:
            self._idle_task.cancel()
            self._idle_task = None

    def schedule_browser_idle_shutdown(self):
        pass

    async def safe_browser_close(target: Union[Browser, BrowserContext]):
        """
        target: browser or context (async Playwright)
        timeout: number of seconds to wait
        """
        try:
            await asyncio.wait_for(target.close(), timeout=5)
            print("[safe_close] Closed gracefully")

        except asyncio.TimeoutError:
            print("[safe_close] Timeout → force kill")
            try:
                pid = None
                if isinstance(target, Browser):
                    pid = target.process.pid
                elif isinstance(target, BrowserContext):
                    browser = target._browser
                    if browser and browser.process:
                        pid = browser.process.pid
                os.kill(pid, signal.SIGKILL)

            except Exception as e:
                print("[safe_close] Kill failed:", e)

        except Exception as e:
            print("[safe_close] Close error:", e)


browser_manager = BrowserManager()
