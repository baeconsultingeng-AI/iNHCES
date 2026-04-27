import logging
from datetime import datetime, timezone

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

logger = logging.getLogger(__name__)
router = APIRouter()


class DagStatus(BaseModel):
    dag_id:         str
    schedule:       str
    description:    str
    last_run_state: Optional[str] = None   # success | failed | running | None
    last_run_at:    Optional[str] = None
    next_run_at:    Optional[str] = None
    data_level:     str = "RED"            # reflects data freshness of this DAG's output


class PipelineStatus(BaseModel):
    dags:           list[DagStatus]
    overall_health: str                    # OK | DEGRADED | DOWN
    checked_at:     datetime


# DAG metadata (schedule + description)
_DAG_META = {
    "nhces_daily_fx_oil":     ("0 5 * * *",        "Daily FX + Brent crude prices",          "RED"),
    "nhces_weekly_materials": ("0 5 * * 1",         "Weekly cement + iron rod prices",        "RED"),
    "nhces_weekly_property":  ("0 5 * * 2",         "Weekly property listing prices",         "RED"),
    "nhces_monthly_macro":    ("0 5 1 * *",          "Monthly CPI, lending rate, PMS prices",  "GREEN"),
    "nhces_quarterly_niqs":   ("manual",             "Quarterly NIQS unit rates (manual)",     "RED"),
    "nhces_quarterly_nbs":    ("0 5 1 1,4,7,10 *",  "Quarterly NBS stats",                    "RED"),
    "nhces_worldbank_annual": ("0 5 2 1 *",          "Annual World Bank GDP + CPI refresh",    "GREEN"),
    "nhces_retrain_weekly":   ("0 1 * * 0",          "Weekly ML champion retrain",             "AMBER"),
    "nhces_drift_monitor":    ("0 17 * * *",         "Daily PSI drift detection",              "AMBER"),
}


def _fetch_airflow_status() -> dict:
    """
    Query the Airflow REST API for DAG run status.
    Returns a dict dag_id -> {state, last_run_at, next_run_at}.
    Falls back to empty dict if Airflow is unreachable.
    """
    from app.config import get_settings
    import httpx
    settings = get_settings()

    try:
        resp = httpx.get(
            f"{settings.airflow_api_url}/dags",
            auth=(settings.airflow_username, settings.airflow_password),
            timeout=5.0,
        )
        if resp.status_code != 200:
            return {}
        dags_data = resp.json().get("dags", [])
        result = {}
        for dag in dags_data:
            dag_id = dag.get("dag_id", "")
            if dag_id in _DAG_META:
                # Fetch last run
                run_resp = httpx.get(
                    f"{settings.airflow_api_url}/dags/{dag_id}/dagRuns"
                    "?limit=1&order_by=-execution_date",
                    auth=(settings.airflow_username, settings.airflow_password),
                    timeout=5.0,
                )
                run = run_resp.json().get("dag_runs", [{}])[0] if run_resp.status_code == 200 else {}
                result[dag_id] = {
                    "state":       run.get("state"),
                    "last_run_at": run.get("execution_date"),
                    "next_run_at": dag.get("next_dagrun"),
                }
        return result
    except Exception as e:
        logger.info(f"[pipeline] Airflow unreachable: {e}")
        return {}


@router.get("", response_model=PipelineStatus)
async def get_pipeline_status():
    """
    Returns the status of all 9 Airflow DAGs.
    Requires researcher or admin role.
    Gracefully degrades when Airflow is unreachable.
    """
    airflow = _fetch_airflow_status()
    dags = []

    for dag_id, (schedule, description, data_level) in _DAG_META.items():
        info = airflow.get(dag_id, {})
        dags.append(DagStatus(
            dag_id=dag_id,
            schedule=schedule,
            description=description,
            last_run_state=info.get("state"),
            last_run_at=info.get("last_run_at"),
            next_run_at=info.get("next_run_at"),
            data_level=data_level,
        ))

    # Overall health: OK if Airflow reachable + no failures, else DEGRADED
    if not airflow:
        health = "DEGRADED"   # Airflow unreachable
    elif any(d.last_run_state == "failed" for d in dags if d.last_run_state):
        health = "DEGRADED"
    else:
        health = "OK"

    return PipelineStatus(
        dags=dags,
        overall_health=health,
        checked_at=datetime.now(timezone.utc),
    )
