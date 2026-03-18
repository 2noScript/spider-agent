import time
import os
import threading
from enum import Enum
from typing import Dict, Any, Optional

from pydantic import BaseModel, Field
from playwright.sync_api import sync_playwright


# ==============================
# Session Mode
# ==============================

class SessionMode(str, Enum):
    NEW_BROWSER = "new_browser"
    REUSE = "reuse"
    PROFILE = "profile"


# ==============================
# Pydantic Models (DATA ONLY)
# ==============================

class RefItem(BaseModel):
    role: Optional[str] = None
    name: Optional[str] = None
    nth: Optional[int] = None


class TabState(BaseModel):
    refs: Dict[str, RefItem] = Field(default_factory=dict)
    visited_urls: set[str] = Field(default_factory=set)
    downloads: list[dict] = Field(default_factory=list)
    tool_calls: int = 0


# ==============================
# Runtime Layer (Playwright)
# ==============================

class TabRuntime:
    def __init__(self, page):
        self.page = page


class Tab:
    def __init__(self, page):
        self.runtime = TabRuntime(page)
        self.state = TabState()


# ==============================
# User Session
# ==============================

class UserSession:
    def __init__(self, context, browser, mode: SessionMode):
        self.context = context
        self.browser = browser
        self.mode = mode

        # sessionKey -> tabId -> Tab
        self.tab_groups: Dict[str, Dict[str, Tab]] = {}

        self.last_access = time.time()
        self.lock = threading.Lock()


# ==============================
# Browser Manager
# ==============================

class BrowserManager:
    def __init__(self):
        self.playwright = sync_playwright().start()
        self.browser_pool = {}
        self.lock = threading.Lock()

    def _build_proxy(self, proxy: Optional[str]):
        if not proxy:
            return None
        return {"server": proxy}

    def create_context(self, mode: SessionMode, proxy=None, profile_dir=None):
        if mode == SessionMode.NEW_BROWSER:
            browser = self.playwright.chromium.launch(
                headless=False,
                proxy=self._build_proxy(proxy)
            )
            context = browser.new_context()
            return context, browser

        elif mode == SessionMode.REUSE:
            key = proxy or "default"

            with self.lock:
                if key not in self.browser_pool:
                    browser = self.playwright.chromium.launch(
                        headless=False,
                        proxy=self._build_proxy(proxy)
                    )
                    self.browser_pool[key] = browser
                else:
                    browser = self.browser_pool[key]

            context = browser.new_context()
            return context, None

        elif mode == SessionMode.PROFILE:
            if not profile_dir:
                raise ValueError("profile_dir required")

            os.makedirs(profile_dir, exist_ok=True)

            context = self.playwright.chromium.launch_persistent_context(
                user_data_dir=profile_dir,
                headless=False,
                proxy=self._build_proxy(proxy)
            )
            return context, None

    def shutdown(self):
        for browser in self.browser_pool.values():
            try:
                browser.close()
            except:
                pass
        self.playwright.stop()


# ==============================
# Session Store
# ==============================

class SessionStore:
    def __init__(self, browser_manager: BrowserManager):
        self.sessions: Dict[str, UserSession] = {}
        self.lock = threading.Lock()
        self.browser_manager = browser_manager

    def normalize_session_key(self, session_key=None, list_item_id=None):
        return str(session_key or list_item_id or "default")

    # ==========================
    # Create User
    # ==========================
    def create_user(self, user_id: str, mode: SessionMode, proxy=None, profile_dir=None):
        context, browser = self.browser_manager.create_context(
            mode, proxy, profile_dir
        )

        user = UserSession(context, browser, mode)

        with self.lock:
            self.sessions[user_id] = user

        return user

    # ==========================
    # Get or Create Tab
    # ==========================
    def get_or_create_tab(
        self,
        user_id: str,
        tab_id: str,
        session_key=None,
        list_item_id=None
    ) -> Tab:
        user = self.sessions.get(user_id)
        if not user:
            raise ValueError("User not found")

        session_key = self.normalize_session_key(session_key, list_item_id)

        with user.lock:
            if session_key not in user.tab_groups:
                user.tab_groups[session_key] = {}

            group = user.tab_groups[session_key]

            if tab_id not in group:
                page = user.context.new_page()
                group[tab_id] = Tab(page)

            user.last_access = time.time()

            return group[tab_id]

    # ==========================
    # Remove Tab
    # ==========================
    def remove_tab(self, user_id: str, tab_id: str, session_key=None):
        user = self.sessions.get(user_id)
        if not user:
            return

        session_key = self.normalize_session_key(session_key)

        with user.lock:
            group = user.tab_groups.get(session_key)
            if not group:
                return

            tab = group.pop(tab_id, None)

            if tab:
                try:
                    tab.runtime.page.close()
                except:
                    pass

            if not group:
                user.tab_groups.pop(session_key, None)

    # ==========================
    # Close User
    # ==========================
    def close_user(self, user_id: str):
        user = self.sessions.pop(user_id, None)
        if not user:
            return

        try:
            user.context.close()
        except:
            pass

        if user.mode == SessionMode.NEW_BROWSER and user.browser:
            try:
                user.browser.close()
            except:
                pass

    # ==========================
    # Cleanup Idle Users
    # ==========================
    def start_cleanup(self, timeout=600, interval=60):
        def loop():
            while True:
                time.sleep(interval)
                now = time.time()
                to_remove = []

                with self.lock:
                    users = list(self.sessions.items())

                for user_id, user in users:
                    with user.lock:
                        if now - user.last_access > timeout:
                            print(f"[CLEANUP] {user_id}")
                            to_remove.append(user_id)

                for user_id in to_remove:
                    self.close_user(user_id)

        threading.Thread(target=loop, daemon=True).start()


# ==============================
# Example Usage
# ==============================

if __name__ == "__main__":
    bm = BrowserManager()
    store = SessionStore(bm)

    store.start_cleanup(timeout=300)

    store.create_user(
        user_id="user1",
        mode=SessionMode.REUSE
    )

    tab = store.get_or_create_tab(
        user_id="user1",
        tab_id="tab1",
        session_key="group1"
    )

    tab.runtime.page.goto("https://bot.sannysoft.com")

    # update state
    tab.state.visited_urls.add("https://bot.sannysoft.com")
    tab.state.tool_calls += 1

    print(tab.state.model_dump())

    input("Press Enter to exit...")

    store.close_user("user1")
    bm.shutdown()