"""
Job Matching & Evaluation Engine - The brain that decides Apply or Skip
"""

import re
from rapidfuzz import fuzz


def title_similarity(resume_title: str, job_title: str) -> int:
    """
    Calculate similarity between resume target title and job title.
    
    Args:
        resume_title: User's target job title from config
        job_title: Actual job posting title
        
    Returns:
        Similarity score (0-100)
    """
    if not resume_title or not job_title:
        return 0
    return fuzz.token_set_ratio(resume_title.lower(), job_title.lower())


def skill_overlap(resume_skills: list, job_description: str) -> int:
    """
    Count how many resume skills appear in the job description.
    
    Args:
        resume_skills: List of skills from resume
        job_description: Full job description text
        
    Returns:
        Number of matching skills
    """
    job_text = job_description.lower()
    matched = []

    for skill in resume_skills:
        if skill.lower() in job_text:
            matched.append(skill)

    return len(set(matched))


def extract_job_experience(text: str) -> int:
    """
    Extract years of experience required from job description.
    
    Args:
        text: Job description text
        
    Returns:
        Years of experience required (0 if not found)
    """
    match = re.search(r"(\d+)\+?\s+years", text.lower())
    return int(match.group(1)) if match else 0


def location_match(user_location: str, job_location: str) -> bool:
    """
    Check if job location matches user preference.
    
    Args:
        user_location: User's preferred location
        job_location: Job's location
        
    Returns:
        True if locations match or job is remote
    """
    if "remote" in job_location.lower():
        return True
    return user_location.lower() in job_location.lower()


def evaluate_job(resume: dict, job: dict, settings: dict) -> dict:
    """
    Main evaluation function - decides whether to apply or skip.
    
    Args:
        resume: Resume profile dictionary
        job: Job profile dictionary
        settings: Configuration settings
        
    Returns:
        Decision dictionary with scores and reasoning
    """
    # Calculate metrics
    score = title_similarity(settings["job"]["title"], job["job_title"])
    skills = skill_overlap(resume["skills"], job["description"])
    job_exp = extract_job_experience(job["description"])
    max_exp = resume["experience_years"] + settings["experience"]["max_extra_years"]

    # Initialize decision object
    decision = {
        "title_match": score,
        "skill_match": skills,
        "job_experience": job_exp,
        "user_experience": resume["experience_years"],
        "max_allowed_experience": max_exp,
        "decision": "SKIP",
        "reasons": []
    }

    # Apply filters
    if score < settings["filters"]["min_title_match"]:
        decision["reasons"].append(f"Low title match ({score}% < {settings['filters']['min_title_match']}%)")

    if skills < settings["filters"]["min_skill_match"]:
        decision["reasons"].append(f"Insufficient skill match ({skills} < {settings['filters']['min_skill_match']})")

    if job_exp > max_exp:
        decision["reasons"].append(f"Experience exceeds limit ({job_exp} years > {max_exp} years)")

    if not location_match(resume["location"], job["location"]):
        decision["reasons"].append(f"Location mismatch ({resume.get('location', 'N/A')} vs {job['location']})")

    # Final decision
    if not decision["reasons"]:
        decision["decision"] = "APPLY"
        decision["reasons"] = ["All criteria met"]

    return decision


def get_match_summary(decision: dict) -> str:
    """
    Get a human-readable summary of the matching decision.
    
    Args:
        decision: Decision dictionary from evaluate_job
        
    Returns:
        Formatted summary string
    """
    emoji = "✅" if decision["decision"] == "APPLY" else "❌"
    
    summary = f"{emoji} {decision['decision']}\n"
    summary += f"Title Match: {decision['title_match']}%\n"
    summary += f"Skill Match: {decision['skill_match']} skills\n"
    summary += f"Experience: {decision['job_experience']} years required (you have {decision.get('user_experience', 0)})\n"
    summary += f"\nReasons:\n"
    
    for reason in decision["reasons"]:
        summary += f"  • {reason}\n"
    
    return summary
