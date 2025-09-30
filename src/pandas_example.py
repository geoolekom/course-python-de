from typing import Any
import pandas as pd

dates = pd.date_range("2024-01-01", periods=6, freq="D")
messy_data = pd.DataFrame(
    {
        "user_id": [1, 2, 2, 3, None, 4],
        "age": [25, None, 30, -5, 150, "unknown"],
        "salary": [50000, 75000, 75000, None, 999999, "60,000"],
        "email": [
            "alice@test.com",
            "",
            "bob@test",
            "charlie@test.com",
            None,
            "dave@test.com",
        ],
        "signup_date": [
            "2024-01-15",
            "2024-02-30",
            "2024-03-15",
            None,
            "invalid",
            "2024-04-01",
        ],
    },
    index=dates,
)


def safe_type_conversion(df: pd.DataFrame) -> pd.DataFrame:
    """Safely convert data types with error handling"""

    # Convert numeric columns
    numeric_cols = ["age", "salary"]
    for col in numeric_cols:
        # Convert to numeric, errors become NaN
        df[col] = pd.to_numeric(df[col], errors="coerce")

        # Report conversion issues
        invalid_count = df[col].isnull().sum()
        print(f"{col}: {invalid_count} invalid values converted to NaN")

    # Convert date columns
    df["signup_date"] = pd.to_datetime(df["signup_date"], errors="coerce")

    return df


def clean_commas(df: pd.DataFrame) -> pd.DataFrame:
    for i, element in enumerate(df["salary"]):
        if isinstance(element, str):
            df["salary"][i] = element.replace(",", "")
    return df


def clean_salaries(df: pd.DataFrame) -> pd.DataFrame:
    for i, element in enumerate(df["salary"]):
        if not pd.notna(element):
            df["salary"][i] = 1000
    return df


df_typed = (
    messy_data.copy().pipe(clean_commas).pipe(safe_type_conversion).pipe(clean_salaries)
)
# print(df_typed)

numbers_df = messy_data.copy().pipe(safe_type_conversion)[["age", "salary"]]


def replace_nan_with_zero(x: Any) -> Any:
    return x if pd.notna(x) else 0


print(numbers_df)
print(numbers_df.map(replace_nan_with_zero))
