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
        max_tokens=250,
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
    logger.info("generate_additonal_info")
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
    logger.info("correct_text")
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
    logger.info("corriger_text")
    response = await _completion(
        f"""Bonjour! Vous trouverez ci-dessous une transcription du français que j'ai parlé.
J'aimerais savoir s'il existe un moyen d'améliorer mon français. 
Pouvez-vous suggérer l'un des éléments suivants ?
1. des erreurs de grammaire ?
2. vocabulaire alternatif ?
3. des expressions idiomatiques et des phrases courantes pour remplacer ma façon de parler ?
4. Des conseils pour une structure de prix appropriée ?
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
    logger.info("transcribe_speech")
    audio_file = open(voice_file, "rb")
    response = openai.Audio.transcribe(settings.T2S_MODEL, audio_file)
    logger.info("transcript: %s", response.text)  # type: ignore
    return response.text  # type: ignore
