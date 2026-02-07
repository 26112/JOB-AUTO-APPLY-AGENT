"""
File Uploader Module - DAY 16

Handles resume and cover letter uploads for job applications.
Works with Indeed's file upload inputs.

⚠️ SAFETY: Only uploads files, does NOT submit
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def upload_resume(page, resume_path: str = "resume/resume.pdf") -> bool:
    """
    Upload resume PDF to the application form.
    
    Args:
        page: Playwright page object
        resume_path: Path to resume file (relative or absolute)
    
    Returns:
        bool: True if upload was successful
    """
    # Resolve to absolute path
    resume_file = Path(resume_path).resolve()
    
    # Check if file exists
    if not resume_file.exists():
        # Try relative to project root
        resume_file = Path(__file__).parent.parent / resume_path
        if not resume_file.exists():
            print(f"❌ Resume file not found: {resume_path}")
            print(f"   Looked in: {resume_file}")
            return False
    
    print(f"📄 Resume file: {resume_file.name}")
    
    # Find file upload inputs
    file_inputs = page.query_selector_all("input[type='file']")
    
    if not file_inputs:
        print("⚠️ No file upload field found on this page")
        print("   Indeed may be using a different upload method")
        return False
    
    print(f"🔍 Found {len(file_inputs)} file upload field(s)")
    
    # Try to upload to each file input
    for idx, file_input in enumerate(file_inputs, 1):
        try:
            # Check if this is a resume upload (not cover letter)
            accept = file_input.get_attribute("accept") or ""
            name = file_input.get_attribute("name") or ""
            element_id = file_input.get_attribute("id") or ""
            
            print(f"   Trying upload #{idx}: accept='{accept}', name='{name}'")
            
            # Upload the file
            file_input.set_input_files(str(resume_file))
            print(f"✅ Resume uploaded successfully: {resume_file.name}")
            return True
            
        except Exception as e:
            print(f"   ⚠️ Upload #{idx} failed: {e}")
            continue
    
    print("❌ Failed to upload resume to any field")
    return False


def upload_cover_letter(page, cover_letter_path: str = "resume/cover_letter.pdf") -> bool:
    """
    Upload cover letter to the application form.
    
    Args:
        page: Playwright page object
        cover_letter_path: Path to cover letter file
    
    Returns:
        bool: True if upload was successful
    """
    cover_letter_file = Path(cover_letter_path).resolve()
    
    if not cover_letter_file.exists():
        cover_letter_file = Path(__file__).parent.parent / cover_letter_path
        if not cover_letter_file.exists():
            print(f"⚠️ Cover letter not found: {cover_letter_path}")
            return False
    
    print(f"📄 Cover letter file: {cover_letter_file.name}")
    
    # Find file upload inputs that might be for cover letter
    file_inputs = page.query_selector_all("input[type='file']")
    
    for file_input in file_inputs:
        try:
            name = (file_input.get_attribute("name") or "").lower()
            element_id = (file_input.get_attribute("id") or "").lower()
            
            # Check if this looks like a cover letter field
            if "cover" in name or "cover" in element_id or "letter" in name:
                file_input.set_input_files(str(cover_letter_file))
                print(f"✅ Cover letter uploaded: {cover_letter_file.name}")
                return True
        except:
            continue
    
    print("⚠️ No cover letter upload field found")
    return False


def select_existing_resume(page) -> bool:
    """
    Select an existing resume from Indeed's saved resumes.
    
    Some Indeed forms show previously uploaded resumes as radio buttons.
    
    Args:
        page: Playwright page object
    
    Returns:
        bool: True if a resume was selected
    """
    print("🔍 Looking for existing resume options...")
    
    # Look for radio buttons with resume-related text
    resume_options = page.query_selector_all("input[type='radio']")
    
    for option in resume_options:
        try:
            # Get the label or parent text
            label_text = option.evaluate(
                """el => {
                    const label = document.querySelector(`label[for='${el.id}']`);
                    if (label) return label.innerText;
                    const parent = el.closest('label');
                    if (parent) return parent.innerText;
                    return '';
                }"""
            ) or ""
            
            # Check if this looks like a resume option
            if "resume" in label_text.lower() or ".pdf" in label_text.lower():
                option.click()
                print(f"✅ Selected existing resume: {label_text[:50]}...")
                return True
        except:
            continue
    
    print("⚠️ No existing resume options found")
    return False


def handle_resume_upload(page, resume_path: str = "resume/resume.pdf") -> dict:
    """
    Main function to handle resume upload in any form.
    
    Tries multiple strategies:
    1. Direct file upload
    2. Select existing resume
    
    Args:
        page: Playwright page object
        resume_path: Path to resume file
    
    Returns:
        dict: Result with method used and success status
    """
    result = {
        "success": False,
        "method": None,
        "message": ""
    }
    
    # Strategy 1: Try direct file upload
    if upload_resume(page, resume_path):
        result["success"] = True
        result["method"] = "file_upload"
        result["message"] = "Resume uploaded via file input"
        return result
    
    # Strategy 2: Try selecting existing resume
    if select_existing_resume(page):
        result["success"] = True
        result["method"] = "existing_resume"
        result["message"] = "Selected existing resume"
        return result
    
    result["message"] = "Could not upload or select resume"
    return result
