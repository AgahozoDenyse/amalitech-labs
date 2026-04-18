import logging
import pandas as pd

from src.fetch_movies import fetch_movies
from src.clean_movies import clean_movies
from src.analysis import run_analysis
from src.visualization import visualize_data
from config import MOVIE_IDS, RAW_DATA_PATH, CLEAN_DATA_PATH


# -----------------------------
# LOGGING SETUP
# -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def main():
    logging.info("Starting TMDB Data Pipeline...")

    # -----------------------------
    # STEP 1: FETCH DATA
    # -----------------------------
    logging.info("Fetching movie data...")
    movies, failed_ids = fetch_movies(MOVIE_IDS)

    df_raw = pd.DataFrame(movies)
    df_raw.to_csv(RAW_DATA_PATH, index=False)


    logging.info(f"Saved raw dataset with {len(df_raw)} movies")
    logging.info(f"Failed movie IDs: {failed_ids}")

    # -----------------------------
    # STEP 2: CLEAN DATA
    # -----------------------------
    df_clean = clean_movies(df_raw)
    df_clean.to_csv(CLEAN_DATA_PATH, index=False)
    

    logging.info(f"Cleaned dataset saved with {len(df_clean)} movies")

    # -----------------------------
    # STEP 3: ANALYSIS
    # -----------------------------
    df_analyzed = run_analysis(df_clean)

    # -----------------------------
    # STEP 4: VISUALIZATION
    # -----------------------------
    visualize_data(df_analyzed)

    logging.info("Pipeline completed successfully!")


# -----------------------------
# ENTRY POINT
# -----------------------------
if __name__ == "__main__":
    main()