import pdfplumber
from pathlib import Path
import re


def extract_resume_text(pdf_path: str) -> str:
    """
    Extract text from a PDF resume.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Extracted text as a string
    """
    text = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)

    return "\n".join(text)


def save_text_to_file(text: str, output_path: str):
    """
    Save extracted text to a file.
    
    Args:
        text: Text to save
        output_path: Path where to save the file
    """
    Path(output_path).write_text(text, encoding="utf-8")


# ========== Day 3: Extract Basic Resume Info ==========

def extract_email(text: str) -> str:
    """
    Extract email address from resume text.
    
    Args:
        text: Resume text
        
    Returns:
        Email address or empty string if not found
    """
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return match.group() if match else ""


def extract_phone(text: str) -> str:
    """
    Extract phone number from resume text.
    
    Args:
        text: Resume text
        
    Returns:
        Phone number or empty string if not found
    """
    match = re.search(r"(\+?\d{1,3}[\s-]?)?\d{10}", text)
    return match.group() if match else ""


def extract_name(text: str) -> str:
    """
    Extract name from resume text (usually at the top).
    
    Args:
        text: Resume text
        
    Returns:
        Name or empty string if not found
    """
    lines = text.splitlines()
    for line in lines[:10]:  # name is usually at top
        line = line.strip()
        if not line:
            continue
        # Name is typically 2-4 words with letters (may have spaces)
        words = line.split()
        if 2 <= len(words) <= 4 and any(c.isalpha() for c in line):
            # Avoid common headers
            if line.lower() not in ['experience', 'education', 'skills', 'projects']:
                return line
    return ""


def extract_location(text: str) -> str:
    """
    Extract location from resume text.
    
    Args:
        text: Resume text
        
    Returns:
        Location or empty string if not found
    """
    common_locations = ["India", "Remote", "Delhi", "Mumbai", "Bangalore", "Hyderabad"]
    for loc in common_locations:
        if loc.lower() in text.lower():
            return loc
    return ""


def build_resume_profile(text: str) -> dict:
    """
    Build a structured resume profile from extracted text.
    
    Args:
        text: Extracted resume text
        
    Returns:
        Dictionary containing name, email, phone, location, and raw text
    """
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "location": extract_location(text),
        "raw_text": text
    }
