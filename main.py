"""
Main script to run the TMDB Movie Data Analysis project.

This script controls the full workflow of the project:
- Fetch movie data from the TMDB API
- Clean and prepare the dataset
- Perform KPI analysis
- Display results
- Generate visualizations

All outputs are handled in this file to keep the project organized.
"""
from src import fetch_movies
from src import cleaned_movies
from src import analysis
from src import visualization


def main():

    # -----------------------------
    # Fetch API data
    # -----------------------------
    df_raw, errors = fetch_movies.fetch_movies()

    # Print warnings from fetching
    if errors:
        print("\nWarnings during data fetching:")
        for err in errors:
            print(err)

    # -----------------------------
    # Clean dataset
    # -----------------------------
    cleaned_movies.clean_data()

    # -----------------------------
    # KPI analysis
    # -----------------------------
    df = analysis.load_data()

    print("\nTop Revenue Movies")
    print(analysis.rank_movies(df, "revenue_musd"))

    print("\nTop Profit Movies")
    print(analysis.rank_movies(df, "profit_musd"))

    print("\nHighest ROI Movies")
    print(analysis.rank_movies(df, "roi"))

    print("\nBruce Willis Sci-Fi Action Movies")
    print(analysis.search_bruce_willis(df))

    print("\nUma Thurman + Tarantino Movies")
    print(analysis.search_tarantino(df))

    print("\nFranchise vs Standalone")
    print(analysis.franchise_vs_standalone(df))

    print("\nMost Successful Franchises")
    print(analysis.successful_franchises(df).head(10))

    print("\nMost Successful Directors")
    print(analysis.successful_directors(df).head(10))

    # -----------------------------
    # Visualizations
    # -----------------------------
    visualization.run_all_visualizations()


if __name__ == "__main__":
    main()