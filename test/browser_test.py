from camoufox.sync_api import Camoufox
import time

with Camoufox() as browser:
    page = browser.new_page()
    page.goto("https://www.tiktok.com/@2noscript?lang=en")
    time.sleep(3000)