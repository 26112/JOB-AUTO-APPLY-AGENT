"""
Indeed Job Reader - Read live job pages and extract job profiles

DAY 11: Opens real job URLs and builds structured job profiles
for decision-making and auto-apply pipeline.
"""

import sys
from pathlib import Path
import time

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from matching.job_reader import build_job_profile


def read_job_page(page, job_url: str) -> dict:
    """
    Read a live Indeed job page and extract job profile.
    
    Args:
        page: Playwright page object
        job_url: URL of the job posting
    
    Returns:
        Dictionary containing job profile with url
    """
    print(f"📄 Reading job page: {job_url[:60]}...")

    try:
        page.goto(job_url, timeout=60000)
        time.sleep(4)  # Wait for dynamic content to load
        
        # Get page HTML
        html = page.content()
        
        # Build job profile using Day 6 job_reader
        job = build_job_profile(html)
        job["url"] = job_url
        
        # Try to extract Indeed-specific fields using selectors
        job = enhance_job_profile_from_indeed(page, job)
        
        return job
        
    except Exception as e:
        print(f"  ⚠️ Error reading page: {e}")
        return {
            "job_title": "",
            "company": "",
            "location": "",
            "description": "",
            "url": job_url,
            "error": str(e)
        }


def enhance_job_profile_from_indeed(page, job: dict) -> dict:
    """
    Enhance job profile with Indeed-specific selectors.
    
    Indeed has structured elements we can directly target
    for more accurate extraction.
    
    Args:
        page: Playwright page object
        job: Initial job profile dictionary
    
    Returns:
        Enhanced job profile
    """
    try:
        # Try Indeed-specific selectors for job title
        title_selectors = [
            "h1.jobsearch-JobInfoHeader-title",
            "h1[data-testid='jobsearch-JobInfoHeader-title']",
            ".jobsearch-JobInfoHeader-title-container h1",
            "h1"
        ]
        for selector in title_selectors:
            try:
                element = page.query_selector(selector)
                if element:
                    title = element.inner_text().strip()
                    if title and len(title) > 3:
                        job["job_title"] = title
                        break
            except:
                continue
        
        # Try Indeed-specific selectors for company
        company_selectors = [
            "[data-testid='inlineHeader-companyName'] a",
            "[data-testid='inlineHeader-companyName']",
            ".jobsearch-InlineCompanyRating-companyHeader a",
            ".jobsearch-InlineCompanyRating a"
        ]
        for selector in company_selectors:
            try:
                element = page.query_selector(selector)
                if element:
                    company = element.inner_text().strip()
                    if company and len(company) > 1:
                        job["company"] = company
                        break
            except:
                continue
        
        # Try Indeed-specific selectors for location
        location_selectors = [
            "[data-testid='inlineHeader-companyLocation']",
            ".jobsearch-JobInfoHeader-subtitle div:last-child",
            "[data-testid='job-location']"
        ]
        for selector in location_selectors:
            try:
                element = page.query_selector(selector)
                if element:
                    location = element.inner_text().strip()
                    if location and len(location) > 1:
                        job["location"] = location
                        break
            except:
                continue
        
        # Try Indeed-specific selectors for job description
        desc_selectors = [
            "#jobDescriptionText",
            ".jobsearch-jobDescriptionText",
            "[id='jobDescriptionText']"
        ]
        for selector in desc_selectors:
            try:
                element = page.query_selector(selector)
                if element:
                    desc = element.inner_text().strip()
                    if desc and len(desc) > 100:
                        job["description"] = desc
                        break
            except:
                continue
                
    except Exception as e:
        print(f"  ⚠️ Enhancement error (non-fatal): {e}")
    
    return job
