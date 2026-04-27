"""
iNHCES O5 Step 4a — MLflow Configuration and Experiment Logger
Provides shared MLflow configuration and a structured logging wrapper
used by both 05_model_benchmarking.py and the Airflow retrain DAG.

Usage:
    from 05_mlflow_config import MLflowLogger
    logger = MLflowLogger()
    with logger.start_run("xgboost") as run:
        logger.log_params({"n_estimators": 100, "max_depth": 2})
        logger.log_metrics({"mape_test": 13.5, "r2_test": 0.91})
        logger.log_model(fitted_model, "xgboost")

Environment variables required (set in Railway + .env.example):
    MLFLOW_TRACKING_URI  — e.g. http://mlflow-service:5000
    MLFLOW_EXPERIMENT    — e.g. nhces_cost_estimation (default)

If MLFLOW_TRACKING_URI is not set, logs to local ./mlruns/ directory.

DATA SOURCE: AMBER — MLflow config. No data.
TETFund NRF 2025 | Department of Quantity Surveying, ABU Zaria
"""

import os
import json
import pickle
import logging
from datetime import date
from contextlib import contextmanager
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

# ── MLflow import (optional — graceful fallback if not installed) ──────────────
try:
    import mlflow
    import mlflow.sklearn
    MLFLOW_AVAILABLE = True
except ImportError:
    MLFLOW_AVAILABLE = False
    logger.warning("mlflow not installed — MLflowLogger will use local JSON fallback")


# ── Configuration ─────────────────────────────────────────────────────────────
MLFLOW_TRACKING_URI  = os.getenv('MLFLOW_TRACKING_URI', './mlruns')
MLFLOW_EXPERIMENT    = os.getenv('MLFLOW_EXPERIMENT',   'nhces_cost_estimation')
MODEL_NAME           = 'nhces_champion'

# Performance thresholds (Delphi Category F targets)
MAPE_TARGET          = 15.0   # %
R2_TARGET            = 0.90
PROMOTION_THRESHOLD  = 0.5    # % MAPE improvement required to promote challenger


class MLflowLogger:
    """
    Wrapper around MLflow tracking. Falls back to local JSON logging
    if MLflow is not available or MLFLOW_TRACKING_URI is unreachable.
    """

    def __init__(self,
                 tracking_uri: str = MLFLOW_TRACKING_URI,
                 experiment:   str = MLFLOW_EXPERIMENT):
        self.tracking_uri = tracking_uri
        self.experiment   = experiment
        self._active_run  = None

        if MLFLOW_AVAILABLE:
            mlflow.set_tracking_uri(tracking_uri)
            mlflow.set_experiment(experiment)
            logger.info(f"MLflow tracking: {tracking_uri} | experiment: {experiment}")
        else:
            logger.warning("MLflow unavailable — using local JSON fallback")

    @contextmanager
    def start_run(self, run_name: str, tags: Optional[Dict] = None):
        """Context manager for a single MLflow run."""
        if MLFLOW_AVAILABLE:
            with mlflow.start_run(run_name=run_name, tags=tags or {}) as run:
                self._active_run = run
                yield run
                self._active_run = None
        else:
            # Local fallback: simulate run with a dict
            class FakeRun:
                info = type('obj', (object,), {
                    'run_id': f"local-{run_name}-{date.today().isoformat()}"
                })()
            fake = FakeRun()
            self._active_run = fake
            yield fake
            self._active_run = None

    def log_params(self, params: Dict[str, Any]):
        if MLFLOW_AVAILABLE and self._active_run:
            mlflow.log_params(params)
        else:
            logger.info(f"[PARAMS] {json.dumps(params, default=str)}")

    def log_metrics(self, metrics: Dict[str, float], step: Optional[int] = None):
        if MLFLOW_AVAILABLE and self._active_run:
            mlflow.log_metrics(metrics, step=step)
        else:
            logger.info(f"[METRICS] {json.dumps(metrics, default=str)}")

    def log_model(self, model: Any, artifact_path: str, registered_name: Optional[str] = None):
        """Log a sklearn-compatible model."""
        if MLFLOW_AVAILABLE and self._active_run:
            mlflow.sklearn.log_model(
                model, artifact_path,
                registered_model_name=registered_name
            )
        else:
            # Save locally as .pkl fallback
            local_dir = os.path.join('./mlruns', artifact_path)
            os.makedirs(local_dir, exist_ok=True)
            pkl_path = os.path.join(local_dir, 'model.pkl')
            with open(pkl_path, 'wb') as f:
                pickle.dump(model, f)
            logger.info(f"[MODEL] Saved locally to {pkl_path}")

    def log_artifact(self, local_path: str):
        if MLFLOW_AVAILABLE and self._active_run:
            mlflow.log_artifact(local_path)
        else:
            logger.info(f"[ARTIFACT] {local_path} (local — not uploaded)")

    def get_production_mape(self) -> Optional[float]:
        """Fetch current Production champion MAPE from MLflow registry."""
        if not MLFLOW_AVAILABLE:
            return None
        try:
            client = mlflow.MlflowClient()
            versions = client.get_latest_versions(MODEL_NAME, stages=["Production"])
            if not versions:
                return None
            run = client.get_run(versions[0].run_id)
            return float(run.data.metrics.get('mape_test', float('inf')))
        except Exception as e:
            logger.warning(f"Could not fetch production MAPE: {e}")
            return None

    def promote_to_staging(self, run_id: str, version: str) -> bool:
        """Transition a model version to Staging."""
        if not MLFLOW_AVAILABLE:
            logger.warning("MLflow not available — cannot promote model")
            return False
        try:
            client = mlflow.MlflowClient()
            client.transition_model_version_stage(
                name=MODEL_NAME, version=version, stage="Staging"
            )
            logger.info(f"Promoted run {run_id} to Staging")
            return True
        except Exception as e:
            logger.error(f"Promotion to Staging failed: {e}")
            return False


# ── Champion promotion decision ────────────────────────────────────────────────
def should_promote(challenger_mape: float, champion_mape: Optional[float]) -> bool:
    """
    Promotion rule: challenger MAPE must be lower than champion by >= threshold.
    If no champion exists (first run), always promote.
    """
    if champion_mape is None:
        return True
    improvement = champion_mape - challenger_mape
    meets = improvement >= PROMOTION_THRESHOLD
    logger.info(
        f"Promotion check: challenger={challenger_mape:.2f}% "
        f"champion={champion_mape:.2f}% "
        f"improvement={improvement:.2f}% "
        f"threshold={PROMOTION_THRESHOLD}% -> {'PROMOTE' if meets else 'KEEP CHAMPION'}"
    )
    return meets


# ── Standard run parameter set for all iNHCES runs ───────────────────────────
def build_run_tags(model_name: str, data_source: str = 'RED-synthetic') -> Dict[str, str]:
    return {
        'project':         'iNHCES',
        'grant':           'TETFund NRF 2025',
        'institution':     'ABU Zaria, Dept. QS',
        'model_name':      model_name,
        'data_source':     data_source,
        'run_date':        date.today().isoformat(),
        'mape_target':     str(MAPE_TARGET),
        'r2_target':       str(R2_TARGET),
    }


if __name__ == "__main__":
    # Quick smoke test
    print("=== MLflow Config Smoke Test ===")
    logger_inst = MLflowLogger()
    with logger_inst.start_run("smoke_test", tags=build_run_tags("ridge")) as run:
        logger_inst.log_params({"alpha": 1.0, "max_iter": 1000})
        logger_inst.log_metrics({"mape_test": 28.5, "r2_test": 0.85, "mae_test": 22000})
    production_mape = logger_inst.get_production_mape()
    print(f"  Current production MAPE: {production_mape}")
    promote = should_promote(challenger_mape=13.5, champion_mape=production_mape)
    print(f"  Would promote 13.5% challenger? {promote}")
    print("[OK] 05_mlflow_config.py ready")
