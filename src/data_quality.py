
from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = PROJECT_DIR / "data" / "raw" / "transactions.csv"

REQUIRED_COLUMNS = [
    "transaction_id",
    "transaction_date",
    "customer_id",
    "amount",
    "currency",
    "status",
]

VALID_STATUSES = {"COMPLETED", "PENDING", "FAILED"}


def validate_data(df):
    errors = []

    # Check 1: Required columns exist
    missing_columns = set(REQUIRED_COLUMNS) - set(df.columns)

    if missing_columns:
        errors.append(f"Missing columns: {sorted(missing_columns)}")
        return errors

    # Check 2: Required fields are not empty
    for column in REQUIRED_COLUMNS:
        missing = df[column].isna() | (
            df[column].astype(str).str.strip() == ""
        )
        if missing.any():
            errors.append(
                f"{column}: {int(missing.sum())} missing values"
            )

    # Check 3: Transaction IDs are unique
    duplicate_count = int(
        df["transaction_id"].duplicated().sum()
    )
    if duplicate_count:
        errors.append(
            f"Found {duplicate_count} duplicate transaction IDs"
        )

    # Check 4: Amounts are numeric and non-negative
    amounts = pd.to_numeric(df["amount"], errors="coerce")

    if amounts.isna().any():
        errors.append("Some amounts are not numeric")

    if (amounts.dropna() < 0).any():
        errors.append("Found negative transaction amounts")

    # Check 5: Dates are valid
    dates = pd.to_datetime(
        df["transaction_date"], errors="coerce"
    )
    if dates.isna().any():
        errors.append("Found invalid transaction dates")

    # Check 6: Status values are supported
    statuses = df["status"].astype(str).str.strip().str.upper()
    invalid_statuses = set(statuses) - VALID_STATUSES

    if invalid_statuses:
        errors.append(
            f"Unexpected statuses: {sorted(invalid_statuses)}"
        )

    return errors


def main():
    df = pd.read_csv(INPUT_FILE)
    errors = validate_data(df)

    if errors:
        print("DATA QUALITY CHECKS FAILED")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    print("ALL DATA QUALITY CHECKS PASSED")
    print(f"Rows checked: {len(df)}")
    print("Required fields: OK")
    print("Unique transaction IDs: OK")
    print("Amounts: OK")
    print("Transaction dates: OK")
    print("Transaction statuses: OK")


def run_quality_checks():
    main()


if __name__ == "__main__":
    run_quality_checks()
