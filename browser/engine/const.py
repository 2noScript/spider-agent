import re

from browser.engine.enum import BrowserType

ALLOWED_URL_SCHEMES = ["http:", "https:"]

# Interactive roles to include - exclude combobox to avoid opening complex widgets
INTERACTIVE_ROLES = [
    "button", "link", "textbox", "checkbox", "radio",
    "menuitem", "tab", "searchbox", "slider", "spinbutton", "switch"
    # "combobox" excluded
]

# Patterns to skip (date pickers, calendar widgets)
SKIP_PATTERNS = [
    re.compile(r"date", re.I),
    re.compile(r"calendar", re.I),
    re.compile(r"picker", re.I),
    re.compile(r"datepicker", re.I),
]

BROWSER_IDLE_TIMEOUT_MS=300000

SUPPORT_BROWSER=[BrowserType.CAMOUFOX]