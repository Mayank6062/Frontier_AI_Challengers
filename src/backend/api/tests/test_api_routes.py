from __future__ import annotations

from fastapi.testclient import TestClient

from backend.api.main import create_app


class InMemoryStorage:
    def __init__(self) -> None:
        self._data: dict[str, dict] = {}

    def put(self, key: str, value: dict) -> None:
        self._data[key] = value

    def get(self, key: str) -> dict | None:
        return self._data.get(key)

    def delete(self, key: str) -> None:
        self._data.pop(key, None)

    def query(self, prefix: str):
        for k, v in list(self._data.items()):
            if k.startswith(prefix):
                yield v


class SimpleSecrets:
    def get_secret(self, name: str) -> str | None:
        if name == "jwt_secret":
            return "test-secret"
        return None


class SimpleLogger:
    def info(self, *a, **k):
        return None

    def debug(self, *a, **k):
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
    client = TestClient(app)
    # Override DI container after startup with lightweight Provided stub
    client.app.state.di_provided = Provided()
    return client


def test_health_and_version():
    client = setup_test_client()
    r = client.get("/healthz")
    assert r.status_code == 200 and r.json().get("status") == "ok"
    r = client.get("/version")
    assert r.status_code == 200 and "version" in r.json()


def test_create_session_and_get():
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


def test_create_engagement():
    client = setup_test_client()
    payload = {"title": "TestEng", "description": "desc"}
    r = client.post("/v1/engagements/", json=payload)
    print('RESPONSE:', r.status_code, r.text)
    assert r.status_code == 201
    data = r.json()
    assert data["title"] == "TestEng"


def test_issue_token():
    client = setup_test_client()
    r = client.post("/v1/auth/token", json={"username": "alice"})
    assert r.status_code == 200
    data = r.json()
    assert "access_token" in data and data["token_type"] == "bearer"
