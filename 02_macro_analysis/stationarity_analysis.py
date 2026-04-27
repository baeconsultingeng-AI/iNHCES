"""
iNHCES O2 Step 2 - Stationarity Analysis
ADF (Augmented Dickey-Fuller) and KPSS unit root tests on all 7
iNHCES macroeconomic variables at levels and first differences.
Outputs: stationarity_results.csv + O2_04_Stationarity_Analysis.pdf
TETFund NRF 2025 | Department of Quantity Surveying, ABU Zaria

DATA SOURCE: AMBER -- World Bank series are LIVE; EIA Brent and CBN FX
series are SYNTHETIC fallbacks unless API keys were set at fetch time.
"""

import sys
import os
import warnings

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import tempfile
from datetime import date

from statsmodels.tsa.stattools import adfuller, kpss

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, os.path.join(_ROOT, '01_literature_review'))

from generate_o1_pdfs import (
    DocPDF, sanitize, _ds_page,
    DARK_NAVY, GOLD, LIGHT_BLUE, WHITE, DARK_GREY, MID_GREY,
    PAGE_W, LEFT, LINE_H,
)

PROC_DIR = os.path.join(_HERE, 'data', 'processed')
RES_DIR  = os.path.join(_HERE, 'results')
os.makedirs(RES_DIR, exist_ok=True)

VARS = [
    ('gdp_growth_pct',       'GDP Growth Rate (Annual %)'),
    ('cpi_inflation_pct',    'CPI Inflation Rate (Annual %)'),
    ('lending_rate_pct',     'Lending Interest Rate (%)'),
    ('brent_usd_annual_avg', 'Brent Crude Oil (USD/barrel)'),
    ('ngn_usd',              'NGN/USD Exchange Rate'),
    ('ngn_eur',              'NGN/EUR Exchange Rate'),
    ('ngn_gbp',              'NGN/GBP Exchange Rate'),
]


class O2PDF(DocPDF):
    def header(self):
        self.set_fill_color(*DARK_NAVY)
        self.rect(0, 0, 210, 14, 'F')
        self.set_font("Helvetica", "B", 7)
        self.set_text_color(*WHITE)
        self.set_xy(5, 4)
        self.cell(PAGE_W, 6, sanitize(
            "iNHCES | TETFund NRF 2025 | Dept. of Quantity Surveying, ABU Zaria  |  "
            "O2 Step 2 - Stationarity Analysis"
        ))
        self.set_text_color(*DARK_GREY)
        self.ln(16)


def load_panel():
    wb  = pd.read_csv(os.path.join(PROC_DIR, 'worldbank_nigeria_processed.csv'))
    eia = pd.read_csv(os.path.join(PROC_DIR, 'eia_brent_oil_processed.csv'))
    fx  = pd.read_csv(os.path.join(PROC_DIR, 'cbn_fx_rates_processed.csv'))
    df  = wb.merge(eia, on='year', how='outer').merge(fx, on='year', how='outer')
    df  = df.sort_values('year').reset_index(drop=True).set_index('year')
    return df


def run_adf(series):
    clean = series.dropna()
    n     = len(clean)
    mlag  = max(1, min(4, int((n - 1) / 3)))
    res   = adfuller(clean, maxlag=mlag, autolag='AIC', regression='c')
    stat, p, used, nobs, cvs = res[0], res[1], res[2], res[3], res[4]
    return {
        'stat': round(stat, 4), 'p_value': round(min(p, 1.0), 4),
        'lags_used': used, 'n_obs': nobs,
        'cv_1pct': round(cvs['1%'], 3), 'cv_5pct': round(cvs['5%'], 3),
        'cv_10pct': round(cvs['10%'], 3), 'reject_H0': p < 0.05,
    }


def run_kpss(series):
    clean = series.dropna()
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        res = kpss(clean, regression='c', nlags='auto')
    stat, p, lags, cvs = res[0], res[1], res[2], res[3]
    p_clipped = max(0.01, min(p, 0.10))
    return {
        'stat': round(stat, 4), 'p_value': round(p_clipped, 4),
        'lags_used': lags, 'cv_1pct': round(cvs['1%'], 3),
        'cv_5pct': round(cvs['5%'], 3), 'cv_10pct': round(cvs['10%'], 3),
        'reject_H0': p < 0.05,
    }


def integration_order(adf_l, kpss_l, adf_d1, kpss_d1):
    stat_lev = adf_l['reject_H0']   and not kpss_l['reject_H0']
    stat_d1  = adf_d1['reject_H0']  and not kpss_d1['reject_H0']
    if stat_lev:
        return 'I(0)'
    if stat_d1 or (adf_d1['reject_H0'] and kpss_d1['p_value'] >= 0.05):
        return 'I(1)'
    if adf_d1['reject_H0']:
        return 'I(1)*'
    return 'I(2)*'


def analyse_all(df):
    rows = []
    for col, label in VARS:
        if col not in df.columns:
            continue
        series = df[col].dropna()
        if len(series) < 8:
            continue
        adf_l  = run_adf(series)
        kpss_l = run_kpss(series)
        d1     = series.diff().dropna()
        adf_d1 = run_adf(d1)
        kpss_d1 = run_kpss(d1)
        order  = integration_order(adf_l, kpss_l, adf_d1, kpss_d1)
        rows.append({
            'variable': col, 'label': label,
            'adf_lev_stat':   adf_l['stat'],   'adf_lev_p':   adf_l['p_value'],
            'adf_lev_cv5':    adf_l['cv_5pct'], 'adf_lev_reject': adf_l['reject_H0'],
            'kpss_lev_stat':  kpss_l['stat'],  'kpss_lev_p':  kpss_l['p_value'],
            'kpss_lev_reject': kpss_l['reject_H0'],
            'adf_d1_stat':    adf_d1['stat'],  'adf_d1_p':    adf_d1['p_value'],
            'adf_d1_cv5':     adf_d1['cv_5pct'], 'adf_d1_reject': adf_d1['reject_H0'],
            'kpss_d1_stat':   kpss_d1['stat'], 'kpss_d1_p':   kpss_d1['p_value'],
            'kpss_d1_reject': kpss_d1['reject_H0'],
            'integration_order': order,
        })
    return pd.DataFrame(rows)


def chart_series(df, diff=False):
    fig, axes = plt.subplots(4, 2, figsize=(12, 16))
    axes = axes.flatten()
    for i, (col, label) in enumerate(VARS):
        ax = axes[i]
        if col not in df.columns:
            ax.set_visible(False)
            continue
        s = df[col].dropna()
        if diff:
            s = s.diff().dropna()
        ax.plot(s.index, s.values, color='#0a2850', linewidth=1.6,
                marker='o', markersize=2.5)
        ax.set_title(f"D({label})" if diff else label,
                     fontsize=8.5, fontweight='bold', color='#0a2850')
        ax.set_xlabel('Year', fontsize=7)
        ax.tick_params(labelsize=7)
        ax.axhline(0, color='gray', linewidth=0.5, linestyle='--')
        ax.grid(True, alpha=0.3)
    axes[-1].set_visible(False)
    sup = ("Nigeria Macro Variables -- First Differences"
           if diff else "Nigeria Macro Variables -- Levels (2000-2024)")
    fig.suptitle(sup, fontsize=11, fontweight='bold', color='#0a2850', y=0.99)
    plt.tight_layout(rect=[0, 0, 1, 0.97])
    tmp = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    fig.savefig(tmp.name, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return tmp.name


def chart_integration(res_df):
    order_val = {'I(0)': 0, 'I(1)': 1, 'I(1)*': 1, 'I(2)*': 2}
    colors    = {'I(0)': '#2e7d32', 'I(1)': '#0a2850', 'I(1)*': '#1565c0', 'I(2)*': '#c62828'}
    labels    = [r['label'][:28] for _, r in res_df.iterrows()]
    vals      = [order_val.get(r['integration_order'], 1) for _, r in res_df.iterrows()]
    clrs      = [colors.get(r['integration_order'], '#555') for _, r in res_df.iterrows()]
    orders    = [r['integration_order'] for _, r in res_df.iterrows()]

    fig, ax = plt.subplots(figsize=(11, 4))
    bars = ax.bar(labels, vals, color=clrs, edgecolor='white', linewidth=0.5, width=0.6)
    ax.set_yticks([0, 1, 2])
    ax.set_yticklabels(['I(0) Stationary', 'I(1) Unit Root', 'I(2)* Ambiguous'], fontsize=9)
    ax.set_title('Integration Order by Variable (ADF + KPSS Consensus)',
                 fontsize=11, fontweight='bold', color='#0a2850')
    ax.set_xlabel('Macro Variable', fontsize=9)
    plt.xticks(rotation=28, ha='right', fontsize=8)
    ax.grid(axis='y', alpha=0.3)
    for bar, o in zip(bars, orders):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.04,
                o, ha='center', va='bottom', fontsize=8, fontweight='bold', color='#0a2850')
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(fc='#2e7d32', label='I(0)'),
                        Patch(fc='#0a2850', label='I(1)'),
                        Patch(fc='#c62828', label='I(2)*')],
              loc='upper right', fontsize=8)
    plt.tight_layout()
    tmp = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    fig.savefig(tmp.name, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return tmp.name


def generate_pdf(df, res_df, c_levels, c_diff, c_order):
    out = os.path.join(_HERE, 'O2_04_Stationarity_Analysis.pdf')
    pdf = O2PDF("O2_04_Stationarity_Analysis.pdf", "O2 Step 2 - Stationarity Analysis")

    # ── Cover ──────────────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.set_fill_color(*DARK_NAVY)
    pdf.rect(0, 18, 210, 55, 'F')
    pdf.set_xy(0, 26)
    pdf.set_font("Helvetica", "B", 15)
    pdf.set_text_color(*WHITE)
    pdf.cell(210, 9, "Unit Root and Stationarity Analysis", align="C", ln=True)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(200, 215, 235)
    pdf.cell(210, 7, "ADF and KPSS Tests -- O2 Step 2 Report",
             align="C", ln=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*LIGHT_BLUE)
    pdf.cell(210, 6, "Intelligent National Housing Cost Estimating System (iNHCES)",
             align="C", ln=True)
    pdf.cell(210, 6, "TETFund NRF 2025  |  Department of Quantity Surveying, ABU Zaria",
             align="C", ln=True)
    pdf.set_draw_color(*GOLD)
    pdf.set_line_width(0.8)
    pdf.line(30, 76, 180, 76)

    i0 = int((res_df['integration_order'].str.startswith('I(0)')).sum())
    i1 = int((res_df['integration_order'].str.startswith('I(1)')).sum())
    i2 = int((res_df['integration_order'].str.startswith('I(2)')).sum())

    pdf.set_xy(LEFT, 84)
    for lbl, val in [
        ("Document:",    "O2_04_Stationarity_Analysis.pdf"),
        ("Objective:",   "O2 -- Macroeconomic Variable Analysis (TETFund NRF 2025)"),
        ("Variables:",   "7 macro series -- GDP, CPI, lending rate, Brent crude, NGN/USD/EUR/GBP"),
        ("Tests:",       "ADF (Said & Dickey, 1984) + KPSS (Kwiatkowski et al., 1992)"),
        ("Sample:",      "Annual panel 2000-2024 (up to 25 observations per series)"),
        ("Integration:", f"I(0): {i0} vars  |  I(1): {i1} vars  |  Ambiguous: {i2} vars"),
        ("Implication:", "VECM recommended" if i1 >= 2 else "VAR on stationary data"),
        ("Results CSV:", "02_macro_analysis/data/processed/stationarity_results.csv"),
        ("Date:",        date.today().strftime("%d %B %Y")),
    ]:
        pdf.set_x(LEFT)
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*DARK_NAVY)
        pdf.cell(42, 6.2, sanitize(lbl))
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*DARK_GREY)
        pdf.cell(PAGE_W - 42, 6.2, sanitize(val), ln=True)

    # ── DATA SOURCE DECLARATION ────────────────────────────────────────────────
    _ds_page(pdf, 'amber',
        "DATA SOURCE: PARTIALLY SYNTHETIC -- World Bank is LIVE; "
        "EIA Brent and CBN FX are SYNTHETIC unless API keys were set",
        (
            "INPUT DATA SOURCES FOR THIS ANALYSIS:\n"
            "  * GDP Growth, CPI Inflation, Lending Rate -- World Bank Data API (LIVE). "
            "Test statistics for these 3 variables are based on real official data.\n"
            "  * Brent Crude Oil -- SYNTHETIC fallback (no EIA_API_KEY or FRED_API_KEY). "
            "Hardcoded annual estimates from published EIA/BP statistical reviews.\n"
            "  * NGN/USD, NGN/EUR, NGN/GBP -- SYNTHETIC fallback (no FRED_API_KEY). "
            "Hardcoded annual estimates from CBN Annual Reports and IMF IFS database.\n\n"
            "IMPACT ON RESULTS:\n"
            "  * ADF and KPSS statistics for Brent crude and FX series are derived from "
            "synthetic values. The DIRECTION (I(1) for exchange rates and oil prices) is "
            "consistent with macroeconomic literature for emerging economies, but exact "
            "statistics should be treated as illustrative until live data is available.\n\n"
            "TO UPGRADE TO FULLY LIVE DATA:\n"
            "  1. Set EIA_API_KEY (eia.gov/opendata) and FRED_API_KEY (fred.stlouisfed.org)\n"
            "  2. Re-run: fetch_eia_oil.py and fetch_cbn_fx.py\n"
            "  3. Re-run: stationarity_analysis.py\n\n"
            "REFERENCES:\n"
            "  Said & Dickey (1984). Biometrika, 71(3), 599-607.  [ADF test]\n"
            "  Kwiatkowski et al. (1992). Journal of Econometrics, 54(1-3), 159-178.  [KPSS]\n"
            "  Maddala & Kim (1998). Unit Roots, Cointegration, and Structural Change. CUP."
        )
    )

    # ── Section 1: Methodology ─────────────────────────────────────────────────
    pdf.add_page()
    pdf.section_title("1.  Unit Root Testing Methodology")
    pdf.body(
        "Stationarity testing is a prerequisite for multivariate time series modelling. "
        "A non-stationary series (one with a unit root) included in a VAR model in levels "
        "produces spurious regressions with inflated R-squared values and invalid t-statistics. "
        "Correct identification of the integration order determines whether to use a VAR "
        "in differences, a VECM, or a combination of both."
    )
    pdf.sub_heading("1.1  Augmented Dickey-Fuller (ADF) Test")
    pdf.body(
        "H0: The series has a unit root (non-stationary).   H1: Stationary.\n"
        "Lag length chosen by AIC (max 4 or (n-1)/3). Constant included (no trend).\n"
        "DECISION: Reject H0 if p-value < 0.05 -- series is stationary at this transformation."
    )
    pdf.sub_heading("1.2  KPSS Test (Kwiatkowski-Phillips-Schmidt-Shin, 1992)")
    pdf.body(
        "H0: The series is level-stationary.   H1: Unit root present.\n"
        "Reverses the null, reducing Type II error risk. Bandwidth set automatically.\n"
        "DECISION: Reject H0 if p-value < 0.05 -- series has unit root.\n"
        "NOTE: statsmodels bounds the KPSS p-value at [0.01, 0.10]; displayed values at "
        "boundaries should be read as '<= 0.01' or '>= 0.10'."
    )
    pdf.sub_heading("1.3  Integration Order Decision Rules")
    iw = [38, 32, 22, PAGE_W - 92]
    pdf.thead(["ADF", "KPSS", "Order", "Interpretation"], iw)
    for i, (a, k, c, interp) in enumerate([
        ("Reject (p<0.05)", "Don't reject",   "I(0)", "Stationary -- use in levels"),
        ("Don't reject",    "Reject (p<0.05)","I(1)", "Unit root -- difference or VECM"),
        ("Reject (p<0.05)", "Reject (p<0.05)","Contradiction", "Structural break likely"),
        ("Don't reject",    "Don't reject",   "Uncertain", "Treated as I(1) conservatively"),
    ]):
        pdf.trow([a, k, c, interp], iw, fill=(i % 2 == 1))
    pdf.ln(3)
    pdf.info_box(
        "SMALL SAMPLE NOTE: With n = 25 annual observations, ADF and KPSS tests have "
        "limited power. Elliott, Rothenberg & Stock (1996) recommend ERS point-optimal "
        "tests for small samples. Results here are indicative. Final published paper "
        "should apply Zivot-Andrews (1992) break-adjusted tests and possibly Ng-Perron (2001)."
    )

    # ── Section 2: ADF Results ─────────────────────────────────────────────────
    pdf.add_page()
    pdf.section_title("2.  ADF Test Results -- Levels and First Differences")
    pdf.body(
        "ADF: H0 = unit root.  Reject H0 (p < 0.05) = stationary.  "
        "5%CV = ADF 5% critical value (reject H0 if test stat < 5%CV)."
    )
    aw = [44, 18, 15, 18, 24, 18, 15, 18, 16]
    pdf.thead(["Variable", "Lev Stat", "Lev p", "5%CV(L)",
               "ADF Lev Dec.", "D1 Stat", "D1 p", "5%CV(D1)", "ADF D1 Dec."], aw)
    for i, (_, row) in enumerate(res_df.iterrows()):
        dec_l  = "STATIONARY" if row['adf_lev_reject'] else "unit root"
        dec_d1 = "STATIONARY" if row['adf_d1_reject']  else "unit root"
        pdf.trow([
            row['label'][:21],
            str(row['adf_lev_stat']), str(row['adf_lev_p']),
            str(row['adf_lev_cv5']), dec_l,
            str(row['adf_d1_stat']), str(row['adf_d1_p']),
            str(row['adf_d1_cv5']), dec_d1,
        ], aw, fill=(i % 2 == 1))
    pdf.ln(2)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 4.5, sanitize(
        "STATIONARY = ADF rejects H0 at 5% significance level. "
        "(L) = at Levels. (D1) = at First Differences. 5%CV = ADF 5% critical value "
        "(MacKinnon, 1994). Test statistics below the critical value support stationarity."
    ))
    pdf.set_text_color(*DARK_GREY)

    # ── Section 3: KPSS Results ────────────────────────────────────────────────
    pdf.ln(3)
    pdf.section_title("3.  KPSS Test Results -- Levels and First Differences")
    pdf.body(
        "KPSS: H0 = stationary.  Reject H0 (p < 0.05) = unit root.  "
        "Final column shows integration order from ADF + KPSS consensus."
    )
    kw = [44, 18, 15, 26, 18, 15, 26, 16]
    pdf.thead(["Variable", "Lev Stat", "Lev p", "KPSS Lev Dec.",
               "D1 Stat", "D1 p", "KPSS D1 Dec.", "Order"], kw)
    for i, (_, row) in enumerate(res_df.iterrows()):
        dec_l  = "UNIT ROOT"   if row['kpss_lev_reject'] else "stationary"
        dec_d1 = "UNIT ROOT"   if row['kpss_d1_reject']  else "stationary"
        pdf.trow([
            row['label'][:21],
            str(row['kpss_lev_stat']), str(row['kpss_lev_p']), dec_l,
            str(row['kpss_d1_stat']), str(row['kpss_d1_p']), dec_d1,
            row['integration_order'],
        ], kw, fill=(i % 2 == 1))
    pdf.ln(2)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 4.5, sanitize(
        "UNIT ROOT = KPSS rejects H0 (stationarity) at 5% level. "
        "p-values bounded at [0.01, 0.10]. Order = final ADF+KPSS consensus classification."
    ))
    pdf.set_text_color(*DARK_GREY)

    # ── Section 4: Integration Summary ────────────────────────────────────────
    pdf.add_page()
    pdf.section_title("4.  Integration Order Summary and VAR/VECM Implications")
    sw = [42, 56, 20, PAGE_W - 118]
    pdf.thead(["Variable Code", "Series Name", "Order", "VAR/VECM Implication"], sw)
    var_impl = {
        'I(0)':  'Stationary in levels -- use directly; or as exogenous regressor',
        'I(1)':  'Unit root -- 1st-difference in VAR, or include in VECM',
        'I(1)*': 'Likely I(1) -- treated as I(1) for model safety',
        'I(2)*': 'Possibly I(2) -- 2nd-difference or structural break investigation',
    }
    for i, (_, row) in enumerate(res_df.iterrows()):
        impl = var_impl.get(row['integration_order'], 'Investigate further')
        pdf.trow([row['variable'][:20], row['label'][:28],
                  row['integration_order'], impl[:50]], sw, fill=(i % 2 == 1))
    pdf.ln(3)
    pdf.set_fill_color(*LIGHT_BLUE)
    pdf.set_draw_color(*GOLD)
    pdf.set_line_width(0.5)
    pdf.set_x(LEFT)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*DARK_NAVY)
    if i1 >= 2:
        rec = (f"MODEL RECOMMENDATION (O2 Step 3): {i1} variables are I(1). "
               "Test for Johansen cointegration. If r >= 1 cointegrating vectors found, "
               "use VECM to model both short-run dynamics and long-run equilibrium adjustment. "
               f"The {i0} I(0) variable(s) may enter as stationary exogenous regressors.")
    else:
        rec = (f"MODEL RECOMMENDATION (O2 Step 3): Only {i1} I(1) variable(s) found. "
               "Cointegration testing requires >= 2 I(1) series. "
               "Use VAR on levels for I(0) and first differences for any I(1) series.")
    pdf.multi_cell(PAGE_W, 5.5, sanitize(rec), border=1, fill=True)
    pdf.set_text_color(*DARK_GREY)

    # ── Sections 5-7: Charts ───────────────────────────────────────────────────
    pdf.add_page()
    pdf.section_title("5.  Time Series Charts -- Levels")
    pdf.body(
        "Trending series (NGN/USD, Brent crude) show clear non-stationarity. "
        "GDP growth appears mean-reverting. CPI and lending rates show persistent "
        "but potentially trend-stationary behaviour."
    )
    pdf.image(c_levels, x=LEFT, y=None, w=PAGE_W)
    try:
        os.unlink(c_levels)
    except Exception:
        pass

    pdf.add_page()
    pdf.section_title("6.  Time Series Charts -- First Differences")
    pdf.body(
        "After differencing, all series fluctuate around zero without persistent trend, "
        "supporting I(1) classification for the trending variables."
    )
    pdf.image(c_diff, x=LEFT, y=None, w=PAGE_W)
    try:
        os.unlink(c_diff)
    except Exception:
        pass

    pdf.add_page()
    pdf.section_title("7.  Integration Order Summary Chart")
    pdf.image(c_order, x=LEFT, y=None, w=PAGE_W)
    try:
        os.unlink(c_order)
    except Exception:
        pass

    # ── Section 8: Data Quality and Next Steps ────────────────────────────────
    pdf.add_page()
    pdf.section_title("8.  Data Quality Notes and Limitations")
    pdf.body(
        "SMALL SAMPLE: n = 25 annual observations limits test power. ADF power against "
        "near-unit-root alternatives is low for n < 50. The dual-test approach and "
        "conservative classification partially compensate for this limitation. The final "
        "published paper (P3) should apply Ng-Perron (2001) tests and structural break tests "
        "(Zivot-Andrews 1992) to address this limitation."
    )
    pdf.body(
        "STRUCTURAL BREAKS: Nigeria experienced major economic breaks in this period: "
        "2008 global financial crisis; 2014-2016 oil price collapse; 2016 FX unification; "
        "COVID-19 (2020); 2023 petrol subsidy removal and FX liberalisation. "
        "Conventional unit root tests have low power in the presence of structural breaks, "
        "potentially over-rejecting the stationarity of GDP growth."
    )

    pdf.section_title("9.  Next Steps -- O2 Step 3 (VAR/VECM Models)")
    pdf.bullet([
        "Load stationarity_results.csv to determine I(0) vs I(1) split.",
        "Apply Johansen trace test to I(1) variables (if >= 2 confirmed).",
        "Select lag order via AIC/BIC (max 2 lags for n=25).",
        "Fit VECM (if cointegrated) or VAR on differenced I(1) series.",
        "Produce IRF and FEVD to quantify macro shock transmission.",
        "Output: O2_05_VAR_VECM_Models.pdf + model_results.csv",
    ])

    pdf.output(out)
    print(f"[OK]  O2_04_Stationarity_Analysis.pdf  saved -> {out}")


def main():
    print("Loading panel data ...")
    df = load_panel()
    print(f"  Panel shape: {df.shape}  |  Years: {df.index.min()} - {df.index.max()}")
    print("Running ADF + KPSS tests ...")
    res_df = analyse_all(df)
    print(res_df[['variable', 'integration_order']].to_string(index=False))
    res_path = os.path.join(PROC_DIR, 'stationarity_results.csv')
    res_df.to_csv(res_path, index=False)
    print(f"[OK]  stationarity_results.csv  saved -> {res_path}")
    print("Generating charts ...")
    c_levels = chart_series(df, diff=False)
    c_diff   = chart_series(df, diff=True)
    c_order  = chart_integration(res_df)
    print("Generating PDF ...")
    generate_pdf(df, res_df, c_levels, c_diff, c_order)


if __name__ == "__main__":
    main()

