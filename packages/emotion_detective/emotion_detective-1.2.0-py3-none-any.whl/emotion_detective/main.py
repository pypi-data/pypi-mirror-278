import pandas as pd
import logging
import typer
from colorama import Fore, Style
from .data.inference.data_ingestion import mov_to_mp3_audio
from .data.inference.data_preprocessing import transcribe_translate
from .models.model_definitions import load_model
from .models.model_predict import get_predictions

app = typer.Typer()

def show_instructions():
    instructions = f"""
{Fore.YELLOW}🕵️ Welcome to the Emotion Detective CLI! 🕵️{Style.RESET_ALL}

{Fore.CYAN}This tool processes 🎥 video and 🎵 audio files to detect emotions. {Style.RESET_ALL}

{Fore.GREEN}🚀 Arguments: {Style.RESET_ALL}
1. {Fore.BLUE}input_path: {Style.RESET_ALL} Path to the input audio (mp3) or video file (mp4). {Fore.RED}[required]{Style.RESET_ALL}
2. {Fore.BLUE}model_path: {Style.RESET_ALL} Path to the saved NLP model. {Fore.RED}[required]{Style.RESET_ALL}
3. {Fore.BLUE}output_audio_path: {Style.RESET_ALL} Path to save the transcribed audio file. Required only when the input is a video file. {Fore.RED}[optional]{Style.RESET_ALL}
4. {Fore.BLUE}batch_size: {Style.RESET_ALL} Batch size used for model prediction. {Fore.RED}[default: 32]{Style.RESET_ALL}

{Fore.MAGENTA}🔔 Please provide the necessary inputs when prompted. 🔔{Style.RESET_ALL}
"""
    print(instructions)

@app.command()
def main(
    input_path: str = typer.Option(None, help="Path to the input audio (mp3) or video file (mp4)."),
    model_path: str = typer.Option("roberta-base", help="Path to the saved NLP model."),
    output_audio_path: str = typer.Option(None, help="Path to save the transcribed audio file. Required only when the input is a video file."),
    batch_size: int = typer.Option(32, help="Batch size used for model prediction.")
) -> pd.DataFrame:
    """Inference pipeline for emotion detection from video and audio files.

    Args:
        input_path (str): Path to input audio (mp3) or video file (mp4).
        model_path (str, optional): Path to the saved NLP model.
        output_audio_path (str, optional): Path to save the transcribed audio file. Required only when the input is a video file. Defaults to None.
        batch_size (int, optional): Batch size used for model prediction. Defaults to 32.

    Returns:
        pd.DataFrame: DataFrame containing transcribed sentences, predicted emotions, their values, and probability.
        
    Authors: Rebecca Borski, Kacper Janczyk, Martin Vladimirov, Amy Suneeth, Andrea Tosheva
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler("logs/emotion_detective.txt")
    console_handler = logging.StreamHandler()

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.info('Starting program...')

    if input_path is None:
        show_instructions()
        input_path = input("Please enter the path to the input audio (mp3) or video file (mp4): ")
        model_path = input(f"Please enter the path to the saved NLP model: ") or model_path
        if input_path.endswith(".mp4"):
            output_audio_path = input("Please enter the path to save the transcribed audio file: ")
        batch_size = int(input("Please enter the batch size used for model prediction: ") or batch_size)

    model = load_model(model_path)

    if output_audio_path:
        logger.info("Converting video to audio...")
        mov_to_mp3_audio(input_path, output_audio_path)
        logger.info("Transcribing and translating audio...")
        transcribed_df = transcribe_translate(output_audio_path)
        print(transcribed_df)
    else:
        transcribed_df = transcribe_translate(input_path)
        print(transcribed_df)

    logger.info("Getting predictions...")
    predictions_df = get_predictions(model, transcribed_df, batch_size=batch_size, text_column='sentence')

    logger.info("Program finished.")
    print(predictions_df)
    return predictions_df

if __name__ == "__main__":
    app()
