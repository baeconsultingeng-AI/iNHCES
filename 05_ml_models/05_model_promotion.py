"""
iNHCES O5 Step 4b — Model Promotion Script
Compares the latest challenger model (from the most recent retrain run)
against the current Production champion. Promotes if MAPE improvement
meets the threshold (>= 0.5 percentage points).

Called by:
  - nhces_retrain_weekly Airflow DAG (Task 5: promote)
  - Admin dashboard "Promote Challenger" button (via FastAPI /pipeline endpoint)

Updates:
  - MLflow model registry stage (Staging -> Production)
  - Supabase ml_models table (is_champion flag)
  - audit_log entry

DATA SOURCE: AMBER — MLflow + Supabase integration code. No data.
TETFund NRF 2025 | Department of Quantity Surveying, ABU Zaria
"""

import os
import json
import logging
from datetime import date
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

# ── Optional Supabase client ──────────────────────────────────────────────────
try:
    from supabase import create_client, Client
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_KEY')
    supabase: Optional[Client] = create_client(SUPABASE_URL, SUPABASE_KEY) \
        if SUPABASE_URL and SUPABASE_KEY else None
    SUPABASE_AVAILABLE = supabase is not None
except ImportError:
    supabase = None
    SUPABASE_AVAILABLE = False
    logger.warning("supabase-py not installed — DB promotion steps will be skipped")

from os.path import dirname, abspath
_HERE = dirname(abspath(__file__))
_ROOT = dirname(_HERE)

import sys
sys.path.insert(0, _HERE)
from os_mlflow_config_import_shim import MLflowLogger, should_promote, build_run_tags, MODEL_NAME

# Re-import directly to avoid naming issue
try:
    from importlib import import_module
    _mod = import_module('05_mlflow_config')
    MLflowLogger   = _mod.MLflowLogger
    should_promote = _mod.should_promote
    build_run_tags = _mod.build_run_tags
    MODEL_NAME     = _mod.MODEL_NAME
except Exception:
    pass  # fall through to inline definitions below


# ── Promotion workflow ────────────────────────────────────────────────────────

class ModelPromoter:
    """
    Orchestrates the champion-challenger promotion decision.
    Used by the Airflow retrain DAG and the admin API endpoint.
    """

    def __init__(self):
        self.mlflow_logger = MLflowLogger()

    def get_staging_model(self) -> Optional[Dict[str, Any]]:
        """
        Fetch the most recent Staging model from MLflow registry.
        Returns dict with run_id, version, mape_test.
        """
        try:
            import mlflow
            client = mlflow.MlflowClient()
            staging = client.get_latest_versions(MODEL_NAME, stages=["Staging"])
            if not staging:
                logger.info("No Staging model found.")
                return None
            v = staging[0]
            run = client.get_run(v.run_id)
            return {
                'run_id':    v.run_id,
                'version':   v.version,
                'mape_test': float(run.data.metrics.get('mape_test', float('inf'))),
                'r2_test':   float(run.data.metrics.get('r2_test', 0.0)),
                'model_name': run.data.tags.get('model_name', 'unknown'),
            }
        except Exception as e:
            logger.error(f"Failed to fetch Staging model: {e}")
            return None

    def get_production_model(self) -> Optional[Dict[str, Any]]:
        """Fetch the current Production champion from MLflow registry."""
        try:
            import mlflow
            client = mlflow.MlflowClient()
            prod = client.get_latest_versions(MODEL_NAME, stages=["Production"])
            if not prod:
                return None
            v = prod[0]
            run = client.get_run(v.run_id)
            return {
                'run_id':    v.run_id,
                'version':   v.version,
                'mape_test': float(run.data.metrics.get('mape_test', float('inf'))),
                'r2_test':   float(run.data.metrics.get('r2_test', 0.0)),
            }
        except Exception as e:
            logger.error(f"Failed to fetch Production model: {e}")
            return None

    def promote_challenger(self, staging: Dict, champion_mape: Optional[float],
                           promoted_by: Optional[str] = None) -> bool:
        """
        Promote staging model to Production if it meets the promotion threshold.
        Returns True if promotion occurred.
        """
        if not should_promote(staging['mape_test'], champion_mape):
            logger.info(
                f"Challenger MAPE {staging['mape_test']:.2f}% does not improve "
                f"champion {champion_mape:.2f}% by >= 0.5%. Keeping current champion."
            )
            return False

        logger.info(
            f"PROMOTING challenger {staging['run_id']} "
            f"(MAPE={staging['mape_test']:.2f}%) to Production "
            f"(was {champion_mape:.2f}%)"
        )

        # Step 1: Transition in MLflow registry
        try:
            import mlflow
            client = mlflow.MlflowClient()
            client.transition_model_version_stage(
                name=MODEL_NAME, version=staging['version'], stage="Production"
            )
            logger.info(f"MLflow: version {staging['version']} -> Production")
        except Exception as e:
            logger.error(f"MLflow promotion failed: {e}")
            return False

        # Step 2: Update Supabase ml_models table
        if SUPABASE_AVAILABLE:
            self._update_supabase(staging, promoted_by)

        # Step 3: Log to audit_log
        self._log_audit(staging, champion_mape, promoted_by)

        return True

    def _update_supabase(self, staging: Dict, promoted_by: Optional[str]):
        """Set is_champion=False for old champion, True for new one in Supabase."""
        try:
            # Demote old champion
            supabase.table('ml_models') \
                .update({'is_champion': False, 'stage': 'Archived'}) \
                .eq('is_champion', True) \
                .execute()
            # Promote new champion
            supabase.table('ml_models') \
                .update({
                    'is_champion': True,
                    'stage': 'Production',
                    'promoted_by': promoted_by,
                    'promoted_at': date.today().isoformat(),
                }) \
                .eq('mlflow_run_id', staging['run_id']) \
                .execute()
            logger.info(f"Supabase ml_models updated: champion = {staging['run_id']}")
        except Exception as e:
            logger.error(f"Supabase update failed: {e}")

    def _log_audit(self, staging: Dict, old_mape: Optional[float], user_id: Optional[str]):
        """Append promotion event to audit_log."""
        entry = {
            'action':    'promote_model',
            'table_name':'ml_models',
            'record_id': staging['run_id'],
            'new_values': json.dumps({
                'run_id':       staging['run_id'],
                'mape_test':    staging['mape_test'],
                'old_mape':     old_mape,
                'promoted_by':  user_id or 'airflow_dag',
                'promoted_at':  date.today().isoformat(),
            }),
        }
        if user_id:
            entry['user_id'] = user_id

        if SUPABASE_AVAILABLE:
            try:
                supabase.table('audit_log').insert(entry).execute()
                logger.info("Promotion event logged to audit_log")
            except Exception as e:
                logger.error(f"audit_log insert failed: {e}")
        else:
            logger.info(f"[AUDIT] {json.dumps(entry, default=str)}")

    def run(self, promoted_by: Optional[str] = None) -> bool:
        """Full promotion workflow: check -> decide -> promote -> audit."""
        staging   = self.get_staging_model()
        if not staging:
            logger.info("No Staging model to evaluate.")
            return False
        champion  = self.get_production_model()
        champ_mape = champion['mape_test'] if champion else None
        return self.promote_challenger(staging, champ_mape, promoted_by)


# ── CLI entry point ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="iNHCES Model Promotion")
    parser.add_argument('--user', default=None, help="User ID or name triggering promotion")
    parser.add_argument('--force', action='store_true',
                        help="Force promotion regardless of MAPE threshold (admin override)")
    args = parser.parse_args()

    print("=== iNHCES Model Promotion ===")
    promoter = ModelPromoter()

    if args.force:
        staging = promoter.get_staging_model()
        if staging:
            print(f"FORCE PROMOTION: {staging['run_id']} (MAPE={staging['mape_test']:.2f}%)")
            promoter.promote_challenger(staging, champion_mape=float('inf'),
                                        promoted_by=args.user or 'admin-force')
        else:
            print("No Staging model found to force-promote.")
    else:
        result = promoter.run(promoted_by=args.user)
        print(f"Promotion result: {'PROMOTED' if result else 'NO CHANGE'}")

    print("[OK] 05_model_promotion.py complete")
