from tools.tailor_resume import tailor_resume
from tools.write_cover_letter import write_cover_letter
from tools.write_outreach import write_outreach
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def writer_node(state):
    with open(os.path.join(BASE_DIR, "data", "master_resume.md"), "r") as f:
        resume = f.read()

    r = tailor_resume(
        state["job_description"], resume,
        state["matching_strengths"], state["gaps"]
    )

    c = write_cover_letter(
        state.get("job_title", "this role"),
        state.get("company", "your company"),
        state["job_description"], resume,
        state["matching_strengths"]
    )

    o = write_outreach(
        state.get("job_title", "this role"),
        state.get("company", "your company"),
        state["matching_strengths"]
    )

    errors = state["errors"]
    if r["error"]: errors.append(f"Resume error: {r['error']}")
    if c["error"]: errors.append(f"Cover letter error: {c['error']}")
    if o["error"]: errors.append(f"Outreach error: {o['error']}")

    return {
        **state,
        "tailored_resume": r["tailored_resume"],
        "cover_letter": c["cover_letter"],
        "outreach_message": o["outreach_message"],
        "errors": errors,
        "steps_log": state["steps_log"] + ["Materials written"]
    }