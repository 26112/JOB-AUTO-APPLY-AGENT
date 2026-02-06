"""
Job Auto Apply Agent - Main Entry Point
Day 5: Config, Preferences & Agent Memory
"""

from resume.parser import extract_resume_text, build_resume_profile
from config.loader import load_settings
from memory.memory import load_memory
import json


def main():
    print("=" * 50)
    print("Job Auto Apply Agent - Initializing...")
    print("=" * 50)
    
    # Load configuration
    settings = load_settings()
    
    # Load agent memory
    memory = load_memory()
    
    # Extract resume profile
    print("\n📄 Loading resume...")
    text = extract_resume_text("resume/resume.pdf")
    profile = build_resume_profile(text)

    # Save profile to file
    with open("data/resume_profile.json", "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2)
    
    print("✅ Resume loaded successfully")
    
    # Display agent status
    print("\n" + "=" * 50)
    print("🤖 Agent Status")
    print("=" * 50)
    
    print(f"\n👤 Profile:")
    print(f"   Name: {profile.get('name', 'N/A')}")
    print(f"   Email: {profile.get('email', 'N/A')}")
    print(f"   Location: {profile.get('location', 'N/A')}")
    print(f"   Skills: {len(profile.get('skills', []))} detected")
    print(f"   Experience: {profile.get('experience_years', 0)} years")
    
    print(f"\n🎯 Target Job:")
    print(f"   Role: {settings['job']['title']}")
    print(f"   Location: {settings['job']['location']}")
    print(f"   Portals: {', '.join(settings['job']['portals'])}")
    print(f"   Max jobs per session: {settings['job']['max_jobs_per_session']}")
    
    print(f"\n📊 Memory:")
    print(f"   Jobs already applied: {len(memory['applied_jobs'])}")
    
    print(f"\n⚙️ Behavior:")
    print(f"   Slow mode: {settings['behavior']['slow_mode']}")
    print(f"   Delay range: {settings['behavior']['random_delay_min']}-{settings['behavior']['random_delay_max']}s")
    
    print("\n" + "=" * 50)
    print("✅ Agent initialized successfully!")
    print("=" * 50)


if __name__ == "__main__":
    main()
