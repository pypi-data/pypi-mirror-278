import torch
import torch.nn as nn
import numpy as np
import pandas as pd
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split
from emotion_detective.logger.logger import setup_logging
from .model_definitions import create_model


def train_and_evaluate(df: pd.DataFrame, mapped_emotion_column: str, input_id_column: str, learning_rate: float, batch_size: int, num_epochs: int, patience: int = 3) -> nn.Module:
    """
    Trains and evaluates a neural network model for emotion detection.

    Args:
        df (pd.DataFrame): DataFrame containing input IDs and mapped emotion labels.
        mapped_emotion_column (str): Column name for emotion labels in the DataFrame.
        input_id_column (str): Column name for input IDs in the DataFrame.
        learning_rate (float): Learning rate for the optimizer.
        batch_size (int): Batch size for training and validation.
        num_epochs (int): Number of epochs to train the model.
        patience (int, optional): Number of epochs to wait for improvement before early stopping. Defaults to 3.

    Returns:
        nn.Module: Trained PyTorch model.
        
    Author: Rebecca Borski
    """
    logger = setup_logging()  
    
    df = df[[input_id_column, mapped_emotion_column]]

    # Ensure input_ids column is in tensor format
    try:
        df[input_id_column] = df[input_id_column].apply(torch.tensor)
    except Exception as e:
        logger.error('Error converting input_ids to tensor: %s', e)
        raise

    # Convert emotion labels to tensor
    try:
        labels = torch.tensor(df[mapped_emotion_column].tolist())
        num_labels = df[mapped_emotion_column].nunique()
        logger.info('Emotion labels converted to tensor')
    except Exception as e:
        logger.error('Error during conversion of emotion labels to tensor: %s', e)
        raise
    
    # Split data into training and validation sets
    try:
        train_inputs, val_inputs, train_labels, val_labels = train_test_split(
            list(df[input_id_column]), labels, test_size=0.2, random_state=42)
        logger.info('Data split into training and validation sets')
    except Exception as e:
        logger.error('Error during data split: %s', e)
        raise

    # Convert lists to tensors and create attention masks
    try:
        train_inputs = torch.nn.utils.rnn.pad_sequence(train_inputs, batch_first=True)
        val_inputs = torch.nn.utils.rnn.pad_sequence(val_inputs, batch_first=True)

        train_masks = torch.tensor([[1 if i < len(seq) else 0 for i in range(train_inputs.size(1))] for seq in train_inputs])
        val_masks = torch.tensor([[1 if i < len(seq) else 0 for i in range(val_inputs.size(1))] for seq in val_inputs])
        logger.info('Tensors and attention masks created')
    except Exception as e:
        logger.error('Error during tensor creation: %s', e)
        raise

    # Create DataLoader for training and validation sets
    try:
        train_dataset = TensorDataset(train_inputs, train_masks, train_labels)
        train_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        val_dataset = TensorDataset(val_inputs, val_masks, val_labels)
        val_dataloader = DataLoader(val_dataset, batch_size=batch_size)
        logger.info('DataLoaders created for training and validation sets')
    except Exception as e:
        logger.error('Error during DataLoader creation: %s', e)
        raise
    
    # Create the model
    try:
        model = create_model(num_labels)
        logger.info('Model created')
    except Exception as e:
        logger.error('Error during model creation: %s', e)
        raise

    # Define loss function and optimizer
    try:
        criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)
        logger.info('Loss function and optimizer defined')
    except Exception as e:
        logger.error('Error during definition of loss function and optimizer: %s', e)
        raise

    # Early stopping parameters
    best_val_loss = np.inf
    epochs_no_improve = 0
    early_stop = False

    # Train the model
    for epoch in range(num_epochs):
        if early_stop:
            logger.info(f'Early stopping at epoch {epoch+1}')
            break
        try:
            model.train()
            total_loss = 0
            for batch in train_dataloader:
                batch_inputs, batch_masks, batch_labels = batch
                optimizer.zero_grad()
                logits = model(input_ids=batch_inputs, attention_mask=batch_masks)[0]
                loss = criterion(logits, batch_labels)
                loss.backward()
                optimizer.step()
                total_loss += loss.item()
            average_train_loss = total_loss / len(train_dataloader)
            logger.info(f'Epoch {epoch+1}/{num_epochs}: Train Loss: {average_train_loss}')

            # Evaluate the model
            model.eval()
            with torch.no_grad():
                total_eval_loss = 0
                for batch in val_dataloader:
                    batch_inputs, batch_masks, batch_labels = batch
                    logits = model(input_ids=batch_inputs, attention_mask=batch_masks)[0]
                    loss = criterion(logits, batch_labels)
                    total_eval_loss += loss.item()
                average_val_loss = total_eval_loss / len(val_dataloader)
                logger.info(f'Epoch {epoch+1}/{num_epochs}: Validation Loss: {average_val_loss}')

                # Check for early stopping
                if average_val_loss < best_val_loss:
                    best_val_loss = average_val_loss
                    epochs_no_improve = 0
                else:
                    epochs_no_improve += 1
                    if epochs_no_improve >= patience:
                        early_stop = True
                        logger.info(f'Validation loss did not improve for {patience} consecutive epochs. Early stopping.')

        except Exception as e:
            logger.error('Error during epoch %d: %s', epoch+1, e)
            raise

    return model
