""" Integration tests for the BuddhistController class.  """

from langchain.output_parsers import PydanticOutputParser
from langchain.llms import OpenAI
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from unittest.mock import MagicMock, AsyncMock
import pytest

from controllers.controller_ehticalai import BuddhistController, RightSpeechEvaluation
from models.model_ethicalai import RightSpeechModel, Base

from utils.DBAdapter import DBAdapter

import utils.settings as settings

# Set up a test database connection
#TEST_DATABASE_URL = "sqlite://:memory:"
TEST_DATABASE_URL = settings.TEST_DATABASE_URL

@pytest.fixture(scope="module")
def test_database_engine() -> Engine:
    """ Create a test database engine."""
    engine = create_engine(TEST_DATABASE_URL)
    # create the tables if they don't exist
    Base.metadata.create_all(engine)
    print(type(engine))
    return engine


@pytest.fixture(scope="module")
def test_database_session(test_database_engine) -> Session:
    """ Create a test database session."""
    session = DBAdapter().unmanaged_session(local_engine=test_database_engine)
    return session


@pytest.mark.asyncio
async def test_process_message_integration(test_database_session: Session):
    # Replace with your actual API key
    openai_api_key = settings.OPENAI_API_KEY

    test_message = "This is a test message to evaluate using Right Speech principles."
    controller = BuddhistController(
        message=test_message,
        session=test_database_session,
        model=RightSpeechModel,
        llm=OpenAI(model_name="text-davinci-002", openai_api_key=openai_api_key),
        output_parser=PydanticOutputParser(pydantic_object=RightSpeechEvaluation),
    )

    response = await controller.process_message()

    assert response is not None, "Expected a response from the LLM"

    assert isinstance(
        response, RightSpeechEvaluation
    ), "Expected a RightSpeechEvaluation object"

    # Validate the response
    assert response.truthfulness >= 1 and response.truthfulness <= 10
    assert response.kindness >= 1 and response.kindness <= 10
    assert response.constructiveness >= 1 and response.constructiveness <= 10
    assert (
        response.absence_of_false_speech >= 1 and response.absence_of_false_speech <= 10
    )
    assert (
        response.absence_of_malicious_speech >= 1
        and response.absence_of_malicious_speech <= 10
    )
    assert (
        response.absence_of_harsh_speech >= 1 and response.absence_of_harsh_speech <= 10
    )
    assert (
        response.absence_of_idle_chatter >= 1 and response.absence_of_idle_chatter <= 10
    )

    # Verify that the model has been saved to the database
    db_record = (
        test_database_session.query(RightSpeechModel)
        .filter_by(rationale=response.rationale)
        .first()
    )
    assert db_record is not None, "Expected the record to be saved to the test database"
