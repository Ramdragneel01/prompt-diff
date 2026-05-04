from fastapi.testclient import TestClient

from prompt_diff.app import create_app
from prompt_diff.config import Settings


def _client() -> TestClient:
    return TestClient(create_app(Settings(frontend_dir="frontend", max_prompt_chars=2000)))


def test_health_ready_root():
    c = _client()
    assert c.get("/").status_code == 200
    assert c.get("/health").json()["status"] == "ok"
    assert c.get("/ready").json()["status"] == "ready"


def test_diff_endpoint():
    c = _client()
    payload = {
        "baseline": "Use {customer_id}. Summarize.",
        "candidate": "Use {account_id}. Summarize with follow-up steps."
    }
    response = c.post("/v1/diff", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert "metrics" in body
    assert "risk" in body


def test_diff_rejects_oversize_prompt():
    c = _client()
    huge = "a" * 5000
    response = c.post("/v1/diff", json={"baseline": huge, "candidate": "ok"})
    assert response.status_code == 400


def test_ui_route_served():
    c = _client()
    response = c.get("/ui/")
    assert response.status_code == 200
    assert "Prompt Diff" in response.text


def test_metrics_endpoint():
    c = _client()
    text = c.get("/metrics").text
    assert "prompt_diff_requests_total" in text
