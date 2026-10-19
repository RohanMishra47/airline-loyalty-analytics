from src.clean import clean_data


def validate_data(
    clean_flight_activity,
    clean_loyalty_history,
    raw_flight_rows,
    raw_loyalty_rows,
):

    duplicates = clean_loyalty_history[
        clean_loyalty_history["Loyalty Number"].duplicated(keep=False)
    ]

    assert duplicates.empty, "Duplicate Loyalty Numbers found in clean_loyalty_history"

    loyalty_check = clean_flight_activity.merge(
        clean_loyalty_history[["Loyalty Number"]],
        on="Loyalty Number",
        how="left",
        indicator=True,
    )

    orphans = loyalty_check[loyalty_check["_merge"] == "left_only"]

    assert orphans.empty, "Orphan Loyalty Numbers found in clean_flight_activity"

    expected_loyalty_cards = {"Aurora", "Nova", "Star"}

    actual_loyalty_cards = set(clean_loyalty_history["Loyalty Card"].dropna().unique())

    unexpected_loyalty_cards = actual_loyalty_cards - expected_loyalty_cards

    assert (
        not unexpected_loyalty_cards
    ), f"Unexpected Loyalty Card values: {unexpected_loyalty_cards}"

    expected_education = {
        "Bachelor",
        "College",
        "Doctor",
        "High School or Below",
        "Master",
    }

    actual_education = set(clean_loyalty_history["Education"].dropna().unique())

    unexpected_education = actual_education - expected_education

    assert (
        not unexpected_education
    ), f"Unexpected Education values: {unexpected_education}"

    expected_marital_status = {
        "Divorced",
        "Married",
        "Single",
    }

    actual_marital_status = set(
        clean_loyalty_history["Marital Status"].dropna().unique()
    )

    unexpected_marital_status = actual_marital_status - expected_marital_status

    assert (
        not unexpected_marital_status
    ), f"Unexpected Marital Status values: {unexpected_marital_status}"

    expected_enrollment_type = {
        "2018 Promotion",
        "Standard",
    }

    actual_enrollment_type = set(
        clean_loyalty_history["Enrollment Type"].dropna().unique()
    )

    unexpected_enrollment_type = actual_enrollment_type - expected_enrollment_type

    assert (
        not unexpected_enrollment_type
    ), f"Unexpected Enrollment Type values: {unexpected_enrollment_type}"

    flight_delta = len(clean_flight_activity) - raw_flight_rows
    loyalty_delta = len(clean_loyalty_history) - raw_loyalty_rows

    print(
        f"Flight activity rows: "
        f"{raw_flight_rows:,} → {len(clean_flight_activity):,} "
        f"(delta: {flight_delta:+,})"
    )

    print(
        f"Loyalty history rows: "
        f"{raw_loyalty_rows:,} → {len(clean_loyalty_history):,} "
        f"(delta: {loyalty_delta:+,})"
    )


if __name__ == "__main__":
    clean_flight_activity, clean_loyalty_history, raw_flight_rows, raw_loyalty_rows = (
        clean_data()
    )

    validate_data(
        clean_flight_activity,
        clean_loyalty_history,
        raw_flight_rows,
        raw_loyalty_rows,
    )
