import pandas as pd
from emotion_detective.logger.logger import setup_logging


def load_data(file_path: str, text_column: str, emotion_column: str) -> pd.DataFrame:
    """
    Load CSV or JSON file and return a DataFrame with specified text and emotion columns.

    Args:
        file_path (str): Path to the CSV or JSON file.
        text_column (str): Name of the column containing text data.
        emotion_column (str): Name of the column containing emotion data.

    Returns:
        pd.DataFrame: DataFrame with specified text and emotion columns.
        
    Author: Martin Vladimirov
    """
    logger = setup_logging()

    # Check file format and load data
    if file_path.endswith('.csv'):
        logger.info("Loading CSV file...")
        df = pd.read_csv(file_path)
    elif file_path.endswith('.json'):
        logger.info("Loading JSON file...")
        df = pd.read_json(file_path)
    else:
        raise ValueError(
            "File format not supported. Please provide a CSV or JSON file.")

    # Log number of rows loaded
    logger.info("Loaded %d rows from file.", len(df))

    # Check if specified columns exist in DataFrame
    if text_column not in df.columns or emotion_column not in df.columns:
        raise ValueError(
            f"DataFrame must contain '{text_column}' and '{emotion_column}' columns.")
    else:
        # Log returning DataFrame with specified columns
        logger.info("Returning DataFrame with '%s' and '%s' columns.",
                    text_column, emotion_column)

    return df[[text_column, emotion_column]]
