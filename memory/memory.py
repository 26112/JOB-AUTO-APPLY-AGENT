"""
Memory Manager - Handles persistent agent memory of applied jobs.
This prevents duplicate applications and enables safe resume/restart.
"""

import json
from pathlib import Path

MEMORY_FILE = Path("data/applied_jobs.json")


def load_memory() -> dict:
    """
    Load the agent's memory from disk.
    
    Returns:
        Dictionary containing applied jobs list
    """
    if not MEMORY_FILE.exists():
        return {"applied_jobs": []}

    return json.loads(MEMORY_FILE.read_text(encoding="utf-8"))


def save_memory(memory: dict):
    """
    Save the agent's memory to disk.
    
    Args:
        memory: Dictionary containing applied jobs list
    """
    MEMORY_FILE.write_text(
        json.dumps(memory, indent=2),
        encoding="utf-8"
    )


def job_already_applied(job_url: str) -> bool:
    """
    Check if a job has already been applied to.
    
    Args:
        job_url: URL of the job posting
        
    Returns:
        True if already applied, False otherwise
    """
    memory = load_memory()
    return job_url in memory["applied_jobs"]


def mark_job_applied(job_url: str):
    """
    Mark a job as applied to prevent re-application.
    
    Args:
        job_url: URL of the job posting
    """
    memory = load_memory()
    if job_url not in memory["applied_jobs"]:
        memory["applied_jobs"].append(job_url)
        save_memory(memory)


def get_applied_count() -> int:
    """
    Get the total number of jobs applied to.
    
    Returns:
        Number of jobs in memory
    """
    memory = load_memory()
    return len(memory["applied_jobs"])


def clear_memory():
    """
    Clear all applied jobs from memory.
    WARNING: Use with caution!
    """
    save_memory({"applied_jobs": []})
