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

import utils.settings as settings

from utils.DBAdapter import DBAdapter
from models.model_ethicalai import RightSpeechModel

from utils.exceptions import LogAndPrintException

logger = logging.getLogger(__name__)

PROMPT_TEMPLATE = """
{format_instructions}

Hello. You are a Buddhist monk, well versed and practices in the art of Right Speech. 

Please evaluate this response based on the right speech principles and provide scores for each metric. Finally provide a rationale for your scores.
The principles and their descriptions are in the jsonobject above.
Use a scale of 1 to 10, where 1 indicates poor alignment with the principle and 10 indicates excellent alignment.

% USER INPUT:
{user_input}

YOUR RESPONSE:
    """


class RightSpeechEvaluation(BaseModel):
    """Right Speech Evaluation, stores the message, metrics, and rationale for the metrics."""

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
    rationale: str = Field(..., description="The rationale for the metrics given above")

    def __str__(self):
        metrics = (
            f"\ttruthfulness:\t\t\t{self.truthfulness}\n\tkindness:\t\t\t{self.kindness}\n"
            f"\tconstructiveness:\t\t{self.constructiveness}\n\tabsence_of_false_speech:\t{self.absence_of_false_speech}\n"
            f"\tabsence_of_malicious_speech:\t{self.absence_of_malicious_speech}\n\tabsence_of_harsh_speech:\t{self.absence_of_harsh_speech}\n"
            f"\tabsence_of_idle_chatter:\t{self.absence_of_idle_chatter}"
        )
        return f"{metrics}\n\nRationale: {self.rationale}"


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
        # set the model (done like this to support more varied testing)
        self._model = model or RightSpeechModel
        if hasattr(self, "_for_model_info") and self._for_model_info:  # type: ignore
            return
        self._for_model_info = False
        # handler the inputted message
        self._message = message
        logger.info("message: %s", self._message)
        # set up the DB session
        self._session = session or DBAdapter().unmanaged_session()

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

    @classmethod
    def for_model_info(cls):
        """Create an instance of the controller that is used to get information about the model **only**."""
        instance = cls.__new__(cls)
        instance._for_model_info = True  # type: ignore
        instance.__init__("", None, RightSpeechModel, None, None)
        return instance

    def _prepare_prompt(self) -> str:
        """
        Prepare the input prompt for the API request to review the message for alignment to Buddhist principles of Right Speech.

        This method creates a prompt using response schemas, format instructions, and a template. The prompt is
        then used as an input for the API request to get the alignment to the given metrics.

        Returns:
            str: The prepared input prompt for the API request.
        """

        if self._for_model_info:
            raise RuntimeError(
                "process_message cannot be called on an instance created with for_model_info"
            )

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

    async def process_message(self) -> Optional[RightSpeechEvaluation]:
        """
        Provide details of alignment to Buddist principles of Right Speech.

        Args:
            message (str): Text to review.

        Returns:
            RightSpeechEvaluation:   scoring, on a scale of 1 to 10,
                    where 1 indicates poor alignment with the principle and 10 indicates excellent alignment to the principle.
        """

        if self._for_model_info:
            raise RuntimeError(
                "process_message cannot be called on an instance created with for_model_info"
            )

        start_time = time.perf_counter()
        logger.info("process_message %s", self._message)

        prompt = self._prepare_prompt()

        try:
            llm_output = self._llm(prompt)  # type: ignore

            logger.info(llm_output)

            response = self._output_parser.parse(llm_output)

            logger.info("Parsed response: %s", response)

            self._model = self._model(**response.dict())
        except Exception as err:
            raise LogAndPrintException(err) from err

        self.save()

        end_time = time.perf_counter()
        processing_time = end_time - start_time
        logger.info("Message processing took %.4f seconds", processing_time)

        return response

    def save(self) -> None:
        """Saves the note to the database"""
        start_time = time.perf_counter()
        try:
            self._session.add(self._model)
            self._session.commit()
            logger.info("Successfully saved RightSpeechModel to the database")
        except Exception as err:
            logger.error("Error during database operation: %s", err)
            self._session.rollback()
        finally:
            end_time = time.perf_counter()
            processing_time = end_time - start_time
            logger.info(f"Database operations took: {processing_time:.4f} seconds")

    def get_model_info(self):
        """returns the model info as a list of tuples
        (which change be used by Gradio, hopefully other interfraces as well)"""
        model_info = []
        for column in self._model.__table__.columns:
            if column.name == "id":  # Skip primary key
                continue
            model_info.append((column.name, type(column.type)))
        return model_info
