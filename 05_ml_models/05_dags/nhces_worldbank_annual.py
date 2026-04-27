"""
iNHCES Airflow DAG — nhces_worldbank_annual
Schedule: 2nd January each year at 05:00 WAT (04:00 UTC)  CRON: 0 4 2 1 *

Refreshes annual World Bank data: Nigeria GDP growth and historical CPI series.
This performs a bulk back-fill covering the last 30 years to catch any
World Bank revisions to historical series.
Writes to Supabase tables: macro_gdp, macro_cpi (historical bulk upsert)
DATA SOURCE: GREEN (live World Bank API)
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
    "retries": 3,
    "retry_delay": timedelta(minutes=30),
    "execution_timeout": timedelta(minutes=60),
}

WB_INDICATORS = {
    "gdp_growth_pct": ("NY.GDP.MKTP.KD.ZG", "macro_gdp"),
    "cpi_annual_pct": ("FP.CPI.TOTL.ZG",   "macro_cpi"),
}


def fetch_worldbank_series(indicator_key: str, **ctx):
    """
    Bulk-fetch 30 years of World Bank data for one indicator.
    DATA SOURCE: GREEN
    """
    import httpx
    from supabase import create_client

    supabase = create_client(
        os.environ["SUPABASE_URL"],
        os.environ["SUPABASE_SERVICE_KEY"],
    )
    wb_code, table = WB_INDICATORS[indicator_key]
    current_year = int(ctx["ds"][:4])
    start_year = current_year - 30

    url = (
        f"https://api.worldbank.org/v2/country/NG/indicator/{wb_code}"
        f"?format=json&date={start_year}:{current_year}&per_page=50"
    )
    resp = httpx.get(url, timeout=30)
    resp.raise_for_status()
    payload = resp.json()
    records = payload[1] if len(payload) > 1 else []

    rows = []
    for rec in records:
        if rec.get("value") is None:
            continue
        rows.append({
            "date": f"{rec['date']}-01-01",
            "variable": indicator_key,
            "value": float(rec["value"]),
            "data_level": "GREEN",
            "source": "WorldBank",
        })

    if rows:
        supabase.table(table).upsert(rows, on_conflict="date,variable").execute()
        logger.info("WorldBank %s: upserted %d rows (%s..%s)", indicator_key, len(rows), start_year, current_year)
    else:
        logger.warning("WorldBank %s: no data returned", indicator_key)


with DAG(
    dag_id="nhces_worldbank_annual",
    default_args=DEFAULT_ARGS,
    description="Annual World Bank GDP growth + CPI historical bulk refresh",
    schedule_interval="0 4 2 1 *",
    start_date=days_ago(365),
    catchup=False,
    tags=["nhces", "macro", "annual", "worldbank"],
) as dag:
    from functools import partial

    for key in WB_INDICATORS:
        PythonOperator(
            task_id=f"fetch_{key}",
            python_callable=fetch_worldbank_series,
            op_kwargs={"indicator_key": key},
        )
