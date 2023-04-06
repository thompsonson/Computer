import logging
import openai

import settings

logger = logging.getLogger(__name__)


async def correct_text(text: str) -> str:
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"please correct the follow text:\n\n{text}",
        temperature=0,
        max_tokens=60,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )
    logger.info(response)
    return response # type: ignore


async def translate_text(text: str) -> str:
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"please translate the following text to/from english/french:\n\n{text}",
        temperature=0,
        max_tokens=60,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )
    logger.info(response)
    return response # type: ignore

def transcribe_speech(voice_file) -> str:
    audio_file = open(voice_file, "rb")
    response = openai.Audio.transcribe(
        settings.T2S_MODEL, audio_file
    )  
    logger.info("transcript: %s", response.text)  # type: ignore
    return response.text # type: ignore
