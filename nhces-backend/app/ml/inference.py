"""
iNHCES ML Inference Engine
Loads the LightGBM champion model and runs predictions.

Loading priority:
  1. Cloudflare R2 (production — CLOUDFLARE_R2_* env vars set)
  2. Local filesystem (development — 05_ml_models/models/champion_model.pkl)
  3. Synthetic fallback (no model file — returns median training value)

The loaded model is cached at module level and only refreshed when
explicitly called via reload_champion().
"""

import os
import io
import pickle
import logging
from pathlib import Path
from typing import Optional
import numpy as np

logger = logging.getLogger(__name__)

# Module-level cache — populated on first call to get_champion()
_champion_cache: Optional[dict] = None

# Path to locally trained champion (development fallback)
_LOCAL_MODEL_PATH = Path(__file__).parent.parent.parent.parent / \
    "05_ml_models" / "models" / "champion_model.pkl"

# Feature order MUST match the training pipeline (05_feature_engineering.py)
FEATURE_COLS = [
    "d_gdp_growth_pct",
    "d_cpi_annual_pct",
    "d_lending_rate_pct",
    "d_brent_usd_barrel",
    "ret_ngn_usd",
    "ret_ngn_eur",
    "ret_ngn_gbp",
    "lag1_d_gdp_growth_pct",
    "lag1_d_cpi_annual_pct",
    "lag1_d_lending_rate_pct",
    "lag1_d_brent_usd_barrel",
    "lag1_ret_ngn_usd",
    "lag1_ret_ngn_eur",
    "lag1_ret_ngn_gbp",
]

# Champion model MAPE (from O5 benchmarking — used for confidence interval)
CHAMPION_MAPE_PCT = 13.66


def _load_from_r2() -> Optional[dict]:
    """Attempt to download champion model from Cloudflare R2."""
    try:
        import boto3
        from app.config import get_settings
        s = get_settings()
        if not s.r2_configured:
            return None
        client = boto3.client(
            "s3",
            endpoint_url=s.cloudflare_r2_endpoint,
            aws_access_key_id=s.cloudflare_r2_access_key,
            aws_secret_access_key=s.cloudflare_r2_secret_key,
        )
        # Supabase v_champion_model stores the r2_artifact_key
        # For now, use the standard key pattern
        key = "models/champion_model.pkl"
        buf = io.BytesIO()
        client.download_fileobj(s.cloudflare_r2_bucket, key, buf)
        buf.seek(0)
        champion = pickle.load(buf)
        logger.info(f"[inference] Champion loaded from R2: {champion.get('name')}")
        return champion
    except Exception as e:
        logger.warning(f"[inference] R2 load failed ({e}), trying local fallback")
        return None


def _load_from_local() -> Optional[dict]:
    """Load champion model from local filesystem (development)."""
    if not _LOCAL_MODEL_PATH.exists():
        logger.warning(f"[inference] Local model not found at {_LOCAL_MODEL_PATH}")
        return None
    with open(_LOCAL_MODEL_PATH, "rb") as f:
        champion = pickle.load(f)
    logger.info(f"[inference] Champion loaded from local: {champion.get('name')} "
                f"(trained {champion.get('trained_date', 'unknown')})")
    return champion


def load_champion_model() -> dict:
    """
    Load the champion model. Called at FastAPI startup (lifespan).
    Tries R2 first, then local filesystem, then raises RuntimeError.
    """
    global _champion_cache
    champion = _load_from_r2() or _load_from_local()
    if champion is None:
        # Graceful degradation: create a synthetic fallback model
        logger.error("[inference] No champion model found — using SYNTHETIC FALLBACK")
        champion = _make_synthetic_fallback()
    _champion_cache = champion
    return champion


def reload_champion() -> dict:
    """Force reload of champion model (called after promotion)."""
    global _champion_cache
    _champion_cache = None
    return load_champion_model()


def get_champion() -> dict:
    """Return cached champion, loading it if not yet cached."""
    global _champion_cache
    if _champion_cache is None:
        load_champion_model()
    return _champion_cache


def predict(feature_vector: np.ndarray) -> dict:
    """
    Run inference with the champion model.

    Args:
        feature_vector: shape (1, 14) — must match FEATURE_COLS order

    Returns:
        dict with predicted_cost_per_sqm, confidence_lower, confidence_upper,
        model_version, model_name, mape_at_prediction, is_synthetic
    """
    champion = get_champion()
    model = champion.get("model")
    is_synthetic = champion.get("is_synthetic", False)

    if model is None or is_synthetic:
        # Synthetic fallback: return median training cost
        pred = 182_500.0
        logger.warning("[inference] Using SYNTHETIC FALLBACK prediction")
    else:
        try:
            raw = model.predict(feature_vector)
            pred = float(raw[0])
            # Clip to plausible Nigerian housing cost range (NGN/sqm)
            pred = max(50_000.0, min(pred, 1_500_000.0))
        except Exception as e:
            logger.error(f"[inference] Model predict() failed: {e}")
            pred = 182_500.0
            is_synthetic = True

    # Confidence interval: ±MAPE around the point estimate
    mape = champion.get("mape", CHAMPION_MAPE_PCT)
    lower = pred * (1 - mape / 100)
    upper = pred * (1 + mape / 100)

    return {
        "predicted_cost_per_sqm": round(pred, 2),
        "confidence_lower": round(lower, 2),
        "confidence_upper": round(upper, 2),
        "model_name": champion.get("name", "unknown"),
        "model_version": champion.get("trained_date", "unknown"),
        "mape_at_prediction": mape,
        "is_synthetic": is_synthetic,
    }


def _make_synthetic_fallback() -> dict:
    """
    Synthetic fallback when no real champion model is available.
    Returns the O5 median training cost (NGN 140,177/sqm).
    DATA SOURCE: RED — replace with real model before publication.
    """
    return {
        "model": None,
        "name": "synthetic_fallback",
        "trained_date": "N/A",
        "mape": CHAMPION_MAPE_PCT,
        "features": FEATURE_COLS,
        "is_synthetic": True,
    }
