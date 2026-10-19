import pandas as pd

from src.db import DB_PATH


def export_table(table_name, filename):
    import sqlite3

    conn = sqlite3.connect(DB_PATH)

    try:
        df = pd.read_sql_query(f'SELECT * FROM "{table_name}"', conn)

        output_path = f"data/processed/{filename}"
        df.to_csv(output_path, index=False)

        print(f"Exported {len(df):,} rows to {output_path}")

    finally:
        conn.close()


def export_power_bi_data():
    export_table("customer_flight_summary_view", "dim_customer.csv")

    export_table("clean_flight_activity", "fact_flight_activity.csv")

    export_table("vw_calendar", "dim_calendar.csv")


if __name__ == "__main__":
    export_power_bi_data()
