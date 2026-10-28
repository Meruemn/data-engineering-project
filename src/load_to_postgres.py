
from pathlib import Path
import os

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.dialects.postgresql import insert
from dotenv import load_dotenv

PROJECT_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = PROJECT_DIR / "data" / "processed" / "transactions_clean.csv"

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "data_engineering")

required_settings = {
    "DB_USER": DB_USER,
    "DB_PASSWORD": DB_PASSWORD,
    "DB_NAME": DB_NAME,
}

missing_settings = [
    name for name, value in required_settings.items()
    if not value
]

if missing_settings:
    raise ValueError(
        f"Missing database settings: {', '.join(missing_settings)}"
    )


def main():
    # 1. Extract the cleaned CSV
    df = pd.read_csv(INPUT_FILE)

    # 2. Convert columns to the correct data types
    df["transaction_id"] = pd.to_numeric(
        df["transaction_id"], errors="raise"
    ).astype("int64")

    df["transaction_date"] = pd.to_datetime(
        df["transaction_date"], errors="raise"
    ).dt.date

    df["amount"] = pd.to_numeric(
        df["amount"], errors="raise"
    )

    # 3. Connect to PostgreSQL
    connection_url = (
        f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    engine = create_engine(connection_url)

    try:
        # 4. Insert new records or update existing records
        with engine.begin() as connection:
            rows = df.to_dict(orient="records")

            insert_stmt = text("""
                INSERT INTO public.transactions
                    (transaction_id, transaction_date, customer_id,
                     amount, currency, status)
                VALUES
                    (:transaction_id, :transaction_date, :customer_id,
                     :amount, :currency, :status)
                ON CONFLICT (transaction_id)
                DO UPDATE SET
                    transaction_date = EXCLUDED.transaction_date,
                    customer_id = EXCLUDED.customer_id,
                    amount = EXCLUDED.amount,
                    currency = EXCLUDED.currency,
                    status = EXCLUDED.status
            """)

            connection.execute(insert_stmt, rows)

            total_rows = connection.execute(
                text("SELECT COUNT(*) FROM public.transactions")
            ).scalar_one()

        print(f"Source rows processed: {len(df)}")
        print(f"Total rows in PostgreSQL: {total_rows}")
        print("UPSERT pipeline completed successfully!")

    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
