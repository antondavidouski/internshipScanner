# Sheet-Opening-Monitor

A lightweight Python + GitHub Actions setup that checks a **public Google Sheet** three times per day and emails you whenever it sees a brand‑new value in the **"opening date"** column.

## Quick start
1. **Fork** this repo and add the following secrets in *Repository → Settings → Secrets*: `SHEET_CSV_URL`, `SMTP_SERVER`, `SMTP_PORT`, `SMTP_USERNAME`, `SMTP_PASSWORD`, `RECIPIENT_EMAIL`.
2. Commit something (or press *Run workflow* manually) – the Action creates `cache/last_opening_date.txt` after the first run.
3. That's it! The workflow will poll the sheet at 06:00, 14:00 and 22:00 UTC every day and notify you if it spots a fresh date.

## Directory layout

```text
sheet-opening-monitor/
├── .github/
│   └── workflows/
│       └── schedule.yml      # cron job that runs 3×/day on free GitHub Actions
├── src/
│   ├── __init__.py           # empty – marks the folder as a module
│   ├── main.py               # orchestrates the run
│   ├── sheet_checker.py      # pulls the sheet & extracts latest opening date
│   └── emailer.py            # SMTP helper
├── cache/                    # created at runtime – holds last_opening_date.txt
├── requirements.txt          # Python dependencies
├── .env.sample               # example env‑var file for local testing
├── .gitignore                # ignores .env, cache, venv etc.
└── README.md                 # setup & usage guide
```

## How it works

The system uses GitHub Actions to run on a schedule (three times per day) and check a public Google Sheet for new opening dates. When a new date is detected, it sends an email notification to the specified recipient.

## Extending / tweaking

* **Frequency** → edit the cron expression in `schedule.yml`.
* **Column name** → change `OPENING_DATE_COL` in `sheet_checker.py`.
* **Multiple recipients** → set `RECIPIENT_EMAIL` to a comma‑separated list.
* **Persistent cache alternative**: switch from the text file to an issue comment, S3 bucket, or GitHub Actions *cache* if you prefer commit‑free runs.

## Local Development

1. Copy `.env.sample` to `.env` and fill in your actual values
2. Install dependencies: `pip install -r requirements.txt`
3. Run the script: `python -m src.main`

> **Why this stack?**  GitHub Actions minutes are free for public repos (<2,000 min/month) and let us run on a cron schedule without maintaining servers. Python keeps the code terse, and a plain SMTP call (or SendGrid) works from Actions without extra infrastructure.
