import pandas as pd
import sqlite3
from pathlib import Path

conn = sqlite3.connect("data/loyalty.db")

csv_folder = Path("data/raw")

table_names = {
    "Calendar.csv": "raw_calendar",
    "Customer Loyalty History.csv": "raw_loyalty_history",
    "Customer Flight Activity.csv": "raw_flight_activity",
    "Airline Loyalty Data Dictionary.csv": "raw_data_dictionary",
}

for csv_file in csv_folder.glob("*.csv"):
    table_name = table_names.get(csv_file.name)

    df = pd.read_csv(csv_file)
    csv_rows = len(df)

    df.to_sql(table_name, conn, if_exists="replace", index=False)

    cursor = conn.execute(f"SELECT COUNT(*) FROM [{table_name}]")
    db_rows = cursor.fetchone()[0]

    # Compare
    if csv_rows == db_rows:
        status = "✓ MATCH"
    else:
        status = "✗ MISMATCH"

    print(f"{table_name}: " f"CSV = {csv_rows:,}, " f"SQLite = {db_rows:,} → {status}")

    print(f"Imported {csv_file.name} -> {table_name} ({len(df):,} rows)")

conn.close()
