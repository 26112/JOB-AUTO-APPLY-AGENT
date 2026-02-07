import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from automation.browser import Browser

def main():
    print("="*50)
    print("DAY 9 - Login Session Manager")
    print("="*50)
    
    browser = Browser(headless=False)
    browser.start()

    # Default to Indeed, but allow user to change url in code easily
    target_url = "https://www.indeed.com"
    browser.open(target_url)

    print("\n👉 ACTION REQUIRED:")
    print("1. Chrome has opened.")
    print("2. Log in manually to your account (Indeed, LinkedIn, etc).")
    print("3. Handle any CAPTCHAs or OTPs.")
    print("4. Once you are fully logged in and see your dashboard, CLOSE the browser window manually X.")
    print("5. Then press ENTER in this terminal.")

    try:
        input("\nPress ENTER after you have closed the browser...")
    except KeyboardInterrupt:
        print("\nOperation cancelled.")

    browser.stop()
    print("\n✅ Session data saved to data/browser_profile/")
    print("You can run this script again to verify you stay logged in!")


if __name__ == "__main__":
    main()
