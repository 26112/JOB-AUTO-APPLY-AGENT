"""
Day 6 Test - Job Description Reader
Tests the job reader module with sample HTML
"""

from matching.job_reader import build_job_profile
from pathlib import Path
import json


def main():
    print("=" * 50)
    print("Day 6 Test - Job Description Reader")
    print("=" * 50)
    
    # Load sample job HTML
    html_path = Path("data/sample_job.html")
    
    if not html_path.exists():
        print("\n❌ Error: sample_job.html not found!")
        return
    
    html = html_path.read_text(encoding="utf-8")
    
    # Build job profile
    print("\n📄 Processing job description...")
    job = build_job_profile(html)
    
    # Display results
    print("\n" + "=" * 50)
    print("✅ Job Profile Extracted")
    print("=" * 50)
    
    print(f"\n📋 Job Title: {job['job_title']}")
    print(f"🏢 Company: {job['company']}")
    print(f"📍 Location: {job['location']}")
    print(f"\n📝 Description Preview:")
    print(f"   {job['description'][:200]}...")
    
    # Save to file
    output_path = Path("data/sample_job_profile.json")
    output_path.write_text(json.dumps(job, indent=2), encoding="utf-8")
    
    print(f"\n💾 Saved to: {output_path}")
    
    # Display full JSON
    print("\n" + "=" * 50)
    print("Complete JSON Output:")
    print("=" * 50)
    print(json.dumps(job, indent=2))
    
    print("\n" + "=" * 50)
    print("✅ Day 6 Test Completed!")
    print("=" * 50)


if __name__ == "__main__":
    main()
