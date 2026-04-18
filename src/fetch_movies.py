import requests
import time
import logging
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3/movie/"

logging.basicConfig(level=logging.INFO)


def fetch_movies(movie_ids):
    if not API_KEY:
        raise ValueError("TMDB API key not found. Check your .env file.")

    movies = []
    failed_ids = []

    for movie_id in movie_ids:
        if movie_id == 0:
            logging.warning("Skipping invalid movie ID: 0")
            continue

        url = f"{BASE_URL}{movie_id}?api_key={API_KEY}"
        credits_url = f"{BASE_URL}{movie_id}/credits?api_key={API_KEY}"

        retries = 3
        for attempt in range(retries):
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()

                data = response.json()

                # -----------------------------
                # FIX: Collection extraction
                # -----------------------------
                collection = data.get("belongs_to_collection")
                if isinstance(collection, dict):
                    data["belongs_to_collection"] = collection.get("name")
                else:
                    data["belongs_to_collection"] = None

                # -----------------------------
                # FETCH CREDITS
                # -----------------------------
                credits_response = requests.get(credits_url, timeout=10)
                credits_response.raise_for_status()
                credits = credits_response.json()

                # Extract cast (top 5)
                cast = [member["name"] for member in credits.get("cast", [])[:5]]
                data["cast"] = "|".join(cast)
                data["cast_size"] = len(credits.get("cast", []))

                # Extract director
                crew = credits.get("crew", [])
                directors = [c["name"] for c in crew if c["job"] == "Director"]
                data["director"] = directors[0] if directors else "UNKNOWN"
                data["crew_size"] = len(crew)

                movies.append(data)
                break

            except requests.exceptions.RequestException as e:
                logging.warning(f"Retry {attempt+1} for movie {movie_id}: {e}")
                time.sleep(2 ** attempt)

        else:
            logging.error(f"Failed to fetch movie {movie_id}")
            failed_ids.append(movie_id)

        time.sleep(0.3)  # Rate limiting

    return movies, failed_ids