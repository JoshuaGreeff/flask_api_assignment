"""Tests for the Flask API's successful and invalid request paths.

The test client checks the same responses a browser or another application would
receive without requiring the local server to stay open during every test.
"""

import pytest

from app import app


@pytest.fixture()
def client():
    """Create a test client so the routes can be checked without opening a browser."""
    # Flask's test client lets these tests make requests without starting the local server manually.
    app.config.update(TESTING=True)

    with app.test_client() as test_client:
        yield test_client


def test_hello_uses_default_greeting(client):
    # This confirms /hello works even when the optional name query parameter is not included.
    response = client.get("/hello")

    assert response.status_code == 200
    assert response.get_json() == {"greeting": "Hello, World!"}


def test_hello_uses_name_when_provided(client):
    # This confirms the route uses the name parameter when a client supplies one.
    response = client.get("/hello?name=Joshua")

    assert response.status_code == 200
    assert response.get_json() == {"greeting": "Hello, Joshua!"}


def test_hello_cleans_and_formats_name(client):
    # Extra spaces and mixed capitalization should still produce a consistent greeting.
    response = client.get("/hello?name=++jOsHuA+++gReEfF++")

    assert response.status_code == 200
    assert response.get_json() == {"greeting": "Hello, Joshua Greeff!"}


def test_hello_rejects_empty_name(client):
    response = client.get("/hello?name=+++")

    assert response.status_code == 400
    assert response.get_json() == {"error": "Name cannot be empty."}


def test_hello_rejects_name_that_is_too_long(client):
    response = client.get(f"/hello?name={'a' * 61}")

    assert response.status_code == 400
    assert response.get_json() == {"error": "Name must be 60 characters or fewer."}


def test_sum_returns_total_for_valid_numbers(client):
    # Check the successful POST response, including its status code and JSON body.
    response = client.post("/sum", json={"numbers": [1, 2, 3.5]})

    assert response.status_code == 200
    assert response.get_json() == {"numbers": [1, 2, 3.5], "sum": 6.5}


def test_sum_rejects_non_json_body(client):
    # Check that malformed input returns a 400 response instead of a server error.
    response = client.post("/sum", data="not json", content_type="text/plain")

    assert response.status_code == 400
    assert response.get_json() == {"error": "Request body must be JSON."}


def test_sum_rejects_malformed_json(client):
    # This exercises the BadRequest exception path for a body that claims to be JSON but is incomplete.
    response = client.post(
        "/sum", data='{"numbers":', content_type="application/json"
    )

    assert response.status_code == 400
    assert response.get_json() == {"error": "Request body contains malformed JSON."}


def test_sum_rejects_missing_numbers_field(client):
    # This makes sure a JSON request cannot skip the field the route needs.
    response = client.post("/sum", json={})

    assert response.status_code == 400
    assert response.get_json() == {"error": "Missing required field: numbers."}


def test_sum_rejects_numbers_that_are_not_a_list(client):
    # Check that the endpoint rejects a value that is not a list.
    response = client.post("/sum", json={"numbers": 6})

    assert response.status_code == 400
    assert response.get_json() == {"error": "The numbers field must be a list."}


def test_sum_rejects_non_numeric_list_items(client):
    # This confirms a list with invalid values is rejected instead of causing an unexpected server error.
    response = client.post("/sum", json={"numbers": [1, "two", 3]})

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "Each item in numbers must be an integer or float."
    }
