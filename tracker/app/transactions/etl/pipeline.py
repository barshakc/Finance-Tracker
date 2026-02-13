from .extract import extract_csv
from .transform import transform_transaction
from .load import load_transactions
from .logging import logger


def run_pipeline(file_path, user):

    logger.info(f"Starting ETL pipeline for user: {user.username} | file={file_path}")

    df = extract_csv(file_path)
    logger.info(f"Extracted {len(df)} rows")

    df = transform_transaction(df)

    count = load_transactions(df, user)
    logger.info(f"Loaded {count} transactions into the database")

    logger.info(f"ETL pipeline completed for user: {user.username}")
    return f" Imported {count} transactions for {user.username}"
