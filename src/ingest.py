import pandas as pd
import sqlite3
from pathlib import Path


def ingest_csv_files(db_path="data/loyalty.db", csv_folder_path="data/raw"):
    """
    Ingest CSV files from a folder into a SQLite database.

    Args:
        db_path: Path to the SQLite database file
        csv_folder_path: Path to the folder containing CSV files
    """
    conn = sqlite3.connect(db_path)
    csv_folder = Path(csv_folder_path)

    table_names = {
        "Calendar.csv": "raw_calendar",
        "Customer Loyalty History.csv": "raw_loyalty_history",
        "Customer Flight Activity.csv": "raw_flight_activity",
        "Airline Loyalty Data Dictionary.csv": "raw_data_dictionary",
    }

    try:
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

            print(
                f"{table_name}: "
                f"CSV = {csv_rows:,}, "
                f"SQLite = {db_rows:,} → {status}"
            )
            print(f"Imported {csv_file.name} -> {table_name} ({len(df):,} rows)")
    finally:
        conn.close()


if __name__ == "__main__":
    ingest_csv_files()
