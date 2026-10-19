from src.db import load_table, run_query
from src.clean import clean_flight_activity

df = load_table("raw_loyalty_history")

sql1 = """
SELECT COUNT(*) AS row_count
FROM raw_flight_activity;
"""
# run_query(sql1)
print(len(clean_flight_activity))
