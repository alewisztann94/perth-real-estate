# Perth Real Estate Analysis

End-to-end data pipeline analyzing 76,000+ property sales across Perth, Western Australia (2021 and 2024 datasets).

## Overview

Combined and cleaned two Kaggle datasets to analyze price trends, suburb comparisons, and geographic patterns in the Perth property market.

## Key Findings

- **35% price increase** across Perth from 2021 to 2024 ($637K → $861K average)
- **Gosnells saw 87% price growth** - largest increase among suburbs with significant sales volume
- **Western suburbs dominate premium market** - Dalkeith ($2.8M), Cottesloe ($2.7M), Peppermint Grove ($2.5M)
- **Price drops linearly with CBD distance** - from $995K within 5km to $461K beyond 30km
- **One-third of all sales** fall in the $500-750K band

## Tech Stack

- Python (pandas) for data cleaning and transformation
- SQLite for data storage and analysis
- SQL for analysis queries

## Project Structure
```
perth-real-estate/
├── data/
│   ├── raw/                    # Original Kaggle datasets
│   ├── processed/              # Cleaned combined CSV
│   └── perth_real_estate.db    # SQLite database
├── scripts/
│   ├── 01_explore_data.py      # Initial data exploration
│   ├── 02_clean_data.py        # Data cleaning and combination
│   ├── 03_load_to_db.py        # Load to SQLite
│   └── 04_analysis_queries.sql # Analysis queries
└── outputs/
```

## Data Cleaning

- Standardized column names across datasets
- Removed invalid prices (<$50K)
- Aligned schema between 2021 and 2024 data
- Combined into single dataset with source tracking

## Notable Query Fixes

During development, identified and corrected several SQL logic issues:

1. **Median calculation** - Original query filtered to median row before aggregation, resulting in COUNT=1 for all suburbs. Fixed using CTEs to calculate stats and median separately, then joining.

2. **Percentage calculation** - Integer division returned 0% for all bands. Fixed by multiplying numerator by 100.0 first to force float conversion.

3. **CBD distance units** - Data stored in metres, not kilometres. Adjusted CASE thresholds by dividing by 1000.

## Running the Project

1. Clone the repo
2. Install dependencies: `pip install pandas`
3. Place raw CSV files in `data/raw/`
4. Run scripts in order:
```
   python scripts/01_explore_data.py
   python scripts/02_clean_data.py
   python scripts/03_load_to_db.py
```
5. Query the database with `04_analysis_queries.sql`

## Data Sources

- [Perth Property Prices 2021](https://www.kaggle.com/datasets/heptix/perth-property-prices)
- [Perth Property Prices 2024](https://www.kaggle.com/datasets/syuzai/perth-house-prices)

## Future Improvements

- Scrape recent sales data for 2025 comparison
- Add geographic visualization (mapping price by suburb)
- Build automated pipeline to refresh data periodically