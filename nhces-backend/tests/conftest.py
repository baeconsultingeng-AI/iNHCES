"""
iNHCES Test Configuration
Shared fixtures, mocks, and test data for the nhces-backend test suite.

TETFund NRF 2025 | Department of Quantity Surveying, ABU Zaria
"""

import os

# ---------------------------------------------------------------------------
# Set environment variables BEFORE any app module is imported.
# pydantic-settings gives env vars higher priority than .env files.
# ---------------------------------------------------------------------------
os.environ.setdefault("SUPABASE_URL",         "https://test.supabase.co")
os.environ.setdefault("SUPABASE_ANON_KEY",    "test-anon-key")
os.environ.setdefault("SUPABASE_SERVICE_KEY", "test-service-key")
os.environ.setdefault("SUPABASE_JWT_SECRET",  "test-jwt-secret-32-chars-minimum-abc!")
os.environ.setdefault("ENVIRONMENT",          "test")
os.environ.setdefault("ALLOWED_ORIGINS",      "http://localhost:3000")

import numpy as np
import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient


# ---------------------------------------------------------------------------
# Clear cached settings so test env vars take effect
# ---------------------------------------------------------------------------
from app.config import get_settings
get_settings.cache_clear()


# ---------------------------------------------------------------------------
# Shared fake data constants (used across multiple test modules)
# ---------------------------------------------------------------------------

FAKE_CHAMPION = {
    "name":         "LightGBM",
    "model":        None,         # None triggers synthetic fallback in predict()
    "version":      "1.0.0-test",
    "is_synthetic": True,
    "mape":         13.66,
    "r2":           0.91,
    "trained_date": "2026-01-01",
}

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
               76.51, 72.36, 68.55]]),  # shape (1, 14)
    "RED",                              # freshness
    {"ngn_usd": 1580.0, "cpi": 32.5},  # snapshot
)

FAKE_SHAP = {
    "ret_ngn_usd":      45_000.0,
    "d_cpi_annual_pct": 25_000.0,
    "computed":         True,
}

FAKE_SHAP_LABELS = [
    {"feature": "ret_ngn_usd",      "label": "NGN/USD Return (%)",      "value": 45_000.0},
    {"feature": "d_cpi_annual_pct", "label": "CPI Inflation (change)",  "value": 25_000.0},
]

FAKE_PROJECTIONS = (
    [
        {
            "horizon_key":      "current",
            "horizon_label":    "Current",
            "years":            0,
            "cost_per_sqm":     250_000.0,
            "total_cost_ngn":   30_000_000.0,
            "confidence_lower": 215_000.0,
            "confidence_upper": 285_000.0,
            "total_lower_ngn":  25_800_000.0,
            "total_upper_ngn":  34_200_000.0,
            "uncertainty_pct":  14.0,
            "is_projection":    False,
        },
        {
            "horizon_key":      "short_term",
            "horizon_label":    "Short-term (<1 yr)",
            "years":            1,
            "cost_per_sqm":     312_500.0,
            "total_cost_ngn":   37_500_000.0,
            "confidence_lower": 265_625.0,
            "confidence_upper": 362_500.0,
            "total_lower_ngn":  31_875_000.0,
            "total_upper_ngn":  43_500_000.0,
            "uncertainty_pct":  19.5,
            "is_projection":    True,
        },
        {
            "horizon_key":      "medium_term",
            "horizon_label":    "Medium-term (<3 yrs)",
            "years":            3,
            "cost_per_sqm":     488_281.0,
            "total_cost_ngn":   58_593_750.0,
            "confidence_lower": 390_625.0,
            "confidence_upper": 585_937.0,
            "total_lower_ngn":  46_875_000.0,
            "total_upper_ngn":  70_312_500.0,
            "uncertainty_pct":  30.0,
            "is_projection":    True,
        },
        {
            "horizon_key":      "long_term",
            "horizon_label":    "Long-term (<5 yrs)",
            "years":            5,
            "cost_per_sqm":     763_000.0,
            "total_cost_ngn":   91_562_500.0,
            "confidence_lower": 572_250.0,
            "confidence_upper": 953_750.0,
            "total_lower_ngn":  68_671_875.0,
            "total_upper_ngn":  114_453_125.0,
            "uncertainty_pct":  50.0,
            "is_projection":    True,
        },
    ],
    0.25,   # annual_inflation_rate
)


# ---------------------------------------------------------------------------
# DB mock factory
# ---------------------------------------------------------------------------

def make_db_mock(data=None, count=0):
    """
    Build a MagicMock supabase-py client.

    Any chain of .table(X).select(Y).eq(...).order(...).limit(N).execute()
    resolves to MagicMock(data=<data>, count=<count>).
    """
    execute_result = MagicMock(data=data if data is not None else [], count=count)
    chain = MagicMock()
    chain.execute.return_value = execute_result
    for method in (
        "select", "insert", "update", "upsert", "delete",
        "eq", "neq", "gt", "gte", "lt", "lte",
        "order", "limit", "range", "single",
    ):
        getattr(chain, method).return_value = chain
    db = MagicMock()
    db.table.return_value = chain
    return db


# ---------------------------------------------------------------------------
# Session-scoped: pre-load fake champion model to skip filesystem / R2 I/O
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session", autouse=True)
def _pre_load_champion():
    import app.ml.inference as inf
    original = inf._champion_cache
    inf._champion_cache = FAKE_CHAMPION
    yield
    inf._champion_cache = original


# ---------------------------------------------------------------------------
# Session-scoped: create the TestClient once for the whole session
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def _patched_app():
    """
    Import the FastAPI app with model-loading mocked.
    The Supabase client is NOT initialised (mocked per-test via get_db patches).
    """
    with patch("app.ml.inference.load_champion_model"):
        with patch("app.database.get_db", return_value=make_db_mock()):
            # Import app after patching so lifespan uses the mock
            from app.main import app as _app
            yield _app


@pytest.fixture(scope="session")
def client(_patched_app):
    """Unauthenticated TestClient — reused across the session."""
    with TestClient(_patched_app, raise_server_exceptions=False) as c:
        yield c


# ---------------------------------------------------------------------------
# Function-scoped: authenticated client
# ---------------------------------------------------------------------------

@pytest.fixture
def authed_client(_patched_app):
    """
    TestClient with both `get_current_user` and `get_optional_user`
    overridden to return a synthetic QS Professional user.
    Dependency overrides are cleared after each test.
    """
    from app.auth import get_current_user, get_optional_user, CurrentUser

    def _fake_user():
        return CurrentUser(
            user_id="test-user-abc-123",
            email="test@example.com",
            role="qsprofessional",
        )

    _patched_app.dependency_overrides[get_current_user] = _fake_user
    _patched_app.dependency_overrides[get_optional_user] = _fake_user

    with TestClient(_patched_app, raise_server_exceptions=False) as c:
        yield c

    _patched_app.dependency_overrides.clear()
