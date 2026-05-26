from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic()

def write_outreach(job_title: str, company: str, strengths: list) -> dict:
    try:
        prompt = f"""
You are an expert at LinkedIn cold outreach. Write a short message to a hiring manager or recruiter.

ROLE: {job_title} at {company}

CANDIDATE'S TOP STRENGTHS FOR THIS ROLE:
{strengths}

Instructions:
- 3-4 sentences max
- Mention the specific role
- Drop one concrete achievement that's relevant
- End with a simple question or call to action
- Tone: direct, confident, not desperate
- No generic openers like "I hope this message finds you well"
- Return only the message text, no commentary
"""

        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )

        return {
            "outreach_message": response.content[0].text.strip(),
            "error": None
        }

    except Exception as e:
        return {
            "outreach_message": None,
            "error": str(e)
        }