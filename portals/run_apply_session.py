"""
Multi-Job Apply Session Runner - DAY 19

Applies to multiple jobs in a controlled, safe manner.

Features:
- Rate limiting between applications
- Duplicate detection
- Session limits
- Human confirmation for each job
- Session summary

⚠️ SAFE LIMITS: Max 3 jobs per session by default
"""

import sys
from pathlib import Path
import json
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from automation.browser import Browser
from automation.rate_limiter import human_pause, quick_pause, should_take_break, long_break, SessionLimiter
from portals.indeed_apply import open_job, click_apply, detect_application_state
from automation.form_inspector import inspect_form_fields
from automation.form_filler import autofill_personal_info
from automation.file_uploader import handle_resume_upload
from automation.cover_letter_handler import handle_cover_letter_any_method
from automation.question_answerer import answer_standard_questions
from automation.submitter import submit_application, click_continue_buttons
from automation.success_detector import detect_success, take_confirmation_screenshot
from app_logging.memory import mark_job_applied, is_job_applied, print_application_summary
from app_logging.sheets_logger import log_application


# ============================================================
# 🔒 CONFIGURATION - SAFE LIMITS
# ============================================================

MAX_PER_SESSION = 3      # Maximum jobs to apply per session (start low!)
CONFIRM_EACH_JOB = True  # Require confirmation for each application
SHEET_URL = ""           # Optional Google Sheet URL


def load_apply_queue() -> list:
    """Load jobs from apply queue."""
    queue_path = Path("data/apply_queue.json")
    if not queue_path.exists():
        return []
    return json.load(open(queue_path, encoding="utf-8"))


def load_resume() -> dict:
    """Load resume profile."""
    return json.load(open("data/resume_profile.json", encoding="utf-8"))


def apply_to_job(browser, job: dict, resume: dict, job_num: int) -> dict:
    """
    Apply to a single job.
    
    Returns:
        dict: Result with success status
    """
    result = {
        "job": job,
        "success": False,
        "submitted": False,
        "reason": ""
    }
    
    try:
        # Step 1: Open job
        print(f"\n📄 Opening job page...")
        open_job(browser.page, job["url"])
        quick_pause(2, 3)
        
        # Step 2: Click Apply
        print("🔍 Looking for Apply button...")
        clicked = click_apply(browser.page)
        
        if not clicked:
            result["reason"] = "Apply button not found"
            return result
        
        quick_pause(3, 5)
        
        # Step 3: Process form pages
        max_pages = 5
        for page_num in range(max_pages):
            # Detect form fields
            fields = inspect_form_fields(browser.page)
            
            # Auto-fill
            filled = autofill_personal_info(browser.page, resume)
            
            # Resume upload
            handle_resume_upload(browser.page)
            
            # Cover letter
            handle_cover_letter_any_method(browser.page)
            
            # Answer questions
            answer_standard_questions(browser.page)
            
            quick_pause(1, 2)
            
            # Try Continue button
            continues = click_continue_buttons(browser.page, max_clicks=1)
            if continues == 0:
                break
            
            quick_pause(2, 3)
        
        # Step 4: Submit
        print("🚀 Submitting application...")
        submitted = submit_application(browser.page)
        result["submitted"] = submitted
        
        if submitted:
            quick_pause(3, 5)
            
            # Check success
            success_result = detect_success(browser.page)
            result["success"] = success_result["success"]
            
            if success_result["success"]:
                result["reason"] = "Application submitted successfully"
                take_confirmation_screenshot(browser.page, job.get("job_title", "job"))
            else:
                result["reason"] = "Submitted but confirmation unclear"
        else:
            result["reason"] = "Submit button not found"
        
        return result
        
    except Exception as e:
        result["reason"] = f"Error: {str(e)}"
        return result


def main():
    print("=" * 60)
    print("🚀 DAY 19: Multi-Job Apply Session")
    print("=" * 60)
    
    # Load jobs
    jobs = load_apply_queue()
    if not jobs:
        print("❌ No jobs in apply queue. Run Day 12 evaluation first.")
        return
    
    resume = load_resume()
    
    # Filter out already applied jobs
    pending_jobs = [j for j in jobs if not is_job_applied(j.get("url", ""))]
    
    print(f"\n📋 Jobs in queue: {len(jobs)}")
    print(f"   Already applied: {len(jobs) - len(pending_jobs)}")
    print(f"   Pending: {len(pending_jobs)}")
    print(f"\n🔒 Session limit: {MAX_PER_SESSION} jobs")
    
    if not pending_jobs:
        print("\n✅ All jobs in queue have been applied to!")
        print_application_summary()
        return
    
    # Show jobs to apply
    print(f"\n📋 Jobs to apply this session (max {MAX_PER_SESSION}):")
    for i, job in enumerate(pending_jobs[:MAX_PER_SESSION], 1):
        print(f"   {i}. {job.get('job_title', 'Unknown')[:40]} @ {job.get('company', 'Unknown')[:25]}")
    
    print("\n" + "⚠️ " * 20)
    print("\n   This will submit REAL applications!")
    print(f"   Up to {min(MAX_PER_SESSION, len(pending_jobs))} jobs will be applied to.")
    print("\n" + "⚠️ " * 20)
    
    response = input("\n👉 Type 'START' to begin session, or anything else to cancel: ").strip()
    if response != "START":
        print("\n❌ Session cancelled")
        return
    
    # Initialize
    limiter = SessionLimiter(max_per_session=MAX_PER_SESSION)
    session_results = []
    
    # Start browser
    print("\n🌐 Starting browser...")
    browser = Browser(headless=False)
    browser.start()
    
    try:
        for i, job in enumerate(pending_jobs):
            # Check limits
            can_apply, reason = limiter.can_apply()
            if not can_apply:
                print(f"\n🛑 {reason}")
                break
            
            print("\n" + "=" * 60)
            print(f"📋 JOB {i + 1}/{min(len(pending_jobs), MAX_PER_SESSION)}")
            print("=" * 60)
            print(f"   Title: {job.get('job_title', 'Unknown')}")
            print(f"   Company: {job.get('company', 'Unknown')}")
            print(f"   Location: {job.get('location', 'Unknown')}")
            
            # Confirm each job (if enabled)
            if CONFIRM_EACH_JOB:
                confirm = input("\n👉 Apply to this job? (y/n/stop): ").strip().lower()
                if confirm == "stop":
                    print("🛑 Session stopped by user")
                    break
                elif confirm != "y":
                    print("⏭️ Skipping this job")
                    continue
            
            # Apply to job
            result = apply_to_job(browser, job, resume, i + 1)
            session_results.append(result)
            
            if result["success"]:
                print(f"\n✅ Successfully applied to {job.get('job_title', 'Unknown')}")
                
                # Log application
                mark_job_applied(job["url"], job, "APPLIED")
                log_application(job, SHEET_URL if SHEET_URL else None)
                
                limiter.record_application()
            else:
                print(f"\n⚠️ Application issue: {result['reason']}")
            
            # Check if we should take a break
            if should_take_break(limiter.session_count):
                long_break(min_minutes=2, max_minutes=5)
            elif i < len(pending_jobs) - 1:
                # Normal delay between applications
                human_pause(min_s=30, max_s=60)
        
        # ========================================
        # SESSION SUMMARY
        # ========================================
        print("\n" + "=" * 60)
        print("📊 SESSION SUMMARY")
        print("=" * 60)
        
        successful = sum(1 for r in session_results if r["success"])
        failed = sum(1 for r in session_results if not r["success"])
        
        print(f"\n   Total attempted: {len(session_results)}")
        print(f"   ✅ Successful: {successful}")
        print(f"   ❌ Failed/Skipped: {failed}")
        
        if session_results:
            print(f"\n   Jobs applied:")
            for r in session_results:
                status = "✅" if r["success"] else "❌"
                print(f"      {status} {r['job'].get('job_title', 'Unknown')[:40]}")
                if not r["success"]:
                    print(f"         Reason: {r['reason']}")
        
        # Save session results
        session_data = {
            "timestamp": datetime.now().isoformat(),
            "total_attempted": len(session_results),
            "successful": successful,
            "failed": failed,
            "results": [
                {
                    "job_title": r["job"].get("job_title"),
                    "company": r["job"].get("company"),
                    "success": r["success"],
                    "reason": r["reason"]
                }
                for r in session_results
            ]
        }
        
        with open("data/last_session_results.json", "w", encoding="utf-8") as f:
            json.dump(session_data, f, indent=2)
        
        print(f"\n💾 Session results saved to: data/last_session_results.json")
        
        # Print overall summary
        print_application_summary()
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Session interrupted by user")
    except Exception as e:
        print(f"\n❌ Session error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n🔒 Closing browser...")
        browser.stop()
    
    print("\n" + "=" * 60)
    print("✅ DAY 19 Session Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
