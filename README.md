# TMDB Movie Data Analysis using Python and TMDB API

## Project Overview

This project builds a complete movie data analysis pipeline using **Python**, **Pandas**, and the **TMDB API**.

The goal of the project is to collect movie data from an API, clean and transform the dataset, perform key performance analysis, and visualize important trends in the movie industry.

The project demonstrates key data analysis tasks including **API data extraction, data cleaning, feature engineering, KPI analysis, and data visualization**.

---

## Project Objectives

The main objectives of this project are:

- Fetch movie data from the **TMDB API**
- Clean and transform the dataset
- Perform **Key Performance Indicator (KPI) analysis**
- Compare **franchise movies vs standalone movies**
- Identify **most successful franchises and directors**
- Visualize trends using **Matplotlib**

---

## Technologies Used

The following tools and libraries were used in this project:

- Python
- Pandas
- Matplotlib
- Requests
- Python-dotenv
- TMDB API

---


## Project Structure

```
tmdb-movie-project/
│
├── data/
│   ├── raw_movies.csv
│   └── cleaned_movies.csv
│
├── images/
│   ├── franchise_vs_standalone.png
│   ├── popularity_vs_rating.png
│   ├── revenue_vs_budget.png
│   ├── roi_by_genre.png
│   └── yearly_revenue.png
│
├── notebooks/
│   ├── TMDB Movie Data Analysis using Pandas and APIs.ipynb
│   └── tmdb_analysis.py
│
├── reports/
│   └── tmdb-movie-project-report.md
│
├── src/
│   ├── fetch_movies.py
│   ├── cleaned_movies.py
│   ├── analysis.py
│   └── visualization.py
│
├── tests/
│
├── main.py
├── README.md
└── .env
```


---

## Data Pipeline

The project follows this workflow:

1. **Data Extraction**  
   Fetch movie data from the TMDB API.

2. **Data Cleaning**  
   Remove unnecessary columns, handle missing values, and format data.

3. **Feature Engineering**  
   Create new variables such as profit and ROI.

4. **KPI Analysis**  
   Analyze revenue, profit, ROI, franchises, and directors.

5. **Visualization**  
   Create charts to explore trends and relationships.

---

## Key Insights

The analysis revealed several important insights:

- Movies with larger budgets tend to generate higher revenue, indicating a positive relationship between investment and earnings.
- Return on investment (ROI) varies across genres, showing that profitability depends on the type of movie.
- The relationship between popularity and rating exists but is not strictly linear.
- Both franchise and standalone movies perform strongly, with no significant difference in average revenue in this dataset.
- Certain directors consistently produce successful movies.

---

## Author

Denyse AGAHOZO 
Data Engineering in Apprenticeship Programme at AmaliTech