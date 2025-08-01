# 🧠 Daily Task Generator

This project automates the generation of daily tasks using data from a configurable Google Sheet. It creates a templated Google Doc containing the day's algorithm topic and problem, integrating with Google Calendar.

---

## 📌 Purpose

Designed for consistency and automation, this tool:

* Reads a structured schedule from Google Sheets
* Generates a Google Doc based on the current date and predefined template
* Creates a Google Calendar reminder
* Runs as a local CRON job in a Docker container

Ideal for self-paced learners who want daily, auto-generated problem-solving tasks with no manual tracking.

---

## ✅ Features (MVP)

* 📅 Date-based scheduling (acts only if today’s row exists)
* 📄 Configurable Google Sheets source
* 🧩 Jinja2-style template rendering into Google Docs
* 🗂 Output to a specific Google Drive folder
* 🔐 Secure credential storage via `.env`
* 🐳 Docker support for clean deployment

---

## 🧪 Planned Tech Stack

* **Python 3**
* **gspread / Google API Python Client** (Docs, Sheets, Calendar)
* **Jinja2** (for template rendering)
* **Docker**
* **pytest** (TDD)
* **cron** (for scheduling)

---

## 🧃 User Stories

* 🗂 **STORY-001**: As a user, I want the correct task from a Google Sheet so that I know which topic to study today.
* 📝 **STORY-002**: As a user, I want to auto-generate a Google Doc with instructions so that I can quickly reference my primary focus for the day.
* ⏰ **STORY-003**: As a user, I want Calendar notifications daily so that I don't forget.
* 🤖 **STORY-004**: As a user, I want this process to be automatic so that I can spend more time focusing on my tasks.
* 📦 **STORY-005**: As a developer, I want the script to be containerized so that I can deploy it later to the cloud.

## 🚀 Getting Started

```bash
# Clone the repo
$ git clone https://github.com/your-username/leetcode-daily-docs.git
$ cd leetcode-daily-docs

# Create your .env file
$ cp .env.example .env

# Install dependencies (if running natively)
$ pip install -r requirements.txt

# Run the script manually
$ python src/main.py

# Or build and run via Docker
$ docker build -t leetcode-daily-docs .
$ docker run --env-file .env leetcode-daily-docs
```

---

## 🛠 Configuration

Create a `config.yaml` file to define which Sheet to use, what columns to extract, and how to build the daily blurb:

```yaml
sheets:
  - name: LeetCode Sheet
    id: "your-google-sheet-id"
    worksheet: "Schedule"
    date_column: "Date"
    output_folder_id: "your-drive-folder-id"
    template_blurb: >
      Today's focus is on {{ Pattern Focus }}.
      You'll solve: {{ Problem Title }} ({{ LeetCode Link }})
    column_mapping:
      Pattern Focus: "Pattern Focus"
      Problem Title: "Problem Title"
      LeetCode Link: "LeetCode Link"
```

---

## 🧱 Project Structure

```
leetcode-daily-docs/
├── src/
│   ├── __init__.py
│   ├── main.py                  # Entrypoint for cron execution
│   ├── scheduler.py             # Controls high-level logic for daily task
│   ├── google_sheets.py         # Pulls today's task row from Google Sheets
│   ├── google_docs.py           # Fills template and writes to Google Docs
│   ├── google_calendar.py       # Creates a Google Calendar event
│   ├── config_loader.py         # Loads and validates config.yaml
│   └── utils.py                 # Logging, date parsing, etc.
│
├── templates/
│   └── default_blurb.j2         # Optional: Jinja2 blurb file if not inline
│
├── tests/
│   ├── __init__.py
│   ├── test_scheduler.py
│   ├── test_google_sheets.py
│   ├── test_google_docs.py
│   ├── test_google_calendar.py
│   ├── test_config_loader.py
│   └── fixtures/
│       └── mock_schedule.csv    # Optional test data
│
├── config.yaml                  # Main runtime configuration
├── .env.example                 # Template for secret keys (gitignored)
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Containerized execution
├── Makefile                     # Optional: `make run`, `make test`, etc.
├── cronjob.txt                  # Example crontab entry
├── README.md                    # Project usage and onboarding
├── ARCHITECTURE.md              # System design and boundaries
└── .gitignore                   # Ignore .env, __pycache__, etc.
```

---

## 📄 License

MIT

---

## 🤝 Contributions

PRs welcome. Please open an issue first for discussion if adding a feature.

---

## 👨‍💻 Author

Brandon Dunbar

---

> "If it’s not automated, it’s broken."
