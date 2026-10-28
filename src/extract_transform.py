
print("My first data engineering pipeline is running!")

from pathlib import Path
import pandas as pd
from data_quality import run_quality_checks

# Locate the project directory
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Define input and output files
INPUT_FILE = PROJECT_DIR / "data" / "raw" / "transactions.csv"
OUTPUT_FILE = PROJECT_DIR / "data" / "processed" / "transactions_clean.csv"


def main():
    run_quality_checks()
    # 1. Extract: Read the raw CSV file
    df = pd.read_csv(INPUT_FILE)

    print("Raw transaction data:")
    print(df)

    # 2. Transform: Clean and validate the data
    df["transaction_date"] = pd.to_datetime(
        df["transaction_date"], errors="coerce"
    )

    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    # Remove rows missing essential fields
    df = df.dropna(
        subset=[
            "transaction_id",
            "transaction_date",
            "customer_id",
            "amount",
            "currency",
            "status",
        ]
    )

    # Remove duplicate transaction IDs
    df = df.drop_duplicates(
        subset=["transaction_id"], keep="first"
    )

    # Standardize text fields
    df["customer_id"] = df["customer_id"].astype(str).str.strip()
    df["currency"] = df["currency"].astype(str).str.upper().str.strip()
    df["status"] = df["status"].astype(str).str.upper().str.strip()

    # Reject invalid monetary values
    df = df[df["amount"] >= 0]

    # 3. Load: Save the cleaned data to a new CSV
    df.to_csv(OUTPUT_FILE, index=False)

    print("\nPipeline completed!")
    print(f"Rows processed: {len(df)}")
    print(f"Clean file saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
