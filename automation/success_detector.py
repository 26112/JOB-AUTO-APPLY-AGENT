"""
Success Detector Module - DAY 18

Detects whether a job application was successfully submitted.
Checks page content for confirmation messages.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def detect_success(page) -> dict:
    """
    Detect if the application was successfully submitted.
    
    Checks for common success messages on the page.
    
    Args:
        page: Playwright page object
    
    Returns:
        dict: Result with success status and message
    """
    result = {
        "success": False,
        "confidence": "unknown",
        "message": "",
        "url": page.url
    }
    
    print("🔍 Checking for submission confirmation...")
    
    # Get page content
    try:
        content = page.content().lower()
        page_text = page.inner_text("body").lower() if page.query_selector("body") else content
    except:
        content = ""
        page_text = ""
    
    # Success indicators (high confidence)
    high_confidence_texts = [
        "application submitted",
        "application has been submitted",
        "thank you for applying",
        "thanks for applying",
        "application received",
        "we received your application",
        "application complete",
        "you have applied",
        "successfully applied",
        "application sent"
    ]
    
    for text in high_confidence_texts:
        if text in page_text or text in content:
            result["success"] = True
            result["confidence"] = "high"
            result["message"] = f"Confirmed: '{text}' found on page"
            print(f"🎉 Application submission confirmed!")
            print(f"   Detection: '{text}'")
            return result
    
    # Medium confidence indicators
    medium_confidence_texts = [
        "thank you",
        "we'll be in touch",
        "next steps",
        "what happens next",
        "confirmation"
    ]
    
    for text in medium_confidence_texts:
        if text in page_text:
            result["success"] = True
            result["confidence"] = "medium"
            result["message"] = f"Likely success: '{text}' found on page"
            print(f"✅ Application likely submitted")
            print(f"   Detection: '{text}'")
            return result
    
    # Check URL for success indicators
    current_url = page.url.lower()
    url_success_indicators = [
        "success",
        "confirmation",
        "applied",
        "complete",
        "thank"
    ]
    
    for indicator in url_success_indicators:
        if indicator in current_url:
            result["success"] = True
            result["confidence"] = "medium"
            result["message"] = f"URL indicates success: '{indicator}' in URL"
            print(f"✅ URL suggests successful submission")
            return result
    
    # No clear confirmation found
    result["message"] = "No clear confirmation found - may need manual verification"
    print("⚠️ Submission confirmation not clearly detected")
    print("   You may need to check your email or Indeed account")
    
    return result


def take_confirmation_screenshot(page, job_title: str = "job") -> str:
    """
    Take a screenshot of the confirmation page.
    
    Args:
        page: Playwright page object
        job_title: Job title for filename
    
    Returns:
        str: Path to screenshot
    """
    import re
    from datetime import datetime
    
    # Clean job title for filename
    clean_title = re.sub(r'[^\w\s-]', '', job_title)[:30].strip().replace(' ', '_')
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    filename = f"data/confirmation_{clean_title}_{timestamp}.png"
    
    try:
        page.screenshot(path=filename)
        print(f"📸 Confirmation screenshot saved: {filename}")
        return filename
    except Exception as e:
        print(f"⚠️ Could not save screenshot: {e}")
        return ""
