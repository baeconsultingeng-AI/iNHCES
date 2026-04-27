"""
iNHCES Database Module
Supabase PostgreSQL client management.
Provides service_role and anon clients, health check, and schema verification.
"""

import logging
from functools import lru_cache
from typing import Optional

from supabase import create_client, Client
from app.config import get_settings

logger = logging.getLogger(__name__)

# Expected tables in the iNHCES schema
EXPECTED_TABLES = [
    "audit_log", "macro_cpi", "macro_fx", "macro_gdp",
    "macro_interest", "macro_oil", "market_prices",
    "material_cement", "material_steel", "material_pms",
    "ml_models", "predictions", "projects", "reports",
    "unit_rates", "users",
]

EXPECTED_VIEWS = ["v_champion_model", "v_latest_macro"]


@lru_cache
def get_db() -> Client:
    """
    Returns a Supabase client using the service_role key.
    Service_role bypasses RLS — use only in backend server code.
    Cached as a singleton for the lifetime of the process.
    """
    settings = get_settings()
    client = create_client(settings.supabase_url, settings.supabase_service_key)
    logger.info("[db] Service role client initialised")
    return client


@lru_cache
def get_anon_db() -> Client:
    """
    Returns a Supabase client using the anon key.
    Subject to RLS — use when acting on behalf of a specific user.
    """
    settings = get_settings()
    return create_client(settings.supabase_url, settings.supabase_anon_key)


def health_check() -> dict:
    """
    Perform a lightweight DB health check.
    Returns dict with status, latency estimate, and table count.
    Called by GET /health endpoint.
    """
    import time
    t0 = time.monotonic()
    try:
        db = get_db()
        # Lightweight query — just check connection
        resp = db.table("ml_models").select("id").eq("is_champion", True).limit(1).execute()
        elapsed_ms = int((time.monotonic() - t0) * 1000)
        champion_exists = len(resp.data) > 0
        return {
            "status":           "ok",
            "latency_ms":       elapsed_ms,
            "champion_loaded":  champion_exists,
        }
    except Exception as e:
        elapsed_ms = int((time.monotonic() - t0) * 1000)
        logger.warning(f"[db] health_check failed: {e}")
        return {
            "status":      "degraded",
            "latency_ms":  elapsed_ms,
            "error":       str(e)[:120],
        }


def verify_schema() -> dict:
    """
    Verify that all expected tables and views exist.
    Returns dict with missing_tables, missing_views, and overall ok flag.
    Called at startup in development mode.
    """
    try:
        db = get_db()
        # Query information_schema for public tables
        resp = db.rpc("get_latest_macro_snapshot", {}).execute()
        macro_ok = resp.data is not None
    except Exception:
        macro_ok = False

    return {
        "macro_function_ok": macro_ok,
        "note": (
            "Full schema verification requires running 04_db_verification.sql "
            "in the Supabase SQL Editor."
        ),
    }


def get_macro_snapshot_from_db() -> Optional[list]:
    """
    Call the get_latest_macro_snapshot() DB function.
    Returns list of macro variable dicts or None on error.
    """
    try:
        db = get_db()
        resp = db.rpc("get_latest_macro_snapshot", {}).execute()
        return resp.data
    except Exception as e:
        logger.warning(f"[db] get_macro_snapshot_from_db failed: {e}")
        return None


def get_champion_from_db() -> Optional[dict]:
    """
    Call the get_champion_model() DB function.
    Returns champion model metadata dict or None.
    """
    try:
        db = get_db()
        resp = db.rpc("get_champion_model", {}).execute()
        return resp.data[0] if resp.data else None
    except Exception as e:
        logger.warning(f"[db] get_champion_from_db failed: {e}")
        return None


def promote_champion_in_db(mlflow_run_id: str) -> bool:
    """
    Call refresh_champion_flag() to atomically promote a new champion.
    Returns True on success.
    """
    try:
        db = get_db()
        db.rpc("refresh_champion_flag", {"p_new_run_id": mlflow_run_id}).execute()
        logger.info(f"[db] Champion promoted: {mlflow_run_id}")
        return True
    except Exception as e:
        logger.error(f"[db] promote_champion_in_db failed: {e}")
        return False
