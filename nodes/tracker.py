import sqlite3
import json
from datetime import datetime
from tools.generate_pdf import generate_pdf
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def tracker_node(state):
    company = state.get("company", "company")

    # Generate PDFs FIRST before anything else
    resume_pdf = generate_pdf(state.get("tailored_resume", ""), "resume", company)
    cover_pdf = generate_pdf(state.get("cover_letter", ""), "cover_letter", company)

    if resume_pdf["path"]:
        print(f"\n📄 Resume PDF saved: {resume_pdf['path']}")
    if cover_pdf["path"]:
        print(f"📄 Cover letter PDF saved: {cover_pdf['path']}")

    # Then save to database
    conn = sqlite3.connect(os.path.join(BASE_DIR, "data", "jobs.db"))
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_url TEXT,
            job_title TEXT,
            company TEXT,
            fit_score REAL,
            recommendation TEXT,
            stage TEXT,
            strengths TEXT,
            gaps TEXT,
            tailored_resume TEXT,
            cover_letter TEXT,
            outreach_message TEXT,
            created_at TEXT
        )
    """)

    cursor.execute("""
        INSERT INTO jobs (
            job_url, job_title, company, fit_score, recommendation,
            stage, strengths, gaps, tailored_resume, cover_letter,
            outreach_message, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        state.get("job_url"),
        state.get("job_title"),
        state.get("company"),
        state.get("fit_score"),
        state.get("recommendation"),
        "applied",
        json.dumps(state.get("matching_strengths", [])),
        json.dumps(state.get("gaps", [])),
        state.get("tailored_resume"),
        state.get("cover_letter"),
        state.get("outreach_message"),
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()

    return {
        **state,
        "resume_pdf_path": resume_pdf["path"],
        "cover_pdf_path": cover_pdf["path"],
        "application_stage": "applied",
        "steps_log": state["steps_log"] + ["Saved to tracker"]
    }