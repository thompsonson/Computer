""" Test the BaseController class. """

import pytest
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase
from pydantic import BaseModel

from typing import Optional, Type
from langchain.schema import BaseOutputParser
from langchain.output_parsers import ResponseSchema
from langchain.llms import OpenAI
from controllers.BaseController import BaseController


class Base(DeclarativeBase):
    """Base class for all models."""

    pass


class BaseControllerForTesting(BaseController):
    """A class for testing the BaseController class."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class MockModel(Base):
    """A mock model class for testing."""

    __tablename__ = "mock_model"
    id = Column(Integer, primary_key=True)
    message = Column(String)


class MockParsedOutput(BaseModel):
    """A mock parsed output class for testing."""

    message: str


class MockOutputParser(BaseOutputParser):
    """A mock output parser class for testing."""

    def get_format_instructions(self) -> str:
        """Return mock format instructions."""
        return "Mock format instructions"

    @property
    def _type(self) -> str:
        """Return the mock type."""
        return "Mock type"

    def parse(self, text: str) -> MockParsedOutput:
        """Parse the input text and return a MockParsedOutput instance."""
        return MockParsedOutput(message=text)

    def __eq__(self, other: object) -> bool:
        """Check if two MockOutputParser instances are equal."""
        if isinstance(other, MockOutputParser):
            return (
                self._type == other._type
                and self.get_format_instructions() == other.get_format_instructions()
            )
        return False


class MockLLM:
    """A mock LLM class for testing."""

    def __call__(self, prompt: str) -> str:
        """Return a sample LLM output."""
        return "Sample LLM Output"


@pytest.fixture
def base_controller():
    """Return a BaseController instance for testing."""
    return BaseController(
        message="Test message",
        model=MockModel,
        session=Session(),
        llm=MockLLM(),
        output_parser=MockOutputParser,
    )


def test_base_controller_init(base_controller):
    """Test the initialization of a BaseController instance."""
    assert base_controller._message == "Test message"
    assert isinstance(base_controller._session, Session)
    assert base_controller._model == MockModel
    assert isinstance(base_controller._llm, MockLLM)
    assert base_controller._output_parser == MockOutputParser()


@pytest.mark.asyncio
async def test_base_controller_process_message(base_controller, monkeypatch):
    """Test the process_message method of a BaseController instance."""

    def mock_save(self):
        """A mock save method."""
        pass

    monkeypatch.setattr(BaseController, "save", mock_save)

    response = await base_controller.process_message()
    assert isinstance(response, BaseModel)


@pytest.fixture
def base_controller_for_testing():
    """Return a BaseControllerForTesting instance for testing."""
    return BaseControllerForTesting(
        message="Test message",
        model=MockModel,
        session=Session(),
        llm=MockLLM(),
        output_parser=MockOutputParser,
    )


def test_base_controller_prepare_prompt(base_controller_for_testing):
    """Test the _prepare_prompt method of a BaseControllerForTesting instance."""
    prepared_prompt = base_controller_for_testing._prepare_prompt()
    print(prepared_prompt)
    expected_prompt = """
Instructions for the AI (personality, style, etc.)
Mock format instructions

% USER INPUT:
Test message

YOUR RESPONSE:
    """
    assert prepared_prompt == expected_prompt
