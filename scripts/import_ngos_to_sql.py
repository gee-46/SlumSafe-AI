import sqlite3
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_FILE = os.path.join(DATA_DIR, "slumsafe.db")

def migrate():
    conn = sqlite3.connect(DB_FILE)
    
    # Migrate ngos
    csv_f = os.path.join(DATA_DIR, "ngos.csv")
    if os.path.exists(csv_f):
        df_ngos = pd.read_csv(csv_f)
        df_ngos.to_sql("ngos", conn, if_exists="replace", index=False)
        os.rename(csv_f, csv_f + ".bak")
        print(f"Migrated ngos.csv -> {len(df_ngos)} rows.")
        
    conn.close()

if __name__ == "__main__":
    migrate()
