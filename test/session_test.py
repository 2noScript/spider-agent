from browser.engine.enum import SessionMode
from browser.engine.session import SessionManager


manager = SessionManager()

# 🥇 new browser 
s1 = manager.create_session(
    SessionMode.NEW_BROWSER,
    proxy="http://127.0.0.1:8080"
)

# 🥈 reuse 
s2 = manager.create_session(SessionMode.REUSE)

# 🥉 profile 
s3 = manager.create_session(
    SessionMode.PROFILE,
    profile_dir="./profiles/user1"
)

page = manager.get_page(s1)
page.goto("https://bot.sannysoft.com")

input("Press Enter to close...")

manager.shutdown()