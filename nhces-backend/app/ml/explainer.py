"""
iNHCES SHAP Explainer
Computes per-feature SHAP values for a single /estimate prediction.
Uses TreeExplainer for LightGBM (fast, exact).
Falls back to uniform distribution if SHAP computation fails.
"""

import logging
import numpy as np
from typing import Optional

from app.ml.inference import FEATURE_COLS, get_champion

logger = logging.getLogger(__name__)

# Human-readable labels for each feature (shown in UI)
FEATURE_LABELS = {
    "d_gdp_growth_pct":        "GDP Growth (change)",
    "d_cpi_annual_pct":        "CPI Inflation (change)",
    "d_lending_rate_pct":      "Lending Rate (change)",
    "d_brent_usd_barrel":      "Brent Crude (change, USD)",
    "ret_ngn_usd":             "NGN/USD Return (%)",
    "ret_ngn_eur":             "NGN/EUR Return (%)",
    "ret_ngn_gbp":             "NGN/GBP Return (%)",
    "lag1_d_gdp_growth_pct":   "GDP Growth (lag-1)",
    "lag1_d_cpi_annual_pct":   "CPI Inflation (lag-1)",
    "lag1_d_lending_rate_pct": "Lending Rate (lag-1)",
    "lag1_d_brent_usd_barrel": "Brent Crude (lag-1)",
    "lag1_ret_ngn_usd":        "NGN/USD Return (lag-1)",
    "lag1_ret_ngn_eur":        "NGN/EUR Return (lag-1)",
    "lag1_ret_ngn_gbp":        "NGN/GBP Return (lag-1)",
}


def compute_shap(X: np.ndarray, top_n: int = 7) -> dict:
    """
    Compute SHAP values for the feature vector X.

    Args:
        X     : np.ndarray shape (1, 14)
        top_n : number of top features to return

    Returns:
        dict mapping feature_name -> shap_value (NGN/sqm contribution).
        Only the top_n features by |SHAP| are returned.
        Includes 'computed': True/False flag.
    """
    champion = get_champion()
    model = champion.get("model")

    if model is None or champion.get("is_synthetic", False):
        return _uniform_fallback(X, top_n)

    try:
        import shap
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X)  # shape (1, 14)
        values = shap_values[0]  # shape (14,)

        # Pick top_n by absolute value
        indices = np.argsort(np.abs(values))[::-1][:top_n]
        result = {
            FEATURE_COLS[i]: round(float(values[i]), 2)
            for i in indices
        }
        result["computed"] = True
        return result

    except Exception as e:
        logger.warning(f"[explainer] SHAP failed ({e}), using uniform fallback")
        return _uniform_fallback(X, top_n)


def get_shap_labels(shap_dict: dict) -> list:
    """
    Convert raw SHAP dict to a sorted list of {feature, label, value}
    for the frontend ShapChart component.
    """
    items = [
        {
            "feature": k,
            "label": FEATURE_LABELS.get(k, k),
            "value": v,
        }
        for k, v in shap_dict.items()
        if k != "computed" and isinstance(v, (int, float))
    ]
    # Sort by absolute value descending
    items.sort(key=lambda x: abs(x["value"]), reverse=True)
    return items


def _uniform_fallback(X: np.ndarray, top_n: int) -> dict:
    """
    When SHAP cannot be computed, distribute the predicted value
    proportionally using the O5 importance rankings as priors.
    DATA SOURCE: RED — replace with real SHAP when model is retrained on real data.
    """
    # O5 SHAP importance priors (synthetic proxy rankings)
    priors = {
        "ret_ngn_usd":            45.0,
        "d_cpi_annual_pct":       25.5,
        "ret_ngn_eur":            11.6,
        "d_brent_usd_barrel":     10.9,
        "ret_ngn_gbp":             3.8,
        "d_gdp_growth_pct":        2.1,
        "d_lending_rate_pct":      1.1,
    }
    # Approximate magnitude from prediction midpoint
    pred = float(X[0].sum())  # rough proxy — replace with real SHAP
    result = {
        feat: round(pred * pct / 100, 2)
        for feat, pct in list(priors.items())[:top_n]
    }
    result["computed"] = False
    return result
