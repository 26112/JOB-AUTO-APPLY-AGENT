"""
Test Script for Indeed Job Reader - DAY 11

This script:
1. Reads job URLs from data/job_links.txt
2. Opens each job page in the browser
3. Extracts job details (title, company, location, description)
4. Saves all jobs to data/jobs_raw.json

⚠️ READ-ONLY AUTOMATION - NO Apply clicks!
"""

import sys
from pathlib import Path
import json

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from automation.browser import Browser
from portals.indeed_reader import read_job_page


def main():
    print("=" * 60)
    print("📚 DAY 11: Indeed Job Reader - Building Job Profiles")
    print("=" * 60)
    
    # Load job links from Day 10
    job_links_file = Path("data/job_links.txt")
    
    if not job_links_file.exists():
        print("❌ No job links found. Run Day 10 first!")
        print("   python portals/test_indeed_search.py")
        return
    
    with open(job_links_file, "r", encoding="utf-8") as f:
        job_links = [line.strip() for line in f if line.strip()]
    
    print(f"\n📋 Found {len(job_links)} job links")
    
    # Limit to first 10 for safety (avoid rate limiting)
    max_jobs = 10
    job_links = job_links[:max_jobs]
    print(f"   Processing first {len(job_links)} jobs for safety\n")

    # Start browser
    print("🌐 Starting browser...")
    browser = Browser(headless=False)
    browser.start()

    jobs = []
    
    print("\n" + "-" * 60)
    for idx, link in enumerate(job_links, 1):
        print(f"\n[{idx}/{len(job_links)}] ", end="")
        
        try:
            job = read_job_page(browser.page, link)
            jobs.append(job)
            
            # Display extracted info
            title = job.get('job_title', 'Unknown')[:40]
            company = job.get('company', 'Unknown')[:25]
            location = job.get('location', 'Unknown')[:20]
            desc_len = len(job.get('description', ''))
            
            print(f"   ✅ {title}")
            print(f"      Company: {company}")
            print(f"      Location: {location}")
            print(f"      Description: {desc_len} chars")
            
            # Add human-like delay between jobs
            browser.human_delay(2, 4)
            
        except Exception as e:
            print(f"   ❌ Failed: {e}")
            jobs.append({
                "job_title": "",
                "company": "",
                "location": "",
                "description": "",
                "url": link,
                "error": str(e)
            })
    
    print("\n" + "-" * 60)

    # Close browser
    print("\n🔒 Closing browser...")
    browser.stop()

    # Save jobs to JSON
    output_file = Path("data/jobs_raw.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=2, ensure_ascii=False)

    # Summary
    successful = sum(1 for j in jobs if j.get('job_title'))
    failed = len(jobs) - successful
    
    print("\n" + "=" * 60)
    print(f"📊 Results Summary:")
    print(f"   ✅ Successfully extracted: {successful} jobs")
    print(f"   ❌ Failed/Empty: {failed} jobs")
    print(f"   💾 Saved to: {output_file}")
    print("=" * 60)
    print("\n✅ DAY 11 Complete!")


if __name__ == "__main__":
    main()
