"""
Test Script for Indeed Job Search - DAY 10

This script:
1. Opens Indeed using saved browser session
2. Searches for jobs using config values
3. Scrolls through results like a human
4. Collects job listing URLs
5. Saves them to a file

⚠️ READ-ONLY AUTOMATION - NO Apply clicks!
"""

import sys
from pathlib import Path

# Add project root to path for imports (MUST be before project imports)
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from automation.browser import Browser
from portals.indeed import build_search_url, collect_job_links, save_job_links
from config.loader import load_settings


def main():
    print("=" * 60)
    print("🔍 DAY 10: Indeed Job Search Automation")
    print("=" * 60)
    
    # Load settings
    settings = load_settings()
    job = settings["job"]
    
    print(f"\n📋 Search Configuration:")
    print(f"   Title: {job['title']}")
    print(f"   Location: {job['location']}")
    print(f"   Posted within: {job['posted_within_days']} days")
    print(f"   Max jobs: {job['max_jobs_per_session']}")

    # Start browser with persistent session
    print("\n🌐 Starting browser...")
    browser = Browser(headless=False)
    browser.start()

    # Build search URL
    search_url = build_search_url(
        job["title"],
        job["location"],
        job["posted_within_days"]
    )
    
    print(f"\n🔗 Search URL: {search_url}")

    # Open Indeed search page
    browser.open(search_url)
    
    # Give page time to fully load
    browser.human_delay(3, 5)

    # Collect job links
    print("\n" + "=" * 60)
    links = collect_job_links(
        browser.page,
        max_jobs=job["max_jobs_per_session"]
    )
    print("=" * 60)

    # Display results
    print(f"\n✅ Found {len(links)} job links:\n")
    for i, link in enumerate(links, 1):
        print(f"  {i:2}. {link}")

    # Save to file
    if links:
        save_job_links(links, "data/job_links.txt")
    else:
        print("\n⚠️ No job links found. See troubleshooting tips:")
        print("   - Try location = 'India' or a city name")
        print("   - Try removing 'Remote' from location")
        print("   - Indeed may have changed their HTML structure")

    # Take a screenshot for verification
    browser.screenshot("data/indeed_search_results.png")
    
    # Close browser
    print("\n🔒 Closing browser...")
    browser.stop()
    
    print("\n" + "=" * 60)
    print("✅ DAY 10 Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
