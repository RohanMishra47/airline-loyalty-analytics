sql1 = """
SELECT
    "Enrollment Type",
    COUNT(*) AS customers,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM customer_flight_summary_view),
        2
    ) AS customer_share_pct
FROM customer_flight_summary_view
GROUP BY "Enrollment Type";
"""

sql2 = """
SELECT
    "Enrollment Type",
    COUNT(*) AS customers,
    ROUND(AVG(CLV), 2) AS avg_clv,
    ROUND(MIN(CLV), 2) AS min_clv,
    ROUND(MAX(CLV), 2) AS max_clv
FROM customer_flight_summary_view
GROUP BY "Enrollment Type";
"""

sql3 = """
SELECT
    "Enrollment Type",
    COUNT(*) AS customers,
    ROUND(AVG(total_flights), 2) AS avg_flights,
    ROUND(AVG(total_distance), 2) AS avg_distance,
    ROUND(AVG(total_points), 2) AS avg_points,
    ROUND(AVG(active_months), 2) AS avg_active_months
FROM customer_flight_summary_view
GROUP BY "Enrollment Type";
"""

if __name__ == "__main__":
    from src.db import run_query

    run_query(sql1, "Customer Mix by Enrollment Type")
    run_query(sql2, "Customer Lifetiem Value (CLV) Comparison")
    run_query(sql3, "Flight Engagement by Enrollment Type")
