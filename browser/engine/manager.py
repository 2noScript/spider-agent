from typing import Any, Dict, Optional
import threading
import time
from playwright.sync_api import sync_playwright
from browser.engine.enum import SessionMode, BrowserType
from browser.engine.models import UserSessionModel
from camoufox.sync_api import Camoufox


class SessionStore:
    def __init__(self, session_timeout: int = 3600):
        self.users: Dict[str, UserSessionModel] = {}
        self.lock = threading.Lock()
        self.session_timeout = session_timeout

    def create_user(self, user_id: str, context: Any) -> UserSessionModel:
        with self.lock:
            session = UserSessionModel(context=context)
            self.users[user_id] = session
            return session

    def get_user(self, user_id: str) -> Optional[UserSessionModel]:
        session = self.users.get(user_id)
        if session:
            session.touch()
        return session

    def cleanup(self):
        now = time.time()
        with self.lock:
            to_remove = [
                uid
                for uid, session in self.users.items()
                if now - session.last_access > self.session_timeout
            ]
            for uid in to_remove:
                sess = self.users.pop(uid)
                try:
                    if hasattr(sess.context, "close"):
                        sess.context.close()
                    elif Camoufox and isinstance(sess.context, Camoufox):
                        sess.context.close()
                except Exception:
                    pass


class BrowserManager:
    def __init__(self):
        self.playwright = sync_playwright().start()
        self.browser_pool: Dict[tuple, Any] = (
            {}
        )  # (browser_type, proxy) -> browser_instance
        self.lock = threading.Lock()

    def _launch_browser(self, browser_type: BrowserType, proxy: Optional[str] = None):
        proxy_config = {"server": proxy} if proxy else None

        if browser_type == BrowserType.CAMOUFOX:
            if not Camoufox:
                raise RuntimeError("Camoufox not installed")
            return Camoufox()
        else:
            raise ValueError(f"Unsupported browser type: {browser_type}")

    def create_context(
        self,
        mode: SessionMode,
        browser_type: BrowserType = BrowserType.CHROMIUM,
        proxy: Optional[str] = None,
        profile_dir: Optional[str] = None,
    ):
        key = (browser_type, proxy or "default")
        with self.lock:
            browser = self.browser_pool.get(key)
            if not browser:
                browser = self._launch_browser(browser_type, proxy)
                self.browser_pool[key] = browser

        # Create context
        if mode == SessionMode.PROFILE and profile_dir:
            if hasattr(browser, "launch_persistent_context"):
                return (
                    browser.launch_persistent_context(user_data_dir=profile_dir),
                    browser,
                )
            else:
                return browser.new_context(), browser
        else:
            if hasattr(browser, "new_context"):
                return browser.new_context(), browser
            else:
                return browser, browser  # Camoufox fallback

    def close_all(self):
        with self.lock:
            for browser in self.browser_pool.values():
                try:
                    if hasattr(browser, "close"):
                        browser.close()
                except Exception:
                    pass
            self.browser_pool.clear()
            self.playwright.stop()


# ------------------------------
# EXAMPLE USAGE
# ------------------------------
if __name__ == "__main__":
    store = SessionStore(session_timeout=60 * 5)  # 5 minutes
    manager = BrowserManager()

    # Create a user with a new Chromium browser context
    context, browser = manager.create_context(
        mode=SessionMode.NEW_BROWSER, browser_type=BrowserType.CHROMIUM
    )
    user_session = store.create_user("user1", context)

    # Open a new tab
    page = context.new_page()
    page.goto("https://example.com")
    user_session.add_tab("default", "tab1", page)

    print("User session created and page opened.")

    # Wait and cleanup inactive sessions
    time.sleep(10)
    store.cleanup()

    # Close all browsers on exit
    manager.close_all()
