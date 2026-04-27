"""
iNHCES Feature Preparation for /estimate Inference

Fetches the last 3 years of macro data from Supabase and computes
the same 14-feature vector used in O5 training:

  I(1) first differences:
    d_gdp_growth_pct, d_cpi_annual_pct, d_lending_rate_pct, d_brent_usd_barrel

  I(2)* percentage returns:
    ret_ngn_usd, ret_ngn_eur, ret_ngn_gbp

  Lag-1 of all transformed features (7 more):
    lag1_d_*, lag1_ret_*

If Supabase data is insufficient (< 3 rows per series), falls back to
synthetic values from the O5 training set median.
DATA SOURCE: RED until Supabase is populated with real macro data.
"""

import logging
import numpy as np
from typing import Optional

from app.ml.inference import FEATURE_COLS

logger = logging.getLogger(__name__)

# Synthetic fallback values (O5 training set medians for 2022-2024)
# DATA SOURCE: RED
_SYNTHETIC_FEATURE_VALUES = {
    "d_gdp_growth_pct":        0.20,
    "d_cpi_annual_pct":        7.20,
    "d_lending_rate_pct":      2.20,
    "d_brent_usd_barrel":     -2.49,
    "ret_ngn_usd":            97.33,
    "ret_ngn_eur":            93.81,
    "ret_ngn_gbp":            96.07,
    "lag1_d_gdp_growth_pct":   0.40,
    "lag1_d_cpi_annual_pct":   4.90,
    "lag1_d_lending_rate_pct": 0.60,
    "lag1_d_brent_usd_barrel": 28.36,
    "lag1_ret_ngn_usd":       76.51,
    "lag1_ret_ngn_eur":       72.36,
    "lag1_ret_ngn_gbp":       68.55,
}


def _fetch_annual_series(table: str, value_col: str, db, n: int = 3) -> list:
    """Fetch the last n annual values from a Supabase macro table, oldest first."""
    try:
        resp = (
            db.table(table)
            .select(f"date,{value_col}")
            .order("date", desc=True)
            .limit(n)
            .execute()
        )
        rows = sorted(resp.data, key=lambda r: r["date"])
        return [float(r[value_col]) for r in rows if r.get(value_col) is not None]
    except Exception as e:
        logger.warning(f"[feature_prep] Failed to fetch {table}.{value_col}: {e}")
        return []


def _diff(series: list) -> Optional[float]:
    """First difference: series[-1] - series[-2]."""
    if len(series) >= 2:
        return series[-1] - series[-2]
    return None


def _pct_change(series: list) -> Optional[float]:
    """Percentage change: (t - t-1) / t-1 * 100."""
    if len(series) >= 2 and series[-2] != 0:
        return (series[-1] - series[-2]) / series[-2] * 100
    return None


def _lag1_diff(series: list) -> Optional[float]:
    """Lagged first difference: series[-2] - series[-3]."""
    if len(series) >= 3:
        return series[-2] - series[-3]
    return None


def _lag1_pct(series: list) -> Optional[float]:
    """Lagged pct change: (t-1 - t-2) / t-2 * 100."""
    if len(series) >= 3 and series[-3] != 0:
        return (series[-2] - series[-3]) / series[-3] * 100
    return None


def build_feature_vector(db) -> tuple:
    """
    Fetch macro data from Supabase and build the 14-feature inference vector.

    Returns:
        X         : np.ndarray shape (1, 14) for model.predict()
        freshness : 'GREEN' | 'AMBER' | 'RED' (worst level across all series)
        snapshot  : dict of feature name -> value (for API response)
    """
    gdp     = _fetch_annual_series("macro_gdp",      "gdp_growth_pct",   db, 3)
    cpi     = _fetch_annual_series("macro_cpi",      "cpi_annual_pct",   db, 3)
    lending = _fetch_annual_series("macro_interest", "lending_rate_pct", db, 3)
    brent   = _fetch_annual_series("macro_oil",      "brent_usd_barrel", db, 3)
    ngn_usd = _fetch_annual_series("macro_fx",       "ngn_usd",          db, 3)
    ngn_eur = _fetch_annual_series("macro_fx",       "ngn_eur",          db, 3)
    ngn_gbp = _fetch_annual_series("macro_fx",       "ngn_gbp",          db, 3)

    def feature(computed: Optional[float], name: str) -> float:
        if computed is not None:
            return computed
        val = _SYNTHETIC_FEATURE_VALUES[name]
        logger.info(f"[feature_prep] Synthetic fallback: {name}={val}")
        return val

    feats = {
        "d_gdp_growth_pct":        feature(_diff(gdp),        "d_gdp_growth_pct"),
        "d_cpi_annual_pct":        feature(_diff(cpi),        "d_cpi_annual_pct"),
        "d_lending_rate_pct":      feature(_diff(lending),    "d_lending_rate_pct"),
        "d_brent_usd_barrel":      feature(_diff(brent),      "d_brent_usd_barrel"),
        "ret_ngn_usd":             feature(_pct_change(ngn_usd), "ret_ngn_usd"),
        "ret_ngn_eur":             feature(_pct_change(ngn_eur), "ret_ngn_eur"),
        "ret_ngn_gbp":             feature(_pct_change(ngn_gbp), "ret_ngn_gbp"),
        "lag1_d_gdp_growth_pct":   feature(_lag1_diff(gdp),   "lag1_d_gdp_growth_pct"),
        "lag1_d_cpi_annual_pct":   feature(_lag1_diff(cpi),   "lag1_d_cpi_annual_pct"),
        "lag1_d_lending_rate_pct": feature(_lag1_diff(lending),"lag1_d_lending_rate_pct"),
        "lag1_d_brent_usd_barrel": feature(_lag1_diff(brent), "lag1_d_brent_usd_barrel"),
        "lag1_ret_ngn_usd":        feature(_lag1_pct(ngn_usd),"lag1_ret_ngn_usd"),
        "lag1_ret_ngn_eur":        feature(_lag1_pct(ngn_eur),"lag1_ret_ngn_eur"),
        "lag1_ret_ngn_gbp":        feature(_lag1_pct(ngn_gbp),"lag1_ret_ngn_gbp"),
    }

    # Freshness: RED if any series had fewer than 2 rows (full synthetic)
    all_have_2 = all(
        len(s) >= 2 for s in [gdp, cpi, lending, brent, ngn_usd, ngn_eur, ngn_gbp]
    )
    freshness = "AMBER" if all_have_2 else "RED"

    X = np.array([[feats[col] for col in FEATURE_COLS]], dtype=np.float32)
    return X, freshness, feats
