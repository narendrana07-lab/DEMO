import sqlite3
import pandas as pd

# Load CSV into DataFrame
df = pd.read_csv('data/raw/customers_raw.csv')

# Create SQLite database and table
conn = sqlite3.connect('data/db/analytics.db')
df.to_sql('customers_raw', conn, if_exists='replace', index=False)
conn.close()

print("ETL complete: CSV loaded into SQLite database.")