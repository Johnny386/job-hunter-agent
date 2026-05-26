from tools.scrape_job import scrape_job
from tools.score_fit import score_fit
from tools.tailor_resume import tailor_resume
from tools.write_cover_letter import write_cover_letter
from tools.write_outreach import write_outreach

with open("data/master_resume.md", "r") as f:
    resume = f.read()

result = scrape_job("https://jobs.lever.co/blablacar/6f33bec1-681f-4eaa-8e68-e894cd6fb37d")
jd = result["raw_text"]

score = score_fit(jd, resume)
print(f"Fit score: {score['fit_score']}/100\n")

r = tailor_resume(jd, resume, score["matching_strengths"], score["gaps"])
print("=== TAILORED RESUME ===")
print(r["tailored_resume"])

c = write_cover_letter("Job Title", "Company", jd, resume, score["matching_strengths"])
print("\n=== COVER LETTER ===")
print(c["cover_letter"])

o = write_outreach("Job Title", "Company", score["matching_strengths"])
print("\n=== OUTREACH MESSAGE ===")
print(o["outreach_message"])