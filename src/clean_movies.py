import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)


def clean_movies(df):
    logging.info("Cleaning dataset...")

    # Drop irrelevant columns
    df.drop(columns=['adult', 'imdb_id', 'original_title', 'video', 'homepage'],
            inplace=True, errors='ignore')

    # -----------------------------
    # SAFE JSON parsing
    # -----------------------------
    def extract_names(obj):
        if isinstance(obj, list):
            return "|".join([item.get("name", "") for item in obj])
        return np.nan

    df['genres'] = df['genres'].apply(extract_names)
    df['production_companies'] = df['production_companies'].apply(extract_names)
    df['production_countries'] = df['production_countries'].apply(extract_names)
    df['spoken_languages'] = df['spoken_languages'].apply(extract_names)

    # -----------------------------
    # Data types
    # -----------------------------
    numeric_cols = ['budget', 'revenue', 'runtime',
                    'popularity', 'vote_count', 'vote_average']

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')

    # Replace 0 with NaN
    df[['budget', 'revenue', 'runtime']] = df[['budget', 'revenue', 'runtime']].replace(0, np.nan)

    # Convert to millions
    df['budget_musd'] = df['budget'] / 1_000_000
    df['revenue_musd'] = df['revenue'] / 1_000_000

    # -----------------------------
    # FIX: Franchise flag
    # -----------------------------
    df['is_franchise'] = df['belongs_to_collection'].notna()

    # Keep only released movies
    if 'status' in df.columns:
        df = df[df['status'] == 'Released']
        df.drop(columns=['status'], inplace=True)

    # Remove duplicates
    df.drop_duplicates(subset=['id'], inplace=True)

    # Drop missing critical fields
    df.dropna(subset=['id', 'title'], inplace=True)

    # Keep rows with enough data
    df = df[df.notna().sum(axis=1) >= 10]

    df.reset_index(drop=True, inplace=True)

    logging.info(f"Cleaned dataset size: {len(df)}")

    return df