"""
iNHCES Airflow DAG — nhces_daily_fx_oil
Schedule: 05:00 WAT daily (04:00 UTC)  CRON: 0 4 * * *

Fetches NGN/USD, NGN/EUR, NGN/GBP exchange rates and Brent crude spot price.
Writes to Supabase tables: macro_fx, macro_oil
DATA SOURCE: RED (synthetic fallback until live API keys are configured)
TETFund NRF 2025 | Department of Quantity Surveying, ABU Zaria
"""

import os
import logging
from datetime import datetime, timedelta

try:
    from airflow import DAG
    from airflow.operators.python import PythonOperator
    from airflow.utils.dates import days_ago
    AIRFLOW_AVAILABLE = True
except ImportError:
    AIRFLOW_AVAILABLE = False
    class DAG:
        def __init__(self, *a, **kw): pass
        def __enter__(self): return self
        def __exit__(self, *a): pass
    class PythonOperator:
        def __init__(self, *a, **kw): pass
    days_ago = lambda n: datetime.utcnow() - timedelta(days=n)

logger = logging.getLogger(__name__)

DEFAULT_ARGS = {
    "owner": "iNHCES",
    "depends_on_past": False,
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=10),
    "execution_timeout": timedelta(minutes=15),
}


def fetch_fx(**ctx):
    """
    Fetch NGN/USD, NGN/EUR, NGN/GBP from CBN or FRED API.
    Falls back to synthetic data when FRED_API_KEY is not set.
    Upserts into Supabase macro_fx table.
    """
    import os
    import json
    from supabase import create_client

    supabase = create_client(
        os.environ["SUPABASE_URL"],
        os.environ["SUPABASE_SERVICE_KEY"],
    )
    fred_key = os.environ.get("FRED_API_KEY", "")
    today = ctx["ds"]  # execution date YYYY-MM-DD

    if fred_key:
        # Live path — fetch from FRED
        import httpx
        series = {
            "ngn_usd": "DEXNAUS",
            "ngn_eur": "DEXUSEU",  # USD/EUR — convert below
            "ngn_gbp": "DEXUSUK",
        }
        rows = []
        for var, sid in series.items():
            url = (
                f"https://api.stlouisfed.org/fred/series/observations"
                f"?series_id={sid}&api_key={fred_key}&file_type=json"
                f"&observation_start={today}&observation_end={today}&limit=1"
            )
            resp = httpx.get(url, timeout=15)
            resp.raise_for_status()
            obs = resp.json().get("observations", [])
            if obs and obs[0]["value"] != ".":
                rows.append({"date": today, "variable": var, "value": float(obs[0]["value"])})
        is_synthetic = False
    else:
        # Synthetic fallback
        rows = [
            {"date": today, "variable": "ngn_usd", "value": 1580.0},
            {"date": today, "variable": "ngn_eur", "value": 1720.0},
            {"date": today, "variable": "ngn_gbp", "value": 2010.0},
        ]
        is_synthetic = True
        logger.warning("FRED_API_KEY not set — using synthetic FX data (RED)")

    for row in rows:
        row["data_level"] = "RED" if is_synthetic else "GREEN"
        row["source"] = "synthetic" if is_synthetic else "FRED/CBN"

    if rows:
        supabase.table("macro_fx").upsert(rows, on_conflict="date,variable").execute()
        logger.info("FX upserted %d rows for %s", len(rows), today)


def fetch_oil(**ctx):
    """
    Fetch Brent crude spot price from EIA or FRED API.
    Falls back to synthetic data when EIA_API_KEY is not set.
    Upserts into Supabase macro_oil table.
    """
    import os
    import httpx
    from supabase import create_client

    supabase = create_client(
        os.environ["SUPABASE_URL"],
        os.environ["SUPABASE_SERVICE_KEY"],
    )
    eia_key = os.environ.get("EIA_API_KEY", "")
    today = ctx["ds"]

    if eia_key:
        url = (
            f"https://api.eia.gov/v2/petroleum/pri/spt/data/"
            f"?api_key={eia_key}&frequency=daily&data[0]=value"
            f"&facets[product][]=EPCBRENT&start={today}&end={today}&length=1"
        )
        resp = httpx.get(url, timeout=15)
        resp.raise_for_status()
        data = resp.json().get("response", {}).get("data", [])
        value = float(data[0]["value"]) if data else 80.0
        is_synthetic = not bool(data)
    else:
        value = 80.0
        is_synthetic = True
        logger.warning("EIA_API_KEY not set — using synthetic Brent data (RED)")

    row = {
        "date": today,
        "variable": "brent_usd_barrel",
        "value": value,
        "data_level": "RED" if is_synthetic else "GREEN",
        "source": "synthetic" if is_synthetic else "EIA",
    }
    supabase.table("macro_oil").upsert([row], on_conflict="date,variable").execute()
    logger.info("Oil upserted for %s: %.2f USD/barrel", today, value)


with DAG(
    dag_id="nhces_daily_fx_oil",
    default_args=DEFAULT_ARGS,
    description="Daily FX rates (NGN/USD, NGN/EUR, NGN/GBP) + Brent crude price",
    schedule_interval="0 4 * * *",
    start_date=days_ago(1),
    catchup=False,
    tags=["nhces", "macro", "daily"],
) as dag:
    t_fx = PythonOperator(task_id="fetch_fx", python_callable=fetch_fx)
    t_oil = PythonOperator(task_id="fetch_oil", python_callable=fetch_oil)

    # Run independently — both write to different tables
    [t_fx, t_oil]
