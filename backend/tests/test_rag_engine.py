"""
BobAccess Pytest Suite
Covers: LightweightEmbeddingFunction, RAGEngine audio formatter, FastAPI /health endpoint.
"""
import math
import pytest
from fastapi.testclient import TestClient


# ── 1. LightweightEmbeddingFunction ──────────────────────────────────────────

def test_embedding_dimension_and_norm():
    """Generated vectors must have the configured dimension and be L2-normalised."""
    from backend.app.rag_engine import LightweightEmbeddingFunction

    ef = LightweightEmbeddingFunction(dim=128)
    result = ef(["hello world IBM accessibility"])

    assert len(result) == 1, "Expected exactly one embedding vector"
    vec = result[0]
    assert len(vec) == 128, f"Expected dim=128, got {len(vec)}"

    norm = math.sqrt(sum(x * x for x in vec))
    assert abs(norm - 1.0) < 1e-6, f"Vector is not unit-normalised; norm={norm}"


def test_embedding_empty_string_returns_zero_vector():
    """An empty string must produce a zero vector without raising."""
    from backend.app.rag_engine import LightweightEmbeddingFunction

    ef = LightweightEmbeddingFunction(dim=128)
    result = ef([""])

    assert len(result) == 1
    assert len(result[0]) == 128
    assert all(x == 0.0 for x in result[0]), "Empty string should produce an all-zero vector"


def test_embedding_identical_texts_produce_identical_vectors():
    """Deterministic: same text must always produce the same embedding."""
    from backend.app.rag_engine import LightweightEmbeddingFunction

    ef = LightweightEmbeddingFunction(dim=128)
    v1 = ef(["latency SLA API Gateway"])[0]
    v2 = ef(["latency SLA API Gateway"])[0]

    assert v1 == v2, "Identical inputs must produce identical embeddings"


# ── 2. RAGEngine._format_audio_answer ────────────────────────────────────────

@pytest.fixture(scope="module")
def engine():
    """Shared RAGEngine instance — ChromaDB persists to ./data/chroma_db."""
    from backend.app.rag_engine import RAGEngine
    return RAGEngine()


def test_format_audio_answer_empty(engine):
    """Empty passage list must return a graceful no-match spoken message."""
    result = engine._format_audio_answer("nonexistent query", [])

    assert "did not find" in result.lower() or "no" in result.lower(), (
        f"Expected a no-match message, got: {result!r}"
    )


def test_format_audio_answer_table_expansion(engine):
    """
    Markdown table rows must be expanded into spoken phrases.
    '| API Gateway | 8ms | 18ms | 99.99% |' → should contain 'API Gateway' and '8ms'.
    """
    passage = "| API Gateway | 8ms | 18ms | 99.99% |"
    result = engine._format_audio_answer("latency targets", [passage])

    assert "API Gateway" in result, f"'API Gateway' not found in: {result!r}"
    assert "8ms" in result, f"'8ms' not found in: {result!r}"


def test_format_audio_answer_strips_markdown_headings(engine):
    """Markdown heading markers (##, **) must be stripped from spoken output."""
    passage = "## Performance Benchmarks\n**API Gateway** operates at 8ms p50 latency."
    result = engine._format_audio_answer("performance", [passage])

    assert "##" not in result, "Heading markers must be stripped"
    assert "**" not in result, "Bold markers must be stripped"
    assert "API Gateway" in result, "Content must survive stripping"


# ── 3. FastAPI /health endpoint ───────────────────────────────────────────────

@pytest.fixture(scope="module")
def client():
    from backend.app.main import app
    return TestClient(app)


def test_main_healthcheck(client):
    """/health must return HTTP 200 with status='healthy'."""
    response = client.get("/health")

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    body = response.json()
    assert body["status"] == "healthy", f"Expected 'healthy', got: {body!r}"
