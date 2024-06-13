import torch
import torch.nn as nn
from transformers import RobertaForSequenceClassification, RobertaConfig
from typing import Any
from emotion_detective.logger.logger import setup_logging
import h5py

def roberta_model(num_labels: int) -> Any:
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
    
class RNNModel(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim, output_dim, n_layers, bidirectional, dropout):
        super(RNNModel, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, num_layers=n_layers, 
                            bidirectional=bidirectional, dropout=dropout, batch_first=True)
        self.fc = nn.Linear(hidden_dim * 2 if bidirectional else hidden_dim, output_dim)
        self.dropout = nn.Dropout(dropout)

    def forward(self, text):
        embedded = self.dropout(self.embedding(text))
        lstm_out, _ = self.lstm(embedded)
        if self.lstm.bidirectional:
            out = self.fc(self.dropout(torch.cat((lstm_out[:, -1, :self.hidden_dim], lstm_out[:, 0, self.hidden_dim:]), dim=1)))
        else:
            out = self.fc(self.dropout(lstm_out[:, -1, :]))
        return out

def rnn_model(vocab_size: int, embedding_dim: int, hidden_dim: int, output_dim: int, n_layers: int, bidirectional: bool, dropout: float) -> Any:
    """
    Creates a classification model using an RNN architecture.

    Args:
        vocab_size (int): Size of the vocabulary.
        embedding_dim (int): Dimension of word embeddings.
        hidden_dim (int): Dimension of hidden states in the RNN.
        output_dim (int): Number of output labels/classes.
        n_layers (int): Number of RNN layers.
        bidirectional (bool): If the RNN is bidirectional.
        dropout (float): Dropout rate.

    Returns:
        model: An RNN model initialized with the specified parameters.
        
    Author: Martin Vladimirov
    """
    model = RNNModel(vocab_size, embedding_dim, hidden_dim, output_dim, n_layers, bidirectional, dropout)
    return model


## accept multiple model inputs (h5, pth) for loading 
def load_model(model_path: str, model_type: str, *args) -> torch.nn.Module:
    """
    Load a pre-trained model from the specified path.

    Args:
        model_path (str): Path to the model file.
        model_type (str): Type of model to load ('roberta' or 'rnn').
        *args: Additional arguments for RNN model configuration.

    Returns:
        torch.nn.Module: The loaded model.
        
    Author: Rebecca Borski, Martin Vladimirov
    """
    try:
        logger = setup_logging()

        if model_type == 'roberta':
            logger.info("Loading a pre-trained Roberta model.")
            model = torch.load(model_path)

        elif model_type == 'rnn':
            logger.info("Loading a pre-trained RNN model.")
            model = torch.load(model_path)

        return model

    except Exception as e:
        logger.error(f"Error in load_model: {e}")
        logger.info("Model loading failed.")
        return None