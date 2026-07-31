# NSE Sector Health Monitor

An end-to-end automated system that tracks and scores the health of all major NSE sectoral indices daily using real market data.

## What it does
Every weekday at 4PM, the pipeline automatically fetches live NSE data, computes a composite health score for each sector, stores results in a SQL database, and exports fresh data for the Tableau dashboard.

## Dashboard
![Dashboard](Screenshot%202026-07-26%20at%2019.32.14.png)

The interactive Tableau dashboard shows:
- **Today's Sector Health Rankings** — which sectors are Strong, Neutral, or Weak
- **Sector Health Trends** — how each sector's health score has evolved over 1.5 years
- **Sector Risk vs Return Analysis** — which sectors offer the best return for their risk
- **Sector Momentum** — which sectors are accelerating vs decelerating

## Scoring Model
Each sector receives a composite health score (0-100) calculated as a weighted combination of:
| Metric | Weight |
|---|---|
| 30-day rolling return | 25% |
| 90-day rolling return | 20% |
| Volatility (inverted) | 20% |
| Momentum | 20% |
| Relative Strength vs Nifty 50 | 15% |

Metrics are z-score normalised and min-max scaled to 0-100.

## Tech Stack
- **Python** — data pipeline, scoring model
- **Pandas & NumPy** — data processing and statistical calculations
- **yfinance** — live NSE data fetching
- **SQLite** — local database storage
- **Tableau** — interactive dashboard
- **cron** — daily automation (Mac)

## Project Structure
```
sector-health/
├── pipeline.py       # Fetches and processes NSE data
├── scoring.py        # Calculates composite health scores
├── database.py       # Stores results in SQLite + exports CSVs
├── sector_health.db  # SQLite database
└── *.csv             # Exported data for Tableau
```

## How to Run
```bash
pip install yfinance pandas numpy
python pipeline.py
python scoring.py
python database.py
```

## Sectors Tracked
Banking, IT, Pharma, Auto, FMCG, Realty, Energy, Metal, Media, Infra
