import pdfplumber
from pathlib import Path
import re
from datetime import datetime


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


# ========== Day 4: Skills, Experience & Companies Extraction ==========

def extract_skills(text: str) -> list:
    """
    Extract skills from resume text using a master skills list.
    
    Args:
        text: Resume text
        
    Returns:
        List of found skills
    """
    skills_file = Path("data/skills_master_list.txt")
    
    if not skills_file.exists():
        return []
    
    skills = skills_file.read_text(encoding="utf-8").splitlines()
    text_lower = text.lower()
    found_skills = []

    for skill in skills:
        skill = skill.strip()
        if skill and skill.lower() in text_lower:
            found_skills.append(skill)

    return sorted(set(found_skills))


def extract_experience_years(text: str) -> float:
    """
    Calculate total years of experience from resume text.
    
    Args:
        text: Resume text
        
    Returns:
        Total years of experience as a float
    """
    years = []

    # Matches ranges like 2021 - 2024 or 2020 – Present
    matches = re.findall(r"(20\d{2})\s*[-–]\s*(20\d{2}|present)", text.lower())

    current_year = datetime.now().year

    for start, end in matches:
        start_year = int(start)
        end_year = current_year if end == "present" else int(end)
        years.append(end_year - start_year)

    return round(sum(years), 1) if years else 0.0


def extract_companies(text: str) -> list:
    """
    Extract company names from resume text.
    
    Args:
        text: Resume text
        
    Returns:
        List of company names
    """
    companies = set()
    
    # Match company names with common suffixes (handles variations)
    patterns = [
        r"([A-Z][a-zA-Z0-9 &]+?)\s+(Pvt\.?\s+Ltd\.?|Private Limited|Ltd\.?|Inc\.?)",
        r"at\s+([A-Z][a-zA-Z0-9 &]+(?:Pvt\.?\s+Ltd\.?|Private Limited|Ltd\.?|Inc\.?)?)"
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            if isinstance(match, tuple):
                # Pattern with suffix captured separately
                company = match[0].strip()
                if len(match) > 1:
                    suffix = match[1].strip()
                    full_company = f"{company} {suffix}"
                else:
                    full_company = company
            else:
                # Pattern captured whole string
                full_company = match.strip()
            
            # Remove "at " prefix if present
            full_company = re.sub(r'^at\s+', '', full_company)
            
            # Filter out common false positives and job titles
            exclude_keywords = ['experience', 'education', 'bachelor', 'technology']
            
            if (len(full_company) > 3 and 
                not any(keyword in full_company.lower() for keyword in exclude_keywords)):
                companies.add(full_company)
    
    return sorted(list(companies))


def build_resume_profile(text: str) -> dict:
    """
    Build a structured resume profile from extracted text.
    
    Args:
        text: Extracted resume text
        
    Returns:
        Dictionary containing all extracted resume information
    """
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "location": extract_location(text),
        "skills": extract_skills(text),
        "experience_years": extract_experience_years(text),
        "companies": extract_companies(text),
        "raw_text": text
    }
