from camoufox.sync_api import Camoufox
import time

with Camoufox() as browser:
    # Create 2 isolated contexts
    context1 = browser.new_context()
    context2 = browser.new_context()

    # Create pages in each context
    page1 = context1.new_page()
    page2 = context2.new_page()

    # Open fingerprint test site
    test_url = "https://bot.sannysoft.com/"

    page1.goto(test_url)
    page2.goto(test_url)

    print("Opened 2 contexts. Compare fingerprints manually.")

    # Keep browser open (3000 seconds ≈ 50 minutes)
    time.sleep(3000)