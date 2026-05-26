import os
import json
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic()

def score_fit(job_description: str, master_resume: str) -> dict:
    try:
        prompt = f"""
You are an expert recruiter. Analyze this job description and candidate resume.

JOB DESCRIPTION:
{job_description}

CANDIDATE RESUME:
{master_resume}

Return ONLY a JSON object with exactly these fields, no explanation, no markdown:
{{
    "job_title": "<extracted job title from the JD>",
    "company": "<extracted company name from the JD>",
    "fit_score": <integer 0-100>,
    "matching_strengths": [<list of strings, max 5>],
    "gaps": [<list of strings, max 5>],
    "recommendation": "<apply|stretch|skip>"
}}

Scoring guide:
- 70-100: strong match, candidate meets most requirements
- 40-69: partial match, worth applying with tailoring
- 0-39: poor match, significant gaps
"""

        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )

        raw = response.content[0].text.strip()

        # Strip markdown code fences if present
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
            raw = raw.strip()

        result = json.loads(raw)

        return {
            "job_title": result["job_title"],
            "company": result["company"],
            "fit_score": result["fit_score"],
            "matching_strengths": result["matching_strengths"],
            "gaps": result["gaps"],
            "recommendation": result["recommendation"],
            "error": None
}

    except Exception as e:
        return {
            "job_title": None,
            "company": None,
            "fit_score": 0,
            "matching_strengths": [],
            "gaps": [],
            "recommendation": "skip",
            "error": str(e)
        }