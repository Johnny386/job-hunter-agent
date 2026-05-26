from graph import build_graph

graph = build_graph()

img = graph.get_graph().draw_mermaid_png()

with open("graph_visual.png", "wb") as f:
    f.write(img)

print("Saved to graph_visual.png")