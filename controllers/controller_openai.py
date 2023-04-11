"""
This module provides utility functions using OpenAI's API.
"""

import logging
import openai

from models.model_notes import NoteModel

import settings

logger = logging.getLogger(__name__)

openai.api_key = settings.OPENAI_API_KEY


async def _completion(text: str) -> str:
    """
    Helper function to generate completion using the OpenAI API.

    Args:
        text (str): Input text for the GPT-3 model.

    Returns:
        str: Generated text completion.
    """
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=text,
        temperature=0,
        max_tokens=60,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )
    logger.info(response)
    return response  # type: ignore


async def generate_additonal_info(note_model: NoteModel) -> None:
    """
    Generate additional information for a given note model.

    Args:
        note_model (NoteModel): The note model to generate additional information for.

    Returns:
        None
    """
    response = await _completion(
        f"please return a name, topic, summary (of no more than one sentance), and sentiment for the following note in json:\n\n{note_model.content}"
    )
    # TODO: verify the text is in json and then parse it into the model
    logger.info(response)
    return response  # type: ignore


async def correct_text(text: str) -> str:
    """
    Correct grammar in the given text.

    Args:
        text (str): Text to correct grammar for.

    Returns:
        str: Text with corrected grammar.
    """
    response = await _completion(
        f"please correct any grammaratical  the follow text:\n\n{text}"
    )
    logger.info(response)
    return response  # type: ignore


async def corriger_text(text: str) -> str:
    """
    Provide suggestions to improve French in the given text.

    Args:
        text (str): Text in French to provide suggestions for.

    Returns:
        str: Text with suggested improvements.
    """
    response = await _completion(
        f"""
Bonjour! Below is a transcription of French I have spoken. 
I would like to know if there is a way to improve my French. Can you suggest any of the following?
1. any grammar mistakes?
2. alternative vocabulary?
3. idiomatic expressions and common phrases to replace how I spoke?
4. any tips for proper sentence structure?
-----------
{text}
"""
    )
    logger.info(response)
    return response  # type: ignore


async def translate_text(text: str) -> str:
    """
    Translate the given text to/from English/French.

    Args:
        text (str): Text to translate.

    Returns:
        str: Translated text.
    """
    response = await _completion(
        f"please translate the following text to/from english/french:\n\n{text}"
    )
    logger.info(response)
    return response  # type: ignore


def transcribe_speech(voice_file) -> str:
    """
    Transcribe speech from a voice file.

    Args:
        voice_file: Path to the voice file.

    Returns:
        str: Transcribed text.
    """
    audio_file = open(voice_file, "rb")
    response = openai.Audio.transcribe(settings.T2S_MODEL, audio_file)
    logger.info("transcript: %s", response.text)  # type: ignore
    return response.text  # type: ignore
