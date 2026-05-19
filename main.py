"""
TMDB Movie Data Pipeline entry point.

Run with:
    python main.py
"""

import logging
import os

import pandas as pd

from config import CLEAN_DATA_PATH, MOVIE_IDS, RAW_DATA_PATH
from src.analysis import compute_kpis, run_analysis
from src.clean_movies import clean_movies
from src.fetch_movies import fetch_movies
from src.visualization import visualize_data

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s – %(message)s",
)
logger = logging.getLogger(__name__)


def _save_failed_ids(failed_ids: list[int], path: str = "data/failed_ids.txt") -> None:
    """Persist failed movie IDs to disk so they can be retried independently."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as fh:
        fh.write("\n".join(str(i) for i in failed_ids))
    logger.info("Saved %d failed IDs → %s", len(failed_ids), path)


def main() -> None:
    """Run the full pipeline: fetch → clean → KPIs → analysis → visualise."""
    logger.info("Starting TMDB Data Pipeline...")

    # ── Step 1: Fetch ────────────────────────────────────────────────────────
    logger.info("Fetching movie data...")
    movies, failed_ids = fetch_movies(MOVIE_IDS)

    if failed_ids:
        logger.warning("%d movie IDs failed – persisting for retry.", len(failed_ids))
        _save_failed_ids(failed_ids)

    df_raw = pd.DataFrame(movies)
    os.makedirs(os.path.dirname(RAW_DATA_PATH), exist_ok=True)
    df_raw.to_csv(RAW_DATA_PATH, index=False)
    logger.info("Saved %d raw movies → %s", len(df_raw), RAW_DATA_PATH)

    # ── Step 2: Clean ────────────────────────────────────────────────────────
    df_clean = clean_movies(df_raw)
    df_clean.to_csv(CLEAN_DATA_PATH, index=False)
    logger.info("Saved %d cleaned movies → %s", len(df_clean), CLEAN_DATA_PATH)

    # ── Step 3: KPIs ─────────────────────────────────────────────────────────
    df_kpis = compute_kpis(df_clean)

    # ── Step 4: Analysis ─────────────────────────────────────────────────────
    results = run_analysis(df_kpis)
    logger.info("Analysis complete. Results: %s", list(results.keys()))

    # ── Step 5: Visualise ────────────────────────────────────────────────────
    visualize_data(df_kpis)

    logger.info("Pipeline completed successfully.")


if __name__ == "__main__":
    main()
