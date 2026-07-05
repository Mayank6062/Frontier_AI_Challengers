from __future__ import annotations

from fastapi.testclient import TestClient
from typing import Any, Iterable

from backend.api.main import create_app


class InMemoryStorage:
    def __init__(self) -> None:
        self._data: dict[str, dict[str, Any]] = {}

    def put(self, key: str, value: dict[str, Any]) -> None:
        self._data[key] = value

    def get(self, key: str) -> dict[str, Any] | None:
        return self._data.get(key)

    def delete(self, key: str) -> None:
        self._data.pop(key, None)

    def query(self, prefix: str) -> Iterable[dict[str, Any]]:
        for k, v in list(self._data.items()):
            if k.startswith(prefix):
                yield v


class SimpleSecrets:
    def get_secret(self, name: str) -> str | None:
        if name == "jwt_secret":
            return "test-secret"
        return None


class SimpleLogger:
    def info(self, *a: Any, **k: Any) -> None:
        return None

    def debug(self, *a: Any, **k: Any) -> None:
        return None


class Provided:
    def __init__(self) -> None:
        self.session_store = InMemoryStorage()
        self.engagement_store = InMemoryStorage()
        self.secrets = SimpleSecrets()
        self.logger = SimpleLogger()
        self.metrics = None
        self.cache = None
        self.storage = None
        self.ledger = None
        self.llm = None


def setup_test_client() -> TestClient:
    app = create_app()
    # Attach a lightweight Provided stub directly to the FastAPI app instance
    app.state.di_provided = Provided()
    client = TestClient(app)
    return client


def test_health_and_version() -> None:
    client = setup_test_client()
    r = client.get("/healthz")
    assert r.status_code == 200 and r.json().get("status") == "ok"
    r = client.get("/version")
    assert r.status_code == 200 and "version" in r.json()


def test_create_session_and_get() -> None:
    client = setup_test_client()
    payload = {"user_id": "user-1"}
    r = client.post("/v1/sessions/", json=payload)
    assert r.status_code == 201
    body = r.json()
    assert body["user_id"] == "user-1"
    sess_id = body["id"]

    r = client.get(f"/v1/sessions/{sess_id}")
    assert r.status_code == 200
    assert r.json()["id"] == sess_id


def test_create_engagement() -> None:
    client = setup_test_client()
    payload = {"title": "TestEng", "description": "desc"}
    r = client.post("/v1/engagements/", json=payload)
    print("RESPONSE:", r.status_code, r.text)
    assert r.status_code == 201
    data = r.json()
    assert data["title"] == "TestEng"


def test_issue_token() -> None:
    client = setup_test_client()
    r = client.post("/v1/auth/token", json={"username": "alice"})
    assert r.status_code == 200
    data = r.json()
    assert "access_token" in data and data["token_type"] == "bearer"
