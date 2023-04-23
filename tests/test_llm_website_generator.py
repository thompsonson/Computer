import asyncio
import pytest
from unittest.mock import AsyncMock, MagicMock
from controllers.prompts.base import BaseController
from langchain.llms import OpenAI
from langchain.output_parsers import PydanticOutputParser
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from controllers.prompts.website import LLMWebsiteGenerator
from models.pydantic.website import WebsiteData, FileData
from models.sql.website import Website, Base

# Mock the response from the LLM
mock_llm_response = {
    "html_content": "<h1>Welcome to My Website</h1>",
    "images": [
        {
            "identifier": "img1",
            "url": "https://example.com/img1.jpg",
            "description": "A beautiful landscape",
        }
    ],
    "files": [
        {
            "identifier": "css1",
            "url": "https://example.com/css/main.css",
            "description": "Main CSS file",
        }
    ],
}


@pytest.fixture
def mock_openai():
    async def _mock_call(*args, **kwargs):
        return mock_llm_response

    mock_openai = MagicMock(spec=OpenAI)
    mock_openai.__call__ = MagicMock(side_effect=_mock_call)
    return mock_openai


# Set up a SQLAlchemy session
@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


@pytest.mark.asyncio
def test_process_message(mock_openai, session):
    message = "Create a website about cats"
    llm_website_generator = LLMWebsiteGenerator(
        message, mock_openai, session, PydanticOutputParser(WebsiteData)
    )
    response = asyncio.run(llm_website_generator.process_message())
    assert response == WebsiteData(
        html_content="<h1>Welcome to My Website</h1>",
        images=[
            FileData(
                identifier="img1",
                url="https://example.com/image1.jpg",
                description="A cat playing with a ball",
            ),
            FileData(
                identifier="img2",
                url="https://example.com/image2.jpg",
                description="A kitten sleeping",
            ),
        ],
        files=[
            FileData(
                identifier="file1",
                url="https://example.com/file1.css",
                description="Main CSS file",
            ),
            FileData(
                identifier="file2",
                url="https://example.com/file2.js",
                description="Main JavaScript file",
            ),
        ],
    )
