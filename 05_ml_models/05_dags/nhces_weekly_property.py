"""
iNHCES Airflow DAG — nhces_weekly_property
Schedule: Tuesday 05:00 WAT (04:00 UTC)  CRON: 0 4 * * 2

Scrapes residential property listing prices (NGN per sqm) by Nigerian
geopolitical zone from PropertyPro.ng / NigeriaPropertyCentre or synthetic
fallback. Writes to Supabase table: market_prices
DATA SOURCE: RED (synthetic — replace with live scraper when available)
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

# Synthetic property price baselines (NGN/sqm) by zone
PROPERTY_BASE = {
    "North Central": 180_000,
    "North East":    145_000,
    "North West":    155_000,
    "South East":    220_000,
    "South South":   260_000,
    "South West":    310_000,  # Lagos premium
}

DEFAULT_ARGS = {
    "owner": "iNHCES",
    "depends_on_past": False,
    "email_on_failure": True,
    "retries": 1,
    "retry_delay": timedelta(minutes=15),
    "execution_timeout": timedelta(minutes=30),
}


def fetch_property_prices(**ctx):
    """
    Upsert property listing prices (NGN/sqm) per zone.
    DATA SOURCE: RED (synthetic)
    When live scraping is implemented, replace body with scraper call and
    update data_level to AMBER or GREEN accordingly.
    """
    import random
    from supabase import create_client

    supabase = create_client(
        os.environ["SUPABASE_URL"],
        os.environ["SUPABASE_SERVICE_KEY"],
    )
    today = ctx["ds"]
    random.seed(hash(today + "property") % (2 ** 31))

    rows = []
    for zone, base in PROPERTY_BASE.items():
        noise = 1 + random.uniform(-0.03, 0.03)
        rows.append({
            "date": today,
            "zone": zone,
            "price_per_sqm_ngn": round(base * noise, 0),
            "property_type": "residential",
            "data_level": "RED",
            "source": "synthetic",
        })

    supabase.table("market_prices").upsert(
        rows, on_conflict="date,zone,property_type"
    ).execute()
    logger.warning("Property prices upserted (SYNTHETIC RED) for %s", today)


with DAG(
    dag_id="nhces_weekly_property",
    default_args=DEFAULT_ARGS,
    description="Weekly residential property listing prices by Nigerian zone",
    schedule_interval="0 4 * * 2",
    start_date=days_ago(7),
    catchup=False,
    tags=["nhces", "property", "weekly"],
) as dag:
    PythonOperator(task_id="fetch_property_prices", python_callable=fetch_property_prices)
