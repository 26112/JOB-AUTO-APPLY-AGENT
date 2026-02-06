"""
Job Description Reader - Extracts and cleans job information from HTML
"""

import re
from bs4 import BeautifulSoup


def clean_job_text(raw_html: str) -> str:
    """
    Converts HTML job description into clean readable text.
    
    Args:
        raw_html: Raw HTML content from job posting
        
    Returns:
        Clean, readable text without HTML tags
    """
    soup = BeautifulSoup(raw_html, "html.parser")

    # Remove scripts and styles
    for tag in soup(["script", "style"]):
        tag.decompose()

    # Get text with newlines for block elements to preserve structure
    text = soup.get_text(separator="\n")
    
    # Clean up excessive whitespace while preserving line breaks
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    text = "\n".join(lines)

    return text


def extract_job_title(text: str) -> str:
    """
    Extract job title from job description text.
    
    Args:
        text: Job description text
        
    Returns:
        Job title or empty string
    """
    # Try to find common title patterns first
    # Look for lines that are short and appear early in the text
    lines = text.split("\n") if "\n" in text else text.split(".")
    
    # Common job title keywords
    title_keywords = ["engineer", "developer", "scientist", "analyst", "manager", 
                     "designer", "architect", "consultant", "specialist", "lead"]
    
    for line in lines[:5]:
        line = line.strip()
        # Check if line is reasonable length for a job title (2-8 words)
        words = line.split()
        if 2 <= len(words) <= 8:
            # Check if it contains common job title keywords
            if any(keyword in line.lower() for keyword in title_keywords):
                # Exclude lines that are clearly not titles
                if not any(exclude in line.lower() for exclude in ["looking for", "we are", "experience"]):
                    return line
    
    # Fallback: return first short line
    for line in lines[:3]:
        line = line.strip()
        if 2 <= len(line.split()) <= 8:
            return line
    
    return ""


def extract_company(text: str) -> str:
    """
    Extract company name from job description text.
    
    Args:
        text: Job description text
        
    Returns:
        Company name or empty string
    """
    patterns = [
        r"Company[:\-]\s*([A-Z][a-zA-Z0-9 &]+?)(?:\s+Location|$)",
        r"at\s+([A-Z][a-zA-Z0-9 &]+?)\s+(?:Pvt|Ltd|Inc|in\s|$)"
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            company = match.group(1).strip()
            # Exclude common false positives
            exclude_words = ["Location", "Remote", "About", "Requirements", "Experience"]
            if not any(word in company for word in exclude_words):
                return company

    return ""


def extract_job_location(text: str) -> str:
    """
    Extract location from job description text.
    
    Args:
        text: Job description text
        
    Returns:
        Location or empty string
    """
    locations = ["Remote", "India", "Bangalore", "Mumbai", "Delhi", "Hyderabad", 
                 "Pune", "Chennai", "Kolkata", "Noida", "Gurgaon"]
    
    for loc in locations:
        if loc.lower() in text.lower():
            return loc
    
    return ""


def build_job_profile(raw_html: str) -> dict:
    """
    Build a complete job profile from raw HTML.
    
    Args:
        raw_html: Raw HTML content from job posting
        
    Returns:
        Dictionary containing job_title, company, location, and description
    """
    text = clean_job_text(raw_html)

    return {
        "job_title": extract_job_title(text),
        "company": extract_company(text),
        "location": extract_job_location(text),
        "description": text
    }
