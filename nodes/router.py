from langgraph.graph import END

def route_by_fit_score(state):
    score = state.get("fit_score", 0)
    if score >= 70:
        return "write_materials"
    elif score >= 40:
        return "ask_user"
    else:
        return END