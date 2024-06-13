import logging
from emotion_detective.logger.logger import setup_logging
from moviepy.editor import VideoFileClip

def mov_to_mp3_audio(input_file: str, output_file: str):
    """
    Extracts audio from a video file and saves it as an mp3 file.

    Args:
        input_file (str): Path to the input video file.
        output_file (str): Path to save the extracted audio as an mp3 file.
    
    Raises:
        Any exceptions encountered during the conversion process.

    Author: Kacper Janczyk
    """
    # Setting up logging
    logger = setup_logging()

    try:
        logger.info("Converting video to audio...")

        # Extracting audio from the video clip
        video_clip = VideoFileClip(input_file)
        audio_clip = video_clip.audio

        # Saving the extracted audio as an mp3 file
        logger.info("Saving audio file...")
        audio_clip.write_audiofile(output_file, codec='mp3')

        # Closing audio and video clips
        audio_clip.close()
        video_clip.close()

    except Exception as e:
        # Logging any errors encountered during the conversion process
        logger.error(f"Error in converting video to audio: {e}")
        raise
