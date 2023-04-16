from quart import Blueprint, request, jsonify, abort
from controllers.controller_ehticalai import BuddhistController

api_blueprint = Blueprint("api", __name__)

# Define a dictionary of allowed tokens for authentication (for demonstration purposes)
ALLOWED_TOKENS = {
    "user1": "token1",
    "user2": "token2",
}


async def authenticate(token):
    """Check if the provided token is valid."""
    return token in ALLOWED_TOKENS.values()


@api_blueprint.route("/api/healthcheck", methods=["GET"])
async def api_healthcheck():
    return "This is the way."


@api_blueprint.route("/api/eithicalai/evaluate_message", methods=["POST"])
async def evaluate_message():
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

    # Return the result as JSON
    return response.json(indent=4)
