import pandas as pd
from src.db import load_table, trim_table
import sqlite3


# Loading the raw tables from SQLite database
def load_raw_data():
    raw_flight_activity = load_table("raw_flight_activity")
    raw_loyalty_history = load_table("raw_loyalty_history")

    return raw_flight_activity, raw_loyalty_history


# Creating the copy of raw dataframes and performing data cleaning operations
def clean_data():
    raw_flight_activity, raw_loyalty_history = load_raw_data()

    raw_flight_rows = len(raw_flight_activity)
    raw_loyalty_rows = len(raw_loyalty_history)

    clean_flight_activity = raw_flight_activity.copy()
    clean_loyalty_history = raw_loyalty_history.copy()

    # ========================
    # Dropping duplicate rows
    # ========================

    clean_flight_activity = clean_flight_activity.drop_duplicates()

    # ============================
    # Adding boolean flag columns
    # ============================

    # Adding a missing salary boolean column to flag rows
    clean_loyalty_history["salary_is_missing"] = clean_loyalty_history["Salary"].isna()

    # Adding a suspicious salary boolean column to flag rows
    clean_loyalty_history["salary_is_suspicious"] = clean_loyalty_history["Salary"] < 0

    # Adding a Is_Churned boolean column to mark if a customer is active or churned
    clean_loyalty_history["Is_Churned"] = clean_loyalty_history[
        "Cancellation Year"
    ].notna()

    # =========================================================
    # Creating a proper datetime columns 'Enrollment_Date' and
    # 'Cancellation_Date'(currently split Year/Month integers)
    # =========================================================
    clean_loyalty_history["Cancellation Date"] = pd.to_datetime(
        {
            "year": clean_loyalty_history["Cancellation Year"],
            "month": clean_loyalty_history["Cancellation Month"],
            "day": 1,
        }
    )

    clean_loyalty_history["Enrollment Date"] = pd.to_datetime(
        {
            "year": clean_loyalty_history["Enrollment Year"],
            "month": clean_loyalty_history["Enrollment Month"],
            "day": 1,
        }
    )

    # =================================================================================
    # Creating a Tenure_Months column from enrollment to cancellation/last active date
    # =================================================================================

    # Creating a valid calendar date to use it as customer last active date
    clean_flight_activity["Flight Date"] = pd.to_datetime(
        {
            "year": clean_flight_activity["Year"],
            "month": clean_flight_activity["Month"],
            "day": 1,
        }
    )

    # Grouping customer loyalty number to get their last(max) activity(flight) date
    last_activity = (
        clean_flight_activity.groupby("Loyalty Number")["Flight Date"]
        .max()
        .reset_index()
        .rename(columns={"Flight Date": "Last Activity Month"})
    )

    # Merging loyalty_history and last_activity dataframes to use the newly created metric "Last Activity Month"
    clean_loyalty_history = clean_loyalty_history.merge(
        last_activity, on="Loyalty Number", how="left"
    )

    # Calcualting Tenure Months
    end_date = clean_loyalty_history["Cancellation Date"].fillna(
        clean_loyalty_history["Last Activity Month"]
    )

    clean_loyalty_history["Tenure Months"] = (
        end_date.dt.year - clean_loyalty_history["Enrollment Date"].dt.year
    ) * 12 + (end_date.dt.month - clean_loyalty_history["Enrollment Date"].dt.month)

    # =========================
    # Standardize text fields
    # =========================

    # Trimming whitespaces from string columns
    clean_flight_activity, clean_loyalty_history = [
        trim_table(df) for df in (clean_flight_activity, clean_loyalty_history)
    ]

    postal_regex = r"^[A-CEGHJ-NPR-TV-Z]\d[A-CEGHJ-NPR-TV-Z] \d[A-CEGHJ-NPR-TV-Z]\d$"

    # Creating a new postal code validation flag boolean column
    clean_loyalty_history["postal_code_is_valid"] = clean_loyalty_history[
        "Postal Code"
    ].str.match(postal_regex, na=False)

    # Seting invalid Canadian postal codes to NULL
    clean_loyalty_history.loc[
        ~clean_loyalty_history["Postal Code"].str.match(postal_regex, na=False),
        "Postal Code",
    ] = pd.NA

    # ===================================================
    # Type-cast Loyalty Card, Education, Marital Status,
    # Enrollment Type as 'category' dtype
    # ===================================================

    categorical_cols = [
        "Loyalty Card",
        "Education",
        "Marital Status",
        "Enrollment Type",
    ]

    for col in categorical_cols:
        clean_loyalty_history[col] = clean_loyalty_history[col].astype("category")

    return (
        clean_flight_activity,
        clean_loyalty_history,
        raw_flight_rows,
        raw_loyalty_rows,
    )


if __name__ == "__main__":
    # Create database connection only when running directly
    conn = sqlite3.connect("data/loyalty.db")

    try:
        (
            clean_flight_activity,
            clean_loyalty_history,
            raw_flight_rows,
            raw_loyalty_rows,
        ) = clean_data()

        clean_loyalty_history.to_sql(
            "clean_loyalty_history", conn, if_exists="replace", index=False
        )

        clean_flight_activity.to_sql(
            "clean_flight_activity", conn, if_exists="replace", index=False
        )

        print(clean_loyalty_history.shape)
        print(clean_flight_activity.shape)
        print(f"Raw Flight Rows: {raw_flight_rows}")
        print(f"Raw Loyalty Rows: {raw_loyalty_rows}")
    finally:
        conn.close()
