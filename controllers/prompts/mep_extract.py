""" controller for requests to create html pages """
import logging
from typing import Optional, Type

from sqlalchemy.orm import Session

from langchain.output_parsers import PydanticOutputParser
from langchain.llms import OpenAI

from controllers.prompts.base import BaseController
from models.sql.mep import MEP as sql_mep, Committee, Activity
from models.pydantic.mep import MEPIn, MEPOut, CommitteeIn, ActivityIn

import utils.settings as settings
from utils.DBAdapter import DBAdapter

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class MEPExtractController(BaseController):
    """MEP controller class for extracting information about MEPs."""

    PROMPT_TEMPLATE = """
Instructions for the AI: Extract the name, affiliation, committees, and activities of the MEP from the provided text. Do not include data from anywhere else. 
{format_instructions}

% USER INPUT:
{user_input}

YOUR RESPONSE:
    """

    def __init__(
        self,
        message: str,
        session: Optional[Session] = None,
        model: Optional[Type[sql_mep]] = None,
        llm: Optional[OpenAI] = None,
        output_parser: Optional[PydanticOutputParser] = None,
    ):
        # set the model
        self._model = model or sql_mep
        # handler the inputted message
        self._message = message
        logger.info("message: %s", self._message)
        # set up the DB session
        self._session = session or DBAdapter().unmanaged_session()

        # set up the LLM to use
        self._llm = llm or OpenAI(
            model_name=settings.GPT_MODEL,
            openai_api_key=settings.OPENAI_API_KEY,
            max_tokens=-1,
            temperature=0.0,
        )  # type: ignore

        # Set up a parser + inject instructions into the prompt template.
        logger.debug("output_parser: %s", output_parser)
        self._output_parser = output_parser or PydanticOutputParser(
            pydantic_object=MEPIn
        )
        logger.debug("_output_parser: %s", self._output_parser)

        super().__init__(self._message, self._model, self._session, self._llm, self._output_parser)  # type: ignore

    async def process_message(self) -> Type[sql_mep]:
        """Process the prompt and return the model with the extracted MEP information."""
        return await super().process_message()

    def response_to_model(self, response: MEPIn) -> None:
        # Create a new MEP instance
        mep = sql_mep(
            name=response.name,
            affiliation=response.affiliation,
            source_url=response.source_url,
        )

        # Create Committee instances for each committee name
        for committee_name in response.committees:
            committee = Committee(name=committee_name)
            mep.committees.append(committee)  # Add the committee to the relationship

        # Create Activity instances for each activity description
        for activity_description in response.activities:
            activity = Activity(description=activity_description)
            mep.activities.append(activity)  # Add the activity to the relationship

        # Set the _model attribute to the newly created MEP instance
        self._model = mep
