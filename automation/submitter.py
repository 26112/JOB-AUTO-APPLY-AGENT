"""
Application Submitter Module - DAY 18

Handles the final submit button click for job applications.

⚠️ CRITICAL: Only use for one job at a time!
This is the point of no return - once clicked, application is sent.
"""

import time
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def submit_application(page) -> bool:
    """
    Click the submit button to finalize the application.
    
    ⚠️ WARNING: This is the final action - application will be submitted!
    
    Args:
        page: Playwright page object
    
    Returns:
        bool: True if submit button was clicked
    """
    print("🔍 Looking for Submit button...")
    
    # Submit button selectors (in priority order)
    submit_selectors = [
        # Indeed SmartApply specific
        "button:has-text('Submit your application')",
        "button:has-text('Submit application')",
        "button:has-text('Submit Application')",
        
        # Generic submit buttons
        "button:has-text('Submit')",
        "button:has-text('Apply')",
        "button:has-text('Send application')",
        
        # Form submit buttons
        "button[type='submit']",
        "input[type='submit']",
        
        # Continue/Next buttons (for multi-page forms)
        "button:has-text('Continue')",
        "button:has-text('Next')",
        
        # Fallback selectors
        "[data-testid='submit-button']",
        ".ia-SubmitButton"
    ]

    for selector in submit_selectors:
        try:
            btn = page.query_selector(selector)
            if btn and btn.is_visible() and btn.is_enabled():
                button_text = btn.inner_text().strip()
                print(f"   Found button: '{button_text}'")
                
                # Click the submit button
                btn.click()
                time.sleep(5)
                
                print(f"✅ Submit button clicked: '{button_text}'")
                return True
                
        except Exception as e:
            continue

    print("❌ Submit button not found or not clickable")
    return False


def click_continue_buttons(page, max_clicks: int = 3) -> int:
    """
    Click Continue/Next buttons to navigate through multi-page forms.
    
    Args:
        page: Playwright page object
        max_clicks: Maximum number of continue clicks
    
    Returns:
        int: Number of continue buttons clicked
    """
    continue_selectors = [
        "button:has-text('Continue')",
        "button:has-text('Next')",
        "button:has-text('Continue to next step')",
    ]
    
    clicks = 0
    
    for _ in range(max_clicks):
        clicked = False
        
        for selector in continue_selectors:
            try:
                btn = page.query_selector(selector)
                if btn and btn.is_visible() and btn.is_enabled():
                    btn.click()
                    time.sleep(3)
                    clicks += 1
                    clicked = True
                    print(f"   Clicked Continue (#{clicks})")
                    break
            except:
                continue
        
        if not clicked:
            break
    
    return clicks


def confirm_before_submit() -> bool:
    """
    Human confirmation before final submit.
    
    Returns:
        bool: True if user confirms
    """
    print("\n" + "=" * 60)
    print("⚠️  FINAL CONFIRMATION REQUIRED")
    print("=" * 60)
    print("\nYou are about to submit a REAL job application.")
    print("This action CANNOT be undone.")
    print("\nType 'SUBMIT' (all caps) to confirm, or anything else to cancel:")
    
    response = input("\n👉 Your response: ").strip()
    
    if response == "SUBMIT":
        print("\n✅ Confirmed - proceeding with submission...")
        return True
    else:
        print("\n❌ Cancelled - no application submitted")
        return False
