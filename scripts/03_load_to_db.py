import pandas as pd
import sqlite3

print("Loading cleaned data into SQLite database...")

# Load cleaned data
df = pd.read_csv('data/processed/perth_real_estate_clean.csv')
print(f"Loaded {len(df):,} rows")

# Connect to SQLite (creates file if doesn't exist)
conn = sqlite3.connect('data/perth_real_estate.db')

# Load to database
df.to_sql('properties', conn, if_exists='replace', index=False)

print(f"✓ Loaded {len(df):,} rows into 'properties' table")

# Verify it worked
result = conn.execute("SELECT COUNT(*) FROM properties").fetchone()
print(f"✓ Verified: {result[0]:,} rows in database")

# Show some quick stats
print("\n" + "=" * 80)
print("DATABASE READY")
print("=" * 80)
print("Location: data/perth_real_estate.db")
print("Table: properties")
print(f"Rows: {result[0]:,}")
print("\nYou can now write SQL queries against this database!")

conn.close()