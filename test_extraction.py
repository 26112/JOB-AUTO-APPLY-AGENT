# Day 3 Testing Script
# This allows you to test the extraction with sample text if you don't have the PDF ready yet

from resume.parser import build_resume_profile
import json


def test_with_sample_text():
    """Test extraction with sample resume text"""
    sample_text = """
Anuj Baghel
Full Stack Developer
anuj.baghel@gmail.com | +91 9876543210
Mumbai, India

EXPERIENCE
Senior Developer at TechCorp
2022 - Present

SKILLS
Python, JavaScript, React, Django

EDUCATION
Bachelor of Technology
2018 - 2022
"""
    
    profile = build_resume_profile(sample_text)
    
    print("=== Testing Resume Extraction ===\n")
    print(json.dumps(profile, indent=2, ensure_ascii=False))
    
    print("\n=== Extraction Results ===")
    print(f"✅ Name: {profile['name']}")
    print(f"✅ Email: {profile['email']}")
    print(f"✅ Phone: {profile['phone']}")
    print(f"✅ Location: {profile['location']}")


if __name__ == "__main__":
    test_with_sample_text()
