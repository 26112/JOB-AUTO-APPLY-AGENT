"""
Day 7 Test - Job Matching & Evaluator
Tests the Apply/Skip logic against sample data
"""

from matching.evaluator import evaluate_job, get_match_summary
import json
import yaml
from pathlib import Path

def main():
    print("=" * 50)
    print("Day 7 Test - Job Matching Engine")
    print("=" * 50)

    # 1. Load Resume Profile
    resume_path = Path("data/resume_profile.json")
    if not resume_path.exists():
        print("❌ Error: data/resume_profile.json not found. Run main.py first.")
        # Create a mock resume for testing if file missing
        print("⚠️ Creating mock resume for testing...")
        resume = {
            "name": "Test User",
            "location": "India",
            "skills": ["python", "machine learning", "sql", "pandas", "scikit-learn", "tensorflow"],
            "experience_years": 3.0
        }
    else:
        resume = json.loads(resume_path.read_text(encoding="utf-8"))

    print(f"\n👤 Analyzing Resume: {resume.get('name', 'Unknown')}")
    print(f"   Skills: {len(resume.get('skills', []))}")
    print(f"   Experience: {resume.get('experience_years', 0)} years")

    # 2. Load Settings
    settings_path = Path("config/settings.yaml")
    if not settings_path.exists():
        print("❌ Error: config/settings.yaml not found.")
        return
    
    settings = yaml.safe_load(settings_path.read_text(encoding="utf-8")) 
    
    print("\n⚙️  Settings Loaded:")
    print(f"   Target Title: {settings['job']['title']}")
    print(f"   Min Title Match: {settings['filters']['min_title_match']}%")
    print(f"   Min Skill Match: {settings['filters']['min_skill_match']}")

    # 3. Define Test Jobs
    test_jobs = [
        {
            "id": 1,
            "job_title": "Machine Learning Engineer",
            "company": "TechCorp",
            "location": "Remote",
            "description": "Looking for a Machine Learning Engineer with Python, SQL, Pandas, Scikit-learn. 2+ years experience required."
        },
        {
            "id": 2,
            "job_title": "Senior Data Scientist",
            "company": "BigData Inc",
            "location": "New York",
            "description": "Senior role requires 8+ years experience in AI, deep learning, and team leadership."
        },
        {
            "id": 3,
            "job_title": "Python Developer",
            "company": "WebSoft",
            "location": "India",
            "description": "Need a Python developer for backend work. Django, Flask, SQL required. 1+ years exp."
        }
    ]

    # 4. Run Evaluation
    print("\n" + "=" * 50)
    print("🚀 Running Evaluation")
    print("=" * 50)

    for job in test_jobs:
        print(f"\n🔎 Evaluating Job #{job['id']}: {job['job_title']} at {job['company']}")
        
        result = evaluate_job(resume, job, settings)
        
        # Display decision
        summary = get_match_summary(result)
        print(summary)
        
        # Validation checks for the user to see logic in action
        if job['id'] == 1:
            print("   (Expected: APPLY - High title match, good skills, Exp OK)")
        elif job['id'] == 2:
            print("   (Expected: SKIP - Experience too high, location mismatch)")
        elif job['id'] == 3:
            print("   (Expected: CHECK - Depends on skill thresholds vs description)")

    print("\n" + "=" * 50)
    print("✅ Day 7 Test Completed!")
    print("=" * 50)

if __name__ == "__main__":
    main()
