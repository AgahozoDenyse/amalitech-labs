import logging

import numpy as np
import pandas as pd

from config import MIN_BUDGET_FOR_ROI, MIN_VOTE_COUNT, TOP_N

logger = logging.getLogger(__name__)


def compute_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add derived KPI columns to the cleaned DataFrame.

    Columns added:
    - ``profit_musd``: revenue minus budget (million USD).
    - ``roi``: revenue / budget ratio. Set to NaN for films whose budget is
      below ``MIN_BUDGET_FOR_ROI`` (defined in config) to avoid misleading
      ratios from near-zero budgets.
    - ``release_year``: integer year extracted from ``release_date``.

    Args:
        df: Cleaned DataFrame (output of ``clean_movies``).

    Returns:
        New DataFrame with the three KPI columns appended.
    """
    logger.info("Computing KPIs...")
    df = df.copy()

    df["profit_musd"] = df["revenue_musd"] - df["budget_musd"]

    # Filter before computing ROI so low-budget outliers don't skew rankings
    df["roi"] = np.where(
        df["budget_musd"] >= MIN_BUDGET_FOR_ROI,
        df["revenue_musd"] / df["budget_musd"],
        np.nan,
    )

    df["release_year"] = df["release_date"].dt.year

    logger.info(
        "KPIs computed. ROI available for %d / %d movies (budget >= $%dM).",
        df["roi"].notna().sum(),
        len(df),
        MIN_BUDGET_FOR_ROI,
    )
    return df


def run_analysis(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """
    Run all analytical queries on the processed DataFrame.

    Assumes ``compute_kpis`` has already been called (i.e. ``profit_musd``,
    ``roi``, and ``release_year`` columns exist).

    Args:
        df: DataFrame with KPI columns.

    Returns:
        Dictionary mapping result names to DataFrames:
        - ``top_revenue``: top N films by revenue.
        - ``top_profit``: top N films by profit.
        - ``top_roi``: top N films by ROI (budget-filtered + MIN_VOTE_COUNT).
        - ``franchise_comparison``: mean/median metrics grouped by is_franchise.
        - ``top_franchises``: top N franchises with >= 2 films by total revenue.
        - ``top_directors``: top N directors (excluding UNKNOWN) by total revenue.
    """
    logger.info("Running analysis...")
    results: dict[str, pd.DataFrame] = {}

    # Sufficiently-voted films only — prevents low-sample-size outliers in rankings
    well_voted = df[df["vote_count"] >= MIN_VOTE_COUNT]

    results["top_revenue"] = (
        well_voted.nlargest(TOP_N, "revenue_musd")[["title", "revenue_musd"]].reset_index(drop=True)
    )
    results["top_profit"] = (
        well_voted.nlargest(TOP_N, "profit_musd")[["title", "profit_musd"]].reset_index(drop=True)
    )
    results["top_roi"] = (
        well_voted.dropna(subset=["roi"])
        .nlargest(TOP_N, "roi")[["title", "roi"]]
        .reset_index(drop=True)
    )

    for name in ("top_revenue", "top_profit", "top_roi"):
        logger.info("%s:\n%s", name, results[name].to_string(index=False))

    results["franchise_comparison"] = df.groupby("is_franchise").agg(
        mean_revenue=("revenue_musd", "mean"),
        median_roi=("roi", "median"),
        mean_budget=("budget_musd", "mean"),
        mean_popularity=("popularity", "mean"),
        mean_rating=("vote_average", "mean"),
    )
    logger.info("Franchise comparison:\n%s", results["franchise_comparison"].to_string())

    franchise_df = df[df["belongs_to_collection"].notna()]
    results["top_franchises"] = (
        franchise_df.groupby("belongs_to_collection")
        .agg(
            total_movies=("id", "count"),
            total_revenue=("revenue_musd", "sum"),
            mean_revenue=("revenue_musd", "mean"),
            mean_rating=("vote_average", "mean"),
        )
        .query("total_movies >= 2")
        .sort_values("total_revenue", ascending=False)
        .head(TOP_N)
    )
    logger.info("Top franchises:\n%s", results["top_franchises"].to_string())

    results["top_directors"] = (
        well_voted[well_voted["director"] != "UNKNOWN"]
        .groupby("director")
        .agg(
            total_movies=("id", "count"),
            total_revenue=("revenue_musd", "sum"),
            mean_rating=("vote_average", "mean"),
        )
        .sort_values("total_revenue", ascending=False)
        .head(TOP_N)
    )
    logger.info("Top directors:\n%s", results["top_directors"].to_string())

    return results
