import logging

def setup_logging():
    """
    Sets up logging for the application.

    This function configures a logger to output log messages to both a file and the console. 
    The log messages include a timestamp, the log level, and the message.

    The log file is saved as 'logs/emotion_detective.txt'.

    Returns:
        logging.Logger: Configured logger instance.
        
    Author: Andrea Tosheva
    """
    # Set up logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Create file handler and set formatter
    file_handler = logging.FileHandler("logs/emotion_detective.txt")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    # Create console handler and set formatter
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
