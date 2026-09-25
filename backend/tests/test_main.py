"""
BobAccess FastAPI endpoint tests.
Covers: GET /, GET /health, POST /api/query, POST /api/documents/upload
"""
import io
import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def client():
    from backend.app.main import app
    return TestClient(app)


# ── GET / ─────────────────────────────────────────────────────────────────────

def test_root_serves_html(client):
    """GET / must return the frontend HTML page (text/html)."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "BobAccess" in response.text


def test_app_route_serves_html(client):
    """GET /app must serve the same frontend HTML."""
    response = client.get("/app")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


# ── GET /health ────────────────────────────────────────────────────────────────

def test_health_returns_200(client):
    """GET /health must return HTTP 200."""
    response = client.get("/health")
    assert response.status_code == 200


def test_health_body_structure(client):
    """GET /health body must contain required keys."""
    body = client.get("/health").json()
    assert body["status"] == "healthy"
    assert "timestamp" in body
    assert "ibm_watson_tts_configured" in body
    assert "watsonx_configured" in body


# ── GET /api/status ────────────────────────────────────────────────────────────

def test_api_status(client):
    """GET /api/status must report service online."""
    body = client.get("/api/status").json()
    assert body["status"] == "online"
    assert body["mcp_enabled"] is True


# ── POST /api/query ────────────────────────────────────────────────────────────

def test_query_returns_spoken_answer(client):
    """POST /api/query must return a non-empty spoken_answer."""
    body = client.post(
        "/api/query",
        json={"query_text": "What is the p99 latency target?", "mode": "audio_summary"}
    ).json()
    assert "spoken_answer" in body
    assert len(body["spoken_answer"]) > 10


def test_query_missing_body_returns_422(client):
    """POST /api/query with empty body must return 422 Unprocessable Entity."""
    response = client.post("/api/query", json={})
    assert response.status_code == 422


def test_query_returns_suggested_followups(client):
    """POST /api/query must include suggested_followups list."""
    body = client.post(
        "/api/query",
        json={"query_text": "Explain the microservices architecture", "mode": "audio_summary"}
    ).json()
    assert isinstance(body.get("suggested_followups"), list)


# ── POST /api/documents/upload ─────────────────────────────────────────────────

def test_upload_text_file(client):
    """POST /api/documents/upload with a plain text file must succeed."""
    content = b"Enterprise system uses microservices on Kubernetes with IBM Db2."
    response = client.post(
        "/api/documents/upload",
        files={"file": ("test.txt", io.BytesIO(content), "text/plain")}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "success"
    assert "document_id" in body["document"]
    assert len(body["audio_narrative_summary"]) > 10


def test_upload_returns_doc_metadata(client):
    """Uploaded document metadata must include filename and character count."""
    content = b"Architecture specification with tables and diagrams."
    body = client.post(
        "/api/documents/upload",
        files={"file": ("spec.md", io.BytesIO(content), "text/markdown")}
    ).json()
    doc = body["document"]
    assert doc["filename"] == "spec.md"
    assert doc["total_characters"] > 0
    assert doc["page_count"] >= 1
