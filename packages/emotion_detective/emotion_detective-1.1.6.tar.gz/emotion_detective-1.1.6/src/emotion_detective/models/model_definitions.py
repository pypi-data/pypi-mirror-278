import torch
from transformers import RobertaForSequenceClassification, RobertaConfig
from typing import Any
from emotion_detective.logger.logger import setup_logging

def create_model(num_labels: int) -> Any:
    """
    Creates a classification model using the Roberta architecture.

    Args:
        num_labels (int): The number of labels/classes for the classification task.

    Returns:
        model: A RobertaForSequenceClassification model initialized with the specified number of labels.
        
    Author: Rebecca Borski
    """
    try:
        logger = setup_logging()

        logger.info("Creating a classification model.")
        config = RobertaConfig.from_pretrained(
            "roberta-base", num_labels=num_labels)

        model = RobertaForSequenceClassification.from_pretrained(
            "roberta-base", config=config)

        return model

    except Exception as e:
        logger.error(f"Error in create_model: {e}")
        logger.info("Model creation failed.")
        return None


def load_model(model_path: str) -> torch.nn.Module:
    """
    Load a pre-trained RobertaForSequenceClassification model from the specified path.

    Args:
        model_path (str): Path to the model file.

    Returns:
        torch.nn.Module: The loaded RobertaForSequenceClassification model.
        
    Author: Rebecca Borski
    """
    model = torch.load(model_path)
    return model
