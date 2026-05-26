import os
import json
from anthropic import Anthropic
from dotenv import load_dotenv
import re

def clean_markdown(text: str) -> str:
    text = re.sub(r'#{1,6}\s*', '', text)        # remove ## headings
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text) # remove **bold**
    text = re.sub(r'\*(.*?)\*', r'\1', text)      # remove *italic*
    text = re.sub(r'•\s*--', '', text)            # remove bullet dividers
    text = re.sub(r'-{2,}', '', text)             # remove -- separators
    return text.strip()

load_dotenv()
client = Anthropic()

def tailor_resume(job_description: str, master_resume: str, strengths: list, gaps: list) -> dict:
    try:
        prompt = f"""
You are an expert resume writer. Rewrite the candidate's resume to better match this job description.

JOB DESCRIPTION:
{job_description}

ORIGINAL RESUME:
{master_resume}

KNOWN STRENGTHS FOR THIS ROLE:
{strengths}

KNOWN GAPS TO MINIMIZE:
{gaps}

Instructions:
- Keep all facts truthful — do not invent experience
- Mirror keywords and language from the job description naturally
- Reorder and reframe bullet points to highlight the most relevant experience first
- Keep the same structure but sharpen the language
- Return the full rewritten resume as plain text, no commentary
"""

        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        return {
            "tailored_resume": clean_markdown(response.content[0].text.strip()),
            "error": None
        }

    except Exception as e:
        return {
            "tailored_resume": None,
            "error": str(e)
        }