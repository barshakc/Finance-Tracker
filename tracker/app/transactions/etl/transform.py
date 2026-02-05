import pandas as pd
from datetime import datetime
from .logging import logger
from django.utils import timezone

EXPENSE_CATEGORIES = [
    "Food",
    "Transportation",
    "Utilities",
    "Entertainment",
    "Healthcare",
    "Education",
    "Clothing",
    "Shopping",
    "Travel",
    "Miscellaneous",
]


def transform_transaction(df):

    logger.info("Starting transformation")

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    invalid_dates = df["date"].isna().sum()

    if invalid_dates:
        logger.warning(f"Dropping {invalid_dates} rows with invalid dates")

    df = df.dropna(subset=["date"])

    df["date"] = df["date"].apply(
        lambda d: timezone.make_aware(d) if timezone.is_naive(d) else d
    )

    df["description"] = df["description"].replace({"None": None})

    df["category"] = df["category"].apply(
        lambda x: (
            str(x).strip().title()
            if pd.notna(x) and str(x).strip() != ""
            else "Miscellaneous"
        )
    )

    def get_type(row):
        return "EXPENSE" if row["amount"] < 0 else "INCOME"

    df["transaction_type"] = df.apply(get_type, axis=1)

    df.loc[
        (df["transaction_type"] == "EXPENSE") & (df["category"].isna()), "category"
    ] = "Miscellaneous"

    df["amount"] = df["amount"].abs()

    return df
