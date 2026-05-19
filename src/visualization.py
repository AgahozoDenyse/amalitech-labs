"""
Visualizations for TMDB movie analysis.
"""

import logging
import os

import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)


def _save(fig_path: str) -> None:
    """Apply tight layout, save figure to *fig_path*, and close it."""
    plt.tight_layout()
    plt.savefig(fig_path, dpi=150)
    plt.close()
    logger.info("Saved chart → %s", fig_path)


def _ensure_output_dir() -> str:
    """Create and return the ``images/`` directory next to the project root."""
    path = os.path.join(os.path.dirname(__file__), "..", "images")
    os.makedirs(path, exist_ok=True)
    return path


def plot_revenue_vs_budget(df, save_path: str) -> None:
    """Scatter plot of production budget vs box-office revenue (million USD)."""
    valid = df.dropna(subset=["budget_musd", "revenue_musd"])
    plt.figure(figsize=(8, 5))
    plt.scatter(valid["budget_musd"], valid["revenue_musd"], alpha=0.6)
    plt.xlabel("Budget (Million USD)")
    plt.ylabel("Revenue (Million USD)")
    plt.title("Revenue vs Budget")
    plt.grid(True, linestyle="--", alpha=0.4)
    _save(os.path.join(save_path, "revenue_vs_budget.png"))


def plot_roi_by_genre(df, save_path: str) -> None:
    """Box plot of ROI distribution for each genre (budget-filtered films only)."""
    temp = df.dropna(subset=["genres", "roi"]).copy()
    temp["genres"] = temp["genres"].str.split("|")
    temp = temp.explode("genres")

    plt.figure(figsize=(12, 6))
    temp.boxplot(column="roi", by="genres", rot=45, grid=False)
    plt.title("ROI Distribution by Genre")
    plt.suptitle("")
    plt.xlabel("Genre")
    plt.ylabel("ROI (revenue / budget)")
    _save(os.path.join(save_path, "roi_by_genre.png"))


def plot_popularity_vs_rating(df, save_path: str) -> None:
    """Scatter plot of audience rating vs TMDB popularity score."""
    valid = df.dropna(subset=["vote_average", "popularity"])
    plt.figure(figsize=(8, 5))
    plt.scatter(valid["vote_average"], valid["popularity"], alpha=0.6)
    plt.xlabel("Vote Average (0–10)")
    plt.ylabel("Popularity Score")
    plt.title("Popularity vs Audience Rating")
    plt.grid(True, linestyle="--", alpha=0.4)
    _save(os.path.join(save_path, "popularity_vs_rating.png"))


def plot_yearly_revenue(df, save_path: str) -> None:
    """Line plot of mean box-office revenue per release year."""
    if "release_year" not in df.columns:
        df = df.copy()
        df["release_year"] = df["release_date"].dt.year

    yearly = df.groupby("release_year")["revenue_musd"].mean().reset_index()
    plt.figure(figsize=(10, 5))
    plt.plot(yearly["release_year"], yearly["revenue_musd"], marker="o", linewidth=1.5)
    plt.xlabel("Release Year")
    plt.ylabel("Average Revenue (Million USD)")
    plt.title("Average Box-Office Revenue Over Time")
    plt.grid(True, linestyle="--", alpha=0.4)
    _save(os.path.join(save_path, "yearly_revenue.png"))


def plot_franchise_vs_standalone(df, save_path: str) -> None:
    """Bar chart comparing mean revenue of franchise vs standalone films."""
    comparison = df.groupby("is_franchise")["revenue_musd"].mean()
    comparison.index = comparison.index.map({True: "Franchise", False: "Standalone"})

    plt.figure(figsize=(6, 4))
    comparison.plot(kind="bar", color=["steelblue", "coral"])
    plt.xlabel("Film Type")
    plt.ylabel("Average Revenue (Million USD)")
    plt.title("Franchise vs Standalone: Average Revenue")
    plt.xticks(rotation=0)
    _save(os.path.join(save_path, "franchise_vs_standalone.png"))


def visualize_data(df) -> None:
    """
    Generate and save all visualisation charts.

    Args:
        df: Processed DataFrame (output of ``compute_kpis``).
    """
    save_path = _ensure_output_dir()
    plot_revenue_vs_budget(df, save_path)
    plot_roi_by_genre(df, save_path)
    plot_popularity_vs_rating(df, save_path)
    plot_yearly_revenue(df, save_path)
    plot_franchise_vs_standalone(df, save_path)
    logger.info("All visualisations generated.")
