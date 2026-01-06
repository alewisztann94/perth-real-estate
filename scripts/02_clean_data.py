import pandas as pd

print("Starting data cleaning...")

# Load datasets
data_2021 = pd.read_csv('data/raw/all_perth_310121.csv')
data_2024 = pd.read_csv('data/raw/perth_property_data.csv')

print(f"Loaded 2021: {len(data_2021):,} rows")
print(f"Loaded 2024: {len(data_2024):,} rows")

# ============================================================================
# CLEAN 2021 DATASET
# ============================================================================
print("\nCleaning 2021 dataset...")

# Standardize column names to lowercase
data_2021.columns = data_2021.columns.str.lower()

# Remove \r from date_sold
data_2021['date_sold'] = data_2021['date_sold'].str.replace('\r', '')

# Keep only columns we care about
cols_2021 = ['address', 'suburb', 'price', 'bedrooms', 'bathrooms', 
             'land_area', 'date_sold', 'postcode', 'latitude', 'longitude', 
             'cbd_dist', 'build_year']
data_2021_clean = data_2021[cols_2021].copy()

# Add source column
data_2021_clean['source'] = '2021_dataset'

print(f"2021 after cleaning: {len(data_2021_clean):,} rows")

# ============================================================================
# CLEAN 2024 DATASET
# ============================================================================
print("\nCleaning 2024 dataset...")

# Standardize column names to lowercase
data_2024.columns = data_2024.columns.str.lower()

# Filter out bad prices (< $50k are likely data errors)
print(f"Before price filter: {len(data_2024):,} rows")
data_2024 = data_2024[data_2024['price'] >= 50000].copy()
print(f"After price filter: {len(data_2024):,} rows (removed {42958 - len(data_2024)} bad prices)")

# Rename columns to match 2021 dataset
data_2024_clean = data_2024.rename(columns={
    'land_size': 'land_area',
    'distance_to_cbd': 'cbd_dist'
}).copy()

# Keep only columns we care about (matching 2021 structure)
cols_2024 = ['address', 'suburb', 'price', 'bedrooms', 'bathrooms', 
             'land_area', 'date_sold', 'postcode', 'latitude', 'longitude', 
             'cbd_dist']
data_2024_clean = data_2024_clean[cols_2024].copy()

# Add build_year column (null for all since 2024 dataset doesn't have it)
data_2024_clean['build_year'] = None

# Add source column
data_2024_clean['source'] = '2024_dataset'

print(f"2024 after cleaning: {len(data_2024_clean):,} rows")

# ============================================================================
# COMBINE DATASETS
# ============================================================================
print("\nCombining datasets...")

combined = pd.concat([data_2021_clean, data_2024_clean], ignore_index=True)

print(f"Combined dataset: {len(combined):,} rows")
print(f"Columns: {combined.columns.tolist()}")

# ============================================================================
# SAVE CLEANED DATA
# ============================================================================
print("\nSaving cleaned data...")

combined.to_csv('data/processed/perth_real_estate_clean.csv', index=False)

print("Done! Cleaned data saved to data/processed/perth_real_estate_clean.csv")

# Show quick stats
print("\n" + "=" * 80)
print("CLEANED DATA SUMMARY")
print("=" * 80)
print(f"Total properties: {len(combined):,}")
print(f"From 2021: {len(combined[combined['source'] == '2021_dataset']):,}")
print(f"From 2024: {len(combined[combined['source'] == '2024_dataset']):,}")
print(f"\nPrice range: ${combined['price'].min():,.0f} - ${combined['price'].max():,.0f}")
print(f"Median price: ${combined['price'].median():,.0f}")
print(f"\nUnique suburbs: {combined['suburb'].nunique()}")
print(f"\nMissing values:")
print(combined.isnull().sum())

#decision to keep certain columns is based on what? and we aren't including an id index for rows?