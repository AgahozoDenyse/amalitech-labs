
"""
This script cleans and prepares the raw movie dataset obtained from the TMDB API.

What this script does:
    - Loads the raw dataset
    - Removes unnecessary columns
    - Extracts useful information from JSON fields
    - Converts columns to correct data types
    - Handles missing or unrealistic values
    - Converts budget and revenue to million USD
    - Saves the cleaned dataset

"""
#-----------------------------------------------------------------------
import pandas as pd
import numpy as np
import os
import ast


# -----------------------------
# Utility Functions
# -----------------------------

def extract_collection(x):
    """Extract collection name from JSON."""
    if pd.notna(x):
        try:
            data = ast.literal_eval(x)
            if isinstance(data, dict):
                return data.get("name")
        except:
            return np.nan
    return np.nan


def extract_pipe_names(x):
    """Convert JSON list to pipe separated names."""
    if pd.notna(x):
        try:
            data = ast.literal_eval(x)
            if isinstance(data, list):
                return "|".join(i["name"] for i in data if "name" in i)
        except:
            return np.nan
    return np.nan


# -----------------------------
# Load Raw Data
# -----------------------------
def clean_data():
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "raw_movies.csv")

    df = pd.read_csv(data_path)


    # -----------------------------
    # Drop Irrelevant Columns
    # -----------------------------

    df.drop(
        columns=["adult", "imdb_id", "original_title", "video", "homepage"],
        inplace=True,
        errors="ignore"
    )


    # -----------------------------
    # Flatten JSON Columns
    # -----------------------------

    df["belongs_to_collection"] = df["belongs_to_collection"].apply(extract_collection)

    df["genres"] = df["genres"].apply(extract_pipe_names)

    df["production_companies"] = df["production_companies"].apply(extract_pipe_names)

    df["production_countries"] = df["production_countries"].apply(extract_pipe_names)

    df["spoken_languages"] = df["spoken_languages"].apply(extract_pipe_names)

    # -----------------------------
    # Extract Cast and Crew Info
    # -----------------------------

    def extract_cast(x):
        """Extract cast names separated by |"""
        if pd.notna(x):
            try:
                data = ast.literal_eval(x)
                cast_list = data.get("cast", [])[:10]
                return "|".join(member.get("name") for member in cast_list if member.get("name"))
            except:
                return np.nan
        return np.nan


    def extract_cast_size(x):
        """Count number of cast members"""
        if pd.notna(x):
            try:
                data = ast.literal_eval(x)
                return len(data.get("cast", []))
            except:
                return np.nan
        return np.nan


    def extract_director(x):
        """Extract director name"""
        if pd.notna(x):
            try:
                data = ast.literal_eval(x)
                crew_list = data.get("crew", [])
                for member in crew_list:
                    if member.get("job") == "Director":
                        return member.get("name")
            except:
                return np.nan
        return np.nan


    def extract_crew_size(x):
        """Count number of crew members"""
        if pd.notna(x):
            try:
                data = ast.literal_eval(x)
                return len(data.get("crew", []))
            except:
                return np.nan
        return np.nan


    # Apply extraction
    df["cast"] = df["credits"].apply(extract_cast)

    df["cast_size"] = df["credits"].apply(extract_cast_size)

    df["director"] = df["credits"].apply(extract_director)

    df["crew_size"] = df["credits"].apply(extract_crew_size)


    # Remove credits column after extraction
    df.drop(columns=["credits"], inplace=True, errors="ignore")

    # -----------------------------
    # Convert Data Types
    # -----------------------------

    df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")

    numeric_columns = ["budget", "revenue", "runtime", "popularity", "vote_count", "vote_average"]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")


    # Replace unrealistic values
    df.loc[df["budget"] == 0, "budget"] = np.nan
    df.loc[df["revenue"] == 0, "revenue"] = np.nan
    df.loc[df["runtime"] == 0, "runtime"] = np.nan


    # -----------------------------
    # Feature Engineering
    # -----------------------------

    df["budget_musd"] = df["budget"] / 1_000_000
    df["revenue_musd"] = df["revenue"] / 1_000_000
    df.drop(columns=["budget", "revenue"], inplace=True, errors="ignore")


    # -----------------------------
    # Data Quality Checks
    # -----------------------------

    df.drop_duplicates(subset=["id"], inplace=True)

    df.dropna(subset=["id", "title"], inplace=True)

    df = df[df.count(axis=1) >= 10]


    # Keep only released movies
    if "status" in df.columns:
        df = df[df["status"] == "Released"]
        df.drop(columns=["status"], inplace=True)


    # -----------------------------
    # Save Clean Dataset
    # -----------------------------

    clean_path = os.path.join(os.path.dirname(__file__), "..", "data", "cleaned_movies.csv")

    df.to_csv(clean_path, index=False)
