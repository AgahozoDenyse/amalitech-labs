import logging

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def _extract_names(obj) -> str:
    """Return pipe-separated names from a list of ``{"name": ...}`` dicts."""
    if isinstance(obj, list):
        return "|".join(
            item.get("name", "") for item in obj if isinstance(item, dict)
        )
    return np.nan


def clean_movies(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and normalise raw TMDB movie data.

    Steps performed:
    - Drop irrelevant columns (adult, imdb_id, original_title, video, homepage).
    - Parse nested list-of-dict fields into pipe-separated strings.
    - Coerce numeric and date columns; replace zero budget/revenue/runtime with NaN.
    - Convert budget and revenue to millions USD.
    - Add ``is_franchise`` boolean and ``release_year`` integer columns.
    - Keep only movies with status == "Released".
    - Remove duplicate IDs and rows missing id or title.
    - Drop rows with fewer than 10 non-null fields.

    Args:
        df: Raw DataFrame produced from the TMDB API response list.

    Returns:
        Cleaned DataFrame with a reset integer index.
    """
    logger.info("Cleaning dataset...")
    df = df.copy()

    df = df.drop(
        columns=["adult", "imdb_id", "original_title", "video", "homepage"],
        errors="ignore",
    )

    for col in ["genres", "production_companies", "production_countries", "spoken_languages"]:
        if col in df.columns:
            df[col] = df[col].apply(_extract_names)

    numeric_cols = ["budget", "revenue", "runtime", "popularity", "vote_count", "vote_average"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "release_date" in df.columns:
        df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")

    for col in ["budget", "revenue", "runtime"]:
        if col in df.columns:
            df[col] = df[col].replace(0, np.nan)

    if "budget" in df.columns:
        df["budget_musd"] = df["budget"] / 1_000_000
    if "revenue" in df.columns:
        df["revenue_musd"] = df["revenue"] / 1_000_000

    df["is_franchise"] = df["belongs_to_collection"].notna()

    if "status" in df.columns:
        df = df[df["status"] == "Released"].drop(columns=["status"])

    df = df.drop_duplicates(subset=["id"])
    df = df.dropna(subset=["id", "title"])
    df = df[df.notna().sum(axis=1) >= 10]
    df = df.reset_index(drop=True)

    logger.info("Cleaned dataset: %d rows remaining.", len(df))
    return df
