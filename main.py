from graph import build_graph

def run(job_url: str):
    graph = build_graph()

    initial_state = {
        "job_url": job_url,
        "job_title": None,
        "company": None,
        "job_description": None,
        "required_skills": None,
        "nice_to_have": None,
        "fit_score": None,
        "matching_strengths": [],
        "gaps": [],
        "recommendation": None,
        "tailored_resume": None,
        "cover_letter": None,
        "outreach_message": None,
        "application_stage": None,
        "steps_log": [],
        "errors": []
    }

    print("Running job hunter agent...\n")
    result = graph.invoke(initial_state)

    print("\n=== RESULTS ===")
    print(f"Fit score:    {result['fit_score']}/100")
    print(f"Recommendation: {result['recommendation']}")
    print(f"\nSteps: {result['steps_log']}")

    if result.get("tailored_resume"):
        print("\n=== TAILORED RESUME ===")
        print(result["tailored_resume"])

    if result.get("cover_letter"):
        print("\n=== COVER LETTER ===")
        print(result["cover_letter"])

    if result.get("outreach_message"):
        print("\n=== OUTREACH MESSAGE ===")
        print(result["outreach_message"])

    if result.get("errors"):
        print("\n=== ERRORS ===")
        for e in result["errors"]:
            print(f"  - {e}")

if __name__ == "__main__":
    url = input("Paste job URL: ").strip()
    run(url)