# DAY 13 Summary - Auto-Apply (Single Job, Safe Mode)

## 🎯 Goal
Test the auto-apply flow with ONE job in safe mode - reach the application form but DO NOT submit.

## ⚠️ Safety Rules
- ❌ Apply to only ONE job
- ❌ Do NOT submit
- ❌ Do NOT loop
- ✅ Observe everything

## ✅ What Was Built

### 1. Auto-Apply Module (`portals/indeed_apply.py`)
- **`open_job()`** - Opens job page
- **`click_apply()`** - Finds and clicks Apply button (multiple selectors)
- **`detect_application_state()`** - Detects if modal/redirect/form
- **`get_page_screenshot()`** - Captures state for verification

### 2. Test Script (`portals/test_single_apply.py`)
- Opens ONE selected job
- Clicks Apply button
- Detects application state
- Takes screenshots at each step
- STOPS for manual inspection

## 📋 Selected Test Job

| Field | Value |
|-------|-------|
| **Title** | AI Engineer |
| **Company** | Dine Development Corporation |
| **Location** | Remote |
| **Experience** | 2 years |
| **Skills Match** | 8 skills |

Selected because: Not "Senior" or "Staff", lowest experience requirement.

## 🔧 How to Run

```bash
python portals/test_single_apply.py
```

## 📊 Expected Outcomes

### ✅ Case 1: Indeed Easy Apply
- Apply modal opens inside Indeed
- Form fields visible (name, email, resume)
- Screenshot captured
- STOP

### ✅ Case 2: Redirect to Company Site
- Browser navigates to company careers page
- External application form loads
- Screenshot captured
- STOP

### ❌ Case 3: Apply Not Found
- Job may have expired
- Different selector needed
- Check screenshot for debugging

## 📸 Screenshots Generated

| Screenshot | Description |
|------------|-------------|
| `data/step1_job_page.png` | Job posting page |
| `data/step2_apply_clicked.png` | After clicking Apply |
| `data/error_state.png` | If any error occurs |

## 🛑 DO NOT DO

- ❌ Don't click Submit
- ❌ Don't fill any fields
- ❌ Don't test multiple jobs today
- ❌ Don't modify form data

Today = reach the form successfully, observe, and STOP.

## ✅ DAY 13 Checklist
- [ ] One job opened
- [ ] Apply button detected
- [ ] Redirect handled (if any)
- [ ] Application form visible
- [ ] No submission made
- [ ] Screenshots captured

## ⏭️ Next Steps (Day 14+)
- Fill form fields automatically
- Handle resume upload
- Multi-job apply loop
- Track applied jobs
