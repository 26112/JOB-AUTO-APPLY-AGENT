from resume.parser import extract_resume_text, build_resume_profile
import json


def main():
    resume_path = "resume/resume.pdf"
    text = extract_resume_text(resume_path)

    profile = build_resume_profile(text)

    with open("data/resume_profile.json", "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2)

    print("Resume profile created ✅")
    print(json.dumps(profile, indent=2))


if __name__ == "__main__":
    main()
