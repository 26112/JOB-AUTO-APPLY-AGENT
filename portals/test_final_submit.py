"""
Final Submit Test - DAY 18

⚠️ CRITICAL: This script will submit ONE real job application!

This is the first full autonomous application.
Human confirmation is REQUIRED before submission.

Steps:
1. Opens the first job from apply_queue.json
2. Goes through full application flow
3. Asks for FINAL CONFIRMATION
4. Clicks Submit
5. Detects success
6. Logs to memory and CSV/Sheets

🛑 DO NOT RUN IN A LOOP - ONE JOB ONLY
"""

import sys
from pathlib import Path
import json
import time

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from automation.browser import Browser
from portals.indeed_apply import open_job, click_apply, detect_application_state, get_page_screenshot
from automation.form_inspector import inspect_form_fields
from automation.form_filler import autofill_personal_info
from automation.file_uploader import handle_resume_upload
from automation.cover_letter_handler import handle_cover_letter_any_method
from automation.question_answerer import answer_standard_questions
from automation.submitter import submit_application, click_continue_buttons, confirm_before_submit
from automation.success_detector import detect_success, take_confirmation_screenshot
from app_logging.memory import mark_job_applied, is_job_applied, print_application_summary
from app_logging.sheets_logger import log_application


# ============================================================
# CONFIGURATION
# ============================================================

# Google Sheet URL (optional - leave empty if not using)
SHEET_URL = ""  # Paste your Google Sheet URL here if you have one

# Get first job from apply queue
def get_test_job():
    queue_path = Path("data/apply_queue.json")
    if not queue_path.exists():
        print("❌ apply_queue.json not found. Run Day 12 evaluation first.")
        return None
    
    jobs = json.load(open(queue_path, encoding="utf-8"))
    if not jobs:
        print("❌ apply_queue.json is empty. No jobs to apply to.")
        return None
    
    # Get first job that hasn't been applied to
    for job in jobs:
        if not is_job_applied(job.get("url", "")):
            return job
    
    print("ℹ️ All jobs in queue have already been applied to.")
    return None


def main():
    print("=" * 60)
    print("🔴 DAY 18: FINAL SUBMIT (ONE JOB ONLY)")
    print("=" * 60)
    
    # Get job to apply
    job = get_test_job()
    if not job:
        return
    
    print(f"\n📋 Job to Apply:")
    print(f"   Title: {job.get('job_title', 'Unknown')}")
    print(f"   Company: {job.get('company', 'Unknown')}")
    print(f"   Location: {job.get('location', 'Unknown')}")
    print(f"   URL: {job.get('url', '')[:60]}...")
    
    # Load resume profile
    resume = json.load(open("data/resume_profile.json", encoding="utf-8"))
    
    print("\n" + "⚠️ " * 20)
    print("\n   THIS WILL SUBMIT A REAL APPLICATION")
    print("   ARE YOU ABSOLUTELY SURE?")
    print("\n" + "⚠️ " * 20)
    
    input("\n👉 Press ENTER to proceed to application flow (you'll confirm again before submit)...")
    
    # Start browser
    print("\n🌐 Starting browser...")
    browser = Browser(headless=False)
    browser.start()
    
    application_result = {
        "job": job,
        "steps_completed": [],
        "submitted": False,
        "success_detected": False,
        "logged": False
    }
    
    try:
        # Step 1: Open job page
        print("\n" + "-" * 40)
        print("STEP 1: Opening job page")
        print("-" * 40)
        open_job(browser.page, job["url"])
        application_result["steps_completed"].append("job_opened")
        
        # Step 2: Click Apply
        print("\n" + "-" * 40)
        print("STEP 2: Clicking Apply button")
        print("-" * 40)
        clicked = click_apply(browser.page)
        
        if not clicked:
            print("❌ Could not find Apply button. Stopping.")
            get_page_screenshot(browser.page, "error_no_apply_button.png")
            return
        
        application_result["steps_completed"].append("apply_clicked")
        browser.human_delay(3, 5)
        
        # Step 3: Handle multi-page forms (Continue buttons)
        print("\n" + "-" * 40)
        print("STEP 3: Navigating application form")
        print("-" * 40)
        
        # Detect and fill each page
        max_pages = 5
        for page_num in range(max_pages):
            print(f"\n   📄 Processing page {page_num + 1}...")
            
            # Inspect form fields
            fields = inspect_form_fields(browser.page)
            print(f"      Fields detected: {len(fields)}")
            
            # Auto-fill personal info
            filled = autofill_personal_info(browser.page, resume)
            if filled:
                print(f"      Auto-filled: {', '.join(filled)}")
            
            # Handle resume upload
            upload_result = handle_resume_upload(browser.page)
            if upload_result["success"]:
                print(f"      Resume: {upload_result['method']}")
            
            # Handle cover letter
            cl_result = handle_cover_letter_any_method(browser.page)
            if cl_result["success"]:
                print(f"      Cover letter: {cl_result['method']}")
            
            # Answer questions
            answered = answer_standard_questions(browser.page)
            if answered:
                print(f"      Questions answered: {len(answered)}")
            
            browser.human_delay(1, 2)
            
            # Try to click Continue/Next
            continues = click_continue_buttons(browser.page, max_clicks=1)
            if continues == 0:
                print("      No more Continue buttons - likely at final page")
                break
            
            browser.human_delay(2, 3)
        
        application_result["steps_completed"].append("form_completed")
        
        # Take screenshot before submit
        get_page_screenshot(browser.page, "before_submit.png")
        
        # ========================================
        # FINAL CONFIRMATION
        # ========================================
        print("\n" + "=" * 60)
        print("📋 PRE-SUBMISSION SUMMARY")
        print("=" * 60)
        print(f"   Job: {job.get('job_title', 'Unknown')}")
        print(f"   Company: {job.get('company', 'Unknown')}")
        print(f"   Steps completed: {', '.join(application_result['steps_completed'])}")
        
        if not confirm_before_submit():
            print("\n❌ Submission cancelled by user")
            return
        
        # Step 4: SUBMIT APPLICATION
        print("\n" + "-" * 40)
        print("STEP 4: SUBMITTING APPLICATION")
        print("-" * 40)
        
        submitted = submit_application(browser.page)
        application_result["submitted"] = submitted
        
        if submitted:
            browser.human_delay(3, 5)
            
            # Step 5: Detect success
            print("\n" + "-" * 40)
            print("STEP 5: Checking submission status")
            print("-" * 40)
            
            success_result = detect_success(browser.page)
            application_result["success_detected"] = success_result["success"]
            
            # Take confirmation screenshot
            screenshot = take_confirmation_screenshot(browser.page, job.get("job_title", "job"))
            
            # Step 6: Log application
            print("\n" + "-" * 40)
            print("STEP 6: Logging application")
            print("-" * 40)
            
            # Mark as applied in memory
            mark_job_applied(job["url"], job, "APPLIED")
            
            # Log to CSV/Sheets
            log_results = log_application(job, SHEET_URL if SHEET_URL else None)
            application_result["logged"] = log_results["csv"]
            
            # ========================================
            # FINAL RESULT
            # ========================================
            print("\n" + "=" * 60)
            if success_result["success"]:
                print("🎉 APPLICATION SUBMITTED SUCCESSFULLY!")
            else:
                print("✅ APPLICATION SUBMITTED (confirmation unclear)")
            print("=" * 60)
            
            print(f"\n📊 Final Summary:")
            print(f"   ├─ Job: {job.get('job_title', 'Unknown')}")
            print(f"   ├─ Company: {job.get('company', 'Unknown')}")
            print(f"   ├─ Submitted: ✅")
            print(f"   ├─ Confirmation: {success_result['confidence']}")
            print(f"   ├─ Logged to memory: ✅")
            print(f"   └─ Logged to CSV: {'✅' if log_results['csv'] else '❌'}")
            
        else:
            print("❌ Submit button not found or could not be clicked")
            get_page_screenshot(browser.page, "error_submit_failed.png")
        
        # Print application summary
        print_application_summary()
        
        # Wait for user to review
        print("\n" + "-" * 40)
        input("👉 Review the result. Press ENTER to close browser...")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        get_page_screenshot(browser.page, "error_state.png")
    finally:
        print("\n🔒 Closing browser...")
        browser.stop()
    
    # Save application result
    with open("data/last_application_result.json", "w", encoding="utf-8") as f:
        # Convert job object to make it JSON serializable
        result_to_save = application_result.copy()
        result_to_save["job"] = {
            "job_title": job.get("job_title"),
            "company": job.get("company"),
            "url": job.get("url")
        }
        json.dump(result_to_save, f, indent=2)
    
    print("\n" + "=" * 60)
    print("✅ DAY 18 Complete!")
    print("   First autonomous application finished.")
    print("=" * 60)


if __name__ == "__main__":
    main()
