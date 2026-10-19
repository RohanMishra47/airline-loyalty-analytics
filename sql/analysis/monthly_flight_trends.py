sql1 = """
SELECT
    Year,
    Month,
    SUM("Total Flights") AS total_flights,
    SUM(Distance) AS total_distance,
    SUM("Points Accumulated") AS total_points
FROM clean_flight_activity
GROUP BY Year, Month
ORDER BY Year, Month;
"""

sql2 = """
WITH monthly AS (
    SELECT
        Year,
        Month,
        SUM("Total Flights") AS total_flights,
        SUM(Distance) AS total_distance,
        SUM("Points Accumulated") AS total_points
    FROM clean_flight_activity
    GROUP BY Year, Month
)

SELECT
    Month,

    MAX(CASE WHEN Year = 2017 THEN total_flights END) AS flights_2017,
    MAX(CASE WHEN Year = 2018 THEN total_flights END) AS flights_2018,

    ROUND(
        (
            MAX(CASE WHEN Year = 2018 THEN total_flights END) -
            MAX(CASE WHEN Year = 2017 THEN total_flights END)
        ) * 100.0 /
        MAX(CASE WHEN Year = 2017 THEN total_flights END),
        2
    ) AS yoy_growth_pct

FROM monthly
GROUP BY Month
ORDER BY Month;
"""

sql3 = """
SELECT
    Month,
    SUM("Total Flights") AS total_flights,
    SUM(Distance) AS total_distance,
    SUM("Points Accumulated") AS total_points
FROM clean_flight_activity
GROUP BY Month
ORDER BY total_flights DESC;
"""

sql4 = """
SELECT
    CASE
        WHEN Month BETWEEN 1 AND 3 THEN 'Q1'
        WHEN Month BETWEEN 4 AND 6 THEN 'Q2'
        WHEN Month BETWEEN 7 AND 9 THEN 'Q3'
        ELSE 'Q4'
    END AS quarter,

    Year,

    SUM("Total Flights") AS total_flights,
    SUM(Distance) AS total_distance,
    SUM("Points Accumulated") AS total_points

FROM clean_flight_activity
GROUP BY Year, quarter
ORDER BY Year, quarter;
"""

if __name__ == "__main__":
    from src.db import run_query

    run_query(sql1, "Monthly Flight Activity")
    run_query(sql2, "Year-over-Year Monthly Flight Comparison")
    run_query(sql3, "Strongest and Weakest Flights Months")
    run_query(sql4, "Quarterly Performance")
