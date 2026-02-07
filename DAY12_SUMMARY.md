# DAY 12 Summary - Live Job Evaluation & Application Queue

## 🎯 Goal
Evaluate real Indeed jobs against your resume and create an application queue with APPLY/SKIP decisions.

## ✅ What Was Built

### 1. Evaluation Runner (`matching/run_evaluation.py`)
- Loads resume profile, scraped jobs, and settings
- Runs each job through the Day 7 evaluator
- Generates decisions with detailed reasoning
- Creates application queue file

### 2. Resume Profile (`data/resume_profile.json`)
- 38 ML-focused skills
- 3 years experience
- Target: Machine Learning Engineer
- Location: Remote

## 🔧 How to Run

```bash
python matching/run_evaluation.py
```

## 📊 Evaluation Results

| Total Jobs | APPLY | SKIP |
|------------|-------|------|
| 10 | 4 (40%) | 6 (60%) |

### ✅ APPLY Queue (4 jobs)

| # | Job Title | Company | Title Match | Skills | Exp |
|---|-----------|---------|-------------|--------|-----|
| 1 | Senior ML Engineer | Tebra | 100% | 18 | 5yr |
| 2 | Senior ML Engineer | Workiva | 100% | 9 | 2yr |
| 3 | Staff Software Engineer - ML | General Motors | 100% | 7 | 4yr |
| 4 | AI Engineer | Dine Development Corp | 84% | 8 | 2yr |

### ❌ SKIP Reasons (6 jobs)

| Job | Company | Reason |
|-----|---------|--------|
| Junior AI/ML Engineer | Therapy Brands | Location mismatch (Columbus, OH) |
| Senior Applied ML Engineer | HPE | Location mismatch (Houston, TX) |
| Staff ML Engineer | Cohere Health | Experience exceeds limit (8yr > 5yr) |
| Staff ML Engineer (GenAI) | Redwood Logistics | Experience exceeds limit (8yr > 5yr) |
| Lead ML Engineer - NBA | Humana | Experience exceeds limit (8yr > 5yr) |
| Staff ML Engineer: Personalization | PrizePicks | Experience exceeds limit (7yr > 5yr) |

## 📁 Output Files

### `data/evaluation_results.json`
Complete evaluation for all jobs with metrics and reasons.

### `data/apply_queue.json`
Only jobs marked APPLY - ready for auto-apply system.

## ⚙️ Current Thresholds (`config/settings.yaml`)

```yaml
filters:
  min_title_match: 70      # Minimum title similarity %
  min_skill_match: 5       # Minimum matching skills

experience:
  max_extra_years: 2       # Max years above your experience
```

With 3 years experience + 2 extra = jobs requiring up to 5 years pass.

## 🔧 Tuning Tips

To get **more APPLY** results:
- Increase `max_extra_years` (e.g., 3 or 4)
- Lower `min_title_match` (e.g., 60)
- Lower `min_skill_match` (e.g., 3)

To get **fewer APPLY** results:
- Decrease `max_extra_years`
- Raise `min_title_match` (e.g., 80)
- Raise `min_skill_match` (e.g., 8)

## ✅ DAY 12 Checklist
- [x] Live jobs evaluated
- [x] Decisions generated (APPLY/SKIP)
- [x] Reasons logged for each decision
- [x] Apply queue created (4 jobs)
- [x] Results saved to disk

## ⏭️ Next Steps (Day 13+)
- Auto-apply to jobs in the queue
- Track applied jobs
- Handle application forms
