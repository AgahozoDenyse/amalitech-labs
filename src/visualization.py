"""
Purpose:
    Create charts to explore relationships between important movie
    variables such as budget, revenue, popularity, and ROI.
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

plt.style.use("ggplot")


# --------------------------------------------------
# Load Dataset
# --------------------------------------------------

def load_data():

    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "cleaned_movies.csv")

    df = pd.read_csv(data_path)

    df["roi"] = df["revenue_musd"] / df["budget_musd"]
    df["release_year"] = pd.to_datetime(df["release_date"]).dt.year
    df["is_franchise"] = df["belongs_to_collection"].notna()

    return df


# --------------------------------------------------
# Revenue vs Budget
# --------------------------------------------------

def plot_revenue_vs_budget(df):

    plt.figure()

    plt.scatter(df["budget_musd"], df["revenue_musd"])

    plt.xlabel("Budget (Million USD)")
    plt.ylabel("Revenue (Million USD)")
    plt.title("Revenue vs Budget")

    plt.show()


# --------------------------------------------------
# ROI Distribution by Genre
# --------------------------------------------------

def plot_roi_by_genre(df):

    temp = df.copy()
    temp = temp.dropna(subset=["genres", "roi"])

    temp["genres"] = temp["genres"].str.split("|")
    temp = temp.explode("genres")

    temp.boxplot(column="roi", by="genres", rot=45)

    plt.title("ROI Distribution by Genre")
    plt.suptitle("")
    plt.xlabel("Genre")
    plt.ylabel("ROI")

    plt.show()


# --------------------------------------------------
# Popularity vs Rating
# --------------------------------------------------

def plot_popularity_vs_rating(df):

    plt.figure()

    plt.scatter(df["vote_average"], df["popularity"])

    plt.xlabel("Vote Average")
    plt.ylabel("Popularity")
    plt.title("Popularity vs Rating")

    plt.show()


# --------------------------------------------------
# Yearly Revenue Trend
# --------------------------------------------------

def plot_yearly_revenue(df):

    yearly = df.groupby("release_year")["revenue_musd"].sum().reset_index()

    plt.figure()

    plt.plot(yearly["release_year"], yearly["revenue_musd"])

    plt.xlabel("Release Year")
    plt.ylabel("Total Revenue (Million USD)")
    plt.title("Yearly Box Office Revenue")

    plt.show()


# --------------------------------------------------
# Franchise vs Standalone
# --------------------------------------------------

def plot_franchise_vs_standalone(df):

    comparison = df.groupby("is_franchise")["revenue_musd"].mean()

    comparison.plot(kind="bar")

    plt.xlabel("Is Franchise")
    plt.ylabel("Average Revenue (Million USD)")
    plt.title("Franchise vs Standalone Performance")

    plt.show()


# --------------------------------------------------
# Run All Visualizations
# --------------------------------------------------

def run_all_visualizations():

    df = load_data()

    plot_revenue_vs_budget(df)
    plot_roi_by_genre(df)
    plot_popularity_vs_rating(df)
    plot_yearly_revenue(df)
    plot_franchise_vs_standalone(df)