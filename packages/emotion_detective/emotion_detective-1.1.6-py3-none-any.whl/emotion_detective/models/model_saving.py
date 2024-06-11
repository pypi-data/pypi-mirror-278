import os
import torch

def save_model(model: torch.nn.Module, model_dir: str, model_name: str):
    """
    Saves the state of a PyTorch model to a binary file.

    Parameters:
    model (torch.nn.Module): The model to save.
    model_dir (str): Directory path where the model will be saved.
    model_name (str): Name of the file to save the model as. 

    Returns:
    None
    
    Author: Andrea Tosheva
    """
    # Create the directory if it doesn't exist
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
    
    # Save the model state to a binary file
    torch.save(model, f'{model_dir}/{model_name}.pth')
