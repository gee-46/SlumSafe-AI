import pandas as pd
import warnings

# Suppress parse warnings for mixed formats
warnings.filterwarnings('ignore')

print("Fetching data from City of Chicago API (Socrata)... pulling 10,000 recent records")
# We use Socrata API for City of Chicago to bypass Kaggle account requirements
url = "https://data.cityofchicago.org/resource/ijzp-q8t2.csv?$limit=10000"

# Fetch data using pandas
df = pd.read_csv(url)

print(f"Data fetched successfully! Found {len(df)} rows.")

# Find the exact names for standard fields which vary whether capitalized or not
date_col = 'date' if 'date' in df.columns else 'Date'
lat_col = 'latitude' if 'latitude' in df.columns else 'Latitude'
lon_col = 'longitude' if 'longitude' in df.columns else 'Longitude'
type_col = 'primary_type' if 'primary_type' in df.columns else 'Primary Type'

print("Extracting Datetime...")
# Date has formats like "2023-01-01T12:00:00.000" in Socrata API
df[date_col] = pd.to_datetime(df[date_col], format='mixed', errors='coerce')

df_extracted = pd.DataFrame()
df_extracted['latitude'] = df[lat_col]
df_extracted['longitude'] = df[lon_col]
df_extracted['hour'] = df[date_col].dt.hour.astype('Int64') # keep as int

# Also pull crime_type so it doesn't break the random forest model trained previously
if type_col in df.columns:
    df_extracted['crime_type'] = df[type_col]
else:
    df_extracted['crime_type'] = "Unknown"

# Clean NaN values
df_extracted = df_extracted.dropna()

print(f"Cleaned data rows remaining: {len(df_extracted)}")

import os
base_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(base_dir, 'data', 'crime_data.csv')
os.makedirs(os.path.dirname(output_path), exist_ok=True)
df_extracted.to_csv(output_path, index=False)
print(f"Saved real Chicago dataset to {output_path} with keys: latitude, longitude, hour")

