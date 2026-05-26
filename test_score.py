from tools.scrape_job import scrape_job
from tools.score_fit import score_fit

# Load your resume
with open("data/master_resume.md", "r") as f:
    resume = f.read()

# Scrape a real job URL
result = scrape_job("https://jobs.lever.co/blablacar/6f33bec1-681f-4eaa-8e68-e894cd6fb37d")
jd = result["raw_text"]

# Score it
score = score_fit(jd, resume)

print(f"Fit score:   {score['fit_score']}/100")
print(f"Recommendation: {score['recommendation']}")
print(f"\nStrengths:")
for s in score['matching_strengths']:
    print(f"  + {s}")
print(f"\nGaps:")
for g in score['gaps']:
    print(f"  - {g}")
print(f"\nError: {score['error']}")