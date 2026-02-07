"""
Single Job Apply Test - DAY 13-17 (Full Application Flow)

⚠️ SAFETY MODE:
- Opens ONE job only
- Clicks Apply button
- Inspects form fields
- Auto-fills personal info
- Uploads resume
- Handles cover letter
- Answers screening questions
- STOPS before final submission

🛑 DO NOT SUBMIT ANYTHING
"""

import sys
from pathlib import Path
import json

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from automation.browser import Browser
from portals.indeed_apply import open_job, click_apply, detect_application_state, get_page_screenshot
from automation.form_inspector import inspect_form_fields, categorize_fields, print_form_map
from automation.form_filler import autofill_personal_info, get_fill_summary
from automation.file_uploader import handle_resume_upload
from automation.cover_letter_handler import handle_cover_letter_any_method
from automation.question_answerer import answer_standard_questions, get_questions_summary


# ============================================================
# 🎯 TEST JOB - AI Engineer at Dine Development Corporation
# ============================================================
JOB_URL = "https://www.indeed.com/rc/clk?jk=bcc177017878a9d3&bb=2dyAVycxwRfePjzV3wF7FzMxRG70WOdWNPmeiBVE3r0PyNwvCjJIE8CIKPNjjbU0AMjQ6i_WnLeApF_jF8TRFrGmR9ahWQzhW89vhULyvzOW8xFKnLswLp7cEptq5fkS&xkcb=SoCJ67M3nbEfP6TxYZ0MbzkdCdPP&fccid=4df31e7755888b93&vjs=3"

JOB_TITLE = "AI Engineer"
JOB_COMPANY = "Dine Development Corporation"


def main():
    print("=" * 60)
    print("🟡 DAY 17: Full Application Flow (NO SUBMIT)")
    print("=" * 60)
    
    print(f"\n📋 Test Job:")
    print(f"   Title: {JOB_TITLE}")
    print(f"   Company: {JOB_COMPANY}")
    print(f"   URL: {JOB_URL[:60]}...")
    
    # Load resume profile
    resume_path = Path("data/resume_profile.json")
    if not resume_path.exists():
        print("❌ Resume profile not found: data/resume_profile.json")
        return
    
    resume = json.load(open(resume_path, encoding="utf-8"))
    print(f"\n📄 Resume Profile:")
    print(f"   Name: {resume.get('name', 'N/A')}")
    print(f"   Email: {resume.get('email', 'N/A')}")
    
    # Check files
    resume_pdf = Path("resume/resume.pdf")
    cover_letter = Path("data/cover_letter.txt")
    print(f"\n📎 Files:")
    print(f"   Resume PDF: {'✅' if resume_pdf.exists() else '⚠️ Not found'}")
    print(f"   Cover Letter: {'✅' if cover_letter.exists() else '⚠️ Not found'}")
    
    print("\n⚠️  SAFETY REMINDERS:")
    print("   • Full application flow will run")
    print("   • Will reach FINAL SUBMIT button")
    print("   • DO NOT click Submit!")
    
    input("\n👉 Press ENTER to start (or Ctrl+C to cancel)...")
    
    # Start browser
    print("\n🌐 Starting browser...")
    browser = Browser(headless=False)
    browser.start()
    
    # Track what was done
    results = {
        "job_opened": False,
        "apply_clicked": False,
        "fields_detected": 0,
        "fields_filled": [],
        "resume_uploaded": False,
        "cover_letter": False,
        "questions_answered": []
    }
    
    try:
        # Step 1: Open job page
        print("\n" + "-" * 40)
        print("STEP 1: Opening job page")
        print("-" * 40)
        open_job(browser.page, JOB_URL)
        get_page_screenshot(browser.page, "step1_job_page.png")
        results["job_opened"] = True
        
        # Step 2: Click Apply
        print("\n" + "-" * 40)
        print("STEP 2: Clicking Apply button")
        print("-" * 40)
        clicked = click_apply(browser.page)
        results["apply_clicked"] = clicked
        
        if clicked:
            browser.human_delay(3, 5)
            
            # Step 3: Detect state
            print("\n" + "-" * 40)
            print("STEP 3: Detecting application state")
            print("-" * 40)
            state = detect_application_state(browser.page)
            get_page_screenshot(browser.page, "step2_apply_clicked.png")
            
            # Step 4: Form Field Detection
            print("\n" + "-" * 40)
            print("STEP 4: Inspecting form fields")
            print("-" * 40)
            fields = inspect_form_fields(browser.page)
            results["fields_detected"] = len(fields)
            print_form_map(fields)
            
            with open("data/form_fields.json", "w", encoding="utf-8") as f:
                json.dump(fields, f, indent=2, ensure_ascii=False)
            
            # Step 5: Auto-Fill Personal Information
            print("\n" + "-" * 40)
            print("STEP 5: Auto-filling personal information")
            print("-" * 40)
            filled = autofill_personal_info(browser.page, resume)
            results["fields_filled"] = filled
            print(f"\n📝 {get_fill_summary(filled)}")
            
            # Step 6: Resume Upload
            print("\n" + "-" * 40)
            print("STEP 6: Uploading resume")
            print("-" * 40)
            upload_result = handle_resume_upload(browser.page, "resume/resume.pdf")
            results["resume_uploaded"] = upload_result["success"]
            if upload_result["success"]:
                print(f"✅ {upload_result['message']}")
            else:
                print(f"ℹ️ {upload_result['message']}")
            
            browser.human_delay(2, 3)
            
            # Step 7: Cover Letter (DAY 17)
            print("\n" + "-" * 40)
            print("STEP 7: Handling cover letter (DAY 17)")
            print("-" * 40)
            cl_result = handle_cover_letter_any_method(browser.page)
            results["cover_letter"] = cl_result["success"]
            if cl_result["success"]:
                print(f"✅ {cl_result['message']}")
            else:
                print(f"ℹ️ {cl_result['message']}")
            
            # Step 8: Answer Screening Questions (DAY 17)
            print("\n" + "-" * 40)
            print("STEP 8: Answering screening questions (DAY 17)")
            print("-" * 40)
            answered = answer_standard_questions(browser.page)
            results["questions_answered"] = answered
            print(f"\n📝 {get_questions_summary(answered)}")
            
            browser.human_delay(2, 3)
            get_page_screenshot(browser.page, "step8_questions_answered.png")
            
            # ========================================
            # FINAL STOP
            # ========================================
            print("\n" + "=" * 60)
            print("🛑 FINAL STEP REACHED — DO NOT SUBMIT!")
            print("=" * 60)
            
            print(f"\n📊 Application Summary:")
            print(f"   ├─ Job opened: ✅")
            print(f"   ├─ Apply clicked: ✅")
            print(f"   ├─ Fields detected: {results['fields_detected']}")
            print(f"   ├─ Fields auto-filled: {len(results['fields_filled'])}")
            print(f"   ├─ Resume: {'✅ Uploaded/Selected' if results['resume_uploaded'] else 'ℹ️ Not needed'}")
            print(f"   ├─ Cover letter: {'✅ Added' if results['cover_letter'] else 'ℹ️ Not required'}")
            print(f"   └─ Questions answered: {len(results['questions_answered'])}")
            
            print("\n⚠️ VERIFY IN BROWSER:")
            print("   1. Is the Submit button visible?")
            print("   2. Are all required fields filled?")
            print("   3. Any validation errors?")
            print("   4. DO NOT click Submit!")
            
        else:
            print("\n❌ Apply button not found")
            get_page_screenshot(browser.page, "step2_apply_not_found.png")
        
        # Save results
        with open("data/application_test_results.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        print(f"\n💾 Results saved to: data/application_test_results.json")
        
        # Wait for manual inspection
        print("\n" + "-" * 40)
        input("👉 Inspect everything. DO NOT SUBMIT. Press ENTER to close browser...")
        
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
    
    print("\n" + "=" * 60)
    print("✅ DAY 17 Test Complete!")
    print("   Full application flow tested (no submission)")
    print("=" * 60)


if __name__ == "__main__":
    main()
