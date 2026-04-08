import sqlite3
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_FILE = os.path.join(DATA_DIR, "slumsafe.db")

def migrate():
    conn = sqlite3.connect(DB_FILE)
    
    # Migrate emergency contacts
    em_csv = os.path.join(DATA_DIR, "emergency_contacts.csv")
    if os.path.exists(em_csv):
        df_em = pd.read_csv(em_csv)
        df_em.to_sql("emergency_contacts", conn, if_exists="replace", index=False)
        os.rename(em_csv, em_csv + ".bak")
        print(f"Migrated emergency_contacts.csv -> {len(df_em)} rows.")

    # Migrate crime_data
    crime_csv = os.path.join(DATA_DIR, "crime_data.csv")
    if os.path.exists(crime_csv):
        df_cr = pd.read_csv(crime_csv)
        df_cr.to_sql("crime_data", conn, if_exists="replace", index=False)
        os.rename(crime_csv, crime_csv + ".bak")
        print(f"Migrated crime_data.csv -> {len(df_cr)} rows.")
        
    conn.close()

if __name__ == "__main__":
    migrate()
