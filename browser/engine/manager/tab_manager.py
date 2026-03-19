from typing import Dict, Set

from playwright.sync_api import Page


class TabManager:
    def __init__(self, page: Page, refs: Dict[str, dict], visited_urls: Set[str]):
        self.page = page
        self.refs = refs
        self.visited_urls = visited_urls
        self.downloads = []
        self.tool_calls = 0
