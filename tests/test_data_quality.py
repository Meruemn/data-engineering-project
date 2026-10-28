
import pandas as pd

from src.data_quality import validate_data


def sample_data():
    return pd.DataFrame({
        "transaction_id": [1001, 1002],
        "transaction_date": ["2026-10-25", "2026-10-26"],
        "customer_id": ["C001", "C002"],
        "amount": [1500.00, 2500.50],
        "currency": ["PHP", "PHP"],
        "status": ["COMPLETED", "PENDING"],
    })


def test_valid_data_passes():
    df = sample_data()

    errors = validate_data(df)

    assert errors == []


def test_duplicate_transaction_ids_are_detected():
    df = sample_data()
    df.loc[1, "transaction_id"] = 1001

    errors = validate_data(df)

    assert any("duplicate transaction IDs" in error for error in errors)


def test_negative_amount_is_detected():
    df = sample_data()
    df.loc[0, "amount"] = -100

    errors = validate_data(df)

    assert any("negative transaction amounts" in error for error in errors)


def test_invalid_status_is_detected():
    df = sample_data()
    df.loc[0, "status"] = "UNKNOWN"

    errors = validate_data(df)

    assert any("Unexpected statuses" in error for error in errors)
