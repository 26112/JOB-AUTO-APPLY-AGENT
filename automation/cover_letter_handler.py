"""
Cover Letter Handler Module - DAY 17

Handles cover letter input for job applications.
Supports both textarea paste and file upload methods.

⚠️ SAFETY: Only fills cover letter fields, does NOT submit
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def handle_cover_letter(page, cover_letter_path: str = "data/cover_letter.txt") -> bool:
    """
    Paste cover letter into textarea field if present.
    
    Args:
        page: Playwright page object
        cover_letter_path: Path to cover letter text file
    
    Returns:
        bool: True if cover letter was pasted
    """
    # Load cover letter
    cover_letter_file = Path(cover_letter_path)
    if not cover_letter_file.exists():
        cover_letter_file = Path(__file__).parent.parent / cover_letter_path
    
    if not cover_letter_file.exists():
        print(f"⚠️ Cover letter file not found: {cover_letter_path}")
        return False
    
    cover_letter = cover_letter_file.read_text(encoding="utf-8")
    print(f"📝 Cover letter loaded ({len(cover_letter)} chars)")

    # Find cover letter textareas
    textareas = page.query_selector_all("textarea")

    for ta in textareas:
        try:
            if not ta.is_visible():
                continue
                
            placeholder = (ta.get_attribute("placeholder") or "").lower()
            name = (ta.get_attribute("name") or "").lower()
            element_id = (ta.get_attribute("id") or "").lower()
            
            # Get label
            label = ""
            try:
                label = ta.evaluate(
                    """el => {
                        const l = document.querySelector(`label[for='${el.id}']`);
                        return l ? l.innerText.toLowerCase() : '';
                    }"""
                ) or ""
            except:
                pass
            
            searchable = f"{placeholder} {name} {element_id} {label}"
            
            # Check if this is a cover letter field
            if any(x in searchable for x in ["cover letter", "cover_letter", "coverletter", 
                                              "message to", "message for", "additional message",
                                              "why are you interested", "tell us about"]):
                ta.fill(cover_letter)
                print("✅ Cover letter pasted successfully")
                return True
                
        except Exception as e:
            continue

    print("ℹ️ No cover letter field found on this page")
    return False


def upload_cover_letter_file(page, cover_letter_path: str = "data/cover_letter.pdf") -> bool:
    """
    Upload cover letter file if file input is present.
    
    Args:
        page: Playwright page object
        cover_letter_path: Path to cover letter PDF file
    
    Returns:
        bool: True if cover letter was uploaded
    """
    cover_letter_file = Path(cover_letter_path).resolve()
    
    if not cover_letter_file.exists():
        cover_letter_file = Path(__file__).parent.parent / cover_letter_path
        if not cover_letter_file.exists():
            print(f"⚠️ Cover letter PDF not found: {cover_letter_path}")
            return False
    
    print(f"📄 Cover letter file: {cover_letter_file.name}")

    # Find file inputs that might be for cover letter
    file_inputs = page.query_selector_all("input[type='file']")

    for file_input in file_inputs:
        try:
            name = (file_input.get_attribute("name") or "").lower()
            element_id = (file_input.get_attribute("id") or "").lower()
            accept = (file_input.get_attribute("accept") or "").lower()
            
            # Check if this looks like a cover letter upload
            if any(x in f"{name} {element_id}" for x in ["cover", "letter", "cl_"]):
                file_input.set_input_files(str(cover_letter_file))
                print("✅ Cover letter uploaded successfully")
                return True
                
        except Exception as e:
            continue

    print("ℹ️ No cover letter upload field found")
    return False


def handle_cover_letter_any_method(page, 
                                    text_path: str = "data/cover_letter.txt",
                                    pdf_path: str = "data/cover_letter.pdf") -> dict:
    """
    Try to add cover letter using any available method.
    
    Tries in order:
    1. Paste into textarea
    2. Upload PDF file
    
    Args:
        page: Playwright page object
        text_path: Path to cover letter text file
        pdf_path: Path to cover letter PDF file
    
    Returns:
        dict: Result with method used and success status
    """
    result = {
        "success": False,
        "method": None,
        "message": ""
    }
    
    # Strategy 1: Paste into textarea
    if handle_cover_letter(page, text_path):
        result["success"] = True
        result["method"] = "textarea"
        result["message"] = "Cover letter pasted into textarea"
        return result
    
    # Strategy 2: Upload PDF (if available)
    if Path(pdf_path).exists() or (Path(__file__).parent.parent / pdf_path).exists():
        if upload_cover_letter_file(page, pdf_path):
            result["success"] = True
            result["method"] = "file_upload"
            result["message"] = "Cover letter PDF uploaded"
            return result
    
    result["message"] = "No cover letter field found (this is OK for most Indeed jobs)"
    return result
