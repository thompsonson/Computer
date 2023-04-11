import logging
import openai

from models.model_notes import NoteModel

import settings

logger = logging.getLogger(__name__)

openai.api_key = settings.OPENAI_API_KEY


async def _completion(text: str) -> str:
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
    response = await _completion(
        f"please return a name, topic, summary (of no more than one sentance), and sentiment for the following note in json:\n\n{note_model.content}"
    )
    # TODO: verify the text is in json and then parse it into the model
    logger.info(response)
    return response  # type: ignore


async def correct_text(text: str) -> str:
    response = await _completion(
        f"please correct any grammaratical  the follow text:\n\n{text}"
    )
    logger.info(response)
    return response  # type: ignore


async def corriger_text(text: str) -> str:
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
    response = await _completion(
        f"please translate the following text to/from english/french:\n\n{text}"
    )
    logger.info(response)
    return response  # type: ignore


def transcribe_speech(voice_file) -> str:
    audio_file = open(voice_file, "rb")
    response = openai.Audio.transcribe(settings.T2S_MODEL, audio_file)
    logger.info("transcript: %s", response.text)  # type: ignore
    return response.text  # type: ignore
