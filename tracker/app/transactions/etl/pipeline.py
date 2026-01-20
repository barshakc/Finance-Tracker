from .extract import extract_csv
from .transform import transform_transactions
from .load import load_transactions


def run_pipeline(file_path, user):

    df = extract_csv(file_path)

    df = transform_transactions(df)

    count = load_transactions(df, user)

    return f" Imported {count} transactions for {user.username}"
