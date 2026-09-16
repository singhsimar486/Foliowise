"""Tests for the unauthenticated service routes.

/health is what Render polls to decide whether a deploy is live, so a change
that breaks it would take the API down on the next release.
"""


def test_root_returns_a_welcome_message(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Foliowise API"}


def test_health_check_reports_healthy(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_openapi_schema_is_generated(client):
    """FastAPI builds this from the route type hints; a bad annotation breaks it."""
    response = client.get("/openapi.json")

    assert response.status_code == 200
    schema = response.json()
    assert schema["info"]["title"] == "Foliowise API"
    assert "/auth/login" in schema["paths"]


def test_cors_headers_are_present_on_a_preflight_request(client):
    response = client.options(
        "/holdings/",
        headers={
            "Origin": "http://localhost:4200",
            "Access-Control-Request-Method": "POST",
        },
    )

    assert response.status_code == 200
    assert "Access-Control-Allow-Origin" in response.headers
    assert "POST" in response.headers["Access-Control-Allow-Methods"]
