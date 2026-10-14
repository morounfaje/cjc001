import pandas as pd
import pytest
from loader import validate, DataValidationError


def make_clean_df():
    return pd.DataFrame({
        "timestamp": ["1", "2", "3"],
        "open": [1, 2, 3],
        "high": [1, 2, 3],
        "low": [1, 2, 3],
        "close": [1, 2, 3],
    })


def test_clean_data_passes():
    df = make_clean_df()
    result = validate(df)
    assert len(result) == 3


def test_missing_value_rejected():
    df = make_clean_df()
    df.loc[1, "close"] = None
    with pytest.raises(DataValidationError):
        validate(df)


def test_duplicate_timestamp_rejected():
    df = make_clean_df()
    df.loc[2, "timestamp"] = df.loc[1, "timestamp"]
    with pytest.raises(DataValidationError):
        validate(df)


def test_out_of_order_rejected():
    df = make_clean_df()
    df = df.iloc[::-1].reset_index(drop=True)
    with pytest.raises(DataValidationError):
        validate(df)


def test_negative_price_rejected():
    df = make_clean_df()
    df.loc[0, "open"] = -1
    with pytest.raises(DataValidationError):
        validate(df)