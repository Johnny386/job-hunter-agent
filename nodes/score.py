from tools.score_fit import score_fit
import os


def score_node(state):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(BASE_DIR, "data", "master_resume.md"), "r") as f:
        resume = f.read()

    result = score_fit(state["job_description"], resume)

    if result["error"]:
        return {
            **state,
            "errors": state["errors"] + [f"Score error: {result['error']}"],
            "steps_log": state["steps_log"] + ["Scoring failed"]
        }

    return {
        **state,
        "job_title": result["job_title"],
        "company": result["company"],
        "fit_score": result["fit_score"],
        "matching_strengths": result["matching_strengths"],
        "gaps": result["gaps"],
        "recommendation": result["recommendation"],
        "steps_log": state["steps_log"] + [f"Fit scored: {result['fit_score']}/100"]
    }