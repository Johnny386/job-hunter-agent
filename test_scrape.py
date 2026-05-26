from tools.scrape_job import scrape_job

url = "https://jobs.lever.co/blablacar/6f33bec1-681f-4eaa-8e68-e894cd6fb37d"

result = scrape_job(url)

if result["error"]:
    print("❌ Error:", result["error"])
else:
    print("✅ Success — first 500 chars:")
    print(result["raw_text"])