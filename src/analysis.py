"""
Perform Key Performance Indicator (KPI) analysis on the cleaned TMDB movie dataset.
"""

import pandas as pd
import os


# -----------------------------
# Load Dataset
# -----------------------------

def load_data():

    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "cleaned_movies.csv")

    df = pd.read_csv(data_path)

    # Feature Engineering
    df["profit_musd"] = df["revenue_musd"] - df["budget_musd"]

    # Safe ROI calculation
    df["roi"] = df["revenue_musd"] / df["budget_musd"]

    # Apply condition: ROI only valid for budget ≥ 10M
    df.loc[df["budget_musd"] < 10, "roi"] = None

    return df


# -----------------------------
# Ranking Function (UDF)
# -----------------------------

def rank_movies(df, column, ascending=False, n=10):

    return df.sort_values(column, ascending=ascending)[["title", column]].head(n)


# -----------------------------
# KPI FILTER DATASETS
# -----------------------------

def prepare_kpi_datasets(df):

    # Dataset for ROI (budget ≥ 10M)
    df_roi = df[df["budget_musd"] >= 10]

    # Dataset for rating (vote_count ≥ 10)
    df_votes = df[df["vote_count"] >= 10]

    return df_roi, df_votes


# -----------------------------
# KPI COMPUTATION (RETURN RESULTS)
# -----------------------------

def compute_kpis():

    df = load_data()

    df_roi, df_votes = prepare_kpi_datasets(df)

    results = {
        "highest_revenue": rank_movies(df, "revenue_musd"),
        "highest_budget": rank_movies(df, "budget_musd"),
        "highest_profit": rank_movies(df, "profit_musd"),
        "lowest_profit": rank_movies(df, "profit_musd", ascending=True),
        "highest_roi": rank_movies(df_roi, "roi"),
        "lowest_roi": rank_movies(df_roi, "roi", ascending=True),
        "most_voted": rank_movies(df, "vote_count"),
        "highest_rated": rank_movies(df_votes, "vote_average"),
        "lowest_rated": rank_movies(df_votes, "vote_average", ascending=True),
        "most_popular": rank_movies(df, "popularity"),
    }

    return results


# -----------------------------
# Search Queries
# -----------------------------

def search_bruce_willis(df):

    result = df[
        df["genres"].str.contains("Science Fiction", na=False) &
        df["genres"].str.contains("Action", na=False) &
        df["cast"].str.contains("Bruce Willis", na=False)
    ]

    return result.sort_values("vote_average", ascending=False)[["title", "vote_average"]]


def search_tarantino(df):

    result = df[
        df["cast"].str.contains("Uma Thurman", na=False) &
        df["director"].str.contains("Quentin Tarantino", na=False)
    ]

    return result.sort_values("runtime")[["title", "runtime"]]


# -----------------------------
# Franchise vs Standalone
# -----------------------------

def franchise_vs_standalone(df):

    df["is_franchise"] = df["belongs_to_collection"].notna()

    return df.groupby("is_franchise").agg(
        mean_revenue=("revenue_musd", "mean"),
        median_roi=("roi", "median"),
        mean_budget=("budget_musd", "mean"),
        mean_popularity=("popularity", "mean"),
        mean_rating=("vote_average", "mean")
    )


# -----------------------------
# Successful Franchises
# -----------------------------

def successful_franchises(df):

    franchises = df.dropna(subset=["belongs_to_collection"])

    result = franchises.groupby("belongs_to_collection").agg(
        movie_count=("title", "count"),
        total_budget=("budget_musd", "sum"),
        total_revenue=("revenue_musd", "sum"),
        mean_revenue=("revenue_musd", "mean"),
        mean_rating=("vote_average", "mean")
    )

    return result.sort_values("total_revenue", ascending=False)


# -----------------------------
# Successful Directors
# -----------------------------

def successful_directors(df):

    result = df.groupby("director").agg(
        movie_count=("title", "count"),
        total_revenue=("revenue_musd", "sum"),
        mean_rating=("vote_average", "mean")
    )

    return result.sort_values("total_revenue", ascending=False)