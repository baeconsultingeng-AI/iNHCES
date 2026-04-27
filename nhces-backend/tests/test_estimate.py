"""
iNHCES — /estimate Endpoint Tests (Agent 06)

Covers:
  POST /estimate — validation, ML pipeline, SHAP, temporal projections,
                   DB persistence (non-fatal), edge cases.

All external I/O (Supabase, ML model, SHAP, temporal engine) is mocked.

TETFund NRF 2025 | Department of Quantity Surveying, ABU Zaria
"""

import numpy as np
import pytest
from unittest.mock import patch, MagicMock


# ---------------------------------------------------------------------------
# Local test constants
# ---------------------------------------------------------------------------

FAKE_PREDICT_RESULT = {
    "predicted_cost_per_sqm": 250_000.0,
    "confidence_lower":       215_000.0,
    "confidence_upper":       285_000.0,
    "mape_at_prediction":     13.66,
    "model_name":             "LightGBM",
    "model_version":          "1.0.0-test",
    "is_synthetic":           True,
}

FAKE_FEATURES = (
    np.array([[0.20, 7.20, 2.20, -2.49,
               97.33, 93.81, 96.07,
               0.40,  4.90, 0.60, 28.36,
               76.51, 72.36, 68.55]]),
    "RED",
    {"ngn_usd": 1580.0, "cpi": 32.5},
)

FAKE_SHAP = {
    "ret_ngn_usd":      45_000.0,
    "d_cpi_annual_pct": 25_000.0,
    "computed":         True,
}

FAKE_SHAP_LABELS = [
    {"feature": "ret_ngn_usd",      "label": "NGN/USD Return (%)",     "value": 45_000.0},
    {"feature": "d_cpi_annual_pct", "label": "CPI Inflation (change)", "value": 25_000.0},
]

FAKE_PROJECTIONS = (
    [
        {
            "horizon_key": "current", "horizon_label": "Current", "years": 0,
            "cost_per_sqm": 250_000.0, "total_cost_ngn": 30_000_000.0,
            "confidence_lower": 215_000.0, "confidence_upper": 285_000.0,
            "total_lower_ngn": 25_800_000.0, "total_upper_ngn": 34_200_000.0,
            "uncertainty_pct": 14.0, "is_projection": False,
        },
        {
            "horizon_key": "short_term", "horizon_label": "Short-term (<1 yr)", "years": 1,
            "cost_per_sqm": 312_500.0, "total_cost_ngn": 37_500_000.0,
            "confidence_lower": 265_625.0, "confidence_upper": 362_500.0,
            "total_lower_ngn": 31_875_000.0, "total_upper_ngn": 43_500_000.0,
            "uncertainty_pct": 19.5, "is_projection": True,
        },
        {
            "horizon_key": "medium_term", "horizon_label": "Medium-term (<3 yrs)", "years": 3,
            "cost_per_sqm": 488_281.0, "total_cost_ngn": 58_593_750.0,
            "confidence_lower": 390_625.0, "confidence_upper": 585_937.0,
            "total_lower_ngn": 46_875_000.0, "total_upper_ngn": 70_312_500.0,
            "uncertainty_pct": 30.0, "is_projection": True,
        },
        {
            "horizon_key": "long_term", "horizon_label": "Long-term (<5 yrs)", "years": 5,
            "cost_per_sqm": 763_000.0, "total_cost_ngn": 91_562_500.0,
            "confidence_lower": 572_250.0, "confidence_upper": 953_750.0,
            "total_lower_ngn": 68_671_875.0, "total_upper_ngn": 114_453_125.0,
            "uncertainty_pct": 50.0, "is_projection": True,
        },
    ],
    0.25,
)


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

# Minimal valid request body
_VALID_BODY = {
    "building_type":     "Residential",
    "construction_type": "New Build",
    "floor_area_sqm":    120.0,
    "num_floors":        1,
    "location_state":    "Kaduna",
    "location_zone":     "North West",
}

# Patch targets in the estimate router
_P_DB       = "app.routers.estimate.get_db"
_P_FEAT     = "app.routers.estimate.build_feature_vector"
_P_PREDICT  = "app.routers.estimate.predict"
_P_SHAP     = "app.routers.estimate.compute_shap"
_P_LABELS   = "app.routers.estimate.get_shap_labels"
_P_PROJ     = "app.routers.estimate.generate_temporal_projections"


def _all_patches(db_data=None):
    """Return a list of context managers that fully mock the estimate pipeline."""
    return [
        patch(_P_DB,      return_value=make_db_mock(data=db_data)),
        patch(_P_FEAT,    return_value=FAKE_FEATURES),
        patch(_P_PREDICT, return_value=FAKE_PREDICT_RESULT),
        patch(_P_SHAP,    return_value=FAKE_SHAP),
        patch(_P_LABELS,  return_value=FAKE_SHAP_LABELS),
        patch(_P_PROJ,    return_value=FAKE_PROJECTIONS),
    ]


# ---------------------------------------------------------------------------
# Successful estimation
# ---------------------------------------------------------------------------

class TestEstimateSuccess:

    def _post(self, client, body=None):
        """Post to /estimate with all external dependencies mocked."""
        import contextlib
        body = body or _VALID_BODY
        with contextlib.ExitStack() as stack:
            for p in _all_patches():
                stack.enter_context(p)
            return client.post("/estimate", json=body)

    def test_returns_200(self, client):
        assert self._post(client).status_code == 200

    def test_response_has_prediction_id(self, client):
        body = self._post(client).json()
        assert "prediction_id" in body
        assert len(body["prediction_id"]) == 36  # UUID4

    def test_response_has_cost_per_sqm(self, client):
        body = self._post(client).json()
        assert body["predicted_cost_per_sqm"] == 250_000.0

    def test_total_cost_equals_cost_per_sqm_times_area(self, client):
        body = self._post(client).json()
        expected_total = round(250_000.0 * 120.0, 2)
        assert body["total_predicted_cost_ngn"] == pytest.approx(expected_total, rel=1e-4)

    def test_confidence_band_present(self, client):
        body = self._post(client).json()
        assert body["confidence_lower"] < body["predicted_cost_per_sqm"]
        assert body["confidence_upper"] > body["predicted_cost_per_sqm"]

    def test_shap_top_features_present(self, client):
        body = self._post(client).json()
        feats = body.get("shap_top_features", [])
        assert isinstance(feats, list)
        assert len(feats) >= 1

    def test_shap_item_has_required_keys(self, client):
        body = self._post(client).json()
        item = body["shap_top_features"][0]
        assert "feature" in item
        assert "label"   in item
        assert "value"   in item

    def test_projections_has_four_horizons(self, client):
        body = self._post(client).json()
        projs = body.get("projections", [])
        assert len(projs) == 4

    def test_projections_first_is_current(self, client):
        body = self._post(client).json()
        assert body["projections"][0]["horizon_key"] == "current"
        assert body["projections"][0]["is_projection"] is False

    def test_projections_last_is_long_term(self, client):
        body = self._post(client).json()
        assert body["projections"][-1]["horizon_key"] == "long_term"
        assert body["projections"][-1]["years"] == 5

    def test_annual_inflation_rate_in_response(self, client):
        body = self._post(client).json()
        assert "annual_inflation_rate" in body
        assert body["annual_inflation_rate"] == pytest.approx(0.25)

    def test_data_freshness_in_response(self, client):
        body = self._post(client).json()
        assert body.get("data_freshness") in ("GREEN", "AMBER", "RED")

    def test_model_name_in_response(self, client):
        body = self._post(client).json()
        assert body["model_name"] == "LightGBM"

    def test_is_synthetic_flag_present(self, client):
        body = self._post(client).json()
        assert "is_synthetic" in body

    def test_api_response_ms_non_negative(self, client):
        body = self._post(client).json()
        assert body.get("api_response_ms", -1) >= 0

    def test_with_optional_project_id(self, client):
        """Including a valid UUID project_id must still return 200."""
        body = dict(_VALID_BODY, project_id="550e8400-e29b-41d4-a716-446655440000")
        resp = self._post(client, body=body)
        assert resp.status_code == 200


# ---------------------------------------------------------------------------
# Input validation (Pydantic)
# ---------------------------------------------------------------------------

class TestEstimateValidation:

    def test_missing_floor_area_returns_422(self, client):
        body = {k: v for k, v in _VALID_BODY.items() if k != "floor_area_sqm"}
        resp = client.post("/estimate", json=body)
        assert resp.status_code == 422

    def test_zero_floor_area_returns_422(self, client):
        body = dict(_VALID_BODY, floor_area_sqm=0)
        resp = client.post("/estimate", json=body)
        assert resp.status_code == 422

    def test_negative_floor_area_returns_422(self, client):
        body = dict(_VALID_BODY, floor_area_sqm=-50)
        resp = client.post("/estimate", json=body)
        assert resp.status_code == 422

    def test_floor_area_exceeds_max_returns_422(self, client):
        body = dict(_VALID_BODY, floor_area_sqm=200_000)
        resp = client.post("/estimate", json=body)
        assert resp.status_code == 422

    def test_missing_location_state_returns_422(self, client):
        body = {k: v for k, v in _VALID_BODY.items() if k != "location_state"}
        resp = client.post("/estimate", json=body)
        assert resp.status_code == 422

    def test_invalid_building_type_returns_422(self, client):
        body = dict(_VALID_BODY, building_type="Castle")
        resp = client.post("/estimate", json=body)
        assert resp.status_code == 422

    def test_invalid_project_id_returns_422(self, client):
        body = dict(_VALID_BODY, project_id="not-a-uuid")
        resp = client.post("/estimate", json=body)
        assert resp.status_code == 422


# ---------------------------------------------------------------------------
# Resilience
# ---------------------------------------------------------------------------

class TestEstimateResilience:

    def test_feature_prep_failure_returns_503(self, client):
        """If feature preparation raises, the API must return 503."""
        with patch(_P_DB,   return_value=make_db_mock()), \
             patch(_P_FEAT, side_effect=RuntimeError("DB timeout")):
            resp = client.post("/estimate", json=_VALID_BODY)
        assert resp.status_code == 503

    def test_db_insert_failure_is_non_fatal(self, client):
        """
        If Supabase insert raises (e.g. schema mismatch), the response
        must still return 200 — DB persistence is best-effort.
        """
        failing_db = make_db_mock()
        # Make the chain's execute() raise for insert calls only
        failing_chain = failing_db.table.return_value
        failing_chain.insert.return_value.execute.side_effect = Exception("insert failed")

        import contextlib
        with contextlib.ExitStack() as stack:
            stack.enter_context(patch(_P_DB,      return_value=failing_db))
            stack.enter_context(patch(_P_FEAT,    return_value=FAKE_FEATURES))
            stack.enter_context(patch(_P_PREDICT, return_value=FAKE_PREDICT_RESULT))
            stack.enter_context(patch(_P_SHAP,    return_value=FAKE_SHAP))
            stack.enter_context(patch(_P_LABELS,  return_value=FAKE_SHAP_LABELS))
            stack.enter_context(patch(_P_PROJ,    return_value=FAKE_PROJECTIONS))
            resp = client.post("/estimate", json=_VALID_BODY)

        assert resp.status_code == 200

