import asyncio
from controllers.prompts.base import BaseController
from langchain.llms import OpenAI
from langchain.output_parsers import PydanticOutputParser
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from models.sql.website import Website
from models.pydantic.website import WebsiteData

import utils.settings as settings


class LLMWebsiteGenerator(BaseController):
    PROMPT_TEMPLATE = """
Please generate a website on the following topic. Remember to replace all line breaks with \n.
{format_instructions}

% USER INPUT:
{user_input}

YOUR RESPONSE:
Please provide the HTML content, images, and other necessary files (such as CSS and JavaScript, based on the best available framework) in a structured format. Ensure that each image or file has a unique identifier, a URL, and an optional description.
    """

    def __init__(
        self,
        message: str,
        llm: OpenAI = None,
        output_parser: PydanticOutputParser = None,
    ):
        # Set up a dummy SQLAlchemy session
        engine = create_engine("sqlite:///:memory:")
        Session = sessionmaker(bind=engine)
        session = Session()

        # Set up the LLM to use
        self._llm = llm or OpenAI(
            model_name=settings.GPT_MODEL,
            openai_api_key=settings.OPENAI_API_KEY,
            max_tokens=-1,
        )  # type: ignore

        # Set up a parser + inject instructions into the prompt template.
        self._output_parser = output_parser or PydanticOutputParser(
            pydantic_object=WebsiteData
        )

        # Set the custom PROMPT_TEMPLATE
        self.PROMPT_TEMPLATE = LLMWebsiteGenerator.PROMPT_TEMPLATE

        super().__init__(
            message=message,
            model=Website,
            session=session,
            llm=self._llm,
            output_parser=self._output_parser,
        )


if __name__ == "__main__":
    message = input("Enter the topic for your website: ")
    print(f"Generating website for topic: {message}...")

    generator = LLMWebsiteGenerator(message)

    loop = asyncio.get_event_loop()
    website_content = loop.run_until_complete(generator.process_message())

    print("Generated website content:")
    print(website_content)
