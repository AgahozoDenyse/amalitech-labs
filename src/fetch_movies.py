"""
Fetch movie data from TMDB API and save raw dataset.
"""

# import requests
# import pandas as pd
# import os
# from dotenv import load_dotenv


# Load API key
load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")

if not API_KEY:
    raise ValueError("TMDB_API_KEY not found. Please check your .env file.")


movie_ids = [
    0, 299534, 19995, 140607, 299536, 597, 135397, 420818,
    24428, 168259, 99861, 284054, 12445, 181808,
    330457, 351286, 109445, 321612, 260513
]


def fetch_movies():

    movies = []
    errors = []   # collect errors instead of printing

    for movie_id in movie_ids:

        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&append_to_response=credits"

        try:
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                movies.append(response.json())

            else:
                errors.append(f"Movie ID {movie_id} not found (status code {response.status_code})")

        except requests.exceptions.RequestException as e:
            errors.append(f"Error fetching movie ID {movie_id}: {e}")

    df = pd.DataFrame(movies)

    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "raw_movies.csv")

    df.to_csv(data_path, index=False)

    return df, errors   # return both