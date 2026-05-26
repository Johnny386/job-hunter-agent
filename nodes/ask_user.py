def ask_user_node(state):
    print(f"\nFit score: {state['fit_score']}/100")
    print(f"Strengths: {state['matching_strengths']}")
    print(f"Gaps: {state['gaps']}")
    answer = input("\nThis is a medium fit. Apply anyway? (yes/no): ").strip().lower()

    if answer == "yes":
        return {
            **state,
            "steps_log": state["steps_log"] + ["User chose to apply"]
        }
    else:
        return {
            **state,
            "recommendation": "skip",
            "steps_log": state["steps_log"] + ["User chose to skip"]
        }