sql1 = """
-- Churn Rate By Tenure Bucket
SELECT
    CASE
        WHEN "Tenure Months" <= 12 THEN '0-12'
        WHEN "Tenure Months" <= 24 THEN '13-24'
        WHEN "Tenure Months" <= 48 THEN '25-48'
        ELSE '49+'
    END AS tenure_bucket,

    COUNT(*) AS customers,

    SUM(Is_Churned) AS churned_customers,

    ROUND(100.0 * SUM(Is_Churned) / COUNT(*),2) AS churn_rate
FROM customer_flight_summary_view
GROUP BY tenure_bucket
ORDER BY churn_rate DESC;
"""

sql2 = """
-- Churn Rate By Enrollment Type
SELECT
    "Enrollment Type",
    COUNT(*) AS customers,
    SUM(Is_Churned) AS churned_customers,
    ROUND(100.0 * SUM(Is_Churned)/COUNT(*),2) AS churn_rate
FROM customer_flight_summary_view
GROUP BY "Enrollment Type"
ORDER BY churn_rate DESC;
"""

sql3 = """
-- Churn Rate By Province
SELECT
    Province,
    COUNT(*) AS customers,
    SUM(Is_Churned) AS churned_customers,
    ROUND(100.0 * SUM(Is_Churned) / COUNT(*), 2) AS churn_rate,
    ROUND(100.0 * SUM(Is_Churned) /
          (SELECT SUM(Is_Churned) FROM customer_flight_summary_view), 2)
          AS share_of_total_churn
FROM customer_flight_summary_view
GROUP BY Province
ORDER BY churn_rate DESC;
"""

sql4 = """
-- Average CLV of Churned vs Active Customers
SELECT
    CASE
        WHEN Is_Churned = 1 THEN 'Churned'
        ELSE 'Active'
    END AS customer_status,

    COUNT(*) AS customers,

    ROUND(AVG(CLV), 2) AS avg_clv,

    MIN(CLV) AS min_clv,
    MAX(CLV) AS max_clv

FROM customer_flight_summary_view
GROUP BY customer_status;
"""

sql5 = """
-- Flight Activity of Churned vs Active Customers
SELECT
    CASE
        WHEN Is_Churned = 1 THEN 'Churned'
        ELSE 'Active'
    END AS customer_status,

    COUNT(*) AS customers,
    ROUND(AVG(total_flights), 2) AS avg_flights,
    ROUND(AVG(total_distance), 2) AS avg_distance,
    ROUND(AVG(total_points), 2) AS avg_points,
    ROUND(AVG(active_months), 2) AS avg_active_months

FROM customer_flight_summary_view
GROUP BY customer_status;
"""

if __name__ == "__main__":
    from src.db import run_query

    run_query(sql1, "Churn Rate By Tenure Bucket")
    run_query(sql2, "Churn Rate By Enrollment Type")
    run_query(sql3, "Churn Rate By Province")
    run_query(sql4, "Average CLV of Churned vs Active Customers")
    run_query(sql5, "Flight Activity of Churned vs Active Customers")
