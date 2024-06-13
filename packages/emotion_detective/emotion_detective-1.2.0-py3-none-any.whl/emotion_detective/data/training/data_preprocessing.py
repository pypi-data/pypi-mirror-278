import nltk
import wordninja
import pandas as pd
from textblob import TextBlob
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from transformers import RobertaTokenizer, BertTokenizer
from emotion_detective.logger.logger import setup_logging

nltk.download('punkt')
nltk.download('wordnet')


def preprocess_text(df: pd.DataFrame, text_column: str, emotion_column: str, tokenizer_name: str = "roberta") -> pd.DataFrame:
    """
    Preprocesses text data in a specified DataFrame column by:
    1. Lowercasing all text.
    2. Tokenizing each lowercased text into individual words.
    3. Lemmatizing each token to its base form using WordNetLemmatizer.
    4. Converting tokens to input IDs using the provided tokenizer.
    5. Mapping emotion labels from strings to integers and storing in a new column.
    6. Automatically determining the maximum length of input sequences and padding/truncating accordingly.

    Parameters:
    df (pd.DataFrame): Input DataFrame containing text data and emotion labels.
    text_column (str): Name of the column in the DataFrame containing text data.
    emotion_column (str): Name of the column in the DataFrame containing emotion labels.
    tokenizer_name (str): Name of the tokenizer to use. Default is "roberta". Supported values are "roberta" and "bert".

    Returns:
    pd.DataFrame: DataFrame with tokenized text, input IDs, and integer emotion labels.

    Raises:
    ValueError: If an invalid tokenizer name is provided.
    Exception: If any error occurs during tokenization, lemmatization, conversion of tokens to input IDs, padding/truncating, or emotion label mapping.

    Author: Martin Vladimirov
    """
    logger = setup_logging()

    logger.info("Lowercasing text...")
    df[text_column] = df[text_column].apply(lambda x: x.lower())

    # Tokenization
    try:
        logger.info("Tokenizing text in column: %s", text_column)
        df[text_column + '_tokens'] = df[text_column].apply(word_tokenize)
    except Exception as e:
        logger.error("Error occurred during tokenization: %s", str(e))
        raise

    # Lemmatization
    try:
        logger.info("Lemmatizing tokens in column: %s", text_column)
        lemmatizer = WordNetLemmatizer()
        df[text_column + '_tokens'] = df[text_column + '_tokens'].apply(
            lambda tokens: [lemmatizer.lemmatize(token) for token in tokens])
    except Exception as e:
        logger.warning("Warning: Lemmatization failed: %s", str(e))

    # Select tokenizer
    logger.info("Selected tokenizer: %s", tokenizer_name)
    if tokenizer_name == 'roberta':
        tokenizer = RobertaTokenizer.from_pretrained("roberta-base")
    elif tokenizer_name == 'bert':
        tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
    else:
        logger.error('Invalid tokenizer.')
        raise ValueError('Please use either "roberta" or "bert" for tokenizer_name.')

    # Convert tokens to input IDs
    try:
        logger.info("Converting tokens to input IDs...")
        df['input_ids'] = df[text_column + '_tokens'].apply(lambda tokens: tokenizer.convert_tokens_to_ids(tokens))
    except Exception as e:
        logger.error("Error occurred during conversion of tokens to input IDs: %s", str(e))
        raise

    # Determine maximum sequence length and pad/truncate
    try:
        logger.info("Determining maximum sequence length based on the longest sentence...")
        max_length = df['input_ids'].apply(len).max()
        logger.info("Maximum sequence length determined: %s", max_length)

        logger.info("Padding/truncating input IDs to maximum length: %s", max_length)
        df['input_ids'] = df['input_ids'].apply(
            lambda ids: ids[:max_length] + [tokenizer.pad_token_id] * (max_length - len(ids)))
    except Exception as e:
        logger.error("Error occurred during padding/truncating input IDs: %s", str(e))
        raise

    # Emotion mapping
    try:
        logger.info("Mapping emotion labels to integers...")
        unique_emotions = df[emotion_column].unique()
        emotion_mapping = {emotion: idx for idx, emotion in enumerate(unique_emotions)}
        df['mapped_emotion'] = df[emotion_column].map(emotion_mapping)
    except Exception as e:
        logger.error("Error occurred during emotion label mapping: %s", str(e))
        raise

    logger.info("Text preprocessing completed.")
    return df


def balancing_multiple_classes(final_df: pd.DataFrame, emotion_column_name: str) -> pd.DataFrame:
    """
    Balance the classes in a DataFrame containing multiple classes.

    Parameters:
    final_df (pd.DataFrame): The DataFrame containing the data.
    emotion_column_name (str): The name of the column containing class labels.

    Returns:
    pd.DataFrame: A balanced DataFrame with an equal number of samples for each class.

    Author: Amy Suneeth
    """
    logger = setup_logging()

    # Determine the minimum count of samples among all classes
    min_count = final_df[emotion_column_name].value_counts().min()
    logger.info("Minimum count of samples among all classes: %d", min_count)

    # Initialize an empty DataFrame to store balanced data
    balanced_df = pd.DataFrame(columns=final_df.columns)

    # Iterate over unique classes
    for emotion in final_df[emotion_column_name].unique():
        # Subset DataFrame for the current class
        emotion_df = final_df[final_df[emotion_column_name] == emotion]
        # If the number of samples for the class is greater than the minimum count, sample randomly
        if len(emotion_df) > min_count:
            logger.warning(
                "Class %s has more samples than the minimum count. Sampling %d samples.", emotion, min_count)
            emotion_df = emotion_df.sample(n=min_count, random_state=1)

        # Concatenate balanced DataFrame with sampled data for the current class
        balanced_df = pd.concat([balanced_df, emotion_df])
        logger.info("Added %d samples of class %s to the balanced DataFrame.", len(
            emotion_df), emotion)

    # Shuffle the balanced DataFrame
    balanced_df = balanced_df.sample(
        frac=1, random_state=1).reset_index(drop=True)
    logger.info(
        "Balancing completed. Total samples in balanced DataFrame: %d", len(balanced_df))

    return balanced_df




def spell_check_and_correct(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Perform spell checking and correction on the input column of a DataFrame.

    Parameters:
    df (pd.DataFrame): Input DataFrame.
    column (str): Column in df containing text with potential spelling errors.

    Returns:
    pd.DataFrame: DataFrame with spelling errors in the specified column corrected.
    
    Author: Amy Suneeth
    """
    logger = setup_logging()
    logger.info("Performing spell checking and correction on column: %s", column)

    def correct_spelling(text: str) -> str:
        """
        Correct spelling errors in a given text.

        Parameters:
        text (str): Input text.

        Returns:
        str: Text with corrected spelling errors.
        
        Author: Amy Suneeth
        """
        logger.info("Correcting spelling errors in text: %s", text)
        
        # Split concatenated words using wordninja
        words = wordninja.split(text)
        logger.debug("Words after splitting with wordninja: %s", words)
        
        # Tokenize the text to handle punctuation
        tokens = word_tokenize(' '.join(words))
        logger.debug("Tokens after word_tokenize: %s", tokens)
        
        # Correct spelling using TextBlob
        corrected_tokens = []
        for token in tokens:
            word = TextBlob(token)
            corrected_word = str(word.correct())
            logger.debug("Corrected word: '%s' to '%s'", token, corrected_word)
            corrected_tokens.append(corrected_word)
        
        return ' '.join(corrected_tokens)

    try:
        df[column] = df[column].apply(correct_spelling)
        logger.info("Spell checking and correction completed.")
    except Exception as e:
        logger.error(
            "Error occurred during spell checking and correction: %s", str(e))
        raise

    return df