import pandas as pd
from datetime import datetime

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
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    df["description"] = df["description"].replace({"None": None})

    df["category"] = df["category"].apply(
        lambda x: x.title() if isinstance(x, str) else None
    )

    def get_type(row):
        return "EXPENSE" if row["amount"] < 0 else "INCOME"

    df["transaction_type"] = df.apply(get_type, axis=1)

    df.loc[
        (df["transaction_type"] == "EXPENSE") & (df["category"].isna()), "category"
    ] = "Miscellaneous"

    df["amount"] = df["amount"].abs()

    return df
