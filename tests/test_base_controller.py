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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class MockModel(Base):
    __tablename__ = "mock_model"
    id = Column(Integer, primary_key=True)
    message = Column(String)


class MockParsedOutput(BaseModel):
    message: str


class MockOutputParser(BaseOutputParser):
    def get_format_instructions(self) -> str:
        return "Mock format instructions"

    @property
    def _type(self) -> str:
        return "Mock type"

    def parse(self, text: str) -> MockParsedOutput:
        return MockParsedOutput(message=text)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, MockOutputParser):
            return (
                self._type == other._type
                and self.get_format_instructions() == other.get_format_instructions()
            )
        return False


class MockLLM:
    def __call__(self, prompt: str) -> str:
        return "Sample LLM Output"


@pytest.fixture
def base_controller():
    return BaseController(
        message="Test message",
        model=MockModel,
        session=Session(),
        llm=MockLLM(),
        output_parser=MockOutputParser,
    )


def test_base_controller_init(base_controller):
    assert base_controller._message == "Test message"
    assert isinstance(base_controller._session, Session)
    assert base_controller._model == MockModel
    assert isinstance(base_controller._llm, MockLLM)
    assert base_controller._output_parser == MockOutputParser()


@pytest.mark.asyncio
async def test_base_controller_process_message(base_controller, monkeypatch):
    def mock_save(self):
        pass

    monkeypatch.setattr(BaseController, "save", mock_save)

    response = await base_controller.process_message()
    assert isinstance(response, BaseModel)


@pytest.fixture
def base_controller_for_testing():
    return BaseControllerForTesting(
        message="Test message",
        model=MockModel,
        session=Session(),
        llm=MockLLM(),
        output_parser=MockOutputParser,
    )


def test_base_controller_prepare_prompt(base_controller_for_testing):
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
