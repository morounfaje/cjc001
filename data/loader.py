import hashlib
import pandas as pd


class DataValidationError(ValueError):
    """Raised when something is wrong with the price data."""
    pass

def file_version(path):
    """A short fingerprint of the file's contents, so every backtest can
    record exactly which version of the data it used."""
    with open(path, "rb") as f:
        contents = f.read()
    return hashlib.sha256(contents).hexdigest()[:16]

def validate(df):
    """Check a price table for basic problems. Returns the same table if it's clean."""

    required_columns = ["timestamp", "open", "high", "low", "close"]
    for col in required_columns:
        if col not in df.columns:
            raise DataValidationError(f"Missing column: {col}")

    if df[required_columns].isna().any().any():
        raise DataValidationError("Found missing (empty) values")

    if df["timestamp"].duplicated().any():
        raise DataValidationError("Found duplicate timestamps")

    if not df["timestamp"].is_monotonic_increasing:
        raise DataValidationError("Timestamps are not in ascending order")

    price_columns = ["open", "high", "low", "close"]
    if (df[price_columns] <= 0).any().any():
        raise DataValidationError("Found a price that is zero or negative")

    print("Data passed all checks.")
    return df

