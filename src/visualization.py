"""
Create visualizations for TMDB movie analysis.
"""

import matplotlib.pyplot as plt
import os
import logging


# -----------------------------
# Setup Logging
# -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# -----------------------------
# Ensure Output Directory
# -----------------------------
def ensure_output_dir():
    """
    Create images directory if it does not exist.
    """
    path = os.path.join(os.path.dirname(__file__), "..", "images")
    os.makedirs(path, exist_ok=True)
    return path


# -----------------------------
# Revenue vs Budget
# -----------------------------
def plot_revenue_vs_budget(df, save_path):
    """
    Scatter plot of budget vs revenue.
    """
    df_valid = df.dropna(subset=["budget_musd", "revenue_musd"])

    plt.figure(figsize=(8, 5))
    plt.scatter(df_valid["budget_musd"], df_valid["revenue_musd"])

    plt.xlabel("Budget (Million USD)")
    plt.ylabel("Revenue (Million USD)")
    plt.title("Revenue vs Budget")

    file_path = os.path.join(save_path, "revenue_vs_budget.png")
    plt.savefig(file_path)
    plt.close()

    logging.info("Saved revenue vs budget plot")


# -----------------------------
# ROI by Genre
# -----------------------------
def plot_roi_by_genre(df, save_path):
    """
    Boxplot of ROI distribution by genre.
    """
    temp = df.dropna(subset=["genres", "roi"]).copy()

    temp["genres"] = temp["genres"].str.split("|")
    temp = temp.explode("genres")

    plt.figure(figsize=(10, 6))
    temp.boxplot(column="roi", by="genres", rot=45)

    plt.title("ROI by Genre")
    plt.suptitle("")
    plt.xlabel("Genre")
    plt.ylabel("ROI")

    file_path = os.path.join(save_path, "roi_by_genre.png")
    plt.savefig(file_path)
    plt.close()

    logging.info("Saved ROI by genre plot")


# -----------------------------
# Popularity vs Rating
# -----------------------------
def plot_popularity_vs_rating(df, save_path):
    """
    Scatter plot of popularity vs rating.
    """
    df_valid = df.dropna(subset=["vote_average", "popularity"])

    plt.figure(figsize=(8, 5))
    plt.scatter(df_valid["vote_average"], df_valid["popularity"])

    plt.xlabel("Vote Average")
    plt.ylabel("Popularity")
    plt.title("Popularity vs Rating")

    file_path = os.path.join(save_path, "popularity_vs_rating.png")
    plt.savefig(file_path)
    plt.close()

    logging.info("Saved popularity vs rating plot")


# -----------------------------
# Yearly Revenue Trend
# -----------------------------
def plot_yearly_revenue(df, save_path):
    """
    Line plot of average revenue over time.
    """
    # Ensure year exists
    if "release_year" not in df.columns:
        df["release_year"] = df["release_date"].dt.year

    yearly = df.groupby("release_year")["revenue_musd"].mean().reset_index()

    plt.figure(figsize=(8, 5))
    plt.plot(yearly["release_year"], yearly["revenue_musd"], marker="o")

    plt.xlabel("Year")
    plt.ylabel("Average Revenue (Million USD)")
    plt.title("Average Revenue Over Time")

    file_path = os.path.join(save_path, "yearly_revenue.png")
    plt.savefig(file_path)
    plt.close()

    logging.info("Saved yearly revenue plot")


# -----------------------------
# Franchise vs Standalone
# -----------------------------
def plot_franchise_vs_standalone(df, save_path):
    """
    Bar chart comparing franchise vs standalone movies.
    """
    comparison = df.groupby("is_franchise")["revenue_musd"].mean()

    plt.figure(figsize=(6, 4))
    comparison.plot(kind="bar")

    plt.xlabel("Franchise")
    plt.ylabel("Average Revenue (Million USD)")
    plt.title("Franchise vs Standalone")

    file_path = os.path.join(save_path, "franchise_vs_standalone.png")
    plt.savefig(file_path)
    plt.close()

    logging.info("Saved franchise comparison plot")


# -----------------------------
# MAIN VISUALIZATION FUNCTION
# -----------------------------
def visualize_data(df):
    """
    Run all visualizations using processed dataframe.
    """
    save_path = ensure_output_dir()

    plot_revenue_vs_budget(df, save_path)
    plot_roi_by_genre(df, save_path)
    plot_popularity_vs_rating(df, save_path)
    plot_yearly_revenue(df, save_path)
    plot_franchise_vs_standalone(df, save_path)

    logging.info("All visualizations generated successfully")