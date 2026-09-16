"""Integration tests for registration, login and the authenticated /auth/me route."""

from datetime import datetime, timedelta

import pytest
from jose import jwt

from app.config import settings
from app.services.auth import ALGORITHM, hash_password, verify_password


# --------------------------------------------------------------------------
# Password hashing
# --------------------------------------------------------------------------


def test_password_hash_is_not_the_plain_password():
    hashed = hash_password("hunter2")
    assert hashed != "hunter2"
    assert hashed.startswith("$2b$")  # bcrypt identifier


def test_password_verifies_against_its_own_hash():
    hashed = hash_password("hunter2")
    assert verify_password("hunter2", hashed) is True
    assert verify_password("hunter3", hashed) is False


def test_same_password_hashes_differently_each_time():
    """bcrypt salts every hash, so two hashes of one password must not match."""
    assert hash_password("hunter2") != hash_password("hunter2")


# --------------------------------------------------------------------------
# Registration
# --------------------------------------------------------------------------


def test_register_returns_the_created_user_without_the_password(client):
    response = client.post(
        "/auth/register", json={"email": "new@example.com", "password": "a-password"}
    )

    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "new@example.com"
    assert body["is_active"] is True
    assert "id" in body
    # The response schema must never leak the hash.
    assert "password" not in body
    assert "password_hash" not in body


def test_register_rejects_a_duplicate_email(client, register_user):
    register_user(email="taken@example.com")

    response = client.post(
        "/auth/register", json={"email": "taken@example.com", "password": "another"}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_register_rejects_a_malformed_email(client):
    response = client.post(
        "/auth/register", json={"email": "not-an-email", "password": "a-password"}
    )

    # Pydantic's EmailStr rejects this before the route body ever runs.
    assert response.status_code == 422


# --------------------------------------------------------------------------
# Login
# --------------------------------------------------------------------------


def test_login_returns_a_bearer_token(client, register_user):
    register_user(email="login@example.com", password="secret-password")

    response = client.post(
        "/auth/login", data={"username": "login@example.com", "password": "secret-password"}
    )

    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]


def test_login_token_carries_the_user_id_and_an_expiry(client, register_user):
    user = register_user(email="claims@example.com")

    response = client.post(
        "/auth/login",
        data={"username": "claims@example.com", "password": "correct-horse-battery-staple"},
    )
    token = response.json()["access_token"]

    claims = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
    assert claims["sub"] == user["id"]
    assert "exp" in claims


def test_login_rejects_a_wrong_password(client, register_user):
    register_user(email="wrongpw@example.com", password="the-real-password")

    response = client.post(
        "/auth/login", data={"username": "wrongpw@example.com", "password": "guessing"}
    )

    assert response.status_code == 401
    # The message must not reveal whether the account exists.
    assert response.json()["detail"] == "Invalid email or password"


def test_login_rejects_an_unknown_email_with_the_same_message(client):
    """An attacker must not be able to enumerate accounts from the error text."""
    response = client.post(
        "/auth/login", data={"username": "nobody@example.com", "password": "guessing"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"


# --------------------------------------------------------------------------
# /auth/me and token validation
# --------------------------------------------------------------------------


def test_me_returns_the_authenticated_user(client, register_user, login):
    user = register_user(email="me@example.com")
    token = login(email="me@example.com")

    response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json()["id"] == user["id"]
    assert response.json()["email"] == "me@example.com"


def test_me_requires_a_token(client):
    response = client.get("/auth/me")
    assert response.status_code == 401


def test_me_rejects_a_garbage_token(client):
    response = client.get("/auth/me", headers={"Authorization": "Bearer not.a.jwt"})

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or expired token"


def test_me_rejects_a_token_signed_with_the_wrong_key(client, register_user):
    """A token this server did not sign must not be accepted."""
    user = register_user(email="forged@example.com")
    forged = jwt.encode(
        {"sub": user["id"], "exp": datetime.utcnow() + timedelta(minutes=30)},
        "a-different-secret",
        algorithm=ALGORITHM,
    )

    response = client.get("/auth/me", headers={"Authorization": f"Bearer {forged}"})

    assert response.status_code == 401


def test_me_rejects_an_expired_token(client, register_user):
    user = register_user(email="expired@example.com")
    expired = jwt.encode(
        {"sub": user["id"], "exp": datetime.utcnow() - timedelta(minutes=1)},
        settings.secret_key,
        algorithm=ALGORITHM,
    )

    response = client.get("/auth/me", headers={"Authorization": f"Bearer {expired}"})

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or expired token"


def test_me_rejects_a_valid_token_for_a_user_that_no_longer_exists(client):
    """Signature alone is not enough: the subject must still resolve to a user."""
    orphan = jwt.encode(
        {
            "sub": "00000000-0000-0000-0000-000000000000",
            "exp": datetime.utcnow() + timedelta(minutes=30),
        },
        settings.secret_key,
        algorithm=ALGORITHM,
    )

    response = client.get("/auth/me", headers={"Authorization": f"Bearer {orphan}"})

    assert response.status_code == 404
