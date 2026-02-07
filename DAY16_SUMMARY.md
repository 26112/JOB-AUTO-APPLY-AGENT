# DAY 16 Summary - Resume & Cover Letter Upload (Controlled)

## 🎯 Goal
Teach the agent to upload/select resume correctly - the key step for Indeed Easy Apply.

## ✅ What Was Built

### 1. File Uploader Module (`automation/file_uploader.py`)
- **`upload_resume()`** - Uploads resume PDF to file input
- **`upload_cover_letter()`** - Uploads cover letter (optional)
- **`select_existing_resume()`** - Selects from saved Indeed resumes
- **`handle_resume_upload()`** - Main function that tries multiple strategies

### 2. Updated Test Script (`portals/test_single_apply.py`)
- Now includes resume upload step (Step 6)
- Handles both file upload and existing resume selection
- Takes screenshot after upload attempt

## 📁 Resume File Setup

### Required File:
Place your resume at:
```
resume/resume.pdf
```

### File Requirements:
- Format: **PDF**
- Max size: **5 MB** (Indeed limit)
- Filename: **resume.pdf**

## 🔧 How to Run

```bash
# Step 1: Add your resume PDF
# Copy your resume to: resume/resume.pdf

# Step 2: Run the test
python portals/test_single_apply.py
```

## 🧠 Upload Strategy

The module tries multiple approaches:

| Priority | Strategy | When Used |
|----------|----------|-----------|
| 1st | Direct file upload | `<input type="file">` found |
| 2nd | Select existing resume | Radio buttons with resume names |

## 📊 Expected Output

```
STEP 6: Uploading resume (DAY 16)
----------------------------------------
📄 Resume file: resume.pdf
🔍 Found 1 file upload field(s)
   Trying upload #1: accept='.pdf,.doc,.docx', name='resume'
✅ Resume uploaded successfully: resume.pdf

📊 Summary:
   Resume upload: ✅ Success
```

## 📸 Screenshots Saved

| Screenshot | Description |
|------------|-------------|
| `step1_job_page.png` | Job posting |
| `step2_apply_clicked.png` | After Apply click |
| `step5_resume_uploaded.png` | After resume upload |

## ⚠️ If No Resume PDF

If you don't have a `resume/resume.pdf` file:
- The script will try to select an existing Indeed resume
- You may see: "⚠️ Resume PDF not found"
- Indeed may show your previously uploaded resumes as options

## 🛑 DO NOT DO TODAY

- ❌ Do not click Submit
- ❌ Do not answer screening questions
- ❌ Do not loop jobs

## ✅ DAY 16 Checklist
- [ ] Resume PDF added to `resume/` folder
- [ ] Resume upload field detected
- [ ] Resume uploaded or existing selected
- [ ] Upload confirmed in browser
- [ ] No submission made

## 🔧 Troubleshooting

### "No file upload field found"
- Indeed SmartApply may show existing resumes instead
- The `select_existing_resume()` function will handle this

### "Resume file not found"
- Add your resume PDF to `resume/resume.pdf`
- Make sure the filename is exactly `resume.pdf`

### Upload appears successful but nothing happens
- Some forms require clicking "Continue" or "Next" after upload
- This is expected - we stop before any submit actions

## ⏭️ Next Steps (Day 17+)
- Handle screening questions
- Click Continue/Next buttons
- Final submit (with confirmation)
- Multi-job apply loop
