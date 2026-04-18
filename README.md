#  TMDB Movie Data Analysis Project

## Project Overview

This project implements a complete **end-to-end data pipeline** using the TMDB (The Movie Database) API.

It demonstrates how to:

* Extract real-world data from an external API
* Clean and transform raw JSON data into structured datasets
* Compute key performance indicators (KPIs)
* Generate insightful visualizations
* Deliver data-driven business insights

The project follows best practices in **data engineering and data analysis**, including modular design, logging, configuration management, and reproducibility.

---

## Pipeline Workflow

The pipeline consists of four main stages:

### 1. Data Extraction

* Fetches movie data from the TMDB API
* Implements **retry logic with exponential backoff**
* Handles API failures gracefully
* Skips invalid movie IDs
* Secures API key using environment variables

---

### 2. Data Cleaning

* Removes irrelevant or redundant columns
* Safely parses nested JSON fields (e.g., genres, collections)
* Handles missing and inconsistent values
* Converts financial metrics to **million USD**
* Produces a clean, analysis-ready dataset

---

### 3. KPI Analysis

* Computes revenue, profit, and ROI
* Identifies top-performing movies by different metrics
* Compares franchise vs standalone performance
* Analyzes director-level performance
* Applies filtering logic (e.g., ROI calculated only for budget ≥ 10M)

---

### 4. Visualization

* Revenue vs Budget (trend relationship)
* ROI distribution across genres
* Popularity vs Rating analysis
* Revenue trends over time
* Franchise vs standalone comparison

---

## Key Insights

* **Budget vs Revenue:** Higher budgets generally lead to higher revenue, but returns are not strictly proportional.
* **ROI Variability:** Certain genres deliver higher returns but also exhibit greater financial risk.
* **Franchise vs Standalone:** In this dataset, **standalone movies slightly outperform franchises in average revenue**, driven by high-performing titles such as *Avatar* and *Titanic*.
* **Popularity vs Rating:** Weak correlation — popularity is influenced by factors beyond perceived quality.
* **Revenue Trends:** A small number of blockbuster films significantly impact yearly averages.
* **Director Performance:** Directors like *James Cameron* achieve high total revenue through a few exceptionally successful films.

---

## Project Structure

```text
tmdb-movie-project/
│
├── src/
│   ├── fetch_movies.py
│   ├── clean_movies.py
│   ├── analysis.py
│   ├── visualization.py
│
├── notebooks/
│   └── tmdb_movie_analysis.ipynb
│
├── data/
├── images/
│
├── main.py
├── config.py
├── requirements.txt
├── README.md
└── .env
```

---

##  How to Run the Project

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd tmdb-movie-project
```

---

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate the environment:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / WSL**

```bash
source venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure API key

Create a `.env` file in the root directory:

```env
TMDB_API_KEY=your_api_key_here
```

---

### 5. Run the data pipeline

```bash
python main.py
```

---

### 6. Run the analysis notebook

```bash
jupyter notebook
```

Open:

```text
notebooks/tmdb_movie_analysis.ipynb
```

Then select **Run → Run All Cells**

---

## Requirements

* Python 3.9+
* pandas
* numpy
* matplotlib
* seaborn
* requests
* python-dotenv

---

## Business Value

This project provides insights into:

* Key drivers of movie revenue
* Profitability across genres
* Comparative performance of franchises vs standalone films
* Trends in audience engagement and popularity

---

## Conclusion

This project demonstrates a **production-style data pipeline**, combining data engineering and analytical techniques to transform raw API data into actionable insights.

It highlights the importance of robust data handling, structured analysis, and clear communication of results.

---
