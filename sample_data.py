import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import requests
import io

# Sample data for visualization
recommended_movies = [
    {"title": "The Dark Knight", "poster_url": "https://image.tmdb.org/t/p/w200/qJ2tW6WMUDux911r6m7haRef0WH.jpg", "genres": "Action, Crime", "cast": "Christian Bale, Heath Ledger"},
    {"title": "Inception", "poster_url": "https://image.tmdb.org/t/p/w200/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg", "genres": "Action, Adventure", "cast": "Leonardo DiCaprio, Joseph Gordon-Levitt"},
    {"title": "Interstellar", "poster_url": "https://image.tmdb.org/t/p/w200/rAiYTfKGqDCRIIqo664sY9XZIvQ.jpg", "genres": "Adventure, Drama", "cast": "Matthew McConaughey, Anne Hathaway"},
]

# Create a plot for recommendations
fig, axs = plt.subplots(1, len(recommended_movies), figsize=(15, 5))

for i, movie in enumerate(recommended_movies):
    # Fetch the poster
    response = requests.get(movie["poster_url"])
    img = Image.open(io.BytesIO(response.content))
    
    # Display the poster
    axs[i].imshow(img)
    axs[i].axis("off")
    axs[i].set_title(movie["title"], fontsize=10)
    axs[i].text(0, -20, f"Genres: {movie['genres']}\nCast: {movie['cast']}", fontsize=8, wrap=True)

# Save and show the result
plt.tight_layout()
output_path = "movie_recommendations.png"
plt.savefig(output_path, dpi=300)
plt.show()

print(f"Recommendations visual saved as: {output_path}")
