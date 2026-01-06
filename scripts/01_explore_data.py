import pandas as pd
import os

print("Script started!")  # Add this line

# Set pandas display options to see more
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# Load both datasets
print("Loading datasets...\n")

data_2021 = pd.read_csv('data/raw/all_perth_310121.csv')
data_2024 = pd.read_csv('data/raw/perth_property_data.csv')

# Basic exploration
print("=" * 80)
print("2021 DATASET")
print("=" * 80)
print(f"Rows: {len(data_2021):,}")
print(f"Columns: {len(data_2021.columns)}")
print(f"\nColumn names:\n{data_2021.columns.tolist()}\n")
print("First few rows:")
print(data_2021.head())
print("\nData types:")
print(data_2021.dtypes)
print("\nMissing values:")
print(data_2021.isnull().sum())

print("\n" + "=" * 80)
print("2024 DATASET")
print("=" * 80)
print(f"Rows: {len(data_2024):,}")
print(f"Columns: {len(data_2024.columns)}")
print(f"\nColumn names:\n{data_2024.columns.tolist()}\n")
print("First few rows:")
print(data_2024.head())
print("\nData types:")
print(data_2024.dtypes)
print("\nMissing values:")
print(data_2024.isnull().sum())

print("\n" + "=" * 80)
print("COLUMN COMPARISON")
print("=" * 80)
print(f"\nColumns in BOTH datasets:")
common = set(data_2021.columns) & set(data_2024.columns)
print(common)

print(f"\nColumns ONLY in 2021:")
print(set(data_2021.columns) - set(data_2024.columns))

print(f"\nColumns ONLY in 2024:")
print(set(data_2024.columns) - set(data_2021.columns))

# Quick stats on price if column exists
print("\n" + "=" * 80)
print("PRICE STATISTICS")
print("=" * 80)

for df_name, df in [("2021", data_2021), ("2024", data_2024)]:
    price_cols = [col for col in df.columns if 'price' in col.lower()]
    if price_cols:
        print(f"\n{df_name} - {price_cols[0]}:")
        print(df[price_cols[0]].describe())