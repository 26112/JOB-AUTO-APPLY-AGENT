"""
Indeed Portal - Job Search Automation Module

This module provides functionality to:
- Build Indeed search URLs with filters
- Collect job listing URLs from search results
- Scroll through results like a human

DAY 10: Read-only automation - NO Apply clicks!
"""

from urllib.parse import quote
import time


def build_search_url(title: str, location: str, days: int = 7) -> str:
    """
    Build an Indeed job search URL with the given parameters.
    
    Args:
        title: Job title to search for
        location: Location to search in
        days: Only show jobs posted within this many days (default: 7)
    
    Returns:
        Complete Indeed search URL
    """
    base = "https://www.indeed.com/jobs"
    params = f"?q={quote(title)}&l={quote(location)}&fromage={days}"
    return base + params


def collect_job_links(page, max_jobs: int = 20) -> list:
    """
    Collect job listing URLs from Indeed search results.
    
    Scrolls through the page multiple times to load more jobs,
    simulating human-like browsing behavior.
    
    Args:
        page: Playwright page object
        max_jobs: Maximum number of job links to collect
    
    Returns:
        List of unique job URLs
    """
    job_links = set()
    
    print(f"🔍 Collecting up to {max_jobs} job links...")

    # Scroll multiple times to load jobs
    for scroll_num in range(5):
        # Try multiple possible selectors for job cards
        # Indeed sometimes changes class names, so we try multiple
        selectors = [
            "a.tapItem",
            "a[data-jk]",
            "div.job_seen_beacon a",
            ".resultContent a[href*='/viewjob']",
            "a[href*='/viewjob']"
        ]
        
        cards = []
        for selector in selectors:
            try:
                cards = page.query_selector_all(selector)
                if cards:
                    print(f"  Found {len(cards)} cards with selector: {selector}")
                    break
            except Exception:
                continue
        
        # Extract hrefs from cards
        for card in cards:
            try:
                href = card.get_attribute("href")
                if href:
                    # Build full URL if relative
                    if href.startswith("/viewjob") or href.startswith("/rc/"):
                        full_url = "https://www.indeed.com" + href
                        job_links.add(full_url)
                    elif "indeed.com" in href and ("/viewjob" in href or "/rc/" in href):
                        job_links.add(href)
            except Exception as e:
                print(f"  ⚠️ Error extracting href: {e}")
                continue

        print(f"  Scroll {scroll_num + 1}/5: Found {len(job_links)} unique jobs so far")
        
        # Scroll down to load more jobs
        try:
            page.mouse.wheel(0, 3000)
        except Exception:
            page.evaluate("window.scrollBy(0, 3000)")
        
        time.sleep(2)

        if len(job_links) >= max_jobs:
            print(f"  ✅ Reached max jobs limit ({max_jobs})")
            break

    return list(job_links)[:max_jobs]


def save_job_links(links: list, filename: str = "data/job_links.txt") -> None:
    """
    Save collected job links to a file.
    
    Args:
        links: List of job URLs
        filename: Output file path
    """
    with open(filename, "w", encoding="utf-8") as f:
        for link in links:
            f.write(link + "\n")
    
    print(f"💾 Saved {len(links)} job links to {filename}")
