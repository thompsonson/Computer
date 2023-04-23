from quart import Blueprint, request, jsonify, abort
from controllers.prompts.generate_html import HtmlController

html_api = Blueprint("html_api", __name__)


@html_api.route("/api/html/healthcheck", methods=["GET"])
async def api_healthcheck():
    """
    A GET request that returns "This is the way."

    Returns:
        str: A string message indicating that the API is functioning correctly.
    """
    return "This is the way."


@html_api.route("/api/html/generate", methods=["POST"])
async def evaluate_message():
    """
    A POST request that extracts a message from a JSON request body and generates a html web page using an instance of HTMLController. Returns the result as JSON.

    Returns:
        dict: A dictionary containing the result of the HTML generation.
    """

    # Parse the JSON request body
    data = await request.json
    message = data.get("message")
    if not message:
        abort(400, "Bad Request: Missing message")

    # Create an instance of the BuddhistController and evaluate the message
    controller = HtmlController(message)
    response = await controller.process_message()

    # Check if the response is not None before returning it as JSON
    if response is not None:
        return response.json(indent=4)
    else:
        abort(400, "Bad Request: Invalid message")
