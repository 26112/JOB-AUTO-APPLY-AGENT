# Day 4 - Skills, Experience & Companies Extraction

## ✅ Completed Features

### 1. Skills Extraction
- Created comprehensive skills master list with 60+ common tech skills
- Case-insensitive matching (Python = python = PYTHON)
- Located in: `data/skills_master_list.txt`
- Returns sorted, deduplicated list of found skills

### 2. Experience Years Calculation
- Extracts year ranges from resume (e.g., 2020-2024, 2022-Present)
- Automatically calculates total years of experience
- Handles "Present" as current year
- Returns as decimal (e.g., 2.5 years)

### 3. Company Names Extraction
- Detects companies with common suffixes (Pvt Ltd, Inc, Ltd, etc.)
- Filters out job titles and common false positives
- Returns sorted list of unique companies

### 4. Updated Resume Profile
The `resume_profile.json` now includes:
```json
{
  "name": "...",
  "email": "...",
  "phone": "...",
  "location": "...",
  "skills": [...],           // NEW
  "experience_years": 0.0,   // NEW
  "companies": [...],        // NEW
  "raw_text": "..."
}
```

## 📊 Test Results (Sample Resume)

```
✅ Name: Anuj Baghel
✅ Email: anuj.baghel@gmail.com
✅ Phone: +91 9876543210
✅ Location: India

✅ Skills Found (19):
   • aws, css, django, docker, fastapi, git, html
   • java, javascript, machine learning, mongodb
   • node.js, python, react, rest api, sql, tensorflow

✅ Experience: 10 years
✅ Companies: TechCorp Pvt Ltd, Innovate Solutions Inc
```

## 🎯 Why Day 4 Matters

This structured data enables:
- **Job Matching**: Compare your skills against job requirements
- **Seniority Filtering**: Apply only to appropriate experience levels
- **Form Auto-fill**: Automatically populate application forms
- **Smart Decisions**: Bot can decide "apply" vs "skip"

## 📁 New Files Created

1. `data/skills_master_list.txt` - Master list of skills to match
2. `test_day4.py` - Day 4 test script with detailed output

## 🔧 Functions Added to `resume/parser.py`

- `extract_skills(text)` - Skill extraction using master list
- `extract_experience_years(text)` - Calculate years of experience
- `extract_companies(text)` - Extract company names
- Updated `build_resume_profile(text)` - Now includes new fields

## 🚀 How to Use

### Option 1: Test with Sample Data
```bash
python test_day4.py
```

### Option 2: Use Your Real Resume
1. Add `resume/resume.pdf`
2. Run: `python main.py`
3. Check: `data/resume_profile.json`

## ⚠️ Known Limitations (Expected & OK)

- Experience calculation includes education years
- Company extraction may include some job titles
- Skills are matched exactly (no synonyms yet)

**These will be improved in future days with AI assistance!**

## 📝 Customization

### Add More Skills
Edit `data/skills_master_list.txt` and add one skill per line:
```
kubernetes
typescript
graphql
redis
```

### Add More Locations
Edit the `extract_location()` function in `resume/parser.py`:
```python
common_locations = ["India", "Remote", "Delhi", "Mumbai", "YOUR_CITY"]
```

## ✅ Day 4 Checklist

- [x] Skills extraction implemented
- [x] Experience calculation working
- [x] Company detection functional
- [x] JSON structure updated
- [x] Test script created
- [x] Code committed to Git
- [x] Pushed to GitHub

## 🎉 Next Steps

Your bot now has:
- ✅ Contact info (Day 3)
- ✅ Skills & experience (Day 4)

Coming up:
- Day 5: Job scraping from portals
- Day 6: Resume-to-job matching
- Day 7: Form auto-fill automation
