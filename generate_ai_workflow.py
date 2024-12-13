
from graphviz import Digraph

# Create a new Digraph object
workflow = Digraph("AI Model Workflow", format="png")

# Set graph attributes
workflow.attr(bgcolor="white")

# Add nodes with colors
workflow.node("A", "Input Movie", shape="ellipse", style="filled", color="lightblue", fontcolor="black")
workflow.node("B", "Vectorization\n(Convert 'Tags' to Vectors)", shape="box", style="filled", color="lightgreen", fontcolor="black")
workflow.node("C", "Similarity Calculation\n(Cosine Similarity)", shape="box", style="filled", color="yellow", fontcolor="black")
workflow.node("D", "Sorting and Ranking\n(Descending Similarity Scores)", shape="box", style="filled", color="orange", fontcolor="black")
workflow.node("E", "Top 25 Recommendations", shape="ellipse", style="filled", color="pink", fontcolor="black")

# Add edges with colors
workflow.edge("A", "B", color="blue", penwidth="2")
workflow.edge("B", "C", color="green", penwidth="2")
workflow.edge("C", "D", color="orange", penwidth="2")
workflow.edge("D", "E", color="red", penwidth="2")

# Save the diagram
output_path = "ai_model_workflow_colored"
workflow.render(output_path, format="png", cleanup=True)

print(f"Enhanced workflow diagram saved as: {output_path}.png")
