""" controller for requests to create html pages """
import logging
from typing import Optional, Type

from sqlalchemy.orm import Session

from langchain.output_parsers import PydanticOutputParser
from langchain.llms import OpenAI

from controllers.prompts.base import BaseController
from models.sql.html import HtmlFile as sql_html, Image as sql_image
from models.pydantic.html import HtmlModel as pydantic_html

import utils.settings as settings
from utils.DBAdapter import DBAdapter

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class HtmlController(BaseController):
    """HTML controller class for generating an HTML webpage and image creation prompts."""

    PROMPT_TEMPLATE = """
Instructions for the AI: In the JSON format desciribed below, return some HTML to create a webpage, references to the images and the DALLE prompts Needed to create them. 
{format_instructions}

% USER INPUT:
{user_input}

YOUR RESPONSE:
    """

    def __init__(
        self,
        message: str,
        session: Optional[Session] = None,
        model: Optional[Type[sql_html]] = None,
        llm: Optional[OpenAI] = None,
        output_parser: Optional[PydanticOutputParser] = None,
    ):
        # set the model
        self._model = model or sql_html
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
        )  # type: ignore

        # Set up a parser + inject instructions into the prompt template.
        logger.debug("output_parser: %s", output_parser)
        self._output_parser = output_parser or PydanticOutputParser(
            pydantic_object=pydantic_html
        )
        logger.debug("_output_parser: %s", self._output_parser)

        super().__init__(self._message, self._model, self._session, self._llm, self._output_parser)  # type: ignore

    async def process_message(self) -> Type[sql_html]:
        """Process the prompt and return the model with the generated HTML and image prompts."""
        return await super().process_message()

    def response_to_model(self, response):
        """overrides the standard method as there is nested models (Image model within the HTML model)"""
        html_file = sql_html(html=response.html, filename=response.filename)

        # Create instances of the Image model and associate them with the HtmlFile instance
        for image_data in response.images:
            image = sql_image(
                image_name=image_data.image_name,
                image_prompt=image_data.image_prompt,
                html_file=html_file,
            )
            html_file.images.append(image)

        self._model = html_file
