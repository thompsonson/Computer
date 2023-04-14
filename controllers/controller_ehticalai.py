"""Controller for the Ethical AI functionality"""

import logging
import time
from typing import Optional, Type
from sqlalchemy.orm import Session

from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI

from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field, validator

import settings

from DBAdapter import DBAdapter
from models.model_ethicalai import RightSpeechModel

logger = logging.getLogger(__name__)

PROMPT_TEMPLATE = """
{format_instructions}

Hello. You are a Buddhist monk, well versed and practices in the art of Right Speech. 

Please evaluate this response based on the right speech principles and provide scores for each metric. 
The principles and their descriptions are in the jsonobject above.
Use a scale of 1 to 10, where 1 indicates poor alignment with the principle and 10 indicates excellent alignment.

% USER INPUT:
{user_input}

YOUR RESPONSE:
    """


class RightSpeechEvaluation(BaseModel):
    truthfulness: int = Field(
        ..., ge=1, le=10, description="Degree of factual accuracy and honesty"
    )
    kindness: int = Field(
        ...,
        ge=1,
        le=10,
        description="Presence of positive, compassionate, and empathetic language",
    )
    constructiveness: int = Field(
        ...,
        ge=1,
        le=10,
        description="Contribution to a conversation or problem-solving process",
    )
    absence_of_false_speech: int = Field(
        ...,
        ge=1,
        le=10,
        description="Absence of false, misleading, or deceptive language",
    )
    absence_of_malicious_speech: int = Field(
        ...,
        ge=1,
        le=10,
        description="Absence of language intended to harm, insult, or demean others",
    )
    absence_of_harsh_speech: int = Field(
        ...,
        ge=1,
        le=10,
        description="Absence of harsh, aggressive, or offensive language",
    )
    absence_of_idle_chatter: int = Field(
        ...,
        ge=1,
        le=10,
        description="Absence of irrelevant, trivial, or gossip-like content",
    )


class BuddhistController:
    """Controller class for Ethical AI"""

    def __init__(
        self,
        message: str,
        session: Optional[Session] = None,
        model: Optional[Type[RightSpeechModel]] = None,
        llm: Optional[OpenAI] = None,
        output_parser: Optional[PydanticOutputParser] = None,
    ):
        """
        sets the model for the controller

        I am consdiering going full on with dependency injection,
            however I like having the fall back as, presently, the
            only value I see in dependancy injection is for testing.
            (hopefully more GPTs come available though!!)

        """
        # handler the inputted message
        self._message = message
        logger.info("message: %s", self._message)
        # set up the DB session
        self._session = session or DBAdapter().unmanaged_session()
        # set the model (done like this to support more varied testing)
        self._model = model or RightSpeechModel

        # set up the LLM to use (done like this to support more varied testing)
        # type: ignore
        self._llm = llm or OpenAI(
            model_name=settings.GPT_MODEL,
            openai_api_key=settings.OPENAI_API_KEY,
        )  # type: ignore

        # Set up a parser + inject instructions into the prompt template. (done like this to support more varied testing)
        self._output_parser = output_parser or PydanticOutputParser(
            pydantic_object=RightSpeechEvaluation
        )

    def _prepare_prompt(self) -> str:
        """
        Prepare the input prompt for the API request to review the message for alignment to Buddhist principles of Right Speech.

        This method creates a prompt using response schemas, format instructions, and a template. The prompt is
        then used as an input for the API request to get the alignment to the given metrics.

        Returns:
            str: The prepared input prompt for the API request.
        """

        format_instructions = self._output_parser.get_format_instructions()
        logger.info(format_instructions)

        prompt = PromptTemplate(
            input_variables=["user_input"],
            partial_variables={"format_instructions": format_instructions},
            template=PROMPT_TEMPLATE,
        )

        prompt_value = prompt.format(user_input=self._message)

        logger.info(prompt_value)

        return str(prompt_value)

    async def process_message(self) -> RightSpeechEvaluation:
        """
        Provide details of alignment to Buddist principles of Right Speech.

        Args:
            message (str): Text to review.

        Returns:
            dict:   scoring, on a scale of 1 to 10,
                    where 1 indicates poor alignment with the principle and 10 indicates excellent alignment to the principle.
        """
        start_time = time.perf_counter()
        logger.info("process_message %s", self._message)

        prompt = self._prepare_prompt()

        try:
            llm_output = self._llm(prompt)  # type: ignore
        except Exception as err:
            logger.error(err)
            print(f"Error: {err=}, {type(err)=}")

        logger.info(llm_output)

        try:
            response = self._output_parser.parse(llm_output)
        except Exception as err:
            logger.error(err)
            print(f"Error: {err=}, {type(err)=}")

        logger.info(f"Parsed response: {response}")

        try:
            self._model = self._model(**response.dict())
        except Exception as e:
            logger.error(e)
            raise e  # need to find a better way to handle this error

        self.save()

        end_time = time.perf_counter()
        processing_time = end_time - start_time
        logger.info(f"Message processing took {processing_time:.4f} seconds")

        return response

    def save(self) -> None:
        """Saves the note to the database"""
        start_time = time.perf_counter()
        try:
            self._session.add(self._model)
            self._session.commit()
            logger.info("Successfully saved RightSpeechModel to the database")
        except Exception as e:
            logger.error(f"Error during database operation: {e}")
            self._session.rollback()
        finally:
            end_time = time.perf_counter()
            processing_time = end_time - start_time
            logger.info(f"Database operations took: {processing_time:.4f} seconds")


REVIEW_FROM_GPT4 = """
Here are a few suggestions to improve the current implementation of the BuddhistController:

Test coverage: Ensure that you have comprehensive test coverage for the different components of the controller, including unit tests, integration tests, and end-to-end tests. This will help you catch potential issues early and ensure that your implementation is robust.

With these improvements, your implementation will be more robust, maintainable, and easier to debug.
"""
