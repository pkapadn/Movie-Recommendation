from graphviz import Digraph

# Create a new Digraph object
flowchart = Digraph("Preprocessing Workflow", format="png")

# Add nodes
flowchart.node("A", "TMDB Movies Dataset")
flowchart.node("B", "TMDB Credits Dataset")
flowchart.node("C", "Merged Datasets")
flowchart.node("D", "Extract Features\n(Genres, Cast, Keywords)")
flowchart.node("E", "Normalize Text\n(Lowercase, Stem)")
flowchart.node("F", "Create 'Tags' Column")

# Add edges
flowchart.edge("A", "C")
flowchart.edge("B", "C")
flowchart.edge("C", "D")
flowchart.edge("D", "E")
flowchart.edge("E", "F")

# Save the diagram
output_path = "preprocessing_workflow"
flowchart.render(output_path, format="png", cleanup=True)

print(f"Flowchart saved as: {output_path}.png")
