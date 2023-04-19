"""
This module provides utility functions using OpenAI's API.
"""

import logging
import openai

from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI

from models.sql.notes import NoteModel, FrenchNoteModel

import utils.settings as settings

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
    logger.info(text)
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
    logger.info("generate_additonal_info %s", note_model)
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
    logger.info("correct_text %s", text)
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
    logger.info("corriger_text %s", text)

    response = await _completion(
        f"""Bonjour ! Vous trouverez ci-dessous une transcription de ce que j'ai dit, en français.
Dites-moi s'il y a des défauts ou des améliorations possibles, par exemple :
1. Erreurs grammaticales
2. Vocabulaire alternatif
3. Idiomes et phrases courantes pour améliorer ma façon de parler
4. Conseils pour une structure syntaxique appropriée
Listez les corrections dans une liste à puces. La retranscription est:
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
    logger.info("translate_text %s", text)
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
    logger.info("transcribe_speech %s", voice_file)
    audio_file = open(voice_file, "rb")
    response = openai.Audio.transcribe(settings.T2S_MODEL, audio_file)
    logger.info("transcript: %s", response.text)  # type: ignore
    return response.text  # type: ignore


async def parsable_corriger_message(message: dict) -> FrenchNoteModel:
    """
    Provide suggestions to improve French in the given text.

    Args:
        text (str): Text in French to provide suggestions for.

    Returns:
        str: Text with suggested improvements.
    """
    logger.info("parsable_corriger_text %s", message)
    llm = OpenAI(
        model_name="text-davinci-003", openai_api_key=settings.OPENAI_API_KEY
    )  # type: ignore
    # sets the schema for how the LLM should respond
    response_schemas = [
        ResponseSchema(name="corriger", description="La transcription corrige"),
        ResponseSchema(name="erreurs", description="Les erreurs grammaticales"),
        ResponseSchema(name="vocabulaire", description="les vocabulaires alternatifs"),
        ResponseSchema(
            name="idiomes",
            description="Idiomes et phrases courantes pour améliorer ma façon de parler",
        ),
        ResponseSchema(
            name="conseils",
            description="Conseils pour une structure syntaxique appropriée",
        ),
    ]

    response_schemas_short = [
        ResponseSchema(name="corriger", description="La transcription corrige"),
        ResponseSchema(name="vocabulaire", description="les vocabulaires alternatifs"),
        ResponseSchema(
            name="conseils",
            description="Conseils pour une structure syntaxique appropriée",
        ),
    ]

    output_parser = StructuredOutputParser.from_response_schemas(response_schemas_short)

    format_instructions = output_parser.get_format_instructions()
    logger.info(format_instructions)

    template = """
Bonjour ! Vous trouverez ci-dessous une transcription de ce que j'ai dit, en français.
Dites-moi s'il y a des défauts ou des améliorations possibles. 

{format_instructions}

% USER INPUT:
{user_input}

YOUR RESPONSE:
"""

    prompt = PromptTemplate(
        input_variables=["user_input"],
        partial_variables={"format_instructions": format_instructions},
        template=template,
    )

    prompt_value = prompt.format(user_input=message["message"])

    logger.info(prompt_value)

    llm_output = llm(prompt_value)
    logger.info(llm_output)

    response = output_parser.parse(llm_output)

    logger.info(response)

    french_note = FrenchNoteModel(
        note_id=message["note_id"],
        corriger=response["corriger"],
        vocabulaire=response["vocabulaire"],
        conseils=response["conseils"],
        erreurs=response["erreurs"],
        idiomes=response["idiomes"],
    )

    return french_note
