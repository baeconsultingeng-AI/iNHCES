"""
iNHCES — Macro Forecasting Module
Uses the VAR(diff, lag=1) model from O2 Step 3 to generate h-step ahead
forecasts of macroeconomic variables at h = 1, 3, 5 years.

Methodology:
  1. Re-fit VAR(1) on first-differenced I(1) series (GDP, CPI, lending, Brent)
  2. Fit AR(1) on percentage-return I(2)* FX series (NGN/USD, EUR, GBP)
  3. Generate h-step ahead point forecasts + 90% confidence intervals
  4. Translate forecasted differences back to engineered feature vectors
     ready for the LightGBM cost model

Horizons:
  h = 1 : short-term  (<1 year)
  h = 3 : medium-term (<3 years)
  h = 5 : long-term   (<5 years)

DATA SOURCE: AMBER/RED — methodology is real; results are synthetic until
real NIQS data + live API data are configured.

TETFund NRF 2025 | Department of Quantity Surveying, ABU Zaria
"""

import os
import sys
import warnings
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
_PROC = os.path.join(_HERE, "data", "processed")

# Feature columns that match 05_feature_engineering.py FEATURE_COLS
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

HORIZONS = {
    "short_term":  {"h": 1, "label": "Short-term (<1 yr)", "years": 1},
    "medium_term": {"h": 3, "label": "Medium-term (<3 yrs)", "years": 3},
    "long_term":   {"h": 5, "label": "Long-term (<5 yrs)", "years": 5},
}


# ── 1. Load processed data ─────────────────────────────────────────────────────
def load_processed_data() -> pd.DataFrame:
    """Load and merge the three O2 processed CSVs."""
    sources = {
        "worldbank": os.path.join(_PROC, "worldbank_nigeria_processed.csv"),
        "oil":       os.path.join(_PROC, "eia_brent_oil_processed.csv"),
        "fx":        os.path.join(_PROC, "cbn_fx_rates_processed.csv"),
    }
    rename_map = {
        "cpi_inflation_pct":  "cpi_annual_pct",
        "brent_usd_annual_avg": "brent_usd_barrel",
    }
    frames = []
    for key, path in sources.items():
        try:
            df = pd.read_csv(path)
            df = df.rename(columns=rename_map)
            df["year"] = pd.to_numeric(df["year"], errors="coerce").astype(int)
            frames.append(df)
        except FileNotFoundError:
            print(f"  [WARN] {key} not found — using synthetic fallback")

    if not frames:
        return _synthetic_fallback()

    merged = frames[0]
    for df in frames[1:]:
        merged = merged.merge(df, on="year", how="outer")
    merged = merged.sort_values("year").reset_index(drop=True)
    return merged[(merged["year"] >= 2000) & (merged["year"] <= 2024)]


def _synthetic_fallback() -> pd.DataFrame:
    """Minimal synthetic data if CSVs unavailable."""
    np.random.seed(2025)
    years = range(2000, 2025)
    return pd.DataFrame({
        "year":              list(years),
        "gdp_growth_pct":    np.random.normal(3.2, 1.8, 25),
        "cpi_annual_pct":    np.cumsum(np.random.normal(0.8, 0.4, 25)) + 10,
        "lending_rate_pct":  np.random.normal(26, 2, 25),
        "brent_usd_barrel":  np.random.normal(65, 20, 25),
        "ngn_usd":           np.cumprod(1 + np.random.normal(0.08, 0.15, 25)) * 120,
        "ngn_eur":           np.cumprod(1 + np.random.normal(0.08, 0.15, 25)) * 140,
        "ngn_gbp":           np.cumprod(1 + np.random.normal(0.08, 0.15, 25)) * 165,
    })


# ── 2. Compute feature series ──────────────────────────────────────────────────
def compute_feature_series(df: pd.DataFrame) -> pd.DataFrame:
    """Build the same feature series as 05_feature_engineering.py."""
    req = {
        "gdp_growth_pct":    lambda yr: 3.2,
        "cpi_annual_pct":    lambda yr: 10 + 0.8 * (yr - 2000),
        "lending_rate_pct":  lambda yr: 26.0,
        "brent_usd_barrel":  lambda yr: 65.0,
        "ngn_usd":           lambda yr: 120 * (1.08 ** (yr - 2000)),
        "ngn_eur":           lambda yr: 140 * (1.08 ** (yr - 2000)),
        "ngn_gbp":           lambda yr: 165 * (1.08 ** (yr - 2000)),
    }
    for col, fn in req.items():
        if col not in df.columns:
            df[col] = df["year"].apply(fn)

    # I(1) first differences
    for col in ["gdp_growth_pct", "cpi_annual_pct", "lending_rate_pct", "brent_usd_barrel"]:
        df[f"d_{col}"] = df[col].diff()

    # I(2)* percentage returns
    for col in ["ngn_usd", "ngn_eur", "ngn_gbp"]:
        df[f"ret_{col}"] = df[col].pct_change() * 100

    # Lag-1 features
    for col in ["d_gdp_growth_pct", "d_cpi_annual_pct", "d_lending_rate_pct",
                "d_brent_usd_barrel", "ret_ngn_usd", "ret_ngn_eur", "ret_ngn_gbp"]:
        df[f"lag1_{col}"] = df[col].shift(1)

    return df.dropna().reset_index(drop=True)


# ── 3. Fit VAR on I(1) differenced series ─────────────────────────────────────
def fit_var(df: pd.DataFrame):
    """Fit VAR(1) on the four first-differenced I(1) series."""
    from statsmodels.tsa.vector_ar.var_model import VAR

    i1_cols = ["d_gdp_growth_pct", "d_cpi_annual_pct",
               "d_lending_rate_pct", "d_brent_usd_barrel"]

    endog = df[i1_cols].values
    model = VAR(endog)
    result = model.fit(maxlags=1, ic="aic")
    return result, i1_cols


# ── 4. Fit AR(1) on FX returns ─────────────────────────────────────────────────
def fit_ar_fx(df: pd.DataFrame) -> dict:
    """Fit simple AR(1) on each FX return series."""
    from statsmodels.tsa.ar_model import AutoReg

    ar_models = {}
    for col in ["ret_ngn_usd", "ret_ngn_eur", "ret_ngn_gbp"]:
        series = df[col].dropna().values
        try:
            m = AutoReg(series, lags=1, old_names=False).fit()
            ar_models[col] = {"model": m, "series": series}
        except Exception:
            # Fallback: use last value + drift
            ar_models[col] = {"model": None, "series": series}
    return ar_models


# ── 5. Generate h-step forecasts ──────────────────────────────────────────────
def forecast_var(var_result, df: pd.DataFrame, h: int) -> tuple:
    """
    Generate h-step ahead VAR forecasts.
    Returns (point_forecasts, lower_ci, upper_ci) each of shape (h, 4).
    """
    i1_cols = ["d_gdp_growth_pct", "d_cpi_annual_pct",
               "d_lending_rate_pct", "d_brent_usd_barrel"]

    y_obs     = df[i1_cols].values
    lag_order = var_result.k_ar
    k         = len(i1_cols)

    # Forecast point estimates
    forecast_input = y_obs[-lag_order:]
    fc = var_result.forecast(y=forecast_input, steps=h)     # (h, k)

    # Residual std as SE proxy (avoids forecast_cov indexing issues)
    resid_std = np.std(var_result.resid, axis=0)            # (k,)
    # SE grows as σ * √h for each step
    se = np.array([resid_std * np.sqrt(s + 1) for s in range(h)])  # (h, k)
    z  = 1.64

    return fc, fc - z * se, fc + z * se


def forecast_fx(ar_models: dict, h: int) -> dict:
    """
    Generate h-step ahead AR(1) forecasts for FX returns.
    Returns dict: col -> {"point": array(h,), "se": array(h,)}
    """
    result = {}
    for col, info in ar_models.items():
        series = info["series"]
        m      = info["model"]

        if m is not None:
            try:
                fc_obj = m.forecast(start=len(series), end=len(series) + h - 1)
                pts    = fc_obj.values if hasattr(fc_obj, "values") else np.array(fc_obj)
                # AR forecast SE grows roughly as σ * √h
                resid_std = np.std(m.resid)
                se = resid_std * np.sqrt(np.arange(1, h + 1))
            except Exception:
                pts = np.full(h, series[-1])
                se  = np.full(h, np.std(series[-3:]) * np.sqrt(np.arange(1, h + 1)))
        else:
            # Mean reversion fallback
            pts = np.full(h, np.mean(series[-5:]))
            se  = np.full(h, np.std(series[-5:]) * np.sqrt(np.arange(1, h + 1)))

        result[col] = {"point": pts, "se": se}
    return result


# ── 6. Build projected feature vectors ────────────────────────────────────────
def build_projected_feature_vectors(
    df: pd.DataFrame,
    var_fc: np.ndarray,      # (h, 4) — I(1) differenced forecasts
    var_lb: np.ndarray,
    var_ub: np.ndarray,
    fx_fc: dict,             # FX return forecasts
    h: int,
) -> list:
    """
    Convert VAR/AR forecasts into feature vectors matching FEATURE_COLS.
    Returns a list of h dicts, each with 'point', 'lower', 'upper' feature arrays.
    """
    i1_names = ["d_gdp_growth_pct", "d_cpi_annual_pct",
                "d_lending_rate_pct", "d_brent_usd_barrel"]
    fx_names = ["ret_ngn_usd", "ret_ngn_eur", "ret_ngn_gbp"]

    vectors = []
    # Store t-1 values for lag computation
    prev_i1 = {n: df[n].iloc[-1] for n in i1_names}
    prev_fx = {n: df[n].iloc[-1] for n in fx_names}

    for step in range(h):
        # Point forecasts for this step
        i1_pt = {i1_names[j]: float(var_fc[step, j]) for j in range(4)}
        i1_lb = {i1_names[j]: float(var_lb[step, j]) for j in range(4)}
        i1_ub = {i1_names[j]: float(var_ub[step, j]) for j in range(4)}

        fx_pt = {n: float(fx_fc[n]["point"][step]) for n in fx_names}
        fx_lb = {n: float(fx_fc[n]["point"][step] - 1.64 * fx_fc[n]["se"][step]) for n in fx_names}
        fx_ub = {n: float(fx_fc[n]["point"][step] + 1.64 * fx_fc[n]["se"][step]) for n in fx_names}

        # Build feature dict (point estimate)
        feat_pt = {**i1_pt, **fx_pt}
        for n in i1_names:
            feat_pt[f"lag1_{n}"] = prev_i1[n]
        for n in fx_names:
            feat_pt[f"lag1_{n}"] = prev_fx[n]

        # Conservative lower (worst case)
        feat_lb = {**i1_lb, **fx_lb}
        for n in i1_names:
            feat_lb[f"lag1_{n}"] = prev_i1[n]
        for n in fx_names:
            feat_lb[f"lag1_{n}"] = prev_fx[n]

        # Conservative upper (worst case)
        feat_ub = {**i1_ub, **fx_ub}
        for n in i1_names:
            feat_ub[f"lag1_{n}"] = prev_i1[n]
        for n in fx_names:
            feat_ub[f"lag1_{n}"] = prev_fx[n]

        vectors.append({
            "step":  step + 1,
            "point": np.array([feat_pt.get(c, 0.0) for c in FEATURE_COLS], dtype=np.float32),
            "lower": np.array([feat_lb.get(c, 0.0) for c in FEATURE_COLS], dtype=np.float32),
            "upper": np.array([feat_ub.get(c, 0.0) for c in FEATURE_COLS], dtype=np.float32),
        })

        # Update lag values for next step
        prev_i1 = i1_pt.copy()
        prev_fx = fx_pt.copy()

    return vectors


# ── 7. Main API function ───────────────────────────────────────────────────────
def get_macro_projections(horizons: list = [1, 3, 5]) -> dict:
    """
    Main entry point. Returns projected feature vectors at each horizon.

    Returns:
        dict with keys: 'current' + each h in horizons
        Each value: {'point': np.array(14,), 'lower': np.array(14,), 'upper': np.array(14,)}
    """
    df_raw = load_processed_data()
    df     = compute_feature_series(df_raw)

    if len(df) < 5:
        print("  [WARN] Insufficient data for VAR fit — using synthetic fallback")
        return _fallback_projections(horizons)

    max_h = max(horizons)

    # Fit models
    try:
        var_result, _ = fit_var(df)
        ar_models     = fit_ar_fx(df)

        # Get forecasts up to max_h steps
        var_fc, var_lb, var_ub = forecast_var(var_result, df, max_h)
        fx_fc = forecast_fx(ar_models, max_h)

        # Build vectors for all steps up to max_h
        all_vectors = build_projected_feature_vectors(
            df, var_fc, var_lb, var_ub, fx_fc, max_h
        )
    except Exception as e:
        print(f"  [WARN] VAR forecasting failed ({e}) — using synthetic fallback")
        return _fallback_projections(horizons)

    # Current feature vector (last row of df)
    current = np.array([df[c].iloc[-1] if c in df.columns else 0.0
                        for c in FEATURE_COLS], dtype=np.float32)

    result = {
        "current": {"point": current, "lower": current * 0.87, "upper": current * 1.13},
    }
    for h in horizons:
        v = all_vectors[h - 1]  # step h is index h-1
        result[h] = v

    return result


def _fallback_projections(horizons: list) -> dict:
    """Synthetic fallback when VAR fitting fails."""
    np.random.seed(2025)
    base = np.array([0.20, 7.20, 2.20, -2.49, 97.33, 93.81, 96.07,
                     0.40, 4.90, 0.60, 28.36, 76.51, 72.36, 68.55], dtype=np.float32)

    result = {
        "current": {"point": base, "lower": base * 0.87, "upper": base * 1.13}
    }
    for h in horizons:
        drift = 1 + 0.08 * h          # 8% macro drift per year
        spread = 0.13 + 0.07 * h      # widening CI
        pt = base * drift
        result[h] = {
            "point": pt,
            "lower": pt * (1 - spread),
            "upper": pt * (1 + spread),
            "step":  h,
        }
    return result


# ── Test run ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== iNHCES Macro Forecaster ===")
    projections = get_macro_projections(horizons=[1, 3, 5])
    for key, v in projections.items():
        label = f"h={key}" if isinstance(key, int) else key
        print(f"  [{label:12s}] feature[0]={v['point'][0]:.3f}  "
              f"CI: [{v['lower'][0]:.3f}, {v['upper'][0]:.3f}]")
    print("[OK] forecast_macro.py ready")
