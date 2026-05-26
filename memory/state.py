from typing import TypedDict, Optional, List

class JobHunterState(TypedDict):

    # ── Input ──────────────────────────────────────────
    job_url: str

    # ── Scraped from job page ──────────────────────────
    job_title: Optional[str]
    company: Optional[str]
    job_description: Optional[str]
    required_skills: Optional[List[str]]
    nice_to_have: Optional[List[str]]

    # ── Fit analysis ──────────────────────────────────
    fit_score: Optional[float]          # 0–100
    matching_strengths: Optional[List[str]]
    gaps: Optional[List[str]]
    recommendation: Optional[str]       # "apply" | "stretch" | "skip"

    # ── Generated materials ───────────────────────────
    tailored_resume: Optional[str]
    cover_letter: Optional[str]
    outreach_message: Optional[str]

    # ── Tracker ───────────────────────────────────────
    application_stage: Optional[str]    # "discovered" | "applied" | "interviewing"

    # ── Meta ──────────────────────────────────────────
    steps_log: List[str]
    errors: List[str]

    resume_pdf_path: Optional[str]
    cover_pdf_path: Optional[str]