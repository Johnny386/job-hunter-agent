from tools.scrape_job import scrape_job

def scrape_node(state):
    result = scrape_job(state["job_url"])

    if result["error"]:
        return {
            **state,
            "errors": state["errors"] + [f"Scrape error: {result['error']}"],
            "steps_log": state["steps_log"] + ["Scrape failed"]
        }

    return {
        **state,
        "job_description": result["raw_text"],
        "steps_log": state["steps_log"] + ["Job page scraped"]
    }