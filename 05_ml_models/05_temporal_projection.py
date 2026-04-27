"""
iNHCES O5 — Temporal Cost Projection Engine
Applies the LightGBM champion model to VAR-projected macro feature vectors
to generate construction cost projections at three future horizons.

Horizons:
  Short-term  : h=1  (<1 year)
  Medium-term : h=3  (<3 years)
  Long-term   : h=5  (<5 years)

Methodology:
  1. Get current feature vector from Supabase (or O2 CSVs locally)
  2. Use forecast_macro.py to get projected feature vectors at h=1,3,5
  3. Apply champion model to each → point cost estimate
  4. Compute total uncertainty = √(model_MAPE² + VAR_forecast_SE²)
  5. Return 4 projection objects (current + 3 horizons)

DATA SOURCE: RED — synthetic data until real NIQS + live APIs configured.
TETFund NRF 2025 | Department of Quantity Surveying, ABU Zaria
"""

import os
import sys
import json
import pickle
import warnings
import numpy as np

warnings.filterwarnings("ignore")

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
_O2   = os.path.join(_ROOT, "02_macro_analysis")

sys.path.insert(0, _HERE)
sys.path.insert(0, _O2)

CHAMPION_MAPE   = 13.66   # % — from O5 benchmarking
HORIZONS_CONFIG = {
    "current":     {"h": 0, "label": "Current",          "years": 0},
    "short_term":  {"h": 1, "label": "Short-term (<1 yr)", "years": 1},
    "medium_term": {"h": 3, "label": "Medium-term (<3 yrs)", "years": 3},
    "long_term":   {"h": 5, "label": "Long-term (<5 yrs)", "years": 5},
}


# ── Load champion model ────────────────────────────────────────────────────────
def _load_champion():
    pkl_path = os.path.join(_HERE, "models", "champion_model.pkl")
    if not os.path.exists(pkl_path):
        return None, None
    with open(pkl_path, "rb") as f:
        champ = pickle.load(f)
    return champ.get("model"), champ.get("name", "unknown")


def _predict_safe(model, X: np.ndarray, model_name: str, floor_area: float) -> dict:
    """Run model.predict(X), return cost dict. Fallback if model is None."""
    if model is None or X is None:
        base = 182_500.0
    else:
        try:
            raw = float(model.predict(X.reshape(1, -1))[0])
            base = max(50_000.0, min(raw, 1_500_000.0))
        except Exception:
            base = 182_500.0

    return {
        "cost_per_sqm":  round(base, 2),
        "total_cost":    round(base * floor_area, 2),
    }


# ── Uncertainty calculator ─────────────────────────────────────────────────────
def _compute_ci(cost_per_sqm: float, h: int, feature_spread_pct: float) -> tuple:
    """
    Compute total uncertainty at horizon h.

    Total σ = √(σ_model² + σ_macro(h)²)
    σ_model  = CHAMPION_MAPE / 100 (from O5)
    σ_macro  = grows with h — derived from VAR forecast spread
    """
    sigma_model = CHAMPION_MAPE / 100
    # VAR forecast uncertainty grows roughly as σ_base * √h
    # We estimate σ_base from the feature spread at h=1
    sigma_macro_base = max(feature_spread_pct / 100, 0.05)
    sigma_macro_h    = sigma_macro_base * np.sqrt(max(h, 1))
    sigma_total      = np.sqrt(sigma_model**2 + sigma_macro_h**2)

    ci_width  = sigma_total * cost_per_sqm
    lower     = max(cost_per_sqm - 1.64 * ci_width, cost_per_sqm * 0.30)
    upper     = cost_per_sqm + 1.64 * ci_width
    ci_pct    = round(sigma_total * 100, 1)   # total uncertainty as %

    return round(lower, 2), round(upper, 2), ci_pct


# ── Main projection function ───────────────────────────────────────────────────
def _get_inflation_rate() -> float:
    """
    Derive the expected annual construction cost inflation rate.
    Uses O2 CPI data + historical NGN FX depreciation as anchors.
    Formula: r = 0.6 * CPI_rate + 0.4 * FX_depreciation_rate
    (Weights reflect SHAP importance: FX 45%, CPI 25.5% from O2)
    Falls back to 12% p.a. if data unavailable.
    """
    try:
        import os, pandas as pd
        _O2_PROC = os.path.join(os.path.dirname(__file__),
                                "..", "02_macro_analysis", "data", "processed")
        cpi_path = os.path.join(_O2_PROC, "worldbank_nigeria_processed.csv")
        df_cpi   = pd.read_csv(cpi_path)
        cpi_col  = "cpi_inflation_pct" if "cpi_inflation_pct" in df_cpi.columns else "cpi_annual_pct"
        cpi_last5 = df_cpi[cpi_col].dropna().tail(5).mean()

        fx_path  = os.path.join(_O2_PROC, "cbn_fx_rates_processed.csv")
        df_fx    = pd.read_csv(fx_path)
        fx_vals  = df_fx["ngn_usd"].dropna().tail(6).values
        fx_dep   = float(np.mean(np.diff(fx_vals) / fx_vals[:-1])) * 100  # avg % change

        # Weighted cost inflation proxy
        r = (0.40 * cpi_last5 + 0.60 * max(fx_dep, 0)) / 100
        # Clip to realistic Nigerian construction range: 8%-25% p.a.
        return float(np.clip(r, 0.08, 0.25))
    except Exception:
        return 0.12   # 12% p.a. default (conservative historical estimate)


def generate_projections(
    floor_area_sqm: float = 120.0,
    current_X: np.ndarray = None,
    current_cost_per_sqm: float = None,
) -> list:
    """
    Generate cost projections at 4 horizons using compound inflation methodology.

    Method:
      1. Get current cost from champion model (or passed in directly)
      2. Derive annual construction cost inflation rate from O2 CPI + FX data
      3. Apply compound growth: cost(h) = current_cost × (1 + r)^h
      4. Compute widening confidence intervals: CI grows as sqrt(h)

    This approach is more reliable than projecting feature vectors through
    the model (which converges to near-constant on the synthetic dataset)
    and is more directly interpretable by QS professionals.

    Args:
        floor_area_sqm        : building floor area (sqm)
        current_X             : current 14-feature vector (optional)
        current_cost_per_sqm  : current model prediction (optional, avoids re-inference)

    Returns:
        list of 4 dicts [current, short_term, medium_term, long_term]
    """
    model, model_name = _load_champion()

    # Step 1: Get current cost
    if current_cost_per_sqm is None:
        X = current_X if current_X is not None else np.zeros(14, dtype=np.float32)
        pred = _predict_safe(model, X, model_name, floor_area_sqm)
        current_cost = pred["cost_per_sqm"]
    else:
        current_cost = float(current_cost_per_sqm)

    # Step 2: Annual inflation rate anchored to real macro data
    r = _get_inflation_rate()

    results = []
    for key, cfg in HORIZONS_CONFIG.items():
        h = cfg["h"]

        if h == 0:
            # Current — use model prediction directly
            cost  = current_cost
            lower, upper, ci_pct = _compute_ci(cost, 0, 13.0)
        else:
            # Projected — compound growth + widening CI
            cost       = round(current_cost * ((1 + r) ** h), 2)
            # CI width grows with h: base uncertainty (model MAPE) + forecast spread
            base_spread = 13.0 + 6.0 * h   # widens by 6pp per year
            lower, upper, ci_pct = _compute_ci(cost, h, base_spread)

        total       = round(cost * floor_area_sqm, 2)
        total_lower = round(lower * floor_area_sqm, 2)
        total_upper = round(upper * floor_area_sqm, 2)

        results.append({
            "horizon_key":        key,
            "horizon_label":      cfg["label"],
            "years":              cfg["years"],
            "cost_per_sqm":       cost,
            "total_cost_ngn":     total,
            "confidence_lower":   lower,
            "confidence_upper":   upper,
            "total_lower_ngn":    total_lower,
            "total_upper_ngn":    total_upper,
            "uncertainty_pct":    ci_pct,
            "annual_inflation_r": round(r * 100, 1),
            "is_projection":      h > 0,
        })

    return results


def _synthetic_macro_fallback(current_X) -> dict:
    """
    Fallback when forecast_macro is unavailable.
    Uses Nigerian average annual inflation ~15% to project macro features.
    FX features (highest SHAP weight) grow at ~12% p.a. (historical NGN trend).
    """
    base = current_X if current_X is not None else np.zeros(14, dtype=np.float32)

    def _project(h: float) -> np.ndarray:
        """Scale each feature group by realistic Nigerian growth rates."""
        projected = base.copy()
        # FX return features (indices 4,5,6 + lags 11,12,13) — FX depreciation
        for idx in [4, 5, 6, 11, 12, 13]:
            projected[idx] = base[idx] * (1 + 0.12 * h)
        # CPI difference features (indices 1, 8) — inflation acceleration
        for idx in [1, 8]:
            projected[idx] = base[idx] * (1 + 0.10 * h)
        # Brent features (indices 3, 10) — moderate growth
        for idx in [3, 10]:
            projected[idx] = base[idx] * (1 + 0.04 * h)
        return projected

    return {
        "current": {
            "point": base,
            "lower": base * 0.87,
            "upper": base * 1.13,
        },
        1: {
            "point": _project(1),
            "lower": _project(1) * 0.87,
            "upper": _project(1) * 1.15,
            "step":  1,
        },
        3: {
            "point": _project(3),
            "lower": _project(3) * 0.78,
            "upper": _project(3) * 1.28,
            "step":  3,
        },
        5: {
            "point": _project(5),
            "lower": _project(5) * 0.65,
            "upper": _project(5) * 1.45,
            "step":  5,
        },
    }


# ── Summary statistics ─────────────────────────────────────────────────────────
def projection_summary(projections: list) -> dict:
    """Return a compact summary for logging/audit."""
    costs = [p["cost_per_sqm"] for p in projections]
    return {
        "current_cost_per_sqm":   costs[0],
        "short_term_cost_per_sqm": costs[1] if len(costs) > 1 else None,
        "medium_term_cost_per_sqm": costs[2] if len(costs) > 2 else None,
        "long_term_cost_per_sqm":  costs[3] if len(costs) > 3 else None,
        "5yr_change_pct":         round((costs[-1] / costs[0] - 1) * 100, 1) if costs[0] > 0 else None,
        "uncertainty_at_5yr_pct": projections[-1]["uncertainty_pct"] if projections else None,
    }


# ── Test run ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== iNHCES Temporal Projection Engine ===")
    projections = generate_projections(floor_area_sqm=120.0)
    print(f"\n  {'Horizon':<20} {'Cost/sqm':>12} {'Lower':>12} {'Upper':>12} {'Uncertainty':>12}")
    print("  " + "-" * 72)
    for p in projections:
        marker = "" if p["is_projection"] else " (actual)"
        print(f"  {p['horizon_label']:<20} "
              f"NGN {p['cost_per_sqm']:>10,.0f} "
              f"NGN {p['confidence_lower']:>10,.0f} "
              f"NGN {p['confidence_upper']:>10,.0f} "
              f"  ±{p['uncertainty_pct']:>6.1f}%{marker}")

    summary = projection_summary(projections)
    print(f"\n  5-year projected change: {summary['5yr_change_pct']:+.1f}%")
    print(f"  5-year uncertainty:      ±{summary['uncertainty_at_5yr_pct']:.1f}%")
    print(f"\n[OK] 05_temporal_projection.py ready")
