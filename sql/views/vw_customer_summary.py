from src.db import execute_script

sql = """
DROP VIEW IF EXISTS customer_flight_summary_view;

CREATE VIEW customer_flight_summary_view AS
WITH customer_flight_date AS (
    SELECT 
        "Loyalty Number", 
        SUM("Total Flights") AS total_flights, 
        SUM("Distance") AS total_distance, 
        SUM("Points Accumulated") AS total_points,
        COUNT(DISTINCT strftime('%Y-%m', "Flight Date")) AS active_months,
        MAX("Flight Date") AS last_flight_date
    FROM clean_flight_activity
    GROUP BY "Loyalty Number"
)
SELECT
    l."Loyalty Number",
    l.Country,
    l.Province,
    l.City,
    l."Postal Code",
    l.Gender,
    l.Education,
    l.Salary,
    l."Marital Status",
    l."Loyalty Card",
    l.CLV,
    l."Enrollment Type",
    l."Enrollment Year",
    l."Enrollment Month",
    l."Cancellation Year",
    l."Cancellation Month",
    l.salary_is_missing,
    l.salary_is_suspicious,
    l.Is_Churned,
    l."Cancellation Date",
    l."Enrollment Date",
    l."Last Activity Month",
    l."Tenure Months",
    CASE
        WHEN l."Tenure Months" <= 12 THEN '0-12 months'
        WHEN l."Tenure Months" <= 24 THEN '13-24 months'
        WHEN l."Tenure Months" <= 48 THEN '25-48 months'
        ELSE '49+ months'
    END AS tenure_band,
    l.postal_code_is_valid,

    -- Flight metrics with NULL handling for customers with zero flight records
    COALESCE(f.total_flights, 0) AS total_flights,
    COALESCE(f.total_distance, 0) AS total_distance,
    COALESCE(f.total_points, 0) AS total_points,
    COALESCE(f.active_months, 0) AS active_months,
    f.last_flight_date
FROM clean_loyalty_history l
LEFT JOIN customer_flight_date f
ON l."Loyalty Number" = f."Loyalty Number";
"""

execute_script(sql, "Customer Summary View")
