# TMDB Movie Data Analysis

## 1. Introduction

This project builds a data pipeline to collect, process, and analyze movie data from the TMDB API.  
The goal is to understand movie performance using financial metrics, audience engagement, and investment efficiency.

The pipeline follows a structured approach including data extraction, cleaning, feature engineering, analysis, and visualization.

---

## 2. Data Source

The data used in this project is retrieved from the TMDB (The Movie Database) API.

Two main endpoints are used:
- Movie details (budget, revenue, popularity, etc.)
- Movie credits (cast and crew information)

The dataset consists of a selected set of popular movies.

---

## 3. Methodology

The workflow is organized into different stages:

### Data Extraction
- Movie data and credits are fetched using the TMDB API  
- Parallel processing is used to improve performance  

### Data Cleaning
- Nested JSON fields are flattened  
- Irrelevant columns are removed  
- Missing or inconsistent values are handled  
- Key fields such as genres and collections are standardized  

### Feature Engineering
New variables are created to support analysis:
- `budget_musd` → budget in million USD  
- `revenue_musd` → revenue in million USD  
- `profit_musd` → revenue minus budget  
- `roi` → return on investment  

### Analysis
Movies are ranked using:
- Revenue  
- Budget  
- Profit  
- ROI  
- Ratings and popularity  

---

## 4. Results and Analysis

### Top Performing Movies

*Avatar* is the highest earning movie in the dataset, generating approximately **2923 million USD** in revenue.  
It is followed by *Avengers: Endgame* and *Titanic*, which also show strong performance.

In terms of profit, the same pattern is observed. These movies not only generated high revenue but also performed well after accounting for production costs.

---

### Return on Investment (ROI)

*Avatar* has the highest ROI, exceeding **12**, meaning it generated more than twelve times its production cost.

Other movies such as *Titanic* and *Jurassic World* also show strong ROI values.

On the lower side, movies like *Star Wars: The Last Jedi* have lower ROI, indicating less efficiency despite being profitable.

![ROI Distribution](reports/figures/roi_distribution.png)

---

### Budget and Revenue Relationship

There is a positive relationship between budget and revenue.  
Movies with larger budgets generally generate higher revenue.

However, higher budgets do not always guarantee better efficiency. Some movies achieve strong performance with relatively moderate budgets.

![Revenue vs Budget](reports/figures/revenue_vs_budget.png)

---

### Audience Engagement

*The Avengers* has the highest number of votes, indicating strong audience engagement.

Highly rated movies include *Avengers: Endgame* and *Avengers: Infinity War*, showing strong audience approval.

However, some movies with high revenue have lower ratings, showing that popularity and perceived quality are not always aligned.

![Popularity vs Rating](reports/figures/popularity_vs_rating.png)

---

### Franchise vs Standalone Movies

Franchise movies generally show more stable performance compared to standalone movies.

However, standalone movies can still achieve high success, although with greater variability.

![Franchise vs Standalone](reports/figures/franchise_vs_standalone.png)

---

### Revenue Trends Over Time

Revenue trends vary across years, with peaks corresponding to major blockbuster releases.

This indicates that performance is influenced by individual high-performing movies rather than a steady trend.

![Yearly Revenue Trend](reports/figures/yearly_revenue_trend.png)

---

## 5. Key Observations

- Higher budgets tend to lead to higher revenue  
- Profit depends on both revenue and cost  
- ROI highlights efficiency rather than scale  
- Popularity and ratings do not always correlate  
- Franchise movies show more consistent performance  

---

## 6. Limitations

- The dataset includes only a limited number of selected movies  
- Results are not representative of the full movie industry  
- Some filters return empty results due to missing data  
- External factors such as inflation are not considered  

---

## 7. Challenges

- Handling nested JSON data required additional processing  
- Some API responses were incomplete or inconsistent  
- Debugging data flow across multiple pipeline stages  
- Ensuring data consistency after transformations  

---

## 8. Conclusion

This project demonstrates how raw API data can be transformed into meaningful insights through a structured data pipeline.

The analysis shows that both budget and efficiency play important roles in movie performance.  
Overall, the pipeline provides useful insights and can be extended for larger datasets or deeper analysis.

---