from playwright.sync_api import sync_playwright
import time
from pathlib import Path
import random


class Browser:
    def __init__(self, headless=False):
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.page = None
        self.user_data_dir = Path("data/browser_profile")

    def start(self):
        self.playwright = sync_playwright().start()

        # Use launch_persistent_context to maintain login state
        self.browser = self.playwright.chromium.launch_persistent_context(
            user_data_dir=str(self.user_data_dir),
            headless=self.headless,
            slow_mo=100,
            # Common arguments to avoid detection and improve stability
            args=[
                "--disable-blink-features=AutomationControlled", 
                "--start-maximized"
            ]
        )

        self.page = self.browser.pages[0] if self.browser.pages else self.browser.new_page()
        print("Persistent browser started ✅")

    def open(self, url: str):
        print(f"Opening {url}")
        try:
            self.page.goto(url, timeout=60000)
            time.sleep(3)
        except Exception as e:
            print(f"⚠️ Error opening {url}: {e}")

    def screenshot(self, name="screenshot.png"):
        try:
            self.page.screenshot(path=name)
            print(f"Screenshot saved: {name}")
        except Exception as e:
            print(f"⚠️ Screenshot failed: {e}")

    def human_delay(self, min_s=2, max_s=5):
        """
        Sleep for a random amount of time to simulate human behavior.
        """
        delay = random.uniform(min_s, max_s)
        print(f"😴 Waiting for {delay:.2f}s...")
        time.sleep(delay)

    def stop(self):
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        print("Browser closed (session saved) 💾")
