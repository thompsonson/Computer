"""
This file defines a Quart Blueprint for an API that allows users to evaluate messages for ethical content using the BuddhistController class from the controller_ethicalai module. The API requires authentication using a Bearer token passed in the Authorization header of the request.

Functions:
- authenticate(token): Check if the provided token is valid by comparing it to a dictionary of allowed tokens. Returns a boolean.
- api_healthcheck(): A GET request that returns "This is the way."
- evaluate_message(): A POST request that extracts a message from a JSON request body and evaluates it for ethical content using an instance of BuddhistController. Returns the result as JSON. Requires authentication using a Bearer token passed in the Authorization header of the request. If the token is missing or invalid, returns a 401 error. If the message is missing from the request body, returns a 400 error.
"""

from quart import Blueprint, request, jsonify, abort
from controllers.controller_ehticalai import BuddhistController

api_blueprint = Blueprint("api", __name__)

# Define a dictionary of allowed tokens for authentication (for demonstration purposes)
ALLOWED_TOKENS = {
    "user1": "token1",
    "user2": "token2",
}


async def authenticate(token):
    """
    Check if the provided token is valid.

    Args:
        token (str): A Bearer token passed in the Authorization header of the request.

    Returns:
        bool: True if the token is valid and False if not.
    """
    return token in ALLOWED_TOKENS.values()


@api_blueprint.route("/api/healthcheck", methods=["GET"])
async def api_healthcheck():
    """
    A GET request that returns "This is the way."

    Returns:
        str: A string message indicating that the API is functioning correctly.
    """
    return "This is the way."


@api_blueprint.route("/api/eithicalai/evaluate_message", methods=["POST"])
async def evaluate_message():
    """
    A POST request that extracts a message from a JSON request body and evaluates it for ethical content using an instance of BuddhistController. Returns the result as JSON.

    Returns:
        dict: A dictionary containing the result of the message evaluation.
    """
    # Check for the presence of an Authorization header with a token
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        abort(401, "Unauthorized: Missing or invalid token")

    # Extract the token from the header and authenticate
    token = auth_header.split(" ")[1]
    if not await authenticate(token):
        abort(401, "Unauthorized: Invalid token")

    # Parse the JSON request body
    data = await request.json
    message = data.get("message")
    if not message:
        abort(400, "Bad Request: Missing message")

    # Create an instance of the BuddhistController and evaluate the message
    controller = BuddhistController(message)
    response = await controller.process_message()

    # Check if the response is not None before returning it as JSON
    if response is not None:
        return response.json(indent=4)
    else:
        abort(400, "Bad Request: Invalid message")
