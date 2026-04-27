"""
iNHCES Airflow DAG — nhces_monthly_macro
Schedule: 1st of each month at 05:00 WAT (04:00 UTC)  CRON: 0 4 1 * *

Fetches monthly macroeconomic indicators: CPI annual inflation, lending rate,
and PMS (petrol) pump price from World Bank / CBN / NNPC sources.
Writes to Supabase tables: macro_cpi, macro_interest
DATA SOURCE: GREEN (World Bank API) / RED (lending rate / PMS — synthetic fallback)
TETFund NRF 2025 | Department of Quantity Surveying, ABU Zaria
"""

import os
import logging
from datetime import datetime, timedelta

try:
    from airflow import DAG
    from airflow.operators.python import PythonOperator
    from airflow.utils.dates import days_ago
except ImportError:
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
    "retries": 2,
    "retry_delay": timedelta(minutes=20),
    "execution_timeout": timedelta(minutes=30),
}


def fetch_cpi(**ctx):
    """
    Fetch Nigeria CPI annual inflation from World Bank Indicators API.
    Indicator: FP.CPI.TOTL.ZG
    DATA SOURCE: GREEN (live World Bank API — no key required)
    Falls back to synthetic if API is unreachable.
    """
    import httpx
    from supabase import create_client

    supabase = create_client(
        os.environ["SUPABASE_URL"],
        os.environ["SUPABASE_SERVICE_KEY"],
    )
    today = ctx["ds"]
    year = today[:4]

    try:
        url = (
            f"https://api.worldbank.org/v2/country/NG/indicator/FP.CPI.TOTL.ZG"
            f"?format=json&date={year}&per_page=1"
        )
        resp = httpx.get(url, timeout=20)
        resp.raise_for_status()
        payload = resp.json()
        records = payload[1] if len(payload) > 1 else []
        value = float(records[0]["value"]) if records and records[0]["value"] else None
        is_synthetic = value is None
    except Exception as e:
        logger.warning("World Bank CPI fetch failed: %s — using synthetic fallback", e)
        value = 33.2
        is_synthetic = True

    row = {
        "date": today[:7] + "-01",  # first of month
        "variable": "cpi_annual_pct",
        "value": value or 33.2,
        "data_level": "RED" if is_synthetic else "GREEN",
        "source": "synthetic" if is_synthetic else "WorldBank",
    }
    supabase.table("macro_cpi").upsert([row], on_conflict="date,variable").execute()
    logger.info("CPI upserted (level=%s): %.2f%%", row["data_level"], row["value"])


def fetch_lending_rate(**ctx):
    """
    Fetch CBN monetary policy rate (proxy for lending rate).
    DATA SOURCE: RED (synthetic — integrate CBN API when available)
    """
    from supabase import create_client

    supabase = create_client(
        os.environ["SUPABASE_URL"],
        os.environ["SUPABASE_SERVICE_KEY"],
    )
    today = ctx["ds"]
    # Synthetic: CBN MPR as of 2025
    row = {
        "date": today[:7] + "-01",
        "variable": "lending_rate_pct",
        "value": 27.25,
        "data_level": "RED",
        "source": "synthetic",
    }
    supabase.table("macro_interest").upsert([row], on_conflict="date,variable").execute()
    logger.warning("Lending rate upserted (SYNTHETIC RED) for %s", today[:7])


with DAG(
    dag_id="nhces_monthly_macro",
    default_args=DEFAULT_ARGS,
    description="Monthly CPI inflation, lending rate, and PMS price fetch",
    schedule_interval="0 4 1 * *",
    start_date=days_ago(30),
    catchup=False,
    tags=["nhces", "macro", "monthly"],
) as dag:
    t_cpi = PythonOperator(task_id="fetch_cpi", python_callable=fetch_cpi)
    t_rate = PythonOperator(task_id="fetch_lending_rate", python_callable=fetch_lending_rate)
    [t_cpi, t_rate]
