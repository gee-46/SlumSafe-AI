import sqlite3
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
CSV_FILE = os.path.join(DATA_DIR, "reports.csv")
DB_FILE = os.path.join(DATA_DIR, "slumsafe.db")

def run_migration():
    if not os.path.exists(CSV_FILE):
        print("No reports.csv found. Nothing to migrate.")
        return
        
    print(f"Connecting to {DB_FILE}...")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create the target table structure if it doesn't already exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            crime_type TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    
    print("Reading data from CSV...")
    try:
        df = pd.read_csv(CSV_FILE)
        
        # Insert records row by row
        inserted = 0
        for _, row in df.iterrows():
            cursor.execute('''
                INSERT INTO reports (crime_type, latitude, longitude, timestamp)
                VALUES (?, ?, ?, ?)
            ''', (row['crime_type'], row['latitude'], row['longitude'], row['timestamp']))
            inserted += 1
            
        conn.commit()
        print(f"Successfully migrated {inserted} records to the SQLite database!")
        print("For safety, renaming reports.csv to reports.csv.bak...")
        os.rename(CSV_FILE, CSV_FILE + ".bak")
        
    except Exception as e:
        print(f"Migration Failed: {e}")
        
    finally:
        conn.close()

if __name__ == "__main__":
    run_migration()
