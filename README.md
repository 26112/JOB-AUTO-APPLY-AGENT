# Job Auto-Apply Bot

An intelligent automation bot for job applications using AI and web automation.

## Project Setup - Day 1 ✅

### Environment
- Python virtual environment (venv)
- Dependencies installed
- Project structure initialized

### Libraries
- playwright - Web automation
- pdfplumber - Resume parsing
- python-dotenv - Environment variables
- rapidfuzz - Fuzzy matching
- pyyaml - Configuration files
- gspread - Google Sheets integration
- oauth2client - OAuth authentication
- openai - AI integration

### Configuration
- Settings stored in `config/settings.yaml`
- Environment variables in `.env`

### How to Run
1. Activate virtual environment:
   ```
   venv\Scripts\activate
   ```

2. Run the bot:
   ```
   python main.py
   ```

## Project Structure
```
job-auto-apply-bot/
├── main.py              # Entry point
├── README.md            # This file
├── .env                 # Environment variables
├── config/              # Configuration files
│   └── settings.yaml
├── resume/              # Resume parsing module
│   └── parser.py
├── ai/                  # AI integration
├── matching/            # Job matching logic
├── portals/             # Job portal integrations
├── automation/          # Automation scripts
├── logging/             # Logging utilities
└── data/                # Data storage
```

## Next Steps
Day 2 and beyond will add:
- Resume parsing
- AI-powered matching
- Web automation for job portals
- Application tracking
