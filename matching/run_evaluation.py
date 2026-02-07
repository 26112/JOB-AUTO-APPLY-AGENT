"""
Job Evaluation Runner - DAY 12

This script:
1. Loads your resume profile
2. Loads scraped jobs from Indeed
3. Evaluates each job against your profile
4. Generates APPLY/SKIP decisions with reasons
5. Creates an application queue

🚫 NO APPLYING - This is decision + planning only.
"""

import json
import yaml
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from matching.evaluator import evaluate_job, get_match_summary


def main():
    print("=" * 60)
    print("🧠 DAY 12: Job Evaluation & Application Queue")
    print("=" * 60)
    
    # Load resume profile
    resume_path = Path("data/resume_profile.json")
    if not resume_path.exists():
        print("❌ Resume profile not found: data/resume_profile.json")
        return
    
    resume = json.load(open(resume_path, encoding="utf-8"))
    print(f"\n📄 Resume: {resume.get('name', 'Unknown')}")
    print(f"   Experience: {resume.get('experience_years', 0)} years")
    print(f"   Skills: {len(resume.get('skills', []))} skills loaded")
    
    # Load jobs
    jobs_path = Path("data/jobs_raw.json")
    if not jobs_path.exists():
        print("❌ Jobs file not found. Run Day 11 first!")
        return
    
    jobs = json.load(open(jobs_path, encoding="utf-8"))
    print(f"\n📋 Jobs to evaluate: {len(jobs)}")
    
    # Load settings
    settings = yaml.safe_load(open("config/settings.yaml", encoding="utf-8"))
    print(f"\n⚙️  Filters:")
    print(f"   Min title match: {settings['filters']['min_title_match']}%")
    print(f"   Min skill match: {settings['filters']['min_skill_match']} skills")
    print(f"   Max extra experience: {settings['experience']['max_extra_years']} years")
    
    # Evaluate each job
    results = []
    apply_queue = []
    
    print("\n" + "-" * 60)
    print("📊 EVALUATION RESULTS")
    print("-" * 60)
    
    for idx, job in enumerate(jobs, 1):
        decision = evaluate_job(resume, job, settings)
        
        job_result = {
            "job_title": job.get("job_title", "Unknown"),
            "company": job.get("company", "Unknown"),
            "location": job.get("location", "Unknown"),
            "url": job.get("url", ""),
            "decision": decision["decision"],
            "reasons": decision["reasons"],
            "metrics": {
                "title_match": decision["title_match"],
                "skill_match": decision["skill_match"],
                "job_experience": decision["job_experience"]
            }
        }
        
        results.append(job_result)
        
        # Print result
        emoji = "✅" if decision["decision"] == "APPLY" else "❌"
        print(f"\n{idx}. {emoji} {job_result['job_title'][:45]}")
        print(f"   Company: {job_result['company'][:30]}")
        print(f"   Title Match: {decision['title_match']}% | Skills: {decision['skill_match']} | Exp: {decision['job_experience']}yr")
        print(f"   → {decision['decision']}: {', '.join(decision['reasons'][:2])}")
        
        if decision["decision"] == "APPLY":
            apply_queue.append(job_result)
    
    print("\n" + "-" * 60)
    
    # Save evaluation results
    with open("data/evaluation_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n💾 Saved evaluation results to: data/evaluation_results.json")
    
    # Save apply queue
    with open("data/apply_queue.json", "w", encoding="utf-8") as f:
        json.dump(apply_queue, f, indent=2, ensure_ascii=False)
    print(f"💾 Saved apply queue to: data/apply_queue.json")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    print(f"   Total jobs evaluated: {len(results)}")
    print(f"   ✅ APPLY: {len(apply_queue)} jobs")
    print(f"   ❌ SKIP: {len(results) - len(apply_queue)} jobs")
    
    if apply_queue:
        print(f"\n📋 APPLY QUEUE:")
        for i, job in enumerate(apply_queue, 1):
            print(f"   {i}. {job['job_title'][:40]} @ {job['company'][:25]}")
    else:
        print("\n⚠️  No jobs matched criteria. Consider adjusting settings.yaml thresholds.")
    
    print("\n" + "=" * 60)
    print("✅ DAY 12 Complete! Application queue is ready.")
    print("=" * 60)


if __name__ == "__main__":
    main()
