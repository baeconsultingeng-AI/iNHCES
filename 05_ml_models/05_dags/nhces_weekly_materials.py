"""
iNHCES Airflow DAG — nhces_weekly_materials
Schedule: Monday 05:00 WAT (04:00 UTC)  CRON: 0 4 * * 1

Fetches cement (50kg bag, NGN) and iron rod (12mm, NGN/tonne) prices by
Nigerian geopolitical zone from BNDES / NBS sources or synthetic fallback.
Writes to Supabase table: material_cement, material_ironrod
DATA SOURCE: RED (synthetic — replace with live NBS/BUA/Dangote API when available)
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

ZONES = [
    "North Central", "North East", "North West",
    "South East", "South South", "South West",
]

# Synthetic price baselines per zone (NGN)
CEMENT_BASE = {
    "North Central": 4800, "North East": 5100, "North West": 4900,
    "South East": 5300, "South South": 5400, "South West": 5200,
}
IRONROD_BASE = {  # per tonne
    "North Central": 920_000, "North East": 950_000, "North West": 930_000,
    "South East": 970_000, "South South": 980_000, "South West": 960_000,
}

DEFAULT_ARGS = {
    "owner": "iNHCES",
    "depends_on_past": False,
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=15),
    "execution_timeout": timedelta(minutes=20),
}


def fetch_cement_prices(**ctx):
    """
    Upsert cement prices per zone into material_cement table.
    DATA SOURCE: RED (synthetic)
    Replace with live BUA/Dangote/NBS price scraper when available.
    """
    import os
    import random
    from supabase import create_client

    supabase = create_client(
        os.environ["SUPABASE_URL"],
        os.environ["SUPABASE_SERVICE_KEY"],
    )
    today = ctx["ds"]
    random.seed(hash(today) % (2 ** 31))

    rows = []
    for zone in ZONES:
        # Synthetic: add ±2% weekly noise
        noise = 1 + random.uniform(-0.02, 0.02)
        rows.append({
            "date": today,
            "zone": zone,
            "price_per_bag_ngn": round(CEMENT_BASE[zone] * noise, 0),
            "data_level": "RED",
            "source": "synthetic",
        })

    supabase.table("material_cement").upsert(rows, on_conflict="date,zone").execute()
    logger.warning("Cement prices upserted (SYNTHETIC RED) for %s", today)


def fetch_ironrod_prices(**ctx):
    """
    Upsert iron rod prices per zone into material_ironrod table.
    DATA SOURCE: RED (synthetic)
    """
    import os
    import random
    from supabase import create_client

    supabase = create_client(
        os.environ["SUPABASE_URL"],
        os.environ["SUPABASE_SERVICE_KEY"],
    )
    today = ctx["ds"]
    random.seed(hash(today + "rod") % (2 ** 31))

    rows = []
    for zone in ZONES:
        noise = 1 + random.uniform(-0.015, 0.015)
        rows.append({
            "date": today,
            "zone": zone,
            "price_per_tonne_ngn": round(IRONROD_BASE[zone] * noise, 0),
            "data_level": "RED",
            "source": "synthetic",
        })

    supabase.table("material_ironrod").upsert(rows, on_conflict="date,zone").execute()
    logger.warning("Iron rod prices upserted (SYNTHETIC RED) for %s", today)


with DAG(
    dag_id="nhces_weekly_materials",
    default_args=DEFAULT_ARGS,
    description="Weekly cement + iron rod prices by Nigerian geopolitical zone",
    schedule_interval="0 4 * * 1",
    start_date=days_ago(7),
    catchup=False,
    tags=["nhces", "materials", "weekly"],
) as dag:
    t_cement = PythonOperator(task_id="fetch_cement_prices", python_callable=fetch_cement_prices)
    t_ironrod = PythonOperator(task_id="fetch_ironrod_prices", python_callable=fetch_ironrod_prices)
    [t_cement, t_ironrod]
