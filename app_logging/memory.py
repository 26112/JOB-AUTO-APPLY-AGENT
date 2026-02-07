"""
Application Memory Module - DAY 18

Tracks applied jobs to prevent duplicate applications.
Stores application history in JSON format.
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

APPLIED_JOBS_FILE = Path(__file__).parent.parent / "data" / "applied_jobs.json"


def load_applied_jobs() -> list:
    """
    Load list of previously applied jobs.
    
    Returns:
        list: List of applied job records
    """
    if not APPLIED_JOBS_FILE.exists():
        return []
    
    try:
        with open(APPLIED_JOBS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except:
        return []


def save_applied_jobs(jobs: list):
    """
    Save applied jobs list to file.
    
    Args:
        jobs: List of applied job records
    """
    with open(APPLIED_JOBS_FILE, 'w', encoding='utf-8') as f:
        json.dump(jobs, f, indent=2, ensure_ascii=False)


def is_job_applied(job_url: str) -> bool:
    """
    Check if a job has already been applied to.
    
    Args:
        job_url: URL of the job
    
    Returns:
        bool: True if job was already applied to
    """
    jobs = load_applied_jobs()
    
    for job in jobs:
        if job.get("url") == job_url:
            return True
    
    return False


def mark_job_applied(job_url: str, job_data: dict = None, status: str = "APPLIED") -> dict:
    """
    Mark a job as applied.
    
    Args:
        job_url: URL of the job
        job_data: Optional job details dictionary
        status: Application status
    
    Returns:
        dict: The applied job record
    """
    jobs = load_applied_jobs()
    
    # Create job record
    record = {
        "url": job_url,
        "applied_at": datetime.now().isoformat(),
        "status": status,
        "portal": "Indeed"
    }
    
    # Add job details if provided
    if job_data:
        record["job_title"] = job_data.get("job_title", "Unknown")
        record["company"] = job_data.get("company", "Unknown")
        record["location"] = job_data.get("location", "Unknown")
    
    jobs.append(record)
    save_applied_jobs(jobs)
    
    print(f"💾 Job marked as applied: {record.get('job_title', job_url[:50])}")
    return record


def get_application_stats() -> dict:
    """
    Get statistics about applications.
    
    Returns:
        dict: Application statistics
    """
    jobs = load_applied_jobs()
    
    stats = {
        "total_applied": len(jobs),
        "by_status": {},
        "by_portal": {},
        "today": 0
    }
    
    today = datetime.now().date().isoformat()
    
    for job in jobs:
        # Count by status
        status = job.get("status", "UNKNOWN")
        stats["by_status"][status] = stats["by_status"].get(status, 0) + 1
        
        # Count by portal
        portal = job.get("portal", "Unknown")
        stats["by_portal"][portal] = stats["by_portal"].get(portal, 0) + 1
        
        # Count today's applications
        applied_at = job.get("applied_at", "")
        if applied_at.startswith(today):
            stats["today"] += 1
    
    return stats


def print_application_summary():
    """
    Print a summary of applications.
    """
    stats = get_application_stats()
    
    print("\n" + "=" * 40)
    print("📊 APPLICATION SUMMARY")
    print("=" * 40)
    print(f"   Total applied: {stats['total_applied']}")
    print(f"   Today: {stats['today']}")
    
    if stats["by_status"]:
        print("\n   By Status:")
        for status, count in stats["by_status"].items():
            print(f"      {status}: {count}")
    
    if stats["by_portal"]:
        print("\n   By Portal:")
        for portal, count in stats["by_portal"].items():
            print(f"      {portal}: {count}")
    
    print("=" * 40)
