# TMDB Movie Data Pipeline

An end-to-end data pipeline that extracts movie metadata and credits from the [TMDB API](https://developer.themoviedb.org/), cleans and enriches the data, computes KPIs, runs analytical queries, and produces visualisation charts.

---

## Project Structure

```
.
├── config.py            # Centralised settings (IDs, paths, constants)
├── main.py              # Pipeline entry point
├── requirements.txt     # Pinned dependencies
├── src/
│   ├── fetch_movies.py  # TMDB API extraction with retry + rate limiting
│   ├── clean_movies.py  # Data cleaning and normalisation
│   ├── analysis.py      # KPI computation and analytical queries
│   └── visualization.py # Chart generation (matplotlib)
├── data/                # Generated CSV outputs (git-ignored)
└── images/              # Generated PNG charts (git-ignored)
```

---

## Setup

### 1. Clone the repository

```bash
git clone <repo-url>
cd amalitech-labs
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your API key

Create a `.env` file in the project root (**never commit this file**):

```env
TMDB_API_KEY=your_api_key_here
```

Get a free API key at <https://www.themoviedb.org/settings/api>.

---

## Running the Pipeline

```bash
python main.py
```

The pipeline executes five steps in sequence:

| Step | Module | Output |
|------|--------|--------|
| 1. Fetch | `src/fetch_movies.py` | `data/raw_movies.csv` |
| 2. Clean | `src/clean_movies.py` | `data/cleaned_movies.csv` |
| 3. KPIs | `src/analysis.compute_kpis` | Enriched DataFrame in memory |
| 4. Analysis | `src/analysis.run_analysis` | Logged rankings and summaries |
| 5. Visualise | `src/visualization.py` | `images/*.png` |

If any movie IDs fail after all retries, they are written to `data/failed_ids.txt` for inspection or re-run.

---

## Configuration

Edit `config.py` to change behaviour without touching pipeline code:

| Variable | Default | Description |
|----------|---------|-------------|
| `MOVIE_IDS` | 18 film IDs | TMDB IDs to fetch |
| `MIN_BUDGET_FOR_ROI` | `10` | Minimum budget (M USD) required to compute ROI |
| `TOP_N` | `10` | Number of results returned in each ranking |
| `RAW_DATA_PATH` | `data/raw_movies.csv` | Output path for raw data |
| `CLEAN_DATA_PATH` | `data/cleaned_movies.csv` | Output path for cleaned data |

---

## Output Charts

| File | Description |
|------|-------------|
| `revenue_vs_budget.png` | Scatter: production budget vs box-office revenue |
| `roi_by_genre.png` | Box plot: ROI distribution per genre |
| `popularity_vs_rating.png` | Scatter: audience rating vs TMDB popularity |
| `yearly_revenue.png` | Line: average revenue trend by release year |
| `franchise_vs_standalone.png` | Bar: mean revenue for franchise vs standalone films |

---

## Key Insights

- **Budget vs Revenue:** Higher budgets correlate with higher revenue, but returns are not strictly proportional — a handful of outliers (e.g. *Avatar*, *Titanic*) drive the relationship.
- **ROI Variability:** Certain genres deliver outsized returns but also exhibit greater financial risk.
- **Franchise vs Standalone:** In this dataset, standalone films slightly outperform franchises in average revenue, driven by individual blockbusters.
- **Popularity vs Rating:** Weak correlation — TMDB popularity is driven by recency and social buzz, not just quality.
- **Director Performance:** A small number of directors account for a disproportionate share of total revenue.

---

## Dependencies

| Package | Version |
|---------|---------|
| pandas | 3.0.1 |
| numpy | 2.4.3 |
| matplotlib | 3.10.8 |
| requests | 2.32.5 |
| python-dotenv | 1.0.1 |

Requires **Python 3.10+** (uses `X | Y` union type syntax).
