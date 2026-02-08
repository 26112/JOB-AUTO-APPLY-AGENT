# 🤖 Job Auto-Apply Agent - Complete Project Summary

> **A fully autonomous job application bot built over 19 days**  
> Built with Python, Playwright, and intelligent automation

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Core Capabilities](#core-capabilities)
3. [System Architecture](#system-architecture)
4. [Module Breakdown](#module-breakdown)
5. [How to Use](#how-to-use)
6. [Configuration](#configuration)
7. [Safety Features](#safety-features)
8. [Troubleshooting](#troubleshooting)

---

## 🎯 Project Overview

This is a **production-ready job auto-apply agent** that:

- ✅ Parses your resume and extracts skills, experience, and contact info
- ✅ Searches job portals (Indeed) for matching positions
- ✅ Evaluates jobs against your profile (APPLY/SKIP decisions)
- ✅ Automatically fills application forms
- ✅ Uploads resume and handles cover letters
- ✅ Answers standard screening questions
- ✅ Submits applications with human confirmation
- ✅ Logs all applications to CSV/JSON/Google Sheets
- ✅ Remembers applied jobs to prevent duplicates

**Repository:** https://github.com/26112/JOB-AUTO-APPLY-AGENT

---

## 🚀 Core Capabilities

### Resume Processing (Days 3-4)
- **Skills Extraction**: Matches 60+ tech skills from master list
- **Experience Calculation**: Extracts years from date ranges
- **Contact Info**: Name, email, phone, location
- **Company Detection**: Previous employer names

**Output:** `data/resume_profile.json`

### Configuration & Memory (Day 5)
- **YAML Configuration**: Central settings file (`config/settings.yaml`)
- **Persistent Memory**: Tracks applied jobs (`data/applied_jobs.json`)
- **Duplicate Prevention**: Never applies to same job twice
- **Session Limits**: Configurable max jobs per session

### Job Description Parsing (Day 6)
- **HTML Cleaning**: BeautifulSoup4 for robust parsing
- **Information Extraction**: Title, company, location
- **Structured Profiles**: Clean JSON for decision-making

### Job Matching & Evaluation (Day 7)
- **Title Similarity**: RapidFuzz fuzzy matching
- **Skill Overlap**: Counts matching skills
- **Experience Check**: Compares years required vs yours
- **Location Check**: Strict matching with Remote support
- **Decision Output**: APPLY/SKIP with detailed reasons

**Output:** `data/evaluation_results.json`, `data/apply_queue.json`

### Browser Automation (Days 8-9)
- **Playwright Integration**: Robust Chrome control
- **Human-Like Behavior**: Random delays, slow-mo actions
- **Persistent Sessions**: Login once, stay logged in
- **Screenshot Capture**: Verification at each step

**Session Data:** `data/browser_profile/`

### Job Portal Scraping (Days 10-11)
- **Indeed Search**: Build search URLs, collect job links
- **Job Page Reading**: Extract live job profiles
- **Auto-Scrolling**: Human-like page navigation

**Output:** `data/job_links.txt`, `data/jobs_raw.json`

### Application Automation (Days 13-17)
- **Apply Button Detection**: Multiple fallback selectors
- **Form Field Inspection**: Detect all inputs, categorize by type
- **Auto-Fill Personal Info**: Smart label/placeholder matching
- **Resume Upload**: Direct upload or existing resume selection
- **Cover Letter Handling**: Paste into textarea or upload PDF
- **Screening Questions**: Auto-answer work authorization, sponsorship, etc.

### Submission & Logging (Days 18-19)
- **Human Confirmation**: Type "SUBMIT" before final action
- **Success Detection**: Check for confirmation messages
- **Memory Logging**: Mark jobs as applied
- **CSV/JSON Logging**: Local application records
- **Google Sheets**: Optional cloud logging
- **Multi-Job Sessions**: Apply to 3-5 jobs with rate limiting

---

## 🏗️ System Architecture

```
JOB AUTO APPLY AGENT/
├── automation/           # Browser control & form handling
│   ├── browser.py           # Playwright controller
│   ├── form_inspector.py    # Form field detection
│   ├── form_filler.py       # Auto-fill personal info
│   ├── file_uploader.py     # Resume/cover letter upload
│   ├── question_answerer.py # Screening question handler
│   ├── cover_letter_handler.py
│   ├── submitter.py         # Submit button logic
│   ├── success_detector.py  # Confirmation detection
│   └── rate_limiter.py      # Human-like delays
│
├── config/              # Configuration
│   ├── settings.yaml        # All agent settings
│   └── loader.py            # YAML loader
│
├── data/                # Data storage
│   ├── resume_profile.json  # Your parsed resume
│   ├── applied_jobs.json    # Memory of applied jobs
│   ├── apply_queue.json     # Jobs to apply to
│   ├── jobs_raw.json        # Scraped job profiles
│   ├── job_links.txt        # Collected job URLs
│   ├── applications_log.csv # Application history
│   ├── skills_master_list.txt
│   ├── cover_letter.txt     # Template cover letter
│   └── browser_profile/     # Persistent session
│
├── logging/             # Application logging
│   ├── memory.py            # Applied jobs tracker
│   └── sheets_logger.py     # Google Sheets integration
│
├── matching/            # Job evaluation
│   ├── job_reader.py        # JD parser
│   ├── evaluator.py         # Match decision logic
│   └── run_evaluation.py    # Batch evaluation runner
│
├── memory/              # Agent memory
│   └── memory.py            # Persistent state
│
├── portals/             # Job portal modules
│   ├── indeed.py            # Indeed search
│   ├── indeed_reader.py     # Indeed job page reader
│   ├── indeed_apply.py      # Indeed apply logic
│   └── run_apply_session.py # Multi-job session runner
│
├── resume/              # Resume files
│   ├── parser.py            # PDF text extraction
│   └── resume.pdf           # Your resume
│
└── main.py              # Entry point
```

---

## 📦 Module Breakdown

### Resume Parser (`resume/parser.py`)
```python
from resume.parser import build_resume_profile

profile = build_resume_profile(pdf_text)
# Returns: name, email, phone, location, skills, experience_years, companies
```

### Config Loader (`config/loader.py`)
```python
from config.loader import load_settings

settings = load_settings()
# Returns: job preferences, experience filters, behavior settings
```

### Memory System (`memory/memory.py`)
```python
from memory.memory import job_already_applied, mark_job_applied

if not job_already_applied(url):
    # ... apply ...
    mark_job_applied(url)
```

### Job Reader (`matching/job_reader.py`)
```python
from matching.job_reader import build_job_profile

job = build_job_profile(html)
# Returns: job_title, company, location, description
```

### Evaluator (`matching/evaluator.py`)
```python
from matching.evaluator import evaluate_job

result = evaluate_job(resume_profile, job_profile, settings)
# Returns: decision (APPLY/SKIP), score, reasons
```

### Browser Controller (`automation/browser.py`)
```python
from automation.browser import Browser

browser = Browser()
browser.start()
browser.open("https://indeed.com")
browser.screenshot("data/page.png")
browser.stop()
```

### Form Filler (`automation/form_filler.py`)
```python
from automation.form_filler import autofill_personal_info

filled = autofill_personal_info(page, resume_profile)
# Fills: email, phone, name fields
```

### Rate Limiter (`automation/rate_limiter.py`)
```python
from automation.rate_limiter import human_pause, SessionLimiter

human_pause()  # Random 30-60 second delay

limiter = SessionLimiter(max_jobs=3)
if limiter.can_continue():
    # ... apply ...
```

---

## 🔧 How to Use

### Initial Setup
```bash
# 1. Clone the repository
git clone https://github.com/26112/JOB-AUTO-APPLY-AGENT.git
cd JOB-AUTO-APPLY-AGENT

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt
playwright install chromium
```

### Quick Start Workflow
```bash
# Step 1: Parse your resume
# Place your resume at: resume/resume.pdf
python main.py

# Step 2: Save Indeed login session
python automation/test_login_session.py
# Log in manually, then close browser

# Step 3: Search for jobs
python portals/test_indeed_search.py

# Step 4: Read job details
python portals/test_indeed_job_reader.py

# Step 5: Evaluate matches
python matching/run_evaluation.py

# Step 6: Apply to jobs (with confirmation)
python portals/run_apply_session.py
```

---

## ⚙️ Configuration

### `config/settings.yaml`

```yaml
# Job Preferences
job:
  title: "Machine Learning Engineer"
  location: "Remote"
  portals: [indeed]
  max_jobs_per_session: 15
  posted_within_days: 7

# Experience Filters
experience:
  max_extra_years: 2           # Apply to jobs requiring up to your_exp + 2
  skip_senior_roles_under_years: 4

# Matching Filters
filters:
  min_title_match: 70          # Minimum title similarity %
  min_skill_match: 5           # Minimum matching skills

# Behavior Settings
behavior:
  slow_mode: true
  random_delay_min: 2
  random_delay_max: 5
```

### Tuning Tips

**To get MORE apply results:**
- Increase `max_extra_years` (e.g., 3 or 4)
- Lower `min_title_match` (e.g., 60)
- Lower `min_skill_match` (e.g., 3)

**To get FEWER apply results:**
- Decrease `max_extra_years`
- Raise `min_title_match` (e.g., 80)
- Raise `min_skill_match` (e.g., 8)

---

## 🛡️ Safety Features

| Feature | Description |
|---------|-------------|
| **Human Confirmation** | Type "SUBMIT" before final action |
| **Session Limits** | Max 3-5 jobs per session |
| **Duplicate Prevention** | Never applies to same job twice |
| **Rate Limiting** | 30-60 second delays between applications |
| **Persistent Memory** | Resume from where you left off |
| **Screenshots** | Verification at each step |

### Session Controls

| Input | Action |
|-------|--------|
| `y` | Apply to this job |
| `n` | Skip this job |
| `stop` | End session immediately |
| `Ctrl+C` | Emergency stop |

---

## 🔧 Troubleshooting

### "No jobs found"
- Try changing location in `config/settings.yaml`
- Remove "Remote" from location
- Check if Indeed changed their HTML structure

### "Apply button not found"
- Ensure you're logged into Indeed
- Run `python automation/test_login_session.py`

### "No fields were auto-filled"
- You may be on the login page, not the application form
- Refresh Indeed login session first

### "Submit button not found"
- The form may have multiple pages
- Check if Continue/Next buttons were clicked

### "All jobs already applied"
- Search for more jobs (run Indeed search)
- Re-evaluate to build new queue

### Rate limited by Indeed
- Increase delay times in `rate_limiter.py`
- Reduce `MAX_PER_SESSION`
- Take longer breaks between sessions

---

## 📊 Screening Questions Auto-Answered

| Question Type | Answer | Detection Pattern |
|--------------|--------|-------------------|
| Work authorization | Yes | "authorized to work", "legally authorized" |
| Sponsorship required | No | "sponsorship", "require visa" |
| Willing to relocate | Yes | "relocate", "willing to move" |
| Remote work | Yes | "remote", "work from home" |
| Start date | 2 weeks | Dropdown selection |
| Salary | Negotiable | Dropdown selection |
| Years experience | From profile | Text input |

---

## 📁 Key Output Files

| File | Description |
|------|-------------|
| `data/resume_profile.json` | Parsed resume data |
| `data/applied_jobs.json` | Memory of applied jobs |
| `data/apply_queue.json` | Jobs ready to apply |
| `data/jobs_raw.json` | Scraped job profiles |
| `data/job_links.txt` | Collected job URLs |
| `data/applications_log.csv` | Application history |
| `data/evaluation_results.json` | All job evaluations |
| `data/last_session_results.json` | Latest session summary |

---

## 🎉 What You've Built

A **production-ready AI agent** that:

1. 🧠 **Understands** your resume and extracts key information
2. 🔍 **Searches** job portals for relevant positions
3. ⚖️ **Evaluates** each job against your qualifications
4. 📝 **Fills** application forms automatically
5. 📎 **Uploads** resume and cover letters
6. ✅ **Answers** screening questions intelligently
7. 🚀 **Submits** applications with safety confirmations
8. 📊 **Logs** everything for tracking

**This is enterprise-level automation!** 🏆

---

## ⏭️ Future Enhancements

- Scheduled sessions (morning/evening)
- LinkedIn integration
- Dashboard and analytics
- Email notifications
- Multi-portal support (Glassdoor, LinkedIn, etc.)
- AI-powered cover letters (per job customization)

---

**Repository:** https://github.com/26112/JOB-AUTO-APPLY-AGENT

**Happy job hunting! 🚀**
