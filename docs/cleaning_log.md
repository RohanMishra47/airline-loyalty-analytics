# Cleaning Log

## Customer Loyalty History

### Salary

**Observation**
- `Salary` contains missing values.
- `Salary` also contains negative values.
- The data dictionary defines Salary as annual income but does not explain negative values.

**Decision**
- Do not modify the original `Salary` values.
- Create `salary_is_missing` to identify missing salaries.
- Create `salary_is_suspicious` to flag negative salary values.

**Rationale**
- The source data does not provide enough information to determine whether
  negative salaries are valid values or data-entry errors.
- Automatically converting negative salaries to positive values or replacing
  them with missing values would introduce an unsupported assumption.
- Keeping the original value and adding flags preserves the source information
  while making the data-quality issue explicit.


### Enrollment and Cancellation Dates

**Observation**
- Enrollment year and month are stored in separate columns.
- Cancellation year and month are stored in separate columns.
- Customers without a cancellation date have missing cancellation year/month
  values.

**Decision**
- Create `Enrollment Date` by combining `Enrollment Year` and
  `Enrollment Month`.
- Create `Cancellation Date` by combining `Cancellation Year` and
  `Cancellation Month`.
- Use the first day of the month (`day=1`) when constructing both dates.

**Rationale**
- Combining the separate year and month fields creates proper datetime
  columns that are easier to use for date-based calculations and analysis.
- The source data does not provide an exact day, so using the first day of
  the month avoids inventing a specific date while preserving the available
  year/month information.
- Using the same first-of-month convention for both dates makes the dates
  suitable for calculating differences in full calendar months.


### Churn Status

**Observation**
- Cancellation information is missing for a large proportion of customers.
- A missing cancellation date indicates that a cancellation was not recorded,
  rather than providing evidence that the customer cancelled.

**Decision**
- Treat customers with a recorded `Cancellation Date` as churned.
- Treat customers without a `Cancellation Date` as active.
- Create `Is_Churned` as a boolean indicator based on whether
  `Cancellation Date` is present.

**Rationale**
- The dataset does not provide a separate churn-status field.
- Using the presence or absence of cancellation information provides a
  transparent definition of churn without inventing cancellation dates for
  active customers.
- Active customers should not be assigned an artificial cancellation date
  simply to make tenure calculations possible.


## Customer Flight Activity

### Duplicate Records

**Observation**
- Exact duplicate records are present in the flight activity data.

**Decision**
- Remove exact duplicate rows from the flight activity data.

**Rationale**
- Duplicate records would cause customer flight activity to be overstated
  when calculating flight counts, distance, points, and other aggregated
  measures.
- Only exact duplicates are removed; non-identical records are retained
  because they may represent legitimate separate observations.


### Flight Activity Month

**Observation**
- Flight activity is recorded using separate `Year` and `Month` fields.
- The flight activity data does not provide an exact flight date.

**Decision**
- Create a datetime column, `Flight Date`, by combining `Year` and `Month`
  and assigning the first day of the month.
- Use this field as the customer's observed flight-activity month.

**Rationale**
- A proper datetime field makes it possible to perform chronological
  operations such as identifying each customer's latest observed activity.
- Because the source data is monthly, assigning day 1 does not imply that a
  flight actually occurred on that day.
- The date represents the month of activity rather than an exact flight date.


### Last Activity Month

**Observation**
- Each customer's flight activity can occur across multiple months.
- Active customers may not have a `Cancellation Date`.

**Decision**
- Group flight activity by `Loyalty Number` and identify the maximum
  `Flight Date` for each customer.
- Use this value as `Last Activity Month`.
- Join `Last Activity Month` to the customer loyalty history data.

**Rationale**
- The latest recorded flight-activity month provides the latest point at
  which the customer was observed in the available transactional data.
- This provides a defensible endpoint for measuring observed tenure for
  customers who do not have a recorded cancellation date.
- The value should not be interpreted as the customer's actual churn date.


## Customer Loyalty History

### Tenure Months

**Observation**
- Churned customers have a `Cancellation Date`, while active customers have
  a missing `Cancellation Date`.
- Using the current date for active customers would extend their tenure beyond
  the period in which their flight activity was observed.

**Decision**
- Create `Tenure Months` as the number of full calendar months between
  `Enrollment Date` and an appropriate observed endpoint.
- For churned customers, use `Cancellation Date` as the endpoint.
- For active customers, use `Last Activity Month` as the endpoint.
- Do not assign an artificial cancellation date to active customers.

**Rationale**
- Cancellation date represents the natural end of observed membership for
  churned customers.
- Active customers have no known end date, so their latest observed
  flight-activity month provides a consistent endpoint without assuming that
  they have churned.
- Using full calendar months is consistent with the year/month granularity of
  the source data.
- This measure represents actual tenure for churned customers and observed
  tenure for active customers.

**Limitation**
- `Tenure Months` for active customers does not represent their eventual
  lifetime tenure because the dataset does not observe their future activity
  or future cancellation.
- `Last Activity Month` represents the last activity observed in the
  available flight activity data, not necessarily the customer's actual last
  flight or actual date of churn.

### Postal Code Validation

**Observation**

* Postal codes were checked against the Canadian postal-code format `A1A 1A1`, including the permitted character set.
* 1,735 postal-code records failed the validation rule.
* Invalid examples included values with an incorrect structure such as `V10 6T5` and `V09 2E9`, as well as values containing disallowed letters such as `U5I 4F1` and `K1F 2R2`.

**Decision**

* Create a `postal_code_is_valid` boolean flag to identify whether each postal code passes validation.
* Set invalid postal-code values to `NULL` in the cleaned dataset.
* Retain the original postal-code values unchanged in the raw dataset.

**Rationale**

* The invalid values cannot be reliably corrected without knowing the intended postal codes.
* Guessing corrections could introduce fabricated location data.
* Setting invalid values to `NULL` prevents downstream analysis from treating malformed postal codes as valid geographic information.
* The validation flag preserves information about the data-quality issue, while the raw table preserves the original values for traceability.

### Categorical Columns — Type Casting

**Observation:**  
`Loyalty Card`, `Education`, `Marital Status`, and `Enrollment Type` each contain a small, finite set of expected values. The observed values were validated against their expected value sets, with no unexpected values found.

**Decision:**  
Converted `Loyalty Card`, `Education`, `Marital Status`, and `Enrollment Type` from their original dtype to pandas `category` dtype.

**Rationale:**  
These columns represent categorical variables rather than free-form text. Converting them to `category` makes their data type more representative of their analytical meaning and provides a more appropriate structure for categorical analysis.