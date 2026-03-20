import re

from browser.engine.core.enum import BrowserType

ALLOWED_URL_SCHEMES = ["http:", "https:"]

INTERACTIVE_ROLES = [
    "button",
    "link",
    "textbox",
    "checkbox",
    "radio",
    "menuitem",
    "tab",
    "searchbox",
    "slider",
    "spinbutton",
    "switch",
]

SKIP_PATTERNS = [
    re.compile(r"date", re.I),
    re.compile(r"calendar", re.I),
    re.compile(r"picker", re.I),
    re.compile(r"datepicker", re.I),
]

SUPPORT_BROWSER = [BrowserType.CAMOUFOX]

PROFILES_PATH = {
    BrowserType.CAMOUFOX: f"profile/{BrowserType.CAMOUFOX}",
    BrowserType.CLOAK: f"profile/{BrowserType.CLOAK}",
}

BROWSER_IDLE_TIMEOUT_S = 300
PAGE_CLOSE_TIMEOUT_S = 5

