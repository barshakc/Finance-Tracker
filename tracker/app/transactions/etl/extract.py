import pandas as pd
from .logging import logger


def extract_csv(file_path):
    logger.info(f"Reading CSV file: {file_path}")
    df = pd.read_csv(file_path)
    return df
