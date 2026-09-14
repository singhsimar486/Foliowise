"""
Shared pytest fixtures for the Foliowise API test suite.

These tests run against a real PostgreSQL database rather than SQLite, because
the application uses Postgres in production and several behaviours (server-side
defaults, CASCADE truncation, string/UUID primary keys) only behave identically
when the test database is the same engine as the real one.

Locally:  docker compose up -d db   (see docker-compose.yml at the repo root)
In CI:    a postgres service container, see .github/workflows/ci.yml
"""

import os

# Settings are read from the environment when app.config is imported, so these
# defaults must be set before any `app.*` import happens anywhere in the suite.
os.environ.setdefault(
    "DATABASE_URL", "postgresql://postgres:postgres@127.0.0.1:5432/foliowise_test"
)
os.environ.setdefault("SECRET_KEY", "test-secret-key-not-used-outside-tests")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

from app.database import Base, engine
from app.main import app
from app import models  # noqa: F401  - registers every model on Base.metadata


def _guard_against_real_database() -> None:
    """Refuse to run if DATABASE_URL does not look like a throwaway test database.

    The suite truncates every table between tests. Pointing it at a real
    database would destroy data, so this fails loudly instead.
    """
    url = os.environ["DATABASE_URL"]
    if "test" not in url.rsplit("/", 1)[-1]:
        raise RuntimeError(
            f"Refusing to run: DATABASE_URL database name must contain 'test'. Got: {url}"
        )


@pytest.fixture(scope="session", autouse=True)
def _database_schema():
    """Create the schema once for the whole session, and drop it at the end."""
    _guard_against_real_database()
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(autouse=True)
def _clean_tables():
    """Empty every table before each test so tests cannot leak state into each other.

    TRUNCATE ... CASCADE is used rather than deleting per-table in dependency
    order, because holdings, transactions and alerts all reference users.
    """
    tables = ", ".join(f'"{table.name}"' for table in Base.metadata.sorted_tables)
    with engine.begin() as connection:
        connection.execute(text(f"TRUNCATE {tables} RESTART IDENTITY CASCADE"))
    yield


@pytest.fixture(scope="session")
def client(_database_schema):
    """A TestClient bound to the real app, with startup and shutdown events run."""
    with TestClient(app) as test_client:
        yield test_client


# --------------------------------------------------------------------------
# Convenience helpers
# --------------------------------------------------------------------------

DEFAULT_PASSWORD = "correct-horse-battery-staple"


@pytest.fixture
def register_user(client):
    """Register a user and return the API's response body."""

    def _register(email: str = "simar@example.com", password: str = DEFAULT_PASSWORD):
        response = client.post(
            "/auth/register", json={"email": email, "password": password}
        )
        assert response.status_code == 201, response.text
        return response.json()

    return _register


@pytest.fixture
def login(client):
    """Log a user in and return the raw access token."""

    def _login(email: str = "simar@example.com", password: str = DEFAULT_PASSWORD):
        # /auth/login uses OAuth2PasswordRequestForm, so the payload is form
        # encoded and the email is sent in the `username` field.
        response = client.post(
            "/auth/login", data={"username": email, "password": password}
        )
        assert response.status_code == 200, response.text
        return response.json()["access_token"]

    return _login


@pytest.fixture
def auth_headers(register_user, login):
    """Register and log in a user, returning an Authorization header for them."""

    def _auth_headers(email: str = "simar@example.com"):
        register_user(email=email)
        token = login(email=email)
        return {"Authorization": f"Bearer {token}"}

    return _auth_headers
