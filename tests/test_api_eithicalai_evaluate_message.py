# test_api.py

import pytest
from quart.testing import QuartClient
from main import app  # Import the Quart app from main.py
from controllers.controller_ehticalai import RightSpeechEvaluation


@pytest.fixture
def client() -> QuartClient:
    print("starting the test_client")
    return app.test_client()


@pytest.mark.asyncio
async def test_evaluate_message(client: QuartClient):
    print("starting the test_evaluate_message")
    # Define the test data for the request
    test_message = {"message": "Freedom from suffering to all beings."}

    auth_header = {"Authorization": "Bearer token1"}

    # Make a POST request to the /api/eithicalai/evaluate_message endpoint
    response = await client.post(
        "/api/eithicalai/evaluate_message", json=test_message, headers=auth_header
    )
    # Check that the response status code is 200 (OK)
    assert response.status_code == 200

    result = await response.get_json()
    print(result)

    # Validate the response data using the Pydantic model
    # evaluation = RightSpeechEvaluation(**response.get_json())

    # Validate the response
    # assert evaluation.truthfulness >= 1 and evaluation.truthfulness <= 10
    # assert evaluation.kindness >= 1 and evaluation.kindness <= 10
    # assert evaluation.constructiveness >= 1 and evaluation.constructiveness <= 10
    # assert (
    #    evaluation.absence_of_false_speech >= 1
    #    and evaluation.absence_of_false_speech <= 10
    # )
    # assert (
    #    evaluation.absence_of_malicious_speech >= 1
    #    and evaluation.absence_of_malicious_speech <= 10
    # )
    # assert (
    #    evaluation.absence_of_harsh_speech >= 1
    #    and evaluation.absence_of_harsh_speech <= 10
    # )
    # assert (
    #    evaluation.absence_of_idle_chatter >= 1
    #    and evaluation.absence_of_idle_chatter <= 10
    # )
    # Assert that the rationale is a non-empty string
    # assert isinstance(evaluation.rationale, str) and evaluation.rationale != ""
