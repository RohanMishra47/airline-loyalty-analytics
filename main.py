import sqlite3

from src.db import DB_PATH
from src.ingest import ingest_csv_files
from src.clean import clean_data
from src.validate import validate_data
from src.export import export_power_bi_data
from src.eda import (
    plot_churn_by_tenure,
    plot_churn_by_province,
    plot_monthly_flight_trends,
    plot_yoy_growth,
    plot_quarterly_trends,
    plot_enrollment_engagement,
    plot_enrollment_clv,
    plot_clv_by_loyalty_card,
    plot_clv_by_education,
    plot_correlation_heatmap,
)


def main():
    print("\n=== Step 1: Ingest raw CSV files ===")
    ingest_csv_files(
        db_path=DB_PATH,
        csv_folder_path="data/raw",
    )

    print("\n=== Step 2: Clean data ===")
    (
        clean_flight_activity,
        clean_loyalty_history,
        raw_flight_rows,
        raw_loyalty_rows,
    ) = clean_data()

    print("\n=== Step 3: Validate cleaned data ===")
    validate_data(
        clean_flight_activity,
        clean_loyalty_history,
        raw_flight_rows,
        raw_loyalty_rows,
    )

    print("\n=== Step 4: Save validated tables to SQLite ===")
    with sqlite3.connect(DB_PATH) as conn:
        clean_loyalty_history.to_sql(
            "clean_loyalty_history",
            conn,
            if_exists="replace",
            index=False,
        )

        clean_flight_activity.to_sql(
            "clean_flight_activity",
            conn,
            if_exists="replace",
            index=False,
        )

    print("\n=== Step 5: Export Power BI data ===")
    export_power_bi_data()

    print("\n=== Step 6: Generate EDA plots ===")
    eda_functions = [
        plot_churn_by_tenure,
        plot_churn_by_province,
        plot_monthly_flight_trends,
        plot_yoy_growth,
        plot_quarterly_trends,
        plot_enrollment_engagement,
        plot_enrollment_clv,
        plot_clv_by_loyalty_card,
        plot_clv_by_education,
        plot_correlation_heatmap,
    ]

    for plot_function in eda_functions:
        print(f"Generating: {plot_function.__name__}")
        plot_function()

    print("\n=== Pipeline completed successfully ===")


if __name__ == "__main__":
    main()
