import pandas as pd
import numpy as np

np.random.seed(42)

def generate_city_data(center_lat, center_lon, num_records):
    lats = center_lat + np.random.randn(num_records) * 0.015
    lons = center_lon + np.random.randn(num_records) * 0.015
    hours = np.random.randint(0, 24, num_records)
    types = np.random.choice(['Theft', 'Assault', 'Vandalism', 'Burglary', 'Other'], num_records)
    
    return pd.DataFrame({
        'latitude': lats,
        'longitude': lons,
        'hour': hours,
        'crime_type': types
    })

df_mumbai = generate_city_data(19.0380, 72.8538, 200) # Mumbai (Dharavi)
df_goa = generate_city_data(15.4909, 73.8278, 150)    # Goa
df_bangalore = generate_city_data(12.9716, 77.5946, 100) # Bangalore

df_all = pd.concat([df_mumbai, df_goa, df_bangalore])

import os
csv_path = 'C:/Users/Dell/.gemini/antigravity/scratch/SlumSafe-AI/data/crime_data.csv'
if os.path.exists(csv_path):
    df_existing = pd.read_csv(csv_path)
    df_combined = pd.concat([df_existing, df_all])
    df_combined.to_csv(csv_path, index=False)
    print(f"Successfully merged Indian datasets with existing Chicago dataset! Total rows: {len(df_combined)}")
else:
    df_all.to_csv(csv_path, index=False)
    print("Successfully generated custom Indian hotspot dataset!")
