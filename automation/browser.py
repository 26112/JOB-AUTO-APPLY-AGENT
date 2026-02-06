from playwright.sync_api import sync_playwright
import time
import random


class Browser:
    def __init__(self, headless=False):
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.page = None

    def human_delay(self, min_s=2, max_s=5):
        """
        Sleep for a random amount of time to simulate human behavior.
        """
        delay = random.uniform(min_s, max_s)
        print(f"😴 Waiting for {delay:.2f}s...")
        time.sleep(delay)

    def start(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=self.headless,
            slow_mo=100  # human-like speed
        )
        self.page = self.browser.new_page()
        print("Browser started ✅")

    def open(self, url: str):
        print(f"Opening {url}")
        self.page.goto(url, timeout=60000)
        time.sleep(3)

    def screenshot(self, name="screenshot.png"):
        self.page.screenshot(path=name)
        print(f"Screenshot saved: {name}")

    def stop(self):
        self.browser.close()
        self.playwright.stop()
        print("Browser closed safely 🛑")
