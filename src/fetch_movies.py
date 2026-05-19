import logging
import os
import random
import time
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3/movie/"
MAX_RETRIES = 3
RATE_LIMIT_DELAY = 0.3  # seconds between requests to stay within TMDB rate limits


def _build_session() -> requests.Session:
    """Create a reusable session with Authorization header set once."""
    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {API_KEY}"})
    return session


def _fetch_with_retry(
    session: requests.Session, url: str, movie_id: int
) -> dict[str, Any] | None:
    """
    Fetch a URL with exponential backoff and explicit 429 handling.

    Returns the parsed JSON dict on success, or None after all retries
    are exhausted or a non-recoverable HTTP error (e.g. 404) is received.
    """
    for attempt in range(MAX_RETRIES):
        try:
            response = session.get(url, timeout=10)

            if response.status_code == 429:
                wait = int(response.headers.get("Retry-After", 10))
                logger.warning(
                    "Rate limited on movie %s. Waiting %ss (Retry-After).", movie_id, wait
                )
                time.sleep(wait)
                continue

            if response.status_code == 404:
                logger.warning("Movie %s not found (404). Skipping.", movie_id)
                return None

            response.raise_for_status()
            return response.json()

        except requests.exceptions.Timeout:
            logger.warning("Timeout on attempt %d for movie %s.", attempt + 1, movie_id)
        except requests.exceptions.ConnectionError:
            logger.warning(
                "Connection error on attempt %d for movie %s.", attempt + 1, movie_id
            )
        except requests.exceptions.HTTPError as exc:
            logger.warning(
                "HTTP %s on attempt %d for movie %s: %s",
                exc.response.status_code,
                attempt + 1,
                movie_id,
                exc,
            )

        backoff = (2**attempt) + random.uniform(0, 1)
        logger.debug("Backing off %.1fs before retry.", backoff)
        time.sleep(backoff)

    logger.error("Gave up fetching movie %s after %d attempts.", movie_id, MAX_RETRIES)
    return None


def fetch_movies(movie_ids: list[int]) -> tuple[list[dict], list[int]]:
    """
    Fetch movie details and credits from the TMDB API.

    Each valid ID results in two API calls: one for movie metadata and one
    for credits (cast + crew). Failed IDs are collected and returned so the
    caller can persist them for a retry run.

    Args:
        movie_ids: List of TMDB movie IDs to fetch. Non-positive IDs are
                   skipped immediately without making any network calls.

    Returns:
        A tuple ``(movies, failed_ids)`` where ``movies`` is a list of raw
        API dicts enriched with ``cast``, ``cast_size``, ``director``, and
        ``crew_size`` fields, and ``failed_ids`` is a list of IDs that could
        not be fetched after all retries.

    Raises:
        ValueError: If ``TMDB_API_KEY`` is not set in the environment.
    """
    if not API_KEY:
        raise ValueError("TMDB_API_KEY not set. Check your .env file.")

    session = _build_session()
    movies: list[dict] = []
    failed_ids: list[int] = []

    for movie_id in movie_ids:
        if not isinstance(movie_id, int) or movie_id <= 0:
            logger.warning("Skipping invalid movie ID: %s", movie_id)
            failed_ids.append(movie_id)
            continue

        data = _fetch_with_retry(session, f"{BASE_URL}{movie_id}", movie_id)
        if data is None:
            failed_ids.append(movie_id)
            time.sleep(RATE_LIMIT_DELAY)
            continue

        # Normalize collection field from nested dict to plain string
        collection = data.get("belongs_to_collection")
        data["belongs_to_collection"] = (
            collection.get("name") if isinstance(collection, dict) else None
        )

        credits = _fetch_with_retry(session, f"{BASE_URL}{movie_id}/credits", movie_id)
        if credits is not None:
            cast_list = credits.get("cast", [])
            crew_list = credits.get("crew", [])
            directors = [c["name"] for c in crew_list if c.get("job") == "Director"]
            data["cast"] = "|".join(m["name"] for m in cast_list[:5])
            data["cast_size"] = len(cast_list)
            data["director"] = directors[0] if directors else "UNKNOWN"
            data["crew_size"] = len(crew_list)
        else:
            data.update({"cast": "", "cast_size": 0, "director": "UNKNOWN", "crew_size": 0})

        movies.append(data)
        time.sleep(RATE_LIMIT_DELAY)

    logger.info("Fetched %d movies. %d failed.", len(movies), len(failed_ids))
    return movies, failed_ids
