from langgraph.graph import StateGraph, END
from memory.state import JobHunterState
from nodes.scrape import scrape_node
from nodes.score import score_node
from nodes.router import route_by_fit_score
from nodes.writer import writer_node
from nodes.ask_user import ask_user_node
from nodes.tracker import tracker_node

def build_graph():
    builder = StateGraph(JobHunterState)

    # Add nodes
    builder.add_node("scrape", scrape_node)
    builder.add_node("score", score_node)
    builder.add_node("ask_user", ask_user_node)
    builder.add_node("write_materials", writer_node)
    builder.add_node("save_to_tracker", tracker_node)

    # Entry point
    builder.set_entry_point("scrape")

    # Linear edges
    builder.add_edge("scrape", "score")

    # Conditional routing after score
    builder.add_conditional_edges(
        "score",
        route_by_fit_score,
        {
            "write_materials": "write_materials",
            "ask_user": "ask_user",
            END: END
        }
    )

    # Ask user branches
    builder.add_conditional_edges(
        "ask_user",
        lambda state: "write_materials" if state.get("recommendation") != "skip" else END,
        {
            "write_materials": "write_materials",
            END: END
        }
    )

    # After writing, save
    builder.add_edge("write_materials", "save_to_tracker")
    builder.add_edge("save_to_tracker", END)

    return builder.compile()