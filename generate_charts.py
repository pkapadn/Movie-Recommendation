from diagrams import Diagram, Node
from diagrams.custom import Custom

# Creating the preprocessing workflow flowchart
with Diagram("Preprocessing Workflow", direction="TB", show=False):
    # Input data
    tmdb_movies = Node("TMDB Movies Dataset")
    tmdb_credits = Node("TMDB Credits Dataset")
    merged_data = Node("Merged Datasets")
    
    # Steps
    feature_extraction = Node("Extract Features (Genres, Cast, Keywords)")
    text_normalization = Node("Normalize Text (Lowercase, Stem)")
    combined_tags = Node("Create 'Tags' Column")

    # Connections
    tmdb_movies >> merged_data
    tmdb_credits >> merged_data
    merged_data >> feature_extraction
    feature_extraction >> text_normalization
    text_normalization >> combined_tags
