# Day 4 Test - Save results to file
from resume.parser import build_resume_profile
import json


def test_day4():
    """Test Day 4 extraction and save to file"""
    sample_text = """
Anuj Baghel
Full Stack Developer
anuj.baghel@gmail.com | +91 9876543210
Mumbai, India

EXPERIENCE
Senior Developer at TechCorp Pvt Ltd
2022 - Present
• Built web applications using Python and Django
• Implemented machine learning models with TensorFlow
• Led team of 5 developers

Software Engineer at Innovate Solutions Inc
2020 - 2022
• Developed REST APIs using FastAPI
• Managed AWS infrastructure
• Worked with React and Node.js

SKILLS
Python, JavaScript, React, Django, FastAPI, Machine Learning, 
TensorFlow, AWS, Docker, Git, SQL, MongoDB, HTML, CSS

EDUCATION
Bachelor of Technology in Computer Science
2016 - 2020
"""
    
    profile = build_resume_profile(sample_text)
    
    # Save to file
    with open("data/test_profile.json", "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2, ensure_ascii=False)
    
    print("=== Day 4 Test Results ===\n")
    print(f"✅ Name: {profile['name']}")
    print(f"✅ Email: {profile['email']}")
    print(f"✅ Phone: {profile['phone']}")
    print(f"✅ Location: {profile['location']}")
    print(f"\n✅ Skills Found ({len(profile['skills'])}):")
    for skill in profile['skills']:
        print(f"   • {skill}")
    print(f"\n✅ Experience: {profile['experience_years']} years")
    print(f"\n✅ Companies Found ({len(profile['companies'])}):")
    for company in profile['companies']:
        print(f"   • {company}")
    
    print(f"\n📄 Full profile saved to: data/test_profile.json")


if __name__ == "__main__":
    test_day4()
