"""
Project configuration settings.
"""

# -----------------------------
# Movie IDs (TMDB)
# -----------------------------
MOVIE_IDS = [
    299534, 19995, 140607, 299536, 597, 135397,
    420818, 24428, 168259, 99861, 284054, 12445,
    181808, 330457, 351286, 109445, 321612, 260513
]

# -----------------------------
# File Paths
# -----------------------------
RAW_DATA_PATH = "data/raw_movies.csv"
CLEAN_DATA_PATH = "data/cleaned_movies.csv"
IMAGES_DIR = "images/"

# -----------------------------
# Analysis Parameters
# -----------------------------
MIN_BUDGET_FOR_ROI = 10  # million USD
TOP_N = 10