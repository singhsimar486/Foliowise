"""Integration tests for the /holdings routes.

The most important test in this file is the tenant isolation one: every holdings
query filters on the user id taken from the JWT, and a bug there would let one
user read another user's portfolio.
"""


def create_holding(client, headers, ticker="AAPL", quantity=10, avg_cost_basis=150.0):
    return client.post(
        "/holdings/",
        headers=headers,
        json={"ticker": ticker, "quantity": quantity, "avg_cost_basis": avg_cost_basis},
    )


# --------------------------------------------------------------------------
# Authentication
# --------------------------------------------------------------------------


def test_holdings_require_authentication(client):
    assert client.get("/holdings/").status_code == 401
    assert client.post(
        "/holdings/", json={"ticker": "AAPL", "quantity": 1, "avg_cost_basis": 1.0}
    ).status_code == 401


# --------------------------------------------------------------------------
# Creating
# --------------------------------------------------------------------------


def test_create_holding_returns_it(client, auth_headers):
    headers = auth_headers()

    response = create_holding(client, headers, ticker="AAPL", quantity=10, avg_cost_basis=150.0)

    assert response.status_code == 201
    body = response.json()
    assert body["ticker"] == "AAPL"
    assert body["quantity"] == 10
    assert body["avg_cost_basis"] == 150.0
    assert "id" in body


def test_ticker_is_normalised_to_uppercase(client, auth_headers):
    """Tickers are stored uppercase so 'aapl' and 'AAPL' are the same holding."""
    headers = auth_headers()

    response = create_holding(client, headers, ticker="aapl")

    assert response.status_code == 201
    assert response.json()["ticker"] == "AAPL"


def test_duplicate_ticker_is_rejected(client, auth_headers):
    headers = auth_headers()
    create_holding(client, headers, ticker="MSFT")

    response = create_holding(client, headers, ticker="MSFT")

    assert response.status_code == 400
    assert "already have a holding" in response.json()["detail"]


def test_duplicate_detection_is_case_insensitive(client, auth_headers):
    """'msft' must collide with an existing 'MSFT' rather than creating a second row."""
    headers = auth_headers()
    create_holding(client, headers, ticker="MSFT")

    response = create_holding(client, headers, ticker="msft")

    assert response.status_code == 400


def test_create_holding_validates_its_payload(client, auth_headers):
    headers = auth_headers()

    response = client.post(
        "/holdings/", headers=headers, json={"ticker": "AAPL", "quantity": "lots"}
    )

    assert response.status_code == 422


# --------------------------------------------------------------------------
# Reading
# --------------------------------------------------------------------------


def test_listing_holdings_starts_empty(client, auth_headers):
    headers = auth_headers()

    response = client.get("/holdings/", headers=headers)

    assert response.status_code == 200
    assert response.json() == []


def test_listing_returns_only_this_users_holdings(client, auth_headers):
    """Tenant isolation. A user must never see another user's positions."""
    alice = auth_headers(email="alice@example.com")
    bob = auth_headers(email="bob@example.com")

    create_holding(client, alice, ticker="AAPL")
    create_holding(client, bob, ticker="TSLA")

    alice_tickers = [h["ticker"] for h in client.get("/holdings/", headers=alice).json()]
    bob_tickers = [h["ticker"] for h in client.get("/holdings/", headers=bob).json()]

    assert alice_tickers == ["AAPL"]
    assert bob_tickers == ["TSLA"]


def test_a_user_cannot_fetch_another_users_holding_by_id(client, auth_headers):
    """Access is denied, which is the property that matters.

    Note the status code: the route looks the holding up by id first and only
    then compares the owner, so a request for someone else's holding returns
    403 while a request for an id that does not exist returns 404. That
    difference tells an attacker which ids are real. Returning 404 in both
    cases, by filtering on user_id inside the query itself, would close that
    gap. This test pins the current behaviour so the change is deliberate.
    """
    alice = auth_headers(email="alice@example.com")
    bob = auth_headers(email="bob@example.com")

    holding_id = create_holding(client, alice, ticker="AAPL").json()["id"]

    response = client.get(f"/holdings/{holding_id}", headers=bob)

    assert response.status_code == 403
    assert client.get(f"/holdings/{holding_id}", headers=alice).status_code == 200


def test_fetching_a_holding_that_does_not_exist_returns_404(client, auth_headers):
    headers = auth_headers()

    response = client.get("/holdings/00000000-0000-0000-0000-000000000000", headers=headers)

    assert response.status_code == 404


# --------------------------------------------------------------------------
# Subscription limits
# --------------------------------------------------------------------------


def test_free_tier_is_capped_at_ten_holdings(client, auth_headers):
    """New accounts default to the free tier, which allows ten holdings."""
    headers = auth_headers()

    for index in range(10):
        response = create_holding(client, headers, ticker=f"TST{index}")
        assert response.status_code == 201, f"holding {index} should have been allowed"

    eleventh = create_holding(client, headers, ticker="OVER")

    assert eleventh.status_code == 403
    assert "Free tier is limited to 10 holdings" in eleventh.json()["detail"]
