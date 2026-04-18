import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)


def run_analysis(df):
    logging.info("Running analysis...")

    # Profit
    df['profit_musd'] = df['revenue_musd'] - df['budget_musd']

    # ROI (only valid budgets)
    df['roi'] = np.where(df['budget_musd'] >= 10,
                         df['revenue_musd'] / df['budget_musd'],
                         np.nan)

    # -----------------------------
    # Rankings
    # -----------------------------
    logging.info("Top Revenue Movies:")
    logging.info(df.nlargest(10, 'revenue_musd')[['title', 'revenue_musd']])

    logging.info("Top Profit Movies:")
    logging.info(df.nlargest(10, 'profit_musd')[['title', 'profit_musd']])

    logging.info("Top ROI Movies (budget >= 10M):")
    logging.info(df.nlargest(10, 'roi')[['title', 'roi']])

    # -----------------------------
    # Advanced Filters
    # -----------------------------
    sci_fi_action = df[
        df['genres'].str.contains("Science Fiction", na=False) &
        df['genres'].str.contains("Action", na=False) &
        df['cast'].str.contains("Bruce Willis", na=False)
    ].sort_values('vote_average', ascending=False)

    if sci_fi_action.empty:
        logging.info("No Sci-Fi Action movies with Bruce Willis found.")
    else:
        logging.info(sci_fi_action[['title', 'vote_average']])

    tarantino = df[
        df['cast'].str.contains("Uma Thurman", na=False) &
        df['director'].str.contains("Quentin Tarantino", na=False)
    ].sort_values('runtime')

    if tarantino.empty:
        logging.info("No Tarantino + Uma Thurman movies found.")
    else:
        logging.info(tarantino[['title', 'runtime']])

    # -----------------------------
    # Franchise vs Standalone
    # -----------------------------
    franchise_analysis = df.groupby('is_franchise').agg({
        'revenue_musd': 'mean',
        'roi': 'median',
        'budget_musd': 'mean',
        'popularity': 'mean',
        'vote_average': 'mean'
    }).rename(columns={
        'revenue_musd': 'mean_revenue',
        'roi': 'median_roi',
        'budget_musd': 'mean_budget',
        'popularity': 'mean_popularity',
        'vote_average': 'mean_rating'
    })

    logging.info("Franchise Analysis:")
    logging.info(franchise_analysis)

    # -----------------------------
    # Top Franchises
    # -----------------------------
    franchises = df[df['belongs_to_collection'].notna()]

    top_franchises = franchises.groupby('belongs_to_collection').agg({
        'id': 'count',
        'revenue_musd': ['sum', 'mean'],
        'vote_average': 'mean'
    })

    top_franchises.columns = ['total_movies', 'total_revenue', 'mean_revenue', 'mean_rating']

    logging.info("Top Franchises:")
    logging.info(top_franchises.sort_values('total_revenue', ascending=False).head(10))

    # -----------------------------
    # Top Directors
    # -----------------------------
    top_directors = df.groupby('director').agg({
        'id': 'count',
        'revenue_musd': 'sum',
        'vote_average': 'mean'
    }).rename(columns={
        'id': 'total_movies',
        'revenue_musd': 'total_revenue',
        'vote_average': 'mean_rating'
    })

    logging.info("Top Directors:")
    logging.info(top_directors.sort_values('total_revenue', ascending=False).head(10))

    return df