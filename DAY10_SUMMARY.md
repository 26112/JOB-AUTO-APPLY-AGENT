# DAY 10 Summary - Job Search Automation (Indeed)

## 🎯 Goal
Build read-only automation to search for jobs on Indeed and collect job listing URLs.

## ✅ What Was Built

### 1. Indeed Search Module (`portals/indeed.py`)
- **`build_search_url()`**: Constructs Indeed search URL with title, location, and date filters
- **`collect_job_links()`**: Scrolls through results and extracts job URLs like a human
- **`save_job_links()`**: Saves collected URLs to a file

### 2. Test Script (`portals/test_indeed_search.py`)
- Loads job preferences from `config/settings.yaml`
- Opens Indeed with persistent browser session
- Scrolls results automatically
- Collects and displays job URLs
- Saves results to `data/job_links.txt`

## 🔧 How to Run

```bash
# Activate virtual environment first
python portals/test_indeed_search.py
```

## 📊 Expected Behavior
1. ✅ Chrome opens with saved session
2. ✅ Indeed job search page loads
3. ✅ Page scrolls automatically (5 times)
4. ✅ Job URLs printed to console
5. ✅ URLs saved to `data/job_links.txt`
6. ✅ Screenshot saved to `data/indeed_search_results.png`

## 🚫 Read-Only Safety
- NO Apply button clicks
- NO tab explosions
- NO form submissions
- Just collecting URLs for later processing

## 🔧 Troubleshooting

### ❌ No jobs found
- Try changing location in `config/settings.yaml` to "India" or a city name
- Try removing "Remote" from location
- Check if Indeed changed their HTML structure

### ❌ Selectors fail
- Indeed sometimes changes class names
- The script tries multiple selectors as fallback
- Check browser console for errors

## 📁 Files Created
- `portals/__init__.py` - Package init
- `portals/indeed.py` - Indeed search module
- `portals/test_indeed_search.py` - Test script

## 📁 Output Files
- `data/job_links.txt` - Collected job URLs
- `data/indeed_search_results.png` - Screenshot of results

## ⏭️ Next Steps (Day 11+)
- Visit each job URL and extract details
- Match jobs against resume
- Build application queue
