"""
Google Sheets Logger Module - DAY 18

Logs job applications to a Google Sheet for tracking.
Requires Google API credentials (credentials.json).

Setup:
1. Create a Google Cloud project
2. Enable Google Sheets API and Drive API
3. Create a Service Account
4. Download credentials.json and place in project root
5. Share your Google Sheet with the service account email
"""

import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def log_to_sheet(sheet_url: str, job: dict, status: str = "APPLIED") -> bool:
    """
    Log a job application to Google Sheets.
    
    Args:
        sheet_url: URL of the Google Sheet
        job: Job data dictionary
        status: Application status
    
    Returns:
        bool: True if logging was successful
    """
    try:
        import gspread
        from oauth2client.service_account import ServiceAccountCredentials
    except ImportError:
        print("⚠️ Google Sheets libraries not installed")
        print("   Run: pip install gspread oauth2client")
        return False
    
    credentials_file = Path(__file__).parent.parent / "credentials.json"
    
    if not credentials_file.exists():
        print("⚠️ credentials.json not found")
        print("   Google Sheets logging skipped")
        return False
    
    try:
        # Set up credentials
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            str(credentials_file), scope
        )
        client = gspread.authorize(creds)
        
        # Open sheet
        sheet = client.open_by_url(sheet_url).sheet1
        
        # Prepare row data
        row = [
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            job.get("company", "Unknown"),
            job.get("job_title", "Unknown"),
            job.get("location", "Unknown"),
            "Indeed",
            status,
            job.get("url", "")
        ]
        
        # Append row
        sheet.append_row(row)
        
        print(f"📊 Logged to Google Sheets: {job.get('job_title', 'Unknown')}")
        return True
        
    except Exception as e:
        print(f"⚠️ Google Sheets logging failed: {e}")
        return False


def log_to_csv(job: dict, status: str = "APPLIED", csv_path: str = "data/applications_log.csv") -> bool:
    """
    Log a job application to a local CSV file (fallback if Sheets not available).
    
    Args:
        job: Job data dictionary
        status: Application status
        csv_path: Path to CSV file
    
    Returns:
        bool: True if logging was successful
    """
    import csv
    
    csv_file = Path(__file__).parent.parent / csv_path
    
    # Check if file exists (to write header)
    file_exists = csv_file.exists()
    
    try:
        with open(csv_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Write header if new file
            if not file_exists:
                writer.writerow([
                    "Date",
                    "Company",
                    "Job Title",
                    "Location",
                    "Portal",
                    "Status",
                    "URL"
                ])
            
            # Write job data
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M"),
                job.get("company", "Unknown"),
                job.get("job_title", "Unknown"),
                job.get("location", "Unknown"),
                "Indeed",
                status,
                job.get("url", "")
            ])
        
        print(f"📄 Logged to CSV: {csv_path}")
        return True
        
    except Exception as e:
        print(f"⚠️ CSV logging failed: {e}")
        return False


def log_application(job: dict, sheet_url: str = None, status: str = "APPLIED") -> dict:
    """
    Log a job application using all available methods.
    
    Args:
        job: Job data dictionary
        sheet_url: Optional Google Sheet URL
        status: Application status
    
    Returns:
        dict: Logging results
    """
    results = {
        "sheets": False,
        "csv": False
    }
    
    # Try Google Sheets
    if sheet_url:
        results["sheets"] = log_to_sheet(sheet_url, job, status)
    
    # Always log to CSV as backup
    results["csv"] = log_to_csv(job, status)
    
    return results
