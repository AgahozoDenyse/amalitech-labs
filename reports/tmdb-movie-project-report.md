# TMDB Movie Data Analysis using Python, Pandas, and API

## Introduction

The movie industry generates billions of dollars annually, making it an important domain for data-driven analysis. Understanding the factors that influence movie success—such as budget, genre, and popularity—can provide valuable insights into revenue and profitability trends.

This project implements a complete data analysis pipeline using Python and the TMDB API. The pipeline extracts movie data, cleans and transforms it, computes key performance indicators (KPIs), and generates visual insights.

---

## Data Extraction

Movie data was obtained from the TMDB API using a predefined list of movie IDs:

299534, 19995, 140607, 299536, 597, 135397, 420818, 24428, 168259, 99861, 284054, 12445, 181808, 330457, 351286, 109445, 321612, 260513.

The extracted data was stored in a Pandas DataFrame and saved as `raw_movies.csv` in the data folder.

### Robust API Handling

To ensure reliability, the extraction process includes:

* Retry logic with exponential backoff
* Graceful handling of API failures
* Skipping invalid movie IDs (e.g., ID = 0)
* Logging of failed requests

These improvements make the pipeline resilient to network or API-related issues.

---

## Data Cleaning and Transformation

### Removed Unnecessary Columns

The following columns were removed to simplify the dataset:

* adult
* imdb_id
* original_title
* video
* homepage

---

### Flattened JSON Columns

The following JSON fields were transformed into readable formats:

* genres
* production_companies
* production_countries
* spoken_languages
* belongs_to_collection

---

### Data Type Conversion

To enable proper analysis:

* `release_date` → converted to datetime
* Numerical fields (`budget`, `revenue`, `runtime`, `popularity`, `vote_count`, `vote_average`) → converted to numeric
* Invalid values handled using `errors="coerce"`

---

### Feature Engineering

New variables were created:

* `budget_musd` = budget / 1,000,000
* `revenue_musd` = revenue / 1,000,000

Additional derived metrics:

* `profit_musd` = revenue_musd − budget_musd
* `roi` = revenue_musd / budget_musd

These features enable meaningful financial comparisons and profitability analysis.

---

## KPI Analysis

Key Performance Indicators (KPIs) were used to evaluate movie performance across financial and audience metrics. These include revenue, profit, ROI, popularity, and ratings.

A reusable ranking function was implemented to standardize comparisons:

```python
def rank_movies(df, column, ascending=False, n=10):
    return df.sort_values(column, ascending=ascending)[["title", column]].head(n)
```

This function allows consistent identification of top-performing movies across different metrics.

---

## Franchise Analysis

The dataset was used to compare franchise and standalone movies.

Findings include:

* Both franchise and standalone movies generate high revenue
* Standalone movies slightly outperform franchises in average revenue within this dataset
* Performance is driven more by individual blockbuster titles than by category

---

## Data Visualization

Several visualizations were created to explore relationships between key variables.

---

### Revenue vs Budget

![Revenue vs Budget](../images/revenue_vs_budget.png)

**Figure 1:** Relationship between movie budget and revenue.

Movies with larger budgets generally generate higher revenue. However, the relationship is not strictly proportional, indicating diminishing returns at higher budget levels.

---

### ROI Distribution by Genre

![ROI by Genre](../images/roi_by_genre.png)

**Figure 2:** Distribution of ROI across movie genres.

ROI varies significantly across genres. Some genres show higher median ROI, suggesting stronger profitability, while others exhibit greater variability and risk.

---

### Popularity vs Rating

![Popularity vs Rating](../images/popularity_vs_rating.png)

**Figure 3:** Relationship between movie ratings and popularity.

There is a weak positive relationship between ratings and popularity. However, popularity is influenced by multiple factors beyond ratings alone.

---

### Yearly Revenue Trend

![Yearly Revenue](../images/yearly_revenue.png)

**Figure 4:** Average revenue by release year.

Revenue trends fluctuate across years, with spikes driven by blockbuster releases. This indicates that a small number of high-performing films significantly impact yearly averages.

---

### Franchise vs Standalone Movies

![Franchise vs Standalone](../images/franchise_vs_standalone.png)

**Figure 5:** Comparison of average revenue between franchise and standalone movies.

Both categories perform strongly, but standalone movies slightly outperform franchises in this dataset, influenced by major individual successes.

---

## Conclusion

This project demonstrates how to build a complete movie data analysis pipeline using Python, Pandas, and the TMDB API.

The pipeline was used to:

* Extract real-world data from an API
* Clean and transform complex datasets
* Compute meaningful KPIs
* Generate visual insights

Key findings include:

* Higher budgets generally lead to higher revenue, but with diminishing returns
* ROI varies significantly, highlighting efficiency differences across movies
* Standalone movies slightly outperform franchises in this dataset
* A small number of blockbuster films dominate overall revenue trends

Overall, this project demonstrates how robust data engineering and structured analysis can transform raw API data into meaningful and actionable insights.
