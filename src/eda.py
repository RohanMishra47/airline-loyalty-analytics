import matplotlib.pyplot as plt
import seaborn as sns
from src.db import run_query, load_sql, save_plot

sns.set_theme(style="whitegrid", context="notebook")


def plot_churn_by_tenure():
    sql = load_sql("churn_analysis", "sql1")
    df = run_query(sql, display=False)

    plt.figure(figsize=(8, 5))

    bars = plt.bar(df["tenure_bucket"], df["churn_rate"])

    plt.title("Churn Rate by Tenure Bucket", fontsize=14, weight="bold")
    plt.xlabel("Tenure (Months)")
    plt.ylabel("Churn Rate (%)")
    plt.ylim(0, 35)

    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height + 0.6,
            f"{height:.2f}%",
            ha="center",
            fontsize=10,
        )

    save_plot("churn_by_tenure.png")


def plot_churn_by_province():
    sql = load_sql("churn_analysis", "sql3")
    df = run_query(sql, display=False)

    # Sort so the highest churn appears at the top
    df = df.sort_values("churn_rate", ascending=True)

    plt.figure(figsize=(9, 6))

    bars = plt.barh(df["Province"], df["churn_rate"])

    plt.title("Churn Rate by Province", fontsize=14, weight="bold")
    plt.xlabel("Churn Rate (%)")
    plt.ylabel("Province")
    plt.xlim(0, max(df["churn_rate"]) + 2)

    # Value labels
    for bar in bars:
        width = bar.get_width()
        plt.text(
            width + 0.2,
            bar.get_y() + bar.get_height() / 2,
            f"{width:.2f}%",
            va="center",
            fontsize=9,
        )

    save_plot("churn_by_province.png")


def plot_monthly_flight_trends():
    sql = load_sql("monthly_flight_trends", "sql2")
    df = run_query(sql, display=False)

    month_labels = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]

    plt.figure(figsize=(10, 5))

    plt.plot(
        df["Month"],
        df["flights_2017"],
        marker="o",
        linewidth=2,
        label="2017",
    )

    plt.plot(
        df["Month"],
        df["flights_2018"],
        marker="o",
        linewidth=2,
        label="2018",
    )

    plt.title("Monthly Flight Activity: 2017 vs 2018", fontsize=14, weight="bold")
    plt.xlabel("Month")
    plt.ylabel("Total Flights")
    plt.xticks(df["Month"], month_labels)
    plt.legend()
    plt.grid(axis="y", alpha=0.3)

    save_plot("monthly_flight_trends.png")


def plot_yoy_growth():
    sql = load_sql("monthly_flight_trends", "sql2")
    df = run_query(sql, display=False)

    month_labels = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]

    plt.figure(figsize=(10, 5))

    bars = plt.bar(df["Month"], df["yoy_growth_pct"], width=0.7)

    plt.title("Year-over-Year Flight Growth (2018 vs 2017)", fontsize=14, weight="bold")
    plt.xlabel("Month")
    plt.ylabel("Growth (%)")
    plt.xticks(df["Month"], month_labels)
    plt.ylim(0, max(df["yoy_growth_pct"]) + 8)
    plt.grid(axis="y", alpha=0.3)

    # Value labels
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height + 0.8,
            f"{height:.1f}%",
            ha="center",
            fontsize=9,
        )

    save_plot("yoy_monthly_growth.png")


def plot_quarterly_trends():
    sql = load_sql("monthly_flight_trends", "sql4")
    df = run_query(sql, display=False)

    # Pivot into: quarter | 2017 | 2018
    pivot = df.pivot(index="quarter", columns="Year", values="total_flights")

    quarters = pivot.index.tolist()
    x = range(len(quarters))
    width = 0.35

    plt.figure(figsize=(8, 5))

    bars_2017 = plt.bar(
        [i - width / 2 for i in x],
        pivot[2017],
        width,
        label="2017",
    )

    bars_2018 = plt.bar(
        [i + width / 2 for i in x],
        pivot[2018],
        width,
        label="2018",
    )

    plt.title("Quarterly Flight Activity: 2017 vs 2018", fontsize=14, weight="bold")
    plt.xlabel("Quarter")
    plt.ylabel("Total Flights")
    plt.xticks(list(x), quarters)
    plt.legend()
    plt.grid(axis="y", alpha=0.3)

    # Value labels
    for bars in (bars_2017, bars_2018):
        for bar in bars:
            height = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                height + 1200,
                f"{int(height):,}",
                ha="center",
                fontsize=8,
            )

    save_plot("quarterly_flight_trends.png")


def plot_enrollment_engagement():
    sql = load_sql("enrollment_channel_performance", "sql3")
    df = run_query(sql, display=False)

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    # Average Flights
    bars = axes[0].bar(
        df["Enrollment Type"],
        df["avg_flights"],
    )
    axes[0].set_title("Average Flights")
    axes[0].set_ylabel("Flights")

    for bar in bars:
        height = bar.get_height()
        axes[0].text(
            bar.get_x() + bar.get_width() / 2,
            height + 1,
            f"{height:.1f}",
            ha="center",
            fontsize=9,
        )

    # Average Active Months
    bars = axes[1].bar(
        df["Enrollment Type"],
        df["avg_active_months"],
    )
    axes[1].set_title("Average Active Months")
    axes[1].set_ylabel("Months")

    for bar in bars:
        height = bar.get_height()
        axes[1].text(
            bar.get_x() + bar.get_width() / 2,
            height + 0.5,
            f"{height:.0f}",
            ha="center",
            fontsize=9,
        )

    fig.suptitle(
        "Enrollment Channel Engagement: Standard vs 2018 Promotion",
        fontsize=14,
        weight="bold",
    )

    save_plot("enrollment_engagement.png")


def plot_enrollment_clv():
    sql = load_sql("enrollment_channel_performance", "sql2")
    df = run_query(sql, display=False)

    plt.figure(figsize=(6, 5))

    bars = plt.bar(
        df["Enrollment Type"],
        df["avg_clv"],
    )

    plt.title(
        "Average Customer Lifetime Value by Enrollment Type", fontsize=14, weight="bold"
    )
    plt.xlabel("Enrollment Type")
    plt.ylabel("Average CLV")
    plt.ylim(0, max(df["avg_clv"]) * 1.12)

    # Value labels
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height + 100,
            f"{height:,.0f}",
            ha="center",
            fontsize=10,
        )

    save_plot("enrollment_clv.png")


def plot_clv_by_loyalty_card():
    sql = """
    SELECT
        "Loyalty Card",
        CLV
    FROM customer_flight_summary_view
    WHERE CLV IS NOT NULL;
    """

    df = run_query(sql, display=False)

    plt.figure(figsize=(8, 5))

    sns.boxplot(
        data=df,
        x="Loyalty Card",
        y="CLV",
    )

    plt.title("Customer Lifetime Value by Loyalty Card", fontsize=14, weight="bold")
    plt.xlabel("Loyalty Card")
    plt.ylabel("Customer Lifetime Value")

    save_plot("clv_by_loyalty_card_boxplot.png")


def plot_clv_by_education():
    sql = load_sql("clv_by_segment", "sql6")
    df = run_query(sql, display=False)

    plt.figure(figsize=(9, 5))

    sns.boxplot(
        data=df,
        x="Education",
        y="CLV",
    )

    plt.title(
        "Customer Lifetime Value by Education",
        fontsize=14,
        weight="bold",
    )
    plt.xlabel("Education")
    plt.ylabel("Customer Lifetime Value")

    plt.xticks(rotation=20)

    save_plot("clv_by_education_boxplot.png")


def plot_correlation_heatmap():
    sql = """
    SELECT
        CLV,
        Salary,
        "Tenure Months",
        total_flights,
        total_distance,
        total_points,
        active_months,
        Is_Churned
    FROM customer_flight_summary_view;
    """

    df = run_query(sql, display=False)

    plt.figure(figsize=(9, 7))

    sns.heatmap(df.corr(numeric_only=True), annot=True, fmt=".2f")

    plt.title("Correlation Matrix of Customer Metrics", fontsize=14, weight="bold")

    save_plot("correlation_heatmap.png")


if __name__ == "__main__":
    plot_churn_by_tenure()
    plot_churn_by_province()
    plot_monthly_flight_trends()
    plot_yoy_growth()
    plot_quarterly_trends()
    plot_enrollment_engagement()
    plot_enrollment_clv()
    plot_clv_by_loyalty_card()
    plot_clv_by_education()
    plot_correlation_heatmap()
