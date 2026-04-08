import sqlite3
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "data", "slumsafe.db")

def check_and_update():
    if not os.path.exists(DB_FILE):
        print("DB not found")
        return
    
    conn = sqlite3.connect(DB_FILE)
    try:
        df = pd.read_sql_query("SELECT * FROM emergency_contacts", conn)
        print("Current emergency_contacts:")
        print(df)
        
        # Check if there's a Bangalore entry
        # Bangalore lat/lon is approx 12.97, 77.59
        bangalore_entries = df[
            (df['latitude'] > 12.9) & (df['latitude'] < 13.0) & 
            (df['longitude'] > 77.5) & (df['longitude'] < 77.7)
        ]
        
        if not bangalore_entries.empty:
            print("Found Bangalore entries, updating phone...")
            cursor = conn.cursor()
            # Update all entries that fall within the Bangalore bounds
            cursor.execute(
                "UPDATE emergency_contacts SET phone = ? WHERE latitude > 12.9 AND latitude < 13.0 AND longitude > 77.5 AND longitude < 77.7", 
                ("+919740259942",)
            )
            conn.commit()
            print("Updated successfully")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    check_and_update()
