"""
This module provides utility functions using OpenAI's API.
"""

import logging
import openai

from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory

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
        f"""
Bonjour ! Vous trouverez ci-dessous une transcription de ce que j'ai dit, en français.
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


class CodeReview:
    """
    Code Review Chat

    This is a chatbot that provides feedback on code quality, efficiency, and readability.

    Example:
        >>> code_review_chat = CodeReview()
        >>> code_review_chat.code_review_completion("def hello():\n    print('hello')\n")

    """

    def __init__(self):
        template = """
You are a kind, truthful Senior Engineer with multiple years experience writting and reviewing code. 
You have a keen eye for detail and are able to provide constructive feedback to your peers.
You like to offer your reviews in a teacher like style.    

Human: Hey, I have some code to review. Are you free?
Senior Engineer: Sure, I'm free.
Human: Excellent. Please review this Python code and provide feedback on its quality, efficiency, and readability. 
Specifically, can you identify any potential bugs, performance issues, or design flaws? 
Additionally, please suggest any improvements or optimizations that could be made to the code.
----------------
{history}
Human: {human_input}
Assistant:"""
        prompt = PromptTemplate(
            input_variables=["history", "human_input"], template=template
        )

        chatgpt_chain = LLMChain(
            llm=OpenAI(temperature=0),  # type: ignore
            prompt=prompt,
            verbose=True,
            memory=ConversationBufferWindowMemory(k=10),
        )

        self.chatgpt_chain = chatgpt_chain

    def code_review_completion(self, text):
        """
        Provide feedback on its quality, efficiency, and readability.
        Is asked to identify bugs, performance issues, and design flaws.
        The feedback should include improvements or optimizations.

        Args:
            text (str): Code to review.

        Returns:
            str: Review of the code.
        """
        response = self.chatgpt_chain.predict(human_input=text)  # type: ignore
        return response


def code_review_chat(text):
    """
    Provide feedback on its quality, efficiency, and readability.
    Is asked to identify bugs, performance issues, and design flaws.
    The feedback should include improvements or optimizations.

    Args:
        text (str): Code to review.

    Returns:
        str: Review of the code.
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": """
You are a kind Senior Engineer with multiple years experience writting and reviewing code. 
You have a keen eye for detail and are able to provide constructive feedback to your peers.
You like to offer your reviews in a teacher like style.
Feedback is arranged in the format:
# Design and Readability:
- ...
# Potential Bugs:
- ...
# Performance:
- ...
# Possible Improvements:
- ...
""",
            },
            {
                "role": "user",
                "content": "Hey, I have some code to review. Are you free?",
            },
            {"role": "assistant", "content": "Sure, I'm free."},
            {
                "role": "user",
                "content": f"""
Excellent. Please review this Python code and provide feedback on its quality, efficiency, and readability. 
Specifically, can you identify any potential bugs, performance issues, or design flaws? 
Additionally, please suggest any improvements or optimizations that could be made to the code.
----------------
{text}
""",
            },
        ],
    )

    logger.info("tokens used: %s", response["usage"]["total_tokens"])  # type: ignore
    logger.info(response)
    return response


def code_review_file_summary(text):
    """
    Summarize the file so it can be used in a code review summary.

    Args:
        text (str): Code to review.

    Returns:
        str: Summary of the code.
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": """
You are a kind Senior Engineer with multiple years experience writting and reviewing code. 
You have a keen eye for detail and are able to provide constructive feedback to your peers.
Part of your approach is to summarize the findings in a code review summary. 
You summarize each file and then review the summaries to generate a final summary.
""",
            },
            {
                "role": "user",
                "content": "Hey, I have some code to review. Are you free?",
            },
            {"role": "assistant", "content": "Sure, I'm free."},
            {
                "role": "user",
                "content": f"""
Excellent. Please review this Python code and provide feedback on its quality, efficiency, and readability. 
Specifically, summarize any potential bugs, performance issues, or design flaws. 
Additionally, summarize any improvements or optimizations that could be made to the code.
----------------
{text}
""",
            },
        ],
    )

    logger.info("tokens used: %s", response["usage"]["total_tokens"])  # type: ignore
    logger.info(response)
    return response


def code_review_summary(text):
    """
    A summary od summaries.

    Args:
        text (str): Summaries of code reviews.

    Returns:
        str: Summary of the summaries.
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": """
You are a truthful Senior Engineer with multiple years experience writting and reviewing code. 
Part of your approach is to summarize the findings in a code review summary. 
Feedback is arranged in the format:
# Design and Readability:
- ...
# Potential Bugs:
- ...
# Performance:
- ...
# Possible Improvements:
- ...
""",
            },
            {
                "role": "user",
                "content": "Hey, I have some summaries of code reviews. Are you free to summarize them?",
            },
            {"role": "assistant", "content": "Sure, I'm free."},
            {
                "role": "user",
                "content": f"""
Excellent. Please summarize this to provide feedback on its quality, efficiency, and readability. 
This text is a concatenation of the file summaries.
----------------
{text}
""",
            },
        ],
    )

    logger.info("tokens used: %s", response["usage"]["total_tokens"])  # type: ignore
    logger.info(response)
    return response
