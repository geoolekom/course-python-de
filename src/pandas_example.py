import pandas as pd

dates = pd.date_range("2024-01-01", periods=6, freq="D")
messy_data = pd.DataFrame(
    {
        "user_id": [1, 2, 2, 3, None, 4],
        "age": [25, None, 30, -5, 150, "unknown"],
        "salary": [50000, 75000, 75000, None, 999999, "60.000"],
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


def salary_default(x: float) -> float:
    if pd.notna(x):
        return x
    else:
        return 1000


print("-----")
df_typed = safe_type_conversion(messy_data.copy())
df_typed["salary"] = df_typed["salary"].apply(salary_default)
print(df_typed)
print("-----")

print("-----RANGE-----")
print(list(range(0, 3)))

print("-----SLICING-----")
print(df_typed[["salary", "age"]][0:3])
print(df_typed.iloc[0:3, [1, 2]])
print(df_typed[df_typed["age"] > 20])
print("-------------")
