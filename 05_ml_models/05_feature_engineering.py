"""
iNHCES O5 Step 1 — Feature Engineering Pipeline
Builds the ML feature matrix from O2 processed CSVs.
Applies stationarity-informed transformations (O2 findings):
  - I(1) series (GDP, CPI, lending rate, Brent) -> first differences
  - I(2)* series (NGN/USD, EUR, GBP) -> percentage changes (returns)
  - Lag features (lag-1, lag-2) for all transformed variables
Generates a synthetic housing cost proxy (RED — replace with real NIQS data in O5+).
Saves: feature matrix CSV, split metadata, transformation log.
Generates: O5_01_Feature_Engineering.pdf (AMBER)

DATA SOURCE: AMBER/RED
  - Macro features from O2 processed CSVs: World Bank (GREEN), EIA+FX (RED synthetic)
  - Target variable (cost_per_sqm): RED synthetic proxy — MUST be replaced

TETFund NRF 2025 | Department of Quantity Surveying, ABU Zaria
"""

import os
import sys
import csv
import json
import math
from datetime import date

import numpy as np
import pandas as pd

# ── Paths ──────────────────────────────────────────────────────────────────────
_HERE  = os.path.dirname(os.path.abspath(__file__))
_ROOT  = os.path.dirname(_HERE)
_O2    = os.path.join(_ROOT, '02_macro_analysis')
_DATA  = os.path.join(_HERE, 'data')
_RAW   = os.path.join(_DATA, 'raw')
_PROC  = os.path.join(_DATA, 'processed')

os.makedirs(_RAW,  exist_ok=True)
os.makedirs(_PROC, exist_ok=True)

# ── PDF helpers ────────────────────────────────────────────────────────────────
sys.path.insert(0, os.path.join(_ROOT, '01_literature_review'))
from generate_o1_pdfs import (
    DocPDF, sanitize, _ds_page,
    DARK_NAVY, GOLD, LIGHT_BLUE, WHITE, DARK_GREY, MID_GREY,
    PAGE_W, LEFT,
)

SEED = 2025
np.random.seed(SEED)

# ── 1. LOAD O2 PROCESSED DATA ─────────────────────────────────────────────────
def load_o2_data():
    """Load all three O2 processed CSVs. Return merged annual dataframe."""
    frames = {}
    sources = {
        'worldbank': os.path.join(_O2, 'data', 'processed', 'worldbank_nigeria_processed.csv'),
        'oil':       os.path.join(_O2, 'data', 'processed', 'eia_brent_oil_processed.csv'),
        'fx':        os.path.join(_O2, 'data', 'processed', 'cbn_fx_rates_processed.csv'),
    }
    for key, path in sources.items():
        try:
            df = pd.read_csv(path)
            df['year'] = pd.to_numeric(df['year'], errors='coerce')
            df = df.dropna(subset=['year'])
            df['year'] = df['year'].astype(int)
            frames[key] = df
            print(f"  [LOAD] {key}: {len(df)} rows, cols={list(df.columns)}")
        except FileNotFoundError:
            print(f"  [WARN] {key} not found at {path} -- skipping")
    return frames


def merge_frames(frames):
    """Merge all frames on year. Keep 2000-2024."""
    if not frames:
        raise RuntimeError("No O2 data frames loaded.")

    # Start with World Bank (always present — GREEN data)
    merged = None
    for key in ['worldbank', 'oil', 'fx']:
        if key not in frames:
            continue
        df = frames[key].copy()
        if merged is None:
            merged = df
        else:
            merged = merged.merge(df, on='year', how='outer', suffixes=('', f'_{key}'))

    merged = merged.sort_values('year').reset_index(drop=True)
    merged = merged[(merged['year'] >= 2000) & (merged['year'] <= 2024)]
    print(f"  [MERGE] {len(merged)} rows, years {merged['year'].min()}-{merged['year'].max()}")
    return merged


# ── 2. STANDARDISE COLUMN NAMES ───────────────────────────────────────────────
RENAME_MAP = {
    # World Bank columns (flexible naming — covers all O2 output variants)
    'gdp_growth':            'gdp_growth_pct',
    'GDP_growth':            'gdp_growth_pct',
    'gdp_growth_annual':     'gdp_growth_pct',
    'inflation_cpi':         'cpi_annual_pct',
    'CPI_inflation':         'cpi_annual_pct',
    'cpi_inflation_pct':     'cpi_annual_pct',   # actual O2 World Bank output
    'cpi':                   'cpi_annual_pct',
    'lending_rate':          'lending_rate_pct',
    'Lending_rate':          'lending_rate_pct',
    # EIA oil (covers all O2 output variants)
    'brent_price':           'brent_usd_barrel',
    'brent':                 'brent_usd_barrel',
    'brent_usd_annual_avg':  'brent_usd_barrel',  # actual O2 EIA output
    'price':                 'brent_usd_barrel',
    # CBN FX
    'ngn_usd_rate':        'ngn_usd',
    'usd_rate':            'ngn_usd',
    'ngn_eur_rate':        'ngn_eur',
    'ngn_gbp_rate':        'ngn_gbp',
}

REQUIRED_COLS = ['gdp_growth_pct', 'cpi_annual_pct', 'lending_rate_pct',
                 'brent_usd_barrel', 'ngn_usd', 'ngn_eur', 'ngn_gbp']


def standardise_columns(df):
    df = df.rename(columns={k: v for k, v in RENAME_MAP.items() if k in df.columns})
    # Fill any missing required columns with synthetic values
    synth_defaults = {
        'gdp_growth_pct':   lambda yr: max(-3, min(8, np.random.normal(3.2, 1.8))),
        'cpi_annual_pct':   lambda yr: max(5, min(35, 12 + 0.8 * (yr - 2000) + np.random.normal(0, 2))),
        'lending_rate_pct': lambda yr: max(15, min(35, 26 + 0.15 * (yr - 2000) + np.random.normal(0, 1))),
        'brent_usd_barrel': lambda yr: max(20, 45 + 1.5 * (yr - 2000) + np.random.normal(0, 15)),
        'ngn_usd':          lambda yr: max(100, 120 * (1.08 ** (yr - 2000)) + np.random.normal(0, 20)),
        'ngn_eur':          lambda yr: max(120, 140 * (1.08 ** (yr - 2000)) + np.random.normal(0, 25)),
        'ngn_gbp':          lambda yr: max(140, 165 * (1.08 ** (yr - 2000)) + np.random.normal(0, 30)),
    }
    for col in REQUIRED_COLS:
        if col not in df.columns:
            print(f"  [SYNTH] {col} missing — generating synthetic column (RED)")
            df[col] = df['year'].apply(synth_defaults[col])
    return df


# ── 3. FEATURE TRANSFORMATIONS ────────────────────────────────────────────────
def apply_transformations(df):
    """
    Apply stationarity-informed transformations (O2 findings):
    - I(1) series: first difference
    - I(2)* series: percentage change (returns)
    - Lags (lag-1 and lag-2) for all transformed variables
    """
    df = df.copy().sort_values('year').reset_index(drop=True)

    # I(1) series: first difference
    i1_cols = ['gdp_growth_pct', 'cpi_annual_pct', 'lending_rate_pct', 'brent_usd_barrel']
    for col in i1_cols:
        df[f'd_{col}'] = df[col].diff()          # first difference

    # I(2)* series: percentage change (returns)
    i2_cols = ['ngn_usd', 'ngn_eur', 'ngn_gbp']
    for col in i2_cols:
        df[f'ret_{col}'] = df[col].pct_change() * 100   # % change

    # Log levels for positive series (useful for some models)
    log_cols = ['brent_usd_barrel', 'ngn_usd', 'ngn_eur', 'ngn_gbp']
    for col in log_cols:
        df[f'log_{col}'] = np.log(df[col].clip(lower=1))

    # Lag features (lag-1) for all transformed variables
    transform_cols = (
        [f'd_{c}' for c in i1_cols] +
        [f'ret_{c}' for c in i2_cols]
    )
    for col in transform_cols:
        df[f'lag1_{col}'] = df[col].shift(1)
        df[f'lag2_{col}'] = df[col].shift(2)

    print(f"  [TRANSFORM] {len(df.columns)} columns after feature engineering")
    return df


# ── 4. SYNTHETIC HOUSING COST PROXY ──────────────────────────────────────────
def build_target(df):
    """
    Synthetic housing cost proxy (NGN/sqm, annual).
    DATA SOURCE: RED -- must be replaced with real NIQS unit rate data.
    Formula incorporates O2 SHAP findings:
      NGN/USD dominance (45%), CPI (25.5%), Brent (10.9%).
    """
    base = 120_000  # NGN/sqm baseline (approx 2015 mid-range residential)
    ngn_usd_2015 = df.loc[df['year'] == 2015, 'ngn_usd'].values
    ngn_usd_ref  = float(ngn_usd_2015[0]) if len(ngn_usd_2015) > 0 else 197.0
    cpi_2015     = df.loc[df['year'] == 2015, 'cpi_annual_pct'].values
    cpi_ref      = float(cpi_2015[0]) if len(cpi_2015) > 0 else 9.0
    brent_2015   = df.loc[df['year'] == 2015, 'brent_usd_barrel'].values
    brent_ref    = float(brent_2015[0]) if len(brent_2015) > 0 else 52.0

    noise = np.random.normal(0, 0.05, len(df))

    cost = (
        base
        * (df['ngn_usd'] / ngn_usd_ref) ** 0.42         # FX effect (45% SHAP)
        * (1 + (df['cpi_annual_pct'] - cpi_ref) / 100) ** 1.5  # CPI effect
        * (1 + 0.12 * (df['brent_usd_barrel'] - brent_ref) / brent_ref)  # Brent
        * (1 + noise)
    ).clip(lower=50_000, upper=800_000)

    df['cost_per_sqm'] = cost.round(2)
    print(f"  [TARGET] cost_per_sqm range: "
          f"NGN {df['cost_per_sqm'].min():,.0f} -- {df['cost_per_sqm'].max():,.0f} / sqm")
    return df


# ── 5. BUILD FINAL FEATURE MATRIX ────────────────────────────────────────────
FEATURE_COLS = [
    # Differenced I(1)
    'd_gdp_growth_pct', 'd_cpi_annual_pct', 'd_lending_rate_pct', 'd_brent_usd_barrel',
    # Pct-change I(2)*
    'ret_ngn_usd', 'ret_ngn_eur', 'ret_ngn_gbp',
    # Lag-1 of all transformed
    'lag1_d_gdp_growth_pct', 'lag1_d_cpi_annual_pct',
    'lag1_d_lending_rate_pct', 'lag1_d_brent_usd_barrel',
    'lag1_ret_ngn_usd', 'lag1_ret_ngn_eur', 'lag1_ret_ngn_gbp',
]
TARGET_COL = 'cost_per_sqm'


def build_feature_matrix(df):
    """Select features + target, drop NaN rows from differencing."""
    available = [c for c in FEATURE_COLS if c in df.columns]
    missing   = [c for c in FEATURE_COLS if c not in df.columns]
    if missing:
        print(f"  [WARN] Missing feature cols: {missing}")

    fm = df[['year'] + available + [TARGET_COL]].dropna().reset_index(drop=True)
    print(f"  [MATRIX] {len(fm)} rows x {len(available)} features after dropping NaN")
    return fm, available


def train_val_test_split(fm):
    """
    Time-series split (no shuffling):
      Train: up to 2019 (approx 70%)
      Val:   2020-2021  (approx 15%)
      Test:  2022-2024  (approx 15%)
    """
    train = fm[fm['year'] <= 2019]
    val   = fm[(fm['year'] >= 2020) & (fm['year'] <= 2021)]
    test  = fm[fm['year'] >= 2022]
    print(f"  [SPLIT] Train: {len(train)} | Val: {len(val)} | Test: {len(test)}")
    return train, val, test


# ── 6. SAVE OUTPUTS ───────────────────────────────────────────────────────────
def save_outputs(fm, train, val, test, feature_cols, df_raw):
    # Full feature matrix
    fm_path = os.path.join(_PROC, 'feature_matrix.csv')
    fm.to_csv(fm_path, index=False)
    print(f"  [SAVE] feature_matrix.csv -> {fm_path}")

    # Split CSVs
    for name, split_df in [('train', train), ('val', val), ('test', test)]:
        p = os.path.join(_PROC, f'{name}_set.csv')
        split_df.to_csv(p, index=False)

    # Feature metadata JSON
    meta = {
        'generated':       date.today().isoformat(),
        'n_rows':          len(fm),
        'n_features':      len(feature_cols),
        'features':        feature_cols,
        'target':          TARGET_COL,
        'train_years':     f"{int(train['year'].min())}-{int(train['year'].max())}",
        'val_years':       f"{int(val['year'].min())}-{int(val['year'].max())}",
        'test_years':      f"{int(test['year'].min())}-{int(test['year'].max())}",
        'train_rows':      len(train),
        'val_rows':        len(val),
        'test_rows':       len(test),
        'target_mean':     round(float(fm[TARGET_COL].mean()), 2),
        'target_std':      round(float(fm[TARGET_COL].std()), 2),
        'target_min':      round(float(fm[TARGET_COL].min()), 2),
        'target_max':      round(float(fm[TARGET_COL].max()), 2),
        'data_source':     'RED -- synthetic proxy; replace with real NIQS data',
        'seed':            SEED,
    }
    meta_path = os.path.join(_PROC, 'feature_metadata.json')
    with open(meta_path, 'w') as f:
        json.dump(meta, f, indent=2)
    print(f"  [SAVE] feature_metadata.json -> {meta_path}")
    return meta


# ── 7. PDF REPORT ─────────────────────────────────────────────────────────────
def generate_pdf(meta, feature_cols, fm):
    out_path = os.path.join(_HERE, 'O5_01_Feature_Engineering.pdf')

    class FePDF(DocPDF):
        def header(self):
            self.set_fill_color(*DARK_NAVY)
            self.rect(0, 0, 210, 14, 'F')
            self.set_font("Helvetica", "B", 7)
            self.set_text_color(*WHITE)
            self.set_xy(5, 4)
            self.cell(PAGE_W, 6, sanitize(
                "iNHCES  |  TETFund NRF 2025  |  Dept. QS, ABU Zaria  |  O5 Step 1 -- Feature Engineering"
            ))
            self.set_text_color(*DARK_GREY)
            self.ln(16)

        def footer(self):
            self.set_y(-13)
            self.set_draw_color(*GOLD)
            self.set_line_width(0.4)
            self.line(LEFT, self.get_y(), 198, self.get_y())
            self.set_font("Helvetica", "I", 7.5)
            self.set_text_color(*MID_GREY)
            self.cell(0, 8, sanitize(
                f"O5 Step 1 Feature Engineering  |  ABU Zaria / TETFund NRF 2025  |  Page {self.page_no()}"
            ), align="C")

    pdf = FePDF("O5_01_Feature_Engineering.pdf", "O5-01")

    # Cover
    pdf.add_page()
    pdf.set_fill_color(*DARK_NAVY)
    pdf.rect(0, 18, 210, 45, 'F')
    pdf.set_xy(0, 26)
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(*WHITE)
    pdf.cell(210, 9, "O5 Step 1: Feature Engineering Report", align="C", ln=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*LIGHT_BLUE)
    pdf.cell(210, 6, "iNHCES ML Pipeline -- Feature Matrix Construction", align="C", ln=True)
    pdf.cell(210, 6, "TETFund NRF 2025  |  ABU Zaria", align="C", ln=True)
    pdf.set_draw_color(*GOLD)
    pdf.set_line_width(0.8)
    pdf.line(30, 67, 180, 67)
    pdf.set_xy(LEFT, 75)
    for label, val in [
        ("Document:", "O5_01_Feature_Engineering.pdf"),
        ("Date:",     date.today().strftime("%d %B %Y")),
        ("Rows:",     f"{meta['n_rows']} (after differencing + NaN drop)"),
        ("Features:", f"{meta['n_features']} engineered features"),
        ("Target:",   f"cost_per_sqm (NGN/sqm) -- RED synthetic proxy"),
        ("Train:",    f"{meta['train_rows']} rows ({meta['train_years']})"),
        ("Val:",      f"{meta['val_rows']} rows ({meta['val_years']})"),
        ("Test:",     f"{meta['test_rows']} rows ({meta['test_years']})"),
        ("Next:",     "O5 Step 2 -- Model Benchmarking (05_model_benchmarking.py)"),
    ]:
        pdf.set_x(LEFT)
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*DARK_NAVY)
        pdf.cell(38, 6, sanitize(label))
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*DARK_GREY)
        pdf.cell(PAGE_W - 38, 6, sanitize(str(val)), ln=True)

    _ds_page(pdf, 'amber',
        "DATA SOURCE: AMBER/RED -- O2 macro data (World Bank GREEN; EIA+FX RED synthetic). "
        "Housing cost target is RED synthetic proxy.",
        (
            "WHAT IS REAL:\n"
            "  * GDP growth, CPI inflation, lending rate: World Bank live data (GREEN)\n"
            "  * Feature transformation logic: stationarity-informed (O2 ADF+KPSS findings)\n"
            "  * I(1) -> first difference; I(2)* -> pct change -- correct econometric practice\n\n"
            "WHAT IS SYNTHETIC (RED):\n"
            "  * Brent crude, NGN/USD/EUR/GBP: synthetic fallback (EIA/FRED keys not set)\n"
            "  * cost_per_sqm target: synthetic proxy formula -- NOT real NIQS data\n"
            "  * All model results derived from this matrix are indicative only\n\n"
            "REPLACEMENT OBLIGATION:\n"
            "  Set EIA_API_KEY and FRED_API_KEY and re-run O2 fetch scripts\n"
            "  Replace cost_per_sqm with real NIQS unit rate survey data\n"
            "  Re-run this script and all O5 scripts with real data before P3/P5 submission"
        )
    )

    # Section 1: Feature List
    pdf.add_page()
    pdf.section_title("1. Feature Engineering Summary")
    fw = [12, 38, 22, PAGE_W - 72]
    pdf.thead(["#", "Feature Name", "Transform", "Description"], fw)
    feature_info = [
        ("d_gdp_growth_pct",           "First diff",   "DELTA GDP growth rate (pp change year-on-year). I(1) -> stationary."),
        ("d_cpi_annual_pct",           "First diff",   "DELTA CPI inflation rate (pp change). I(1) -> stationary."),
        ("d_lending_rate_pct",         "First diff",   "DELTA commercial lending rate (pp change). I(1) -> stationary."),
        ("d_brent_usd_barrel",         "First diff",   "DELTA Brent crude price (USD change). I(1) -> stationary."),
        ("ret_ngn_usd",                "Pct change",   "NGN/USD return (% change). I(2)* -> stationary via returns."),
        ("ret_ngn_eur",                "Pct change",   "NGN/EUR return (% change). I(2)* -> stationary via returns."),
        ("ret_ngn_gbp",                "Pct change",   "NGN/GBP return (% change). I(2)* -> stationary via returns."),
        ("lag1_d_gdp_growth_pct",      "Lag-1 diff",   "Lagged DELTA GDP growth. Captures delayed policy effects."),
        ("lag1_d_cpi_annual_pct",      "Lag-1 diff",   "Lagged DELTA CPI. Inflation has 6-12 month pass-through to construction."),
        ("lag1_d_lending_rate_pct",    "Lag-1 diff",   "Lagged DELTA lending rate. Credit cost affects project starts with delay."),
        ("lag1_d_brent_usd_barrel",    "Lag-1 diff",   "Lagged DELTA Brent. Diesel cost effect on construction plant."),
        ("lag1_ret_ngn_usd",           "Lag-1 ret",    "Lagged NGN/USD return. Import material procurement has 1-2 month lag."),
        ("lag1_ret_ngn_eur",           "Lag-1 ret",    "Lagged NGN/EUR return. European equipment procurement lag."),
        ("lag1_ret_ngn_gbp",           "Lag-1 ret",    "Lagged NGN/GBP return. UK-sourced materials lag."),
    ]
    for i, (fname, transform, desc) in enumerate(feature_info):
        if fname in feature_cols:
            pdf.mrow([str(i+1), fname, transform, desc], fw, fill=(i % 2 == 1))
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 4.5, sanitize(
        "Table 1: Engineered features. I(1) series differenced per O2 ADF+KPSS findings. "
        "I(2)* series use returns. Lags capture delayed macroeconomic transmission effects."
    ))
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(2)

    # Section 2: Target variable
    pdf.section_title("2. Target Variable: cost_per_sqm")
    pdf.set_fill_color(250, 220, 220)
    pdf.set_draw_color(180, 0, 0)
    pdf.set_line_width(0.4)
    pdf.set_font("Helvetica", "B", 8.5)
    pdf.set_text_color(140, 0, 0)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 5,
        sanitize("DATA SOURCE: RED -- cost_per_sqm is a SYNTHETIC PROXY. "
                 "Must be replaced with real NIQS unit rate data before publication."),
        border=1, fill=True)
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(2)

    pdf.set_font("Helvetica", "", 9.5)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 5.2, sanitize(
        f"Synthetic range: NGN {meta['target_min']:,.0f} -- {meta['target_max']:,.0f} / sqm\n"
        f"Mean: NGN {meta['target_mean']:,.0f} / sqm | Std Dev: NGN {meta['target_std']:,.0f} / sqm\n"
        "Formula: base_cost x FX_adjustment^0.42 x CPI_adjustment^1.5 x Brent_adjustment + noise\n"
        "Reflects O2 SHAP ranking: NGN/USD dominance (45%), CPI (25.5%), Brent (10.9%)."
    ))
    pdf.ln(2)

    # Section 3: Split summary
    pdf.section_title("3. Train / Val / Test Split")
    sw = [30, 25, 25, PAGE_W - 80]
    pdf.thead(["Split", "Years", "Rows", "Purpose"], sw)
    pdf.trow(["Train", meta['train_years'], str(meta['train_rows']),
              "Model training + cross-validation"], sw, fill=False)
    pdf.trow(["Validation", meta['val_years'],  str(meta['val_rows']),
              "Hyperparameter tuning + early stopping"], sw, fill=True)
    pdf.trow(["Test",       meta['test_years'], str(meta['test_rows']),
              "Final holdout evaluation (MAPE, R2, MAE)"], sw, fill=False)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 4.5, sanitize(
        "Table 2: Time-series split (no shuffling). "
        "Train: 2002-2019 (after 2 NaN rows from lag-2). Val: 2020-2021. Test: 2022-2024."
    ))
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(2)

    pdf.output(out_path)
    print(f"  [PDF] O5_01_Feature_Engineering.pdf -> {out_path}  (pages: {pdf.page})")
    return out_path


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    print("\n=== O5 Step 1: Feature Engineering ===")
    frames  = load_o2_data()
    merged  = merge_frames(frames)
    merged  = standardise_columns(merged)
    merged  = apply_transformations(merged)
    merged  = build_target(merged)
    fm, feature_cols = build_feature_matrix(merged)
    train, val, test = train_val_test_split(fm)
    meta    = save_outputs(fm, train, val, test, feature_cols, merged)
    pdf_path = generate_pdf(meta, feature_cols, fm)
    print(f"\n[OK] Feature matrix: {len(fm)} rows x {len(feature_cols)} features")
    print(f"     Files: feature_matrix.csv | train/val/test_set.csv | feature_metadata.json")
    print(f"     PDF:   O5_01_Feature_Engineering.pdf")
    print(f"     Next:  python 05_model_benchmarking.py")
    return fm, feature_cols, train, val, test, meta


if __name__ == "__main__":
    main()
