from automation.browser import Browser
import os


def main():
    print("Testing Browser Automation...")
    
    # Ensure data directory exists for screenshot
    if not os.path.exists("data"):
        os.makedirs("data")

    browser = Browser(headless=False)
    browser.start()

    browser.open("https://example.com")
    browser.screenshot("data/example.png")

    browser.stop()
    print("Test Completed Successfully ✅")


if __name__ == "__main__":
    main()
