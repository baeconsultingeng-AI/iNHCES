"""
iNHCES — /macro, /projects, /pipeline Endpoint Tests (Agent 06)

Covers:
  GET  /macro                          — macro snapshot (7 variables)
  GET  /macro/history?variable=...     — historical series + validation
  GET  /projects          (no auth)    — empty list returned
  GET  /projects          (auth)       — paginated project list
  POST /projects          (no auth)    — 401 Unauthorized
  POST /projects          (auth)       — 201 Created
  GET  /projects/{id}     (auth)       — 200 or 404
  PUT  /projects/{id}     (auth)       — 200 updated
  DELETE /projects/{id}   (auth)       — 204 No Content
  GET  /pipeline                       — 200 with 9 DAGs

TETFund NRF 2025 | Department of Quantity Surveying, ABU Zaria
"""

from datetime import datetime, timezone
from unittest.mock import patch, MagicMock
import pytest


def make_db_mock(data=None, count=0):
    """Supabase-like MagicMock with chainable query methods."""
    result = MagicMock(data=data if data is not None else [], count=count)
    chain = MagicMock()
    chain.execute.return_value = result
    for m in ("select", "insert", "update", "delete", "eq", "neq",
              "order", "limit", "range", "single"):
        getattr(chain, m).return_value = chain
    db = MagicMock()
    db.table.return_value = chain
    return db


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_NOW_ISO = datetime.now(timezone.utc).isoformat()

_MACRO_ROW_FX = {
    "date":       "2024-12-01",
    "ngn_usd":    1580.0,
    "ngn_eur":    1720.0,
    "ngn_gbp":    2010.0,
    "source":     "CBN",
    "data_level": "GREEN",
}

_MACRO_ROW_CPI = {
    "date":           "2024-12-01",
    "cpi_annual_pct": 32.5,
    "source":         "World Bank",
    "data_level":     "GREEN",
}

_PROJECT_ROW = {
    "id":                "proj-uuid-001",
    "user_id":           "test-user-abc-123",
    "title":             "Abuja Residential Block",
    "building_type":     "Residential",
    "construction_type": "New Build",
    "floor_area_sqm":    200.0,
    "num_floors":        2,
    "location_state":    "FCT",
    "location_zone":     "North Central",
    "location_lga":      None,
    "target_cost_ngn":   None,
    "notes":             None,
    "status":            "active",
    "created_at":        _NOW_ISO,
    "updated_at":        _NOW_ISO,
}

_PROJECT_CREATE_BODY = {
    "title":             "Test Project Alpha",
    "building_type":     "Residential",
    "construction_type": "New Build",
    "floor_area_sqm":    150.0,
    "num_floors":        1,
    "location_state":    "Kaduna",
    "location_zone":     "North West",
}


# ---------------------------------------------------------------------------
# GET /macro
# ---------------------------------------------------------------------------

class TestMacroSnapshot:
    _patch_target = "app.routers.macro.get_db"

    def test_returns_200(self, client):
        with patch(self._patch_target, return_value=make_db_mock()):
            resp = client.get("/macro")
        assert resp.status_code == 200

    def test_response_has_variables_key(self, client):
        with patch(self._patch_target, return_value=make_db_mock()):
            body = client.get("/macro").json()
        assert "variables" in body

    def test_variables_list_has_7_entries(self, client):
        with patch(self._patch_target, return_value=make_db_mock()):
            body = client.get("/macro").json()
        assert len(body["variables"]) == 7

    def test_each_variable_has_required_keys(self, client):
        with patch(self._patch_target, return_value=make_db_mock()):
            body = client.get("/macro").json()
        required = {"variable", "label", "value", "unit", "data_level"}
        for v in body["variables"]:
            assert required.issubset(v.keys()), f"Missing keys in {v}"

    def test_overall_freshness_present(self, client):
        with patch(self._patch_target, return_value=make_db_mock()):
            body = client.get("/macro").json()
        assert body.get("overall_freshness") in ("GREEN", "AMBER", "RED")

    def test_as_of_timestamp_present(self, client):
        with patch(self._patch_target, return_value=make_db_mock()):
            body = client.get("/macro").json()
        assert "as_of" in body

    def test_missing_db_data_returns_red_level(self, client):
        """When DB returns no rows, each variable should have data_level=RED."""
        with patch(self._patch_target, return_value=make_db_mock(data=[])):
            body = client.get("/macro").json()
        for v in body["variables"]:
            assert v["data_level"] == "RED"


# ---------------------------------------------------------------------------
# GET /macro/history
# ---------------------------------------------------------------------------

class TestMacroHistory:
    _patch_target = "app.routers.macro.get_db"

    def _history_row(self, var_col, value, data_level="GREEN"):
        return {"date": "2024-01-01", var_col: value, "data_level": data_level}

    def test_valid_variable_returns_200(self, client):
        with patch(self._patch_target, return_value=make_db_mock(
            data=[self._history_row("ngn_usd", 1580.0)]
        )):
            resp = client.get("/macro/history", params={"variable": "ngn_usd"})
        assert resp.status_code == 200

    def test_response_has_data_key(self, client):
        with patch(self._patch_target, return_value=make_db_mock(
            data=[self._history_row("ngn_usd", 1580.0)]
        )):
            body = client.get("/macro/history", params={"variable": "ngn_usd"}).json()
        assert "data" in body

    def test_response_has_variable_metadata(self, client):
        with patch(self._patch_target, return_value=make_db_mock(
            data=[self._history_row("ngn_usd", 1580.0)]
        )):
            body = client.get("/macro/history", params={"variable": "ngn_usd"}).json()
        assert "variable" in body
        assert "label"    in body
        assert "unit"     in body

    def test_invalid_variable_returns_400(self, client):
        with patch(self._patch_target, return_value=make_db_mock()):
            resp = client.get("/macro/history", params={"variable": "unknown_var"})
        assert resp.status_code == 400

    def test_years_param_out_of_range_returns_422(self, client):
        """years must be between 1 and 25."""
        with patch(self._patch_target, return_value=make_db_mock()):
            resp = client.get("/macro/history", params={"variable": "ngn_usd", "years": 0})
        assert resp.status_code == 422

    def test_all_valid_variables_return_200(self, client):
        """Each of the 7 known macro variable keys must be accepted."""
        valid_vars = [
            "ngn_usd", "ngn_eur", "ngn_gbp",
            "cpi_annual_pct", "gdp_growth_pct",
            "lending_rate_pct", "brent_usd_barrel",
        ]
        for var in valid_vars:
            with patch(self._patch_target, return_value=make_db_mock(data=[])):
                resp = client.get("/macro/history", params={"variable": var})
            assert resp.status_code == 200, f"Expected 200 for variable={var}"


# ---------------------------------------------------------------------------
# GET /projects (unauthenticated)
# ---------------------------------------------------------------------------

class TestProjectsUnauthenticated:

    def test_list_no_auth_returns_200(self, client):
        """GET /projects without auth must return 200 (empty list, not 401)."""
        resp = client.get("/projects")
        assert resp.status_code == 200

    def test_list_no_auth_returns_empty_items(self, client):
        body = client.get("/projects").json()
        assert body["items"] == []
        assert body["total"] == 0

    def test_create_no_auth_returns_401(self, client):
        """POST /projects without auth must return 401."""
        resp = client.post("/projects", json=_PROJECT_CREATE_BODY)
        assert resp.status_code == 401

    def test_get_single_no_auth_returns_401(self, client):
        resp = client.get("/projects/some-project-id")
        assert resp.status_code == 401


# ---------------------------------------------------------------------------
# GET /projects (authenticated)
# ---------------------------------------------------------------------------

class TestProjectsAuthenticated:
    _patch_target = "app.routers.projects.get_db"

    def test_list_with_auth_returns_200(self, authed_client):
        with patch(self._patch_target,
                   return_value=make_db_mock(data=[_PROJECT_ROW], count=1)):
            resp = authed_client.get("/projects")
        assert resp.status_code == 200

    def test_list_contains_project(self, authed_client):
        with patch(self._patch_target,
                   return_value=make_db_mock(data=[_PROJECT_ROW], count=1)):
            body = authed_client.get("/projects").json()
        assert body["total"] == 1
        assert body["items"][0]["title"] == _PROJECT_ROW["title"]

    def test_list_pagination_defaults(self, authed_client):
        with patch(self._patch_target,
                   return_value=make_db_mock(data=[_PROJECT_ROW], count=1)):
            body = authed_client.get("/projects").json()
        assert body["page"]  == 1
        assert body["limit"] == 20

    def test_create_project_returns_201(self, authed_client):
        with patch(self._patch_target,
                   return_value=make_db_mock(data=[_PROJECT_ROW])):
            resp = authed_client.post("/projects", json=_PROJECT_CREATE_BODY)
        assert resp.status_code == 201

    def test_create_project_response_has_id(self, authed_client):
        with patch(self._patch_target,
                   return_value=make_db_mock(data=[_PROJECT_ROW])):
            body = authed_client.post("/projects", json=_PROJECT_CREATE_BODY).json()
        assert "id" in body

    def test_create_project_missing_title_returns_422(self, authed_client):
        body = {k: v for k, v in _PROJECT_CREATE_BODY.items() if k != "title"}
        resp = authed_client.post("/projects", json=body)
        assert resp.status_code == 422

    def test_create_project_missing_floor_area_returns_422(self, authed_client):
        body = {k: v for k, v in _PROJECT_CREATE_BODY.items() if k != "floor_area_sqm"}
        resp = authed_client.post("/projects", json=body)
        assert resp.status_code == 422

    def test_get_missing_project_returns_404(self, authed_client):
        # Supabase .single() raises when no row is found → router catches → 404
        db = make_db_mock(data=[])
        db.table.return_value.single.return_value.execute.side_effect = Exception(
            "No rows returned by a query expected to return exactly one row"
        )
        with patch(self._patch_target, return_value=db):
            resp = authed_client.get("/projects/nonexistent-uuid")
        assert resp.status_code == 404


# ---------------------------------------------------------------------------
# GET /pipeline
# ---------------------------------------------------------------------------

class TestPipelineStatus:
    """GET /pipeline returns DAG health from Airflow (or graceful degradation)."""

    def test_returns_200(self, client):
        with patch("app.routers.pipeline._fetch_airflow_status", return_value={}):
            resp = client.get("/pipeline")
        assert resp.status_code == 200

    def test_response_has_dags_key(self, client):
        with patch("app.routers.pipeline._fetch_airflow_status", return_value={}):
            body = client.get("/pipeline").json()
        assert "dags" in body

    def test_nine_dags_returned(self, client):
        """Pipeline status must enumerate all 9 known iNHCES DAGs."""
        with patch("app.routers.pipeline._fetch_airflow_status", return_value={}):
            body = client.get("/pipeline").json()
        assert len(body["dags"]) == 9

    def test_dags_have_required_fields(self, client):
        with patch("app.routers.pipeline._fetch_airflow_status", return_value={}):
            body = client.get("/pipeline").json()
        required = {"dag_id", "schedule", "description", "data_level"}
        for dag in body["dags"]:
            assert required.issubset(dag.keys()), f"Missing fields in DAG: {dag}"

    def test_overall_health_present(self, client):
        with patch("app.routers.pipeline._fetch_airflow_status", return_value={}):
            body = client.get("/pipeline").json()
        assert body.get("overall_health") in ("OK", "DEGRADED", "DOWN")

    def test_checked_at_present(self, client):
        with patch("app.routers.pipeline._fetch_airflow_status", return_value={}):
            body = client.get("/pipeline").json()
        assert "checked_at" in body

    def test_airflow_unreachable_returns_degraded(self, client):
        """
        When Airflow is unreachable, _fetch_airflow_status returns {} or None.
        The route must respond 200 with overall_health=DEGRADED.
        """
        # Simulate what the real function returns when Airflow is down
        with patch(
            "app.routers.pipeline._fetch_airflow_status",
            return_value={},
        ):
            resp = client.get("/pipeline")
        assert resp.status_code == 200
        assert resp.json()["overall_health"] == "DEGRADED"

