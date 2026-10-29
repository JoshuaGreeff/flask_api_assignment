"""A small Flask API with greeting and number-summing endpoints.

The routes validate request data, clean name input, and return JSON responses that
clients can use consistently.

It applies the same basic ideas as a command-line program, but request parameters and
JSON bodies take the place of typed terminal input.
"""

from flask import Flask, jsonify, request
from werkzeug.exceptions import BadRequest


# This creates the Flask application that serves both REST endpoints.
app = Flask(__name__)
# Keep a clear limit on the optional name before returning it to the client.
MAX_NAME_LENGTH = 60


def normalize_name(raw_name):
    """Remove extra spaces and format each word in a supplied name."""
    # split() separates the words, capitalize() formats them, and join() rebuilds one clean name.
    words = raw_name.strip().split()
    return " ".join(word.capitalize() for word in words)


@app.get("/hello")
def hello():
    """Return a greeting and use the optional name query parameter when provided."""
    # A missing name uses the default greeting, while a supplied name is cleaned first.
    raw_name = request.args.get("name")
    if raw_name is None:
        greeting = "Hello, World!"
    else:
        name = normalize_name(raw_name)
        if not name:
            return jsonify({"error": "Name cannot be empty."}), 400
        if len(name) > MAX_NAME_LENGTH:
            return jsonify({"error": "Name must be 60 characters or fewer."}), 400
        greeting = f"Hello, {name}!"

    # jsonify returns the formatted greeting as JSON instead of plain text.
    return jsonify({"greeting": greeting})


@app.post("/sum")
def sum_numbers():
    """Add a list of numbers sent in a JSON request body."""
    # Return a helpful JSON error instead of attempting to read a non-JSON body.
    if not request.is_json:
        return jsonify({"error": "Request body must be JSON."}), 400

    # BadRequest is raised for malformed JSON, so return a clear client error instead of a traceback.
    try:
        data = request.get_json()
    except BadRequest:
        return jsonify({"error": "Request body contains malformed JSON."}), 400

    # The request body should be a JSON object before the API tries to read the numbers field.
    if not isinstance(data, dict):
        return jsonify({"error": "JSON body must be an object."}), 400

    # Check that the numbers field exists before adding anything together.
    numbers = data.get("numbers")
    if numbers is None:
        return jsonify({"error": "Missing required field: numbers."}), 400

    # Only a list can be added together, so reject a single number or another data type.
    if not isinstance(numbers, list):
        return jsonify({"error": "The numbers field must be a list."}), 400

    # Confirm every list item is numeric. Boolean values count as integers in Python, so they are excluded here.
    valid_numbers = all(
        isinstance(number, (int, float)) and not isinstance(number, bool)
        for number in numbers
    )
    if not valid_numbers:
        return jsonify({"error": "Each item in numbers must be an integer or float."}), 400

    # sum() handles the numbers list, and jsonify sends both the original data and the answer back to the client.
    total = sum(numbers)
    return jsonify({"numbers": numbers, "sum": total})


if __name__ == "__main__":
    # Keeping the port here means `python app.py` starts the local server on port 5000.
    app.run(host="127.0.0.1", port=5000, debug=True)
