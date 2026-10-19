from src.db import run_query

sql1 = """
-- CLV by Loyalty Card
SELECT
    "Loyalty Card",
    COUNT(*) AS customers,
    ROUND(AVG(CLV), 2) AS avg_clv,
    ROUND(MIN(CLV), 2) AS min_clv,
    ROUND(MAX(CLV), 2) AS max_clv
FROM clean_loyalty_history
GROUP BY "Loyalty Card"
ORDER BY avg_clv DESC;
"""

sql2 = """
-- CLV by Education
SELECT
    Education,
    COUNT(*) AS customers,
    ROUND(AVG(CLV), 2) AS avg_clv,
    ROUND(MIN(CLV), 2) AS min_clv,
    ROUND(MAX(CLV), 2) AS max_clv
FROM clean_loyalty_history
GROUP BY Education
ORDER BY avg_clv DESC;
"""

sql3 = """
-- CLV by Province
SELECT
    Province,
    COUNT(*) AS customers,
    ROUND(AVG(CLV), 2) AS avg_clv,
    ROUND(MIN(CLV), 2) AS min_clv,
    ROUND(MAX(CLV), 2) AS max_clv
FROM clean_loyalty_history
GROUP BY Province
ORDER BY avg_clv DESC;
"""

sql4 = """
-- CLV by Province and Loyalty Card
SELECT
    Province,
    "Loyalty Card",
    COUNT(*) AS customers,
    ROUND(AVG(CLV), 2) AS avg_clv,
    ROUND(MIN(CLV), 2) AS min_clv,
    ROUND(MAX(CLV), 2) AS max_clv
FROM clean_loyalty_history
GROUP BY
    Province,
    "Loyalty Card"
ORDER BY
    Province,
    avg_clv DESC;
"""

sql5 = """
-- CLV by Marital Status
SELECT
    "Marital Status",
    COUNT(*) AS customers,
    ROUND(AVG(CLV), 2) AS avg_clv,
    ROUND(MIN(CLV), 2) AS min_clv,
    ROUND(MAX(CLV), 2) AS max_clv
FROM clean_loyalty_history
GROUP BY "Marital Status"
ORDER BY avg_clv DESC;
"""

sql6 = """
SELECT
    Education,
    CLV
FROM customer_flight_summary_view
WHERE CLV IS NOT NULL;
"""
if __name__ == "__main__":
    from src.db import run_query

    run_query(sql1, "CLV Distribution By Loyalty Card")
    run_query(sql2, "CLV Distribution By Education")
    run_query(sql3, "CLV Distribution By Province")
    run_query(sql4, "CLV by Province and Loyalty Card")
    run_query(sql5, "CLV Distribution By Marital Status")
