"""
Project-wide configuration settings.

All file paths are resolved relative to this file so the project works
regardless of the working directory the pipeline is launched from.
"""

from pathlib import Path

BASE_DIR = Path(__file__).parent

# ── Movie IDs ─────────────────────────────────────────────────────────────────
MOVIE_IDS: list[int] = [
    299534, 19995, 140607, 299536, 597, 135397,
    420818, 24428, 168259, 99861, 284054, 12445,
    181808, 330457, 351286, 109445, 321612, 260513,
]

# ── File paths ────────────────────────────────────────────────────────────────
RAW_DATA_PATH: str = str(BASE_DIR / "data" / "raw_movies.csv")
CLEAN_DATA_PATH: str = str(BASE_DIR / "data" / "cleaned_movies.csv")
IMAGES_DIR: str = str(BASE_DIR / "images")

# ── Analysis parameters ───────────────────────────────────────────────────────
MIN_BUDGET_FOR_ROI: int = 10   # million USD — films below this are excluded from ROI
MIN_VOTE_COUNT: int = 100      # minimum votes required for a film to appear in rating/ROI rankings
TOP_N: int = 10                # number of results returned in ranking queries
