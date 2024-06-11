import torch
import whisper
import pandas as pd
from emotion_detective.logger.logger import setup_logging
from torch.utils.data import DataLoader, TensorDataset
from transformers import RobertaTokenizer
from nltk.tokenize import sent_tokenize


def transcribe_translate(path: str, language: str = "en") -> pd.DataFrame:
    """
    Transcribes and translates audio files.

    Parameters:
    - path (str): The path to the audio file for transcription.
    - language (str, optional): The language of the audio and the target language for translation. Default is 'en' (English).

    Returns:
    - pandas.DataFrame: A DataFrame containing transcribed and translated sentences along with their corresponding start and end times.

    Author: Kacper Janczyk
    """
    logger = setup_logging()
    try:
        logger.info("Transcribing and translating audio files...")

        text_dict = {"sentence": [], "start_time": [],
                     "end_time": [], 'tokens': []}

        logger.info("Loading Whisper model...")
        model = whisper.load_model("base")

        logger.info("Transcribing audio file...")
        result = model.transcribe(path, language=language)

        logger.info("Extracting transcription chunks...")
        for segment in result['segments']:
            text_dict["sentence"].append(segment['text'])
            text_dict["start_time"].append(segment['start'])
            text_dict["end_time"].append(segment['end'])

        sentences = sent_tokenize(" ".join(text_dict["sentence"]))
        text_dict["sentence"] = sentences

        df = pd.DataFrame(text_dict["sentence"], columns=["sentence"])
        return df

    except Exception as e:
        logger.error(
            "An error occurred during transcription and tokenization of audio files: %s", e)
        return pd.DataFrame()


def dataset_loader(df: pd.DataFrame, text_column: str, batch_size=1) -> torch.utils.data.DataLoader:
    """
    Creates a PyTorch DataLoader for a given DataFrame.

    Parameters:
    - df (pandas.DataFrame): The DataFrame containing the dataset.
    - text_column (str): The name of the column in df containing text data.
    - batch_size (int): The batch size to be used for loading the data.

    Returns:
    - torch.utils.data.DataLoader: A DataLoader object configured with the provided DataFrame and batch size.

    Author: Kacper Janczyk
    """
    logger = setup_logging()
    logger.info("Starting dataset_loader function")

    try:
        tokenizer = RobertaTokenizer.from_pretrained('roberta-base')
        max_length = max(len(tokenizer.encode(text, add_special_tokens=True)) for text in df[text_column])
        logger.info("Max length of tokenized texts: %s", max_length)

        tokenized_texts = [
            tokenizer.encode(
                text, add_special_tokens=True, max_length=max_length, pad_to_max_length=True
            ) for text in df[text_column]
        ]
        inputs = torch.tensor(tokenized_texts)
        masks = (inputs != tokenizer.pad_token_id).long()
        dataset = TensorDataset(inputs, masks)
        data_loader = DataLoader(
            dataset, batch_size=batch_size, shuffle=False, num_workers=0)
        logger.info(f"DataLoader size: {len(data_loader)}")

    except Exception as e:
        logger.error("An error occurred during dataset loading: %s", e)
        raise

    logger.info("Successfully created DataLoader")
    return data_loader
