"""
Day 7 Test - Job Matching & Evaluator
Tests the Apply/Skip logic against sample data
"""

from matching.evaluator import evaluate_job
import json
import yaml
from pathlib import Path

def main():
    print("=" * 50)
    print("Day 7 Test - Job Matching Engine")
    print("=" * 50)

    # 1. Load Resume Profile (with Mock Fallback)
    resume_path = Path("data/resume_profile.json")
    if not resume_path.exists():
        print("⚠️ Resume profile not found. Using Mock Profile.")
        resume = {
            "name": "Mock Candidate",
            "skills": ["python", "machine learning", "sql", "pandas", "scikit-learn"],
            "experience_years": 3.0,
            "location": "Remote"
        }
    else:
        resume = json.loads(resume_path.read_text(encoding="utf-8"))

    # 2. Load Settings (YAML Fix)
    settings_path = Path("config/settings.yaml")
    if not settings_path.exists():
        print("❌ Error: config/settings.yaml not found.")
        return
    
    settings = yaml.safe_load(settings_path.read_text(encoding="utf-8")) 

    # 3. Define Test Job
    job = {
        "job_title": "Machine Learning Engineer",
        "company": "ABC Technologies",
        "location": "Remote",
        "description": "Looking for a Machine Learning Engineer with Python, SQL, Pandas, Scikit-learn. 2+ years experience required."
    }

    # 4. Run Evaluation
    print(f"\nEvaluating Job: {job['job_title']} at {job['company']}")
    result = evaluate_job(resume, job, settings)
    
    print("\nDecision Output:")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
