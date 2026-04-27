"""
iNHCES Pipeline Monitor Service
Queries the Airflow REST API for DAG status information.
Used by the GET /pipeline endpoint and the frontend PipelineHealth dashboard card.

Falls back gracefully when Airflow is unreachable.
"""

import logging
from typing import Optional
import httpx

logger = logging.getLogger(__name__)

# Cache TTL in seconds — don't hammer Airflow on every dashboard refresh
_CACHE: dict = {}
_CACHE_TTL = 60   # seconds


def _settings():
    from app.config import get_settings
    return get_settings()


def _auth() -> tuple:
    s = _settings()
    return (s.airflow_username, s.airflow_password)


def _base_url() -> str:
    return _settings().airflow_api_url


def get_dag_list() -> list[dict]:
    """
    Fetch all DAGs from the Airflow API.
    Returns a list of dag dicts or [] if unreachable.
    """
    try:
        resp = httpx.get(
            f"{_base_url()}/dags",
            auth=_auth(),
            timeout=5.0,
            headers={"Content-Type": "application/json"},
        )
        resp.raise_for_status()
        return resp.json().get("dags", [])
    except Exception as e:
        logger.info(f"[pipeline_monitor] DAG list unavailable: {e}")
        return []


def get_last_dag_run(dag_id: str) -> Optional[dict]:
    """
    Fetch the most recent run for a given DAG.
    Returns a run dict or None if unavailable.
    """
    try:
        resp = httpx.get(
            f"{_base_url()}/dags/{dag_id}/dagRuns",
            auth=_auth(),
            params={"limit": 1, "order_by": "-execution_date"},
            timeout=5.0,
        )
        resp.raise_for_status()
        runs = resp.json().get("dag_runs", [])
        return runs[0] if runs else None
    except Exception as e:
        logger.info(f"[pipeline_monitor] Run info for {dag_id} unavailable: {e}")
        return None


def get_full_pipeline_status(dag_ids: list[str]) -> dict:
    """
    For each dag_id, fetch the last run state and timestamps.
    Returns a dict: dag_id -> {state, last_run_at, next_run_at}.

    Used by GET /pipeline router. Results are not cached here
    (caching is the router's responsibility).
    """
    dag_list = get_dag_list()
    dag_meta = {d["dag_id"]: d for d in dag_list}

    result = {}
    for dag_id in dag_ids:
        meta = dag_meta.get(dag_id, {})
        run  = get_last_dag_run(dag_id)
        result[dag_id] = {
            "is_paused":   meta.get("is_paused", False),
            "state":       run.get("state") if run else None,
            "last_run_at": run.get("execution_date") if run else None,
            "next_run_at": meta.get("next_dagrun"),
        }

    return result


def trigger_dag(dag_id: str, conf: Optional[dict] = None) -> bool:
    """
    Manually trigger a DAG run via the Airflow REST API.
    Used by the admin dashboard and emergency retrain.
    Returns True on success.
    """
    try:
        resp = httpx.post(
            f"{_base_url()}/dags/{dag_id}/dagRuns",
            auth=_auth(),
            json={"conf": conf or {}},
            timeout=10.0,
        )
        resp.raise_for_status()
        run_id = resp.json().get("dag_run_id", "unknown")
        logger.info(f"[pipeline_monitor] Triggered {dag_id}: run_id={run_id}")
        return True
    except Exception as e:
        logger.error(f"[pipeline_monitor] Failed to trigger {dag_id}: {e}")
        return False


def get_overall_health(statuses: dict) -> str:
    """
    Derive overall pipeline health string from per-DAG statuses.
    Returns 'OK', 'DEGRADED', or 'DOWN'.
    """
    if not statuses:
        return "DOWN"

    states = [v.get("state") for v in statuses.values()]
    if all(s is None for s in states):
        return "DOWN"       # Airflow unreachable
    if any(s == "failed" for s in states if s):
        return "DEGRADED"
    return "OK"
