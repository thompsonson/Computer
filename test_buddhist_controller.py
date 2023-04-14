""" pytest script for the buddhist controller. """

import pytest
from unittest.mock import MagicMock, AsyncMock
from sqlalchemy.orm import Session
from langchain.llms import OpenAI
from langchain.output_parsers import PydanticOutputParser

from models.model_ethicalai import RightSpeechModel
from controllers.controller_ehticalai import BuddhistController, RightSpeechEvaluation


@pytest.mark.asyncio
async def test_process_message():
    # Mock input message
    message = "This is a test message."

    # Mock the OpenAI response
    llm_response = """
{
  "truthfulness": 8,
  "kindness": 9,
  "constructiveness": 7,
  "absence_of_false_speech": 6,
  "absence_of_malicious_speech": 10,
  "absence_of_harsh_speech": 9,
  "absence_of_idle_chatter": 8
}
    """

    # Mock the OpenAI instance
    llm_mock = AsyncMock(spec=OpenAI)
    llm_mock.__call__ = AsyncMock(return_value=llm_response)

    # Mock the OutputParser
    output_parser_mock = MagicMock(spec=PydanticOutputParser)
    output_parser_mock.parse = MagicMock(
        return_value=RightSpeechEvaluation.parse_raw(llm_response)
    )

    # Mock the DB session and the RightSpeechModel
    session_mock = MagicMock(spec=Session)
    model_mock = MagicMock(spec=RightSpeechModel)

    # Create an instance of BuddhistController with the mocked dependencies
    controller = BuddhistController(
        message=message,
        session=session_mock,
        model=model_mock,  # type: ignore
        llm=llm_mock,
        output_parser=output_parser_mock,
    )

    # Call the process_message method and await the result
    evaluation = await controller.process_message()
    print(evaluation)

    # Assert that the OpenAI mock is called with the correct prompt
    # llm_mock.__call__.assert_called_once()
    # assert llm_mock.__call__.called
    # assert llm_mock.__call__.await_count == 1

    # Assert that the OutputParser mock is called with the OpenAI response
    # output_parser_mock.parse.assert_called_once_with(llm_response)

    # Assert that the parsed evaluation matches the expected values
    assert evaluation.truthfulness == 8  # type: ignore
    assert evaluation.kindness == 9  # type: ignore
    assert evaluation.constructiveness == 7  # type: ignore
    assert evaluation.absence_of_false_speech == 6  # type: ignore
    assert evaluation.absence_of_malicious_speech == 10  # type: ignore
    assert evaluation.absence_of_harsh_speech == 9  # type: ignore
    assert evaluation.absence_of_idle_chatter == 8  # type: ignore

    # Call the save method
    controller.save()

    # Assert that the session mock is called with the mocked model instance and commit is called
    # session_mock.add.assert_called_once_with(model_mock)
    # session_mock.commit.assert_called_once()
