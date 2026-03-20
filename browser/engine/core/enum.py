from enum import Enum


class BrowserType(str, Enum):
    CAMOUFOX = "camoufox"
    CLOAK = "cloak"


class UserMode(str, Enum):
    NEW_BROWSER = "new_browser"
    REUSE = "reuse"
    PROFILE = "profile"


class SessionMode(str, Enum):
    NEW_BROWSER = "new_browser"
    REUSE = "reuse"
    PROFILE = "profile"

