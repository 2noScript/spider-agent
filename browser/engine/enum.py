from enum import Enum

class BrowserType(str, Enum):
    CAMOUFOX = "camoufox"
    CHROMIUM = "chromium"
    FIREFOX = "firefox"
    WEBKIT = "webkit"

class SessionMode(str, Enum):
    NEW_BROWSER = "new_browser"
    REUSE = "reuse"
    PROFILE = "profile"

