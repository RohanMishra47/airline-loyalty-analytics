from src.db import execute_script

sql = """
DROP VIEW IF EXISTS vw_calendar;

CREATE VIEW vw_calendar AS
SELECT
    "Date",
    "Start of Year",
    "Start of Quarter",
    "Start of Month",

    CAST(strftime('%Y', "Date") AS INTEGER)
        AS year_number,

    CAST(strftime('%m', "Date") AS INTEGER)
        AS month_number,

    CASE CAST(strftime('%m', "Date") AS INTEGER)
        WHEN 1 THEN 'January'
        WHEN 2 THEN 'February'
        WHEN 3 THEN 'March'
        WHEN 4 THEN 'April'
        WHEN 5 THEN 'May'
        WHEN 6 THEN 'June'
        WHEN 7 THEN 'July'
        WHEN 8 THEN 'August'
        WHEN 9 THEN 'September'
        WHEN 10 THEN 'October'
        WHEN 11 THEN 'November'
        WHEN 12 THEN 'December'
    END AS month_name,

    CAST(
        (CAST(strftime('%m', "Date") AS INTEGER) + 2) / 3
        AS INTEGER
    ) AS quarter_number,

    'Q' || CAST(
        (CAST(strftime('%m', "Date") AS INTEGER) + 2) / 3
        AS INTEGER
    ) AS quarter_label,

    strftime('%Y', "Date") || '-Q' ||
    CAST(
        (CAST(strftime('%m', "Date") AS INTEGER) + 2) / 3
        AS INTEGER
    ) AS year_quarter

FROM raw_calendar;
"""

execute_script(sql, "Calendar Quarterly View")
