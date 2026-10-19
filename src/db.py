import pandas as pd
import sqlite3
from importlib import import_module
import matplotlib.pyplot as plt

DB_PATH = "data/loyalty.db"


def execute_script(sql: str, title: str):
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(sql)
        conn.commit()

    print(f"{title} script is executed and commited")


def run_query(
    sql,
    title="Running SQL Query",
    export_csv=False,
    filename=None,
    preview_rows=10,
    display=True,
):
    conn = sqlite3.connect(DB_PATH)

    try:
        df = pd.read_sql_query(sql, conn)

        if display:
            print(f"\n{'='*55}")
            print(title)
            print(f"{'='*55}")

            if export_csv:
                if filename is None:
                    raise ValueError("Please provide a filename when export_csv=True.")

                df.to_csv(f"exports/powerbi/{filename}", index=False)

                print(
                    f"Successfully exported {len(df):,} rows to exports/powerbi/{filename}\n"
                )
                print(f"Preview (First {preview_rows} rows):")
                print(df.head(preview_rows).to_string(index=False))
            else:
                print(df.to_string(index=False))

        elif export_csv:
            if filename is None:
                raise ValueError("Please provide a filename when export_csv=True.")

            df.to_csv(f"exports/powerbi/{filename}", index=False)

        return df

    finally:
        conn.close()


def load_table(table_name: str) -> pd.DataFrame:
    """
    Load a SQLite table into a pandas DataFrame.

    Parameters
    ----------
    table_name : str
        Name of the table in the SQLite database.

    Returns
    -------
    pd.DataFrame
        DataFrame containing all rows from the specified table.
    """
    conn = sqlite3.connect(DB_PATH)
    query = f"SELECT * FROM {table_name}"
    return pd.read_sql_query(query, conn)


def trim_table(df: pd.DataFrame) -> pd.DataFrame:
    """Strips leading/trailing whitespace from column names and all string data."""

    # 1. Trim column headers
    df.columns = df.columns.str.strip()

    # 2. Trim all string/object cells
    str_cols = df.select_dtypes(include=["object", "string"]).columns
    df[str_cols] = df[str_cols].apply(lambda x: x.str.strip())

    return df


def load_sql(filename: str, sql_query: str) -> str:
    """
    Dynamically import a SQL module and return the requested query string.

    Example:
        load_sql("churn_analysis", "TENURE_QUERY")
    """
    module = import_module(f"sql.analysis.{filename}")

    try:
        return getattr(module, sql_query)
    except AttributeError:
        raise ValueError(f"'{sql_query}' not found in sql.analysis.{filename}")


def save_plot(filename):
    """
    Save the current matplotlib figure to plots/eda and close it.
    """
    plt.tight_layout()
    plt.savefig(f"plots/eda/{filename}", dpi=300, bbox_inches="tight")
    plt.close()
