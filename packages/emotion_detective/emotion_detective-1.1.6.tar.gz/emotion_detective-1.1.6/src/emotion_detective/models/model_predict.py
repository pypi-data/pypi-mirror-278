import torch
import numpy as np
import pandas as pd
from emotion_detective.data.inference.data_preprocessing import dataset_loader
from emotion_detective.logger.logger import setup_logging


def get_predictions(model: torch.nn.Module, df: pd.DataFrame, text_column: str, batch_size: int) -> pd.DataFrame:
    """
    Obtain predictions from a model based on the input DataFrame.

    Args:
        model (torch.nn.Module): The Roberta model to use for predictions, expected to be in evaluation mode.
        df (pandas.DataFrame): DataFrame containing the sentences for prediction.
        text_column (str): The column name of the text data in the DataFrame.
        batch_size (int): The batch size to use for the DataLoader.

    Returns:
        pandas.DataFrame: A DataFrame containing the original sentences, maximum prediction probability,
        and predicted class index for each sentence.
        
    Author: Amy Suneeth
    """
    logger = setup_logging()
    logger.info("Starting predictions...")

    data_loader = dataset_loader(df, text_column, batch_size)

    model.eval()
    all_max_probs = []
    all_preds = []
    all_sentences = df[text_column].tolist()

    with torch.no_grad():
        for batch_inputs, batch_masks in data_loader:
            try:
                outputs = model(batch_inputs, attention_mask=batch_masks)
                logits = outputs.logits
            except Exception as e:
                logger.error(f"Error in get_predictions: {e}")
                raise e

            probs = torch.softmax(logits, dim=-1).cpu().numpy()
            preds = torch.argmax(logits, dim=-1).cpu().numpy()

            for i in range(len(probs)):
                max_prob_index = np.argmax(probs[i])
                all_max_probs.append(probs[i][max_prob_index])
                all_preds.append(preds[i])

    result_df = pd.DataFrame({
        'sentence': all_sentences,
        'max_prediction_probability': all_max_probs,
        'predicted_class_index': all_preds
    })

    logger.info("Predictions completed.")
    return result_df
