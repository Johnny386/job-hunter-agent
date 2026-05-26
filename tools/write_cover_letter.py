from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic()

def write_cover_letter(job_title: str, company: str, job_description: str, master_resume: str, strengths: list) -> dict:
    try:
        prompt = f"""
You are an expert cover letter writer. Write a compelling, concise cover letter for this role.

ROLE: {job_title} at {company}

JOB DESCRIPTION:
{job_description}

CANDIDATE RESUME:
{master_resume}

TOP STRENGTHS FOR THIS ROLE:
{strengths}

Instructions:
- 3 short paragraphs max
- Opening: why this role and company specifically
- Middle: 2-3 concrete achievements that directly match the requirements
- Closing: confident call to action
- Tone: professional but human, not generic
- Do not start with "I am writing to apply"
- Return only the cover letter text, no subject line, no commentary
"""

        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )

        return {
            "cover_letter": response.content[0].text.strip(),
            "error": None
        }

    except Exception as e:
        return {
            "cover_letter": None,
            "error": str(e)
        }