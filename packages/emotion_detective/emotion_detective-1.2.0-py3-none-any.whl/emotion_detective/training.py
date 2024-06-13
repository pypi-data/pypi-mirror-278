import typer
from colorama import Fore, Style
from .logger.logger import setup_logging
from .data.training.data_ingestion import load_data
from .data.training.data_preprocessing import balancing_multiple_classes, preprocess_text, spell_check_and_correct
from .models.model_saving import save_model
from .models.model_training import train_and_evaluate
from .models.model_definitions import roberta_model, rnn_model

app = typer.Typer()

def show_instructions():
    instructions = f"""
{Fore.YELLOW}🎭 Welcome to the Emotion Classifier Training CLI! 🎭{Style.RESET_ALL}

{Fore.CYAN}This tool trains a classification model to detect emotions from text data.{Style.RESET_ALL}

{Fore.GREEN}🚀 Instructions: {Style.RESET_ALL}
1. {Fore.BLUE}file_path: {Style.RESET_ALL} Path to the file containing the input data. {Fore.RED}[required]{Style.RESET_ALL}
2. {Fore.BLUE}text_column: {Style.RESET_ALL} Name of the column in the DataFrame containing text data. {Fore.RED}[required]{Style.RESET_ALL}
3. {Fore.BLUE}emotion_column: {Style.RESET_ALL} Name of the column in the DataFrame containing emotion labels. {Fore.RED}[required]{Style.RESET_ALL}
4. {Fore.BLUE}mapped_emotion_column: {Style.RESET_ALL} Name of the column in the DataFrame containing mapped emotion labels. {Fore.RED}[required]{Style.RESET_ALL}
5. {Fore.BLUE}input_id_column: {Style.RESET_ALL} Name of the column in the DataFrame containing input IDs. {Fore.RED}[required]{Style.RESET_ALL}
6. {Fore.BLUE}learning_rate: {Style.RESET_ALL} Learning rate for the optimizer. {Fore.RED}[required]{Style.RESET_ALL}
7. {Fore.BLUE}batch_size: {Style.RESET_ALL} Batch size for training and validation DataLoaders. {Fore.RED}[required]{Style.RESET_ALL}
8. {Fore.BLUE}num_epochs: {Style.RESET_ALL} Number of epochs to train the model. {Fore.RED}[required]{Style.RESET_ALL}
9. {Fore.BLUE}patience: {Style.RESET_ALL} Patience for early stopping. {Fore.RED}[required]{Style.RESET_ALL}
10. {Fore.BLUE}model_type: {Style.RESET_ALL} Type of model that is going to be used (roberta, rnn) {Fore.RED}[required]{Style.RESET_ALL}
11. {Fore.BLUE}model_dir: {Style.RESET_ALL} Directory where the trained model will be saved. {Fore.RED}[required]{Style.RESET_ALL}
12. {Fore.BLUE}model_name: {Style.RESET_ALL} Name to use when saving the trained model. {Fore.RED}[required]{Style.RESET_ALL}

{Fore.MAGENTA}🔔 Please provide the necessary inputs when prompted. 🔔{Style.RESET_ALL}
"""
    print(instructions)


def training_pipeline(
    file_path: str,
    text_column: str,
    emotion_column: str,
    mapped_emotion_column: str,
    input_id_column: str,
    learning_rate: float,
    batch_size: int,
    num_epochs: int,
    patience: int,
    model_type: str,
    model_dir: str,
    model_name: str
):
    logger = setup_logging()

    try:
        # Load data
        logger.info("Loading data...")
        df = load_data(file_path, text_column, emotion_column)

        # Balance classes
        logger.info("Balancing classes...")
        df = balancing_multiple_classes(df, emotion_column)

        logger.info("Correcting spelling mistakes...")
        df = spell_check_and_correct(df, text_column)

        # Preprocess text
        logger.info("Preprocessing text...")
        df = preprocess_text(df, text_column, emotion_column)
        
        if model_type == 'roberta':
            model = roberta_model()
        if model_type == 'rnn': 
            model = rnn_model() 
             
        # Train and evaluate model
        logger.info("Training and evaluating model...")
        # TODO: update inputs 
        model = train_and_evaluate(df, mapped_emotion_column, input_id_column, learning_rate, batch_size, num_epochs, patience)

        # Save model
        logger.info("Saving model...")
        save_model(model, model_dir, model_name)

        logger.info("Training pipeline completed successfully.")

    except Exception as e:
        logger.error(f"Error in training pipeline: {e}")
        raise

@app.command()
def train(
    file_path: str = typer.Option(None, help="Path to the file containing the input data"),
    text_column: str = typer.Option(None, help="Name of the column in the DataFrame containing text data"),
    emotion_column: str = typer.Option(None, help="Name of the column in the DataFrame containing emotion labels"),
    mapped_emotion_column: str = typer.Option(None, help="Name of the column in the DataFrame containing mapped emotion labels"),
    input_id_column: str = typer.Option(None, help="Name of the column in the DataFrame containing input IDs"),
    learning_rate: float = typer.Option(None, help="Learning rate for the optimizer"),
    batch_size: int = typer.Option(None, help="Batch size for training and validation DataLoaders"),
    num_epochs: int = typer.Option(None, help="Number of epochs to train the model"),
    patience: int = typer.Option(None, help="Patience for Early Stopping"),
    model_type: str = typer.Option(None, help="Type of model that is going to be used (roberta, rnn)"),
    model_dir: str = typer.Option(None, help="Directory where the trained model will be saved"),
    model_name: str = typer.Option(None, help="Name to use when saving the trained model"),
):
    show_instructions()
    file_path = input(f"Enter file path: ")
    text_column = input(f"Enter text column name: ")
    emotion_column = input(f"Enter emotion column name: ")
    mapped_emotion_column = input(f"Enter mapped emotion column name: ")
    input_id_column = input(f"Enter input id column name: ")
    learning_rate = float(input(f"Enter learning rate: "))
    batch_size = int(input(f"Enter batch size: "))
    num_epochs = int(input(f"Enter number of epochs: "))
    patience = int(input(f"Enter patience: "))
    model_type = str(input(f"Enter model type: "))
    model_dir = input(f"Enter model directory: ")
    model_name = input(f"Enter model name: ")

    training_pipeline(
        file_path,
        text_column,
        emotion_column,
        mapped_emotion_column,
        input_id_column,
        learning_rate,
        batch_size,
        num_epochs,
        patience,
        model_type,
        model_dir,
        model_name
    )

if __name__ == "__main__":
    app()

