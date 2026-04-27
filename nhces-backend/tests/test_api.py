"""
iNHCES — API Health & General Tests (Agent 06)

Covers:
  GET /       — root health response
  GET /health — DB + ML model status
  GET /docs   — OpenAPI documentation
  GET /redoc  — ReDoc documentation
  CORS        — preflight OPTIONS returns correct headers

TETFund NRF 2025 | Department of Quantity Surveying, ABU Zaria
"""

import pytest
from unittest.mock import patch


# ---------------------------------------------------------------------------
# GET /
# ---------------------------------------------------------------------------

class TestRoot:
    def test_returns_200(self, client):
        resp = client.get("/")
        assert resp.status_code == 200

    def test_body_has_system_key(self, client):
        body = client.get("/").json()
        assert body["system"] == "iNHCES API"

    def test_body_has_version(self, client):
        body = client.get("/").json()
        assert "version" in body

    def test_body_has_status_operational(self, client):
        body = client.get("/").json()
        assert body["status"] == "operational"

    def test_body_has_docs_link(self, client):
        body = client.get("/").json()
        assert body.get("docs") == "/docs"


# ---------------------------------------------------------------------------
# GET /health
# ---------------------------------------------------------------------------

class TestHealth:
    def test_returns_200_when_db_ok(self, client):
        with patch(
            "app.database.health_check",
            return_value={"status": "ok", "latency_ms": 12, "champion_loaded": False},
        ):
            resp = client.get("/health")
        assert resp.status_code == 200

    def test_overall_status_ok_when_db_ok(self, client):
        with patch(
            "app.database.health_check",
            return_value={"status": "ok", "latency_ms": 12, "champion_loaded": False},
        ):
            body = client.get("/health").json()
        assert body["status"] == "ok"

    def test_overall_status_degraded_when_db_fails(self, client):
        with patch(
            "app.database.health_check",
            return_value={"status": "degraded", "error": "connection refused"},
        ):
            body = client.get("/health").json()
        assert body["status"] == "degraded"

    def test_body_has_db_key(self, client):
        with patch(
            "app.database.health_check",
            return_value={"status": "ok", "latency_ms": 5},
        ):
            body = client.get("/health").json()
        assert "db" in body

    def test_body_has_ml_model_key(self, client):
        with patch(
            "app.database.health_check",
            return_value={"status": "ok"},
        ):
            body = client.get("/health").json()
        assert "ml_model" in body


# ---------------------------------------------------------------------------
# OpenAPI / ReDoc
# ---------------------------------------------------------------------------

class TestDocs:
    def test_openapi_docs_accessible(self, client):
        resp = client.get("/docs")
        assert resp.status_code == 200

    def test_redoc_accessible(self, client):
        resp = client.get("/redoc")
        assert resp.status_code == 200

    def test_openapi_json_schema_accessible(self, client):
        resp = client.get("/openapi.json")
        assert resp.status_code == 200

    def test_openapi_schema_has_paths(self, client):
        schema = client.get("/openapi.json").json()
        assert "/estimate" in schema["paths"]
        assert "/macro" in schema["paths"]


# ---------------------------------------------------------------------------
# CORS headers
# ---------------------------------------------------------------------------

class TestCORS:
    _origin = "http://localhost:3000"

    def test_cors_origin_in_response(self, client):
        resp = client.get("/", headers={"Origin": self._origin})
        assert resp.headers.get("access-control-allow-origin") in (
            self._origin, "*"
        )

    def test_cors_preflight_returns_200(self, client):
        resp = client.options(
            "/estimate",
            headers={
                "Origin":                         self._origin,
                "Access-Control-Request-Method":  "POST",
                "Access-Control-Request-Headers": "Content-Type",
            },
        )
        assert resp.status_code == 200

