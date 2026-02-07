"""
Indeed Auto-Apply Module - DAY 13

⚠️ SAFETY FIRST:
- Opens job page
- Clicks Apply button
- Handles redirects
- STOPS before final submission

This is read-only automation + controlled click.
"""

import time
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def open_job(page, job_url: str):
    """
    Open a job posting page.
    
    Args:
        page: Playwright page object
        job_url: URL of the job to open
    """
    print(f"📄 Opening job: {job_url[:60]}...")
    page.goto(job_url, timeout=60000)
    time.sleep(5)
    print("   Page loaded ✅")


def click_apply(page):
    """
    Find and click the Apply button on Indeed job page.
    
    Handles multiple button variants:
    - Apply now
    - Apply on company site
    - Easy Apply
    
    Args:
        page: Playwright page object
    
    Returns:
        bool: True if Apply button was clicked
    """
    print("🔍 Looking for Apply button...")

    # Indeed Apply button selectors (in priority order)
    apply_selectors = [
        # Indeed Easy Apply buttons
        "button#indeedApplyButton",
        "button[id*='indeedApply']",
        "button.jobsearch-IndeedApplyButton-contentWrapper",
        
        # Standard Apply buttons  
        "button:has-text('Apply now')",
        "button:has-text('Apply Now')",
        "a:has-text('Apply now')",
        "a:has-text('Apply Now')",
        
        # Generic Apply buttons
        "button:has-text('Apply')",
        "a:has-text('Apply')",
        
        # Apply on company site
        "button:has-text('Apply on company site')",
        "a:has-text('Apply on company site')",
        
        # Fallback selectors
        "[data-testid='indeedApplyButton']",
        ".jobsearch-IndeedApplyButton-newDesign",
        "button.ia-IndeedApplyButton"
    ]

    for selector in apply_selectors:
        try:
            button = page.query_selector(selector)
            if button and button.is_visible():
                button_text = button.inner_text().strip()
                print(f"   Found button: '{button_text}'")
                button.click()
                time.sleep(5)
                print("   Apply button clicked ✅")
                return True
        except Exception as e:
            continue

    print("   ❌ Apply button not found")
    return False


def detect_application_state(page):
    """
    Detect what state we're in after clicking Apply.
    
    Returns:
        str: One of 'modal', 'redirect', 'form', 'unknown'
    """
    print("🔍 Detecting application state...")
    
    current_url = page.url
    
    # Check if redirected to external site
    if "indeed.com" not in current_url:
        print(f"   Redirected to company site: {current_url[:50]}...")
        return "redirect"
    
    # Check for Indeed Easy Apply modal
    modal_selectors = [
        ".indeed-apply-widget",
        "[class*='IndeedApply']",
        ".ia-Modal",
        "[role='dialog']",
        ".icl-Modal"
    ]
    
    for selector in modal_selectors:
        try:
            modal = page.query_selector(selector)
            if modal and modal.is_visible():
                print("   Indeed Easy Apply modal detected")
                return "modal"
        except:
            continue
    
    # Check for form elements
    form_selectors = [
        "input[type='email']",
        "input[type='text']",
        "textarea",
        "input[type='file']"
    ]
    
    for selector in form_selectors:
        try:
            form_element = page.query_selector(selector)
            if form_element and form_element.is_visible():
                print("   Application form detected")
                return "form"
        except:
            continue
    
    print("   State unknown - may need manual inspection")
    return "unknown"


def get_page_screenshot(page, name="apply_state.png"):
    """
    Take a screenshot for verification.
    """
    try:
        page.screenshot(path=f"data/{name}")
        print(f"   📸 Screenshot saved: data/{name}")
    except Exception as e:
        print(f"   ⚠️ Screenshot failed: {e}")
