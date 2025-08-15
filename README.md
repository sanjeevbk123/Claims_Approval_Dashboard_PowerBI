# Insurance Claims Performance Dashboard (One-Day Build)

This project is a compact, portfolio-ready BI solution that demonstrates:
- Synthetic data generation for insurance claims
- Python ETL (cleaning and transformations)
- SQLite data storage for analytics
- Artifacts ready to plug into Tableau or Power BI

## Quick Start (Local Machine)
1) Install Python 3.12+ and PyCharm (Community is fine).
2) Open this folder as a project in PyCharm.
3) In PyCharm Terminal: `python -m venv .venv` then activate it (Windows: `.venv\Scripts\activate`, macOS/Linux: `source .venv/bin/activate`)
4) Install deps: `pip install -r requirements.txt`
5) Run: `python src/generate_and_etl.py`
6) Open `data/processed/clean_claims.csv` (for Tableau/Power BI) or `data/processed/insurance.db` (SQLite) to build dashboards.

## What it builds
- `data/raw/insurance_claims.csv`: Raw synthetic claims
- `data/processed/clean_claims.csv`: Cleaned dataset
- `data/processed/insurance.db`: SQLite database with `Claims` table
- `reports/summary.xlsx`: Quick Excel with a few pivot-style summaries
- `sql/sample_queries.sql`: Sample SQL you can show or run

## Resume bullets (you can adapt)
• Designed and developed an Insurance Claims Performance Dashboard using SQL, Tableau/Power BI, and Python, tracking KPIs like approval rate, fraud flags, and settlement time.  
• Built an ETL pipeline in Python to generate, clean, and process 500+ claim records, storing them in SQLite for BI reporting.  
• Created an interactive dashboard with filters and KPIs, enabling self-service analytics for claim trends and agent performance.

