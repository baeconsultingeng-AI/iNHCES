"""
iNHCES Temporal Cost Projection — Backend Module
Wraps the O5 temporal projection engine for use by the FastAPI /estimate endpoint.

Methodology: Compound Nigerian construction cost inflation (anchored to CPI + FX data)
applied to the current ML model estimate at 3 future horizons (1yr, 3yr, 5yr).

DATA SOURCE: AMBER/RED — inflation rate derived from real World Bank CPI + synthetic FX.
TETFund NRF 2025 | Department of Quantity Surveying, ABU Zaria
"""

import os
import sys
import logging
import importlib.util
import numpy as np
from pathlib import Path

logger = logging.getLogger(__name__)

# Locate O2 and O5 directories relative to backend
_BACKEND  = Path(__file__).parent.parent.parent          # nhces-backend/
_ROOT     = _BACKEND.parent                              # iNHCES/
_O2_PROC  = _ROOT / "02_macro_analysis" / "data" / "processed"
_O5_MDLS  = _ROOT / "05_ml_models" / "models"

HORIZONS = [
    {"key": "current",     "label": "Current",              "years": 0, "h": 0},
    {"key": "short_term",  "label": "Short-term (<1 yr)",   "years": 1, "h": 1},
    {"key": "medium_term", "label": "Medium-term (<3 yrs)", "years": 3, "h": 3},
    {"key": "long_term",   "label": "Long-term (<5 yrs)",   "years": 5, "h": 5},
]

CHAMPION_MAPE = 13.66  # % — from O5 benchmarking


# ── Inflation rate from O2 data ────────────────────────────────────────────────
def _get_annual_inflation_rate() -> float:
    """
    Derive expected annual construction cost inflation from O2 macro data.
    Formula: r = 0.40*CPI + 0.60*FX_depreciation (SHAP-weighted).
    Falls back to 12% if data unavailable.
    """
    try:
        import pandas as pd

        # CPI from World Bank (GREEN data)
        cpi_path = _O2_PROC / "worldbank_nigeria_processed.csv"
        df_cpi   = pd.read_csv(str(cpi_path))
        cpi_col  = next((c for c in ["cpi_inflation_pct", "cpi_annual_pct"]
                         if c in df_cpi.columns), None)
        if cpi_col is None:
            raise ValueError("CPI column not found")
        cpi_avg = float(df_cpi[cpi_col].dropna().tail(5).mean())

        # FX depreciation from CBN/FRED data
        fx_path = _O2_PROC / "cbn_fx_rates_processed.csv"
        df_fx   = pd.read_csv(str(fx_path))
        fx_vals = df_fx["ngn_usd"].dropna().tail(6).values
        if len(fx_vals) >= 2:
            fx_dep = float(np.mean(np.diff(fx_vals) / fx_vals[:-1])) * 100
        else:
            fx_dep = 12.0

        # Weighted: FX dominates (O2 SHAP: NGN/USD 45%, CPI 25.5%)
        r = (0.40 * cpi_avg + 0.60 * max(fx_dep, 0)) / 100
        rate = float(np.clip(r, 0.08, 0.25))   # clip to 8–25% p.a.
        logger.info(f"[temporal] Inflation rate derived: {rate*100:.1f}% p.a. "
                    f"(CPI={cpi_avg:.1f}%, FX dep={fx_dep:.1f}%)")
        return rate

    except Exception as e:
        logger.warning(f"[temporal] Inflation rate fallback (12%): {e}")
        return 0.12


# ── CI computation ─────────────────────────────────────────────────────────────
def _compute_ci(cost: float, h: int) -> tuple:
    """
    Total uncertainty at horizon h.
    σ_total = √(σ_model² + σ_forecast(h)²)
    σ_model = 13.66% (champion MAPE)
    σ_forecast grows with √h
    """
    sigma_model    = CHAMPION_MAPE / 100
    sigma_forecast = (0.06 * np.sqrt(max(h, 1)))   # 6% base spread, grows with √h
    sigma_total    = float(np.sqrt(sigma_model**2 + sigma_forecast**2))

    ci_w  = sigma_total * cost
    lower = max(cost - 1.64 * ci_w, cost * 0.25)
    upper = cost + 1.64 * ci_w
    return round(lower, 2), round(upper, 2), round(sigma_total * 100, 1)


# ── Main projection function ───────────────────────────────────────────────────
def generate_temporal_projections(
    current_cost_per_sqm: float,
    floor_area_sqm:       float,
) -> tuple:
    """
    Generate cost projections at Current, 1yr, 3yr, 5yr horizons.

    Args:
        current_cost_per_sqm : NGN/sqm from champion model
        floor_area_sqm        : building floor area

    Returns:
        (projections: list[dict], annual_inflation_rate: float)
    """
    r = _get_annual_inflation_rate()

    projections = []
    for cfg in HORIZONS:
        h = cfg["h"]

        # Cost at horizon h using compound growth
        cost = round(current_cost_per_sqm * ((1 + r) ** h), 2)

        # Confidence interval (widens with h)
        lower, upper, unc_pct = _compute_ci(cost, h)

        projections.append({
            "horizon_key":       cfg["key"],
            "horizon_label":     cfg["label"],
            "years":             cfg["years"],
            "cost_per_sqm":      cost,
            "total_cost_ngn":    round(cost * floor_area_sqm, 2),
            "confidence_lower":  lower,
            "confidence_upper":  upper,
            "total_lower_ngn":   round(lower * floor_area_sqm, 2),
            "total_upper_ngn":   round(upper * floor_area_sqm, 2),
            "uncertainty_pct":   unc_pct,
            "annual_inflation_r": round(r * 100, 1),
            "is_projection":     h > 0,
        })

    logger.info(
        f"[temporal] Projections: Current={current_cost_per_sqm:,.0f} | "
        f"1yr={projections[1]['cost_per_sqm']:,.0f} | "
        f"3yr={projections[2]['cost_per_sqm']:,.0f} | "
        f"5yr={projections[3]['cost_per_sqm']:,.0f} NGN/sqm"
    )

    return projections, round(r * 100, 1)
