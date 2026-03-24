import pytest
pytest.importorskip("httpx")

from fastapi.testclient import TestClient
from app.main import app
from app.api.routes import get_service


class FakePriceService:
    async def get_all(self, ticker):
        if ticker == "btc_usd":
            return [{"ticker": ticker, "price": 100.5, "timestamp": 1700000000}]
        return []

    async def get_latest(self, ticker):
        if ticker == "btc_usd":
            return {"ticker": ticker, "price": 101.0, "timestamp": 1700000060}
        return None

    async def get_filtered(self, ticker, from_ts, to_ts):
        if ticker == "btc_usd" and from_ts <= 1700000000 <= to_ts:
            return [{"ticker": ticker, "price": 99.0, "timestamp": 1700000000}]
        return []


@pytest.fixture
def override_service():
    app.dependency_overrides[get_service] = lambda: FakePriceService()
    yield
    app.dependency_overrides.clear()


def test_health():
    client = TestClient(app)
    resp = client.get("/health")
    assert resp.status_code == 200


def test_get_all_prices_ok(override_service):
    client = TestClient(app)
    resp = client.get("/prices", params={"ticker": "btc_usd"})
    assert resp.status_code == 200
    assert len(resp.json()) == 1


def test_get_all_prices_invalid_ticker(override_service):
    client = TestClient(app)
    resp = client.get("/prices", params={"ticker": "sol_usd"})
    assert resp.status_code == 400


def test_get_latest_ok(override_service):
    client = TestClient(app)
    resp = client.get("/prices/latest", params={"ticker": "btc_usd"})
    assert resp.status_code == 200
    assert resp.json()["price"] == 101.0


def test_get_filtered_ok(override_service):
    client = TestClient(app)
    resp = client.get(
        "/prices/filter",
        params={"ticker": "btc_usd", "from_ts": 1699990000, "to_ts": 1700010000},
    )
    assert resp.status_code == 200
    assert resp.json()[0]["timestamp"] == 1700000000
