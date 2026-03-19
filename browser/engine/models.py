from pydantic import BaseModel, Field
from typing import Any, Dict, Set, List, Optional
from enum import Enum
import threading
import time
from playwright.sync_api import Page

class TabStateModel(BaseModel):
    page: Page
    refs: Dict[str, dict] = Field(default_factory=dict)
    visited_urls: Set[str] = Field(default_factory=set)
    downloads: List[dict] = Field(default_factory=list)
    tool_calls: int = 0

    class Config:
        arbitrary_types_allowed = True

class UserSessionModel(BaseModel):
    context: Any
    tab_groups: Dict[str, Dict[str, TabStateModel]] = Field(default_factory=dict)
    last_access: float = Field(default_factory=lambda: time.time())
    _lock: threading.Lock = Field(default_factory=threading.Lock, exclude=True)

    class Config:
        arbitrary_types_allowed = True

    def touch(self):
        self.last_access = time.time()

    def add_tab(self, session_key: str, tab_id: str, page: Page):
        with self._lock:
            if session_key not in self.tab_groups:
                self.tab_groups[session_key] = {}
            self.tab_groups[session_key][tab_id] = TabStateModel(page=page)

    def get_tab(self, session_key: str, tab_id: str) -> Optional[TabStateModel]:
        return self.tab_groups.get(session_key, {}).get(tab_id)