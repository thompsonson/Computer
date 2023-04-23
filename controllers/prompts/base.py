""" Base controller class for all controllers. """

import logging
import time
from typing import Type
from sqlalchemy.orm import Session
from sqlalchemy.orm import DeclarativeBase

from langchain.schema import BaseOutputParser
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI

from utils.exceptions import LogAndPrintException

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class BaseController:
    """Base controller class for all controllers."""

    PROMPT_TEMPLATE = """
Instructions for the AI (personality, style, etc.)
{format_instructions}

% USER INPUT:
{user_input}

YOUR RESPONSE:
    """

    def __init__(
        self,
        message: str,
        model: Type[DeclarativeBase],
        session: Session,
        llm: OpenAI,
        output_parser: Type[BaseOutputParser],
    ):
        self._model = model

        self._message = message
        logger.info("message: %s", self._message)

        self._session = session

        self._llm = llm

        self._output_parser = output_parser
        logger.debug("_output_parser: %s", self._output_parser)

    def _prepare_prompt(self) -> str:
        """Prepare the input prompt for the API request"""

        format_instructions = self._output_parser.get_format_instructions()  # type: ignore
        logger.info(format_instructions)

        prompt = PromptTemplate(
            input_variables=["user_input"],
            partial_variables={"format_instructions": format_instructions},  # type: ignore
            template=self.PROMPT_TEMPLATE,  # type: ignore
        )

        prompt_value = prompt.format(user_input=self._message)

        logger.info(prompt_value)

        return str(prompt_value)

    def response_to_model(self, response):
        """standard method to convert response to sqlalchemy model"""
        self._model = self._model(**response.dict())

    async def process_message(self) -> Type[DeclarativeBase]:
        """Process the prompt and return the model"""
        start_time = time.perf_counter()
        logger.info("process_message %s", self._message)

        prompt = self._prepare_prompt()

        try:
            llm_output = self._llm(prompt)  # type: ignore

            logger.info(llm_output)

            response = self._output_parser.parse(llm_output)  # type: ignore

            logger.info("Parsed response: %s", response)
            logger.info("type of parsed response: %s", type(response))
            logger.info("dict from parsed response: %s", response.dict())

            self.response_to_model(response)

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
            logger.info("Successfully saved model to the database")
        except Exception as err:
            logger.error("Error during database operation: %s", err)
            self._session.rollback()
        finally:
            end_time = time.perf_counter()
            processing_time = end_time - start_time
            logger.info("Message processing took %.4f seconds", processing_time)
