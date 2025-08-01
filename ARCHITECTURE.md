# 🏗️ ARCHITECTURE.md

## 🎯 Overview

This project is a self-scheduling automation tool that:

* Reads a user-configured Google Sheet
* Matches today's date to a task row
* Generates a templated Google Doc with instructional content
* Creates a Google Calendar event

It is designed to be run daily via cron on a local machine (or containerized environment) and to support eventual migration to a cloud scheduler.

---

## 🧱 System Components

### 1. `scheduler.py`

* Pulls in today’s date and searches for a row in the configured Google Sheet(s)
* Ignores the sheet if today’s date is not found

### 2. `google_sheets.py`

* Connects to the specified Google Sheet
* Fetches rows from the worksheet
* Maps column headers to keys based on the user’s config

### 3. `google_docs.py`

* Renders the user-defined `template_blurb` using Jinja2 or similar
* Fills in placeholders from the sheet row (e.g. `{{ Pattern Focus }}`)
* Writes the document to the configured Drive folder

### 4. `google_calendar.py`

* Creates and schedules a Google Calendar event for the task
* Attaches the generated Google Doc
* Uses event title, description, and timing info derived from config or defaults

### 5. `main.py`

* Serves as the orchestrator
* Loads config
* Iterates over configured sheets
* Calls scheduler → sheets → docs (+ calendar)
* Logs all actions

### 6. `config_loader.py` (planned)

* Parses `config.yaml`
* Supports one or many sheets
* Validates required fields

---

## 📁 Data Flow

```text
main.py
  └── config_loader.py       # loads config.yaml
      └── scheduler.py       # finds today's row
          └── google_sheets.py
              └── returns task row
          └── google_docs.py     # fills and writes document
          └── google_calendar.py (optional)
```

---

## 📄 Configuration-Driven Design

* Each daily task results in a scheduled event
* Event metadata (title, time, description) may be derived from the config or computed from task data
  This tool is designed to be easily portable and modifiable:
* Task logic is decoupled from source schema (via column mapping)
* All inputs (sheet ID, template, etc.) are user-specified
* Document content is driven entirely by the config and sheet data

---

## 🛡️ Design Principles

* **Configurable over hardcoded**
* **Fail gracefully** (if no task found today, log and exit silently)
* **TDD-friendly**: core modules are unit-testable
* **I/O separation**: business logic is not coupled to API details
* **Secure secrets**: credentials live in `.env` and never enter version control

---

## 📦 Deployment Model

* Local CRON job running `docker run`
* Reads from local mounted `.env` + `config.yaml`
* Logs are output locally or to an optional GDrive/remote log later

---

## 🧠 Summary

This project is built to run cleanly, safely, and modularly — even when extended to cloud platforms or adapted to new workflows. With a clear config and strict module responsibilities, it serves as both a productivity tool and a showcase of thoughtful architecture.
