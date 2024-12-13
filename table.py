import pandas as pd
import matplotlib.pyplot as plt
import ast

# Load the dataset
movies_file_path = "tmdb_5000_movies.csv"
movies_df = pd.read_csv(movies_file_path)

# Function to extract genres from the 'genres' column
def extract_genres(genre_str):
    try:
        genres = ast.literal_eval(genre_str)  # Parse the string as a list of dictionaries
        return [genre['name'] for genre in genres]  # Extract the 'name' field from each dictionary
    except:
        return []

# Apply the function to extract genres
movies_df['genre_list'] = movies_df['genres'].apply(extract_genres)

# Exploding the genre list to analyze genre-level metrics
exploded_df = movies_df.explode('genre_list')

# Calculating average ratings and vote counts for each genre
genre_metrics_sorted = exploded_df.groupby('genre_list').agg(
    avg_rating=('vote_average', 'mean'),
    total_votes=('vote_count', 'sum')
).reset_index()

# Sorting genres by average rating in descending order
genre_metrics_sorted = genre_metrics_sorted.sort_values(by='avg_rating', ascending=False)

# Visualizing the table
fig, ax = plt.subplots(figsize=(12, 6))
ax.axis("tight")
ax.axis("off")

# Convert the data to a list for the table
table_data = [genre_metrics_sorted.columns.to_list()] + genre_metrics_sorted.values.tolist()

# Create the table
table = ax.table(
    cellText=table_data,
    loc="center",
    cellLoc="center",
    colColours=["#f4f4f4"] * len(genre_metrics_sorted.columns),
)

# Highlight top 3 genres by avg_rating in green
for row in range(1, len(table_data)):
    if row <= 4:  # Top 3 rows (after headers)
        for col in range(len(genre_metrics_sorted.columns)):
            cell = table[(row, col)]
            cell.set_facecolor("#d4edda")  # Light green for highlighting

# Style the headers
for col, header in enumerate(genre_metrics_sorted.columns):
    cell = table[(0, col)]
    cell.set_facecolor("#add8e6")  # Light blue for headers
    cell.set_text_props(weight="bold")

# Adjust layout and save the figure
plt.title("Genre Metrics: Average Ratings and Total Votes", fontsize=16, weight="bold")
plt.tight_layout()
output_path = "genre_metrics_table.png"
plt.savefig(output_path, dpi=300)
plt.show()

print(f"Table visualization saved as: {output_path}")
