"""
iNHCES O2 Step 1 -- World Bank Macroeconomic Data Fetcher
Fetches Nigeria GDP growth, CPI inflation, and lending rate from the public
World Bank Data API. No API key required.

Indicators:
  NY.GDP.MKTP.KD.ZG  GDP growth (annual %)
  FP.CPI.TOTL.ZG     CPI inflation (annual %)
  FR.INR.LEND        Lending interest rate (%)

Outputs:
  data/raw/worldbank_nigeria.csv                -- raw long-format data
  data/processed/worldbank_nigeria_processed.csv -- wide-format, year-indexed
  O2_01_WorldBank_Macro_Nigeria.pdf             -- PDF report with charts

Run: .venv\Scripts\python.exe 02_macro_analysis\fetch_worldbank.py
API: https://api.worldbank.org/v2  (public, no key required)

TETFund NRF 2025 | Department of Quantity Surveying, ABU Zaria
"""

import sys
import os
import time
import tempfile

import requests
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import date

# ── Path: import DocPDF from 01_literature_review ─────────────────────────────
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, os.path.join(_ROOT, '01_literature_review'))

from generate_o1_pdfs import (
    DocPDF, sanitize, _ds_page,
    DARK_NAVY, GOLD, LIGHT_BLUE, WHITE, DARK_GREY, MID_GREY,
    PAGE_W, LEFT, LINE_H,
)

# ── Directories ───────────────────────────────────────────────────────────────
RAW_DIR  = os.path.join(_HERE, 'data', 'raw')
PROC_DIR = os.path.join(_HERE, 'data', 'processed')
for d in (RAW_DIR, PROC_DIR):
    os.makedirs(d, exist_ok=True)

# ── Indicator config ──────────────────────────────────────────────────────────
INDICATORS = {
    'NY.GDP.MKTP.KD.ZG': ('gdp_growth_pct',   'GDP Growth (Annual %)'),
    'FP.CPI.TOTL.ZG':    ('cpi_inflation_pct', 'CPI Inflation (Annual %)'),
    'FR.INR.LEND':       ('lending_rate_pct',  'Lending Interest Rate (%)'),
}
START_YEAR = 2000
END_YEAR   = 2024
WB_BASE    = 'https://api.worldbank.org/v2'


# ── Custom PDF class ──────────────────────────────────────────────────────────
class O2PDF(DocPDF):
    def header(self):
        self.set_fill_color(*DARK_NAVY)
        self.rect(0, 0, 210, 14, 'F')
        self.set_font("Helvetica", "B", 7)
        self.set_text_color(*WHITE)
        self.set_xy(5, 4)
        self.cell(PAGE_W, 6, sanitize(
            "iNHCES | TETFund NRF 2025 | Dept. of Quantity Surveying, ABU Zaria"
            "  |  O2 Step 1 - Macroeconomic Variable Analysis"
        ))
        self.set_text_color(*DARK_GREY)
        self.ln(16)


# ── Data fetch ────────────────────────────────────────────────────────────────
def fetch_indicator(code):
    """Fetch one World Bank indicator for Nigeria (NG). Returns list or None."""
    url = (f"{WB_BASE}/country/NG/indicator/{code}"
           f"?format=json&per_page=100&date={START_YEAR}:{END_YEAR}")
    try:
        resp = requests.get(url, timeout=25)
        resp.raise_for_status()
        payload = resp.json()
        if len(payload) < 2 or not payload[1]:
            return None
        return [
            {'year': int(r['date']),
             'value': float(r['value']) if r['value'] is not None else np.nan}
            for r in payload[1]
        ]
    except Exception as exc:
        print(f"  WARNING: Could not fetch {code}: {exc}")
        return None


def build_dataframe():
    """Fetch all indicators and merge into a wide DataFrame indexed by year."""
    df = pd.DataFrame({'year': list(range(START_YEAR, END_YEAR + 1))})
    fetch_ok = True
    for code, (col, _) in INDICATORS.items():
        rows = fetch_indicator(code)
        if rows is None:
            fetch_ok = False
            df[col] = np.nan
        else:
            tmp = pd.DataFrame(rows).rename(columns={'value': col})
            df = df.merge(tmp, on='year', how='left')
        time.sleep(0.3)
    return df.sort_values('year').reset_index(drop=True), fetch_ok


# ── Chart ─────────────────────────────────────────────────────────────────────
def make_chart(df):
    """Return path to a temp PNG of the three indicator time series."""
    fig, axes = plt.subplots(3, 1, figsize=(9, 7), sharex=True)
    fig.patch.set_facecolor('#F7F9FC')
    configs = [
        ('gdp_growth_pct',   'GDP Growth (Annual %)',       '#1A5276', '#D6EAF8'),
        ('cpi_inflation_pct','CPI Inflation (Annual %)',    '#922B21', '#FADBD8'),
        ('lending_rate_pct', 'Lending Interest Rate (%)',  '#1E8449', '#D5F5E3'),
    ]
    for ax, (col, label, colour, bg) in zip(axes, configs):
        ax.set_facecolor(bg)
        v = df.dropna(subset=[col])
        if not v.empty:
            ax.plot(v['year'], v[col], color=colour, linewidth=1.8,
                    marker='o', markersize=3.5, markerfacecolor='white',
                    markeredgecolor=colour, markeredgewidth=1.0)
            ax.fill_between(v['year'], v[col], alpha=0.15, color=colour)
        ax.axhline(0, color='#888888', linewidth=0.6, linestyle='--')
        ax.set_ylabel(label, fontsize=7.5, color=colour, fontweight='bold')
        ax.tick_params(labelsize=7)
        ax.spines[['top', 'right']].set_visible(False)
        ax.grid(axis='y', alpha=0.4, linewidth=0.5)
    axes[2].set_xlabel('Year', fontsize=8)
    fig.suptitle(
        'Nigeria Macroeconomic Indicators (2000-2024)\nSource: World Bank Data API (api.worldbank.org)',
        fontsize=9, fontweight='bold', color='#0F2850')
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    tmp = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    fig.savefig(tmp.name, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close(fig)
    return tmp.name


# ── PDF ───────────────────────────────────────────────────────────────────────
def generate_pdf(df, fetch_ok, chart_path):
    pdf = O2PDF("O2_01_WorldBank_Macro_Nigeria.pdf",
                "O2 Step 1 - World Bank Macro Data")

    # ── Cover ─────────────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.set_fill_color(*DARK_NAVY)
    pdf.rect(0, 18, 210, 55, 'F')
    pdf.set_xy(0, 26)
    pdf.set_font("Helvetica", "B", 15)
    pdf.set_text_color(*WHITE)
    pdf.cell(210, 9, "Nigeria Macroeconomic Indicators", align="C", ln=True)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(200, 215, 235)
    pdf.cell(210, 7, "World Bank Data API -- O2 Step 1 Data Collection Report",
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

    n_missing  = int(df[list(df.columns[1:])].isna().sum().sum())
    status_str = "LIVE DATA -- World Bank API" if fetch_ok else "PARTIAL -- some indicators unavailable"
    pdf.set_xy(LEFT, 84)
    for label, val in [
        ("Document:",      "O2_01_WorldBank_Macro_Nigeria.pdf"),
        ("Objective:",     "O2 -- Macroeconomic Variable Analysis (TETFund NRF 2025)"),
        ("Data source:",   "World Bank Data API (api.worldbank.org/v2) -- no key required"),
        ("Country:",       "Nigeria (NG / NGA)"),
        ("Indicators:",    "GDP Growth, CPI Inflation, Lending Interest Rate (3 series)"),
        ("Date range:",    f"{START_YEAR}-{END_YEAR} (annual, {END_YEAR - START_YEAR + 1} observations)"),
        ("Missing cells:", f"{n_missing}" if n_missing else "None detected"),
        ("Fetch status:",  status_str),
        ("Raw CSV:",       "02_macro_analysis/data/raw/worldbank_nigeria.csv"),
        ("Processed CSV:", "02_macro_analysis/data/processed/worldbank_nigeria_processed.csv"),
        ("Date:",          date.today().strftime("%d %B %Y")),
    ]:
        pdf.set_x(LEFT)
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*DARK_NAVY)
        pdf.cell(42, 6.2, sanitize(label))
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*DARK_GREY)
        pdf.cell(PAGE_W - 42, 6.2, sanitize(val), ln=True)

    if not fetch_ok:
        pdf.ln(2)
        pdf.set_fill_color(255, 220, 180)
        pdf.set_draw_color(180, 80, 0)
        pdf.set_line_width(0.4)
        pdf.set_x(LEFT)
        pdf.set_font("Helvetica", "B", 8.5)
        pdf.set_text_color(140, 50, 0)
        pdf.multi_cell(PAGE_W, 5.5, sanitize(
            "  WARNING: One or more indicators could not be fetched from the World Bank API. "
            "Affected columns contain NaN. Verify internet connectivity and re-run."
        ), border=1, fill=True)
        pdf.set_text_color(*DARK_GREY)

    # ── Data Source Declaration ─────────────────────────────────────────────────────────
    _ds_page(pdf, 'green' if fetch_ok else 'amber',
        "DATA SOURCE: LIVE -- World Bank Data API (api.worldbank.org/v2)" if fetch_ok
        else "DATA SOURCE WARNING -- One or more World Bank indicators could not be fetched",
        (
            "SOURCE: World Bank Data API (api.worldbank.org/v2)\n"
            "No API key required. Data fetched programmatically in fetch_worldbank.py.\n\n"
            "SERIES FETCHED:\n"
            "  * NY.GDP.MKTP.KD.ZG -- Nigeria GDP Growth Rate (Annual %) -- World Bank National Accounts\n"
            "  * FP.CPI.TOTL.ZG    -- Nigeria CPI Inflation (Annual %) -- World Bank / IMF IFS\n"
            "  * FR.INR.LEND        -- Nigeria Lending Interest Rate (%) -- World Bank / CBN\n\n"
            "COVERAGE: Annual, 2000-2024 (up to 25 observations per series).\n"
            "FETCH STATUS: " + ("LIVE -- all series retrieved from World Bank API at time of generation."
            if fetch_ok else
            "PARTIAL -- one or more series unavailable. NaN cells present. "
            "Verify internet connectivity and re-run.") + "\n\n"
            "WHAT IS REAL IN THIS DOCUMENT:\n"
            "  * All numeric values were retrieved directly from the World Bank Data API. "
            "No values were invented, estimated, or substituted by an AI model.\n"
            "  * The data is the official World Bank time series for Nigeria -- the same "
            "data available at data.worldbank.org.\n\n"
            "WHAT IS AI-AUTHORED (methodology/framing only, not the data):\n"
            "  * The iNHCES relevance explanations, summary statistics layout, and chart "
            "design were authored by GitHub Copilot / Claude as part of the iNHCES "
            "TETFund NRF 2025 research pipeline at ABU Zaria.\n\n"
            "CITATION FOR USE:\n"
            "  World Bank (2025). World Development Indicators: Nigeria. "
            "World Bank Data API. Retrieved " + date.today().strftime("%d %B %Y") + ". "
            "api.worldbank.org/v2/country/NG/indicator/"
        )
    )

    # ── Indicators overview ─────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.section_title("Indicators Overview and iNHCES Relevance")
    pdf.body(
        "Three annual macroeconomic indicators were fetched from the World Bank Data API "
        "for Nigeria (country code: NG) covering 2000-2024. These are mandatory iNHCES ML "
        "input features because they directly drive construction material costs and housing "
        "investment volumes."
    )
    iw = [55, 40, 91]
    pdf.thead(["WB Indicator Code", "Column Name", "iNHCES Relevance"], iw)
    for i, (code, (col, label)) in enumerate(INDICATORS.items()):
        desc = {
            'gdp_growth_pct':   "Economic output signal; expansion drives construction demand and input costs",
            'cpi_inflation_pct':"Direct proxy for materials price escalation and NGN purchasing power erosion",
            'lending_rate_pct': "Cost of capital; high rates suppress housing investment and increase project finance costs",
        }[col]
        pdf.mrow((code, col, label + " -- " + desc), iw, fill=(i % 2 == 0), bold_first=True)

    pdf.ln(4)
    pdf.section_title("Summary Statistics (2000-2024)")
    col_names   = [c[0] for c in INDICATORS.values()]
    col_labels  = [c[1] for c in INDICATORS.values()]
    sw = [50, 22, 22, 22, 22, 22, 26]
    pdf.thead(["Indicator", "Min", "Max", "Mean", "Median", "Std Dev", "Latest (yr)"], sw)
    for col_name, label in zip(col_names, col_labels):
        s = df[col_name].dropna()
        latest_yr = int(df.loc[df[col_name].notna(), 'year'].max()) if not s.empty else None
        lv = df.loc[df['year'] == latest_yr, col_name].values[0] if latest_yr else np.nan
        pdf.mrow((
            label,
            f"{s.min():.2f}" if not s.empty else "N/A",
            f"{s.max():.2f}" if not s.empty else "N/A",
            f"{s.mean():.2f}" if not s.empty else "N/A",
            f"{s.median():.2f}" if not s.empty else "N/A",
            f"{s.std():.2f}" if not s.empty else "N/A",
            f"{lv:.2f} ({latest_yr})" if latest_yr else "N/A",
        ), sw, fill=True)

    # ── Chart ──────────────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.section_title("Time Series Chart -- Nigeria Macroeconomic Indicators (2000-2024)")
    pdf.body(
        "Annual values for GDP growth, CPI inflation, and lending interest rate. Key "
        "inflections: 2009 global financial crisis (GDP dip), 2016 Nigerian recession "
        "(GDP contraction to -1.6%), COVID-19 impact (2020), and the 2022-2024 inflation "
        "surge following fuel subsidy removal and NGN float policy."
    )
    pdf.ln(2)
    if os.path.exists(chart_path):
        pdf.image(chart_path, x=LEFT, y=None, w=PAGE_W)
    pdf.ln(3)
    pdf.info_box(
        "iNHCES interpretation: High CPI and elevated lending rates are the dominant "
        "cost-push signals for construction material price escalation. GDP growth is a "
        "leading demand indicator. These three variables will be tested for stationarity "
        "(ADF/KPSS) in 02_macro_analysis/stationarity_analysis.py before ML model inclusion."
    )

    # ── Annual data table ──────────────────────────────────────────────────────
    pdf.add_page()
    pdf.section_title("Annual Data Table (2000-2024)")
    pdf.body(
        "Raw annual values as returned by the World Bank API. N/A = value not yet "
        "reported. The processed CSV (worldbank_nigeria_processed.csv) contains this "
        "table in wide format for downstream analysis."
    )
    pdf.ln(2)
    tw = [22, 55, 55, 54]
    pdf.thead(["Year", "GDP Growth (%)", "CPI Inflation (%)", "Lending Rate (%)"], tw)
    for i, row in df.iterrows():
        def fmt(v):
            return f"{v:.2f}" if pd.notna(v) else "N/A"
        pdf.mrow((
            str(int(row['year'])),
            fmt(row['gdp_growth_pct']),
            fmt(row['cpi_inflation_pct']),
            fmt(row['lending_rate_pct']),
        ), tw, fill=(i % 2 == 0))

    # ── Data quality & next steps ──────────────────────────────────────────────
    pdf.add_page()
    pdf.section_title("Data Quality Notes")
    pdf.bullet([
        "GDP growth and CPI inflation are generally complete for Nigeria 2000-2023; "
        "2024 values may be preliminary estimates pending IMF/World Bank reconciliation.",
        "Lending interest rate (FR.INR.LEND) has known gaps for Nigeria. The CBN "
        "Statistical Bulletin (cbn.gov.ng) is the definitive supplementary source.",
        "All values are annual averages. Monthly granularity is available from CBN "
        "and will be incorporated in the stationarity analysis step.",
        "Missing values in the processed CSV should be imputed using linear interpolation "
        "before ML training (handled in stationarity_analysis.py).",
    ])
    pdf.ln(3)
    pdf.section_title("Next Steps in the O2 Pipeline")
    ns_w = [36, 46, 104]
    pdf.thead(["Step", "Script", "Purpose"], ns_w)
    for i, row in enumerate([
        ("O2 Step 1", "fetch_eia_oil.py",        "Fetch Brent crude oil prices (USD/barrel) -- mandatory iNHCES feature"),
        ("O2 Step 1", "fetch_cbn_fx.py",         "Fetch NGN/USD, NGN/EUR, NGN/GBP exchange rates"),
        ("O2 Step 2", "stationarity_analysis.py","ADF/KPSS unit-root tests and differencing for all macro variables"),
        ("O2 Step 3", "var_vecm_model.py",        "VAR/VECM cointegration modelling of macro variable panel"),
        ("O2 Step 4", "shap_variable_selection.py","SHAP feature importance ranking for ML model variable selection"),
    ]):
        pdf.mrow(row, ns_w, fill=(i % 2 == 0))
    pdf.ln(4)
    pdf.info_box(
        "Source: World Bank Data API (https://api.worldbank.org/v2). "
        "World Bank Group Open Data. Licensed under CC BY 4.0. "
        "Indicator metadata: data.worldbank.org/indicator. "
        "Last accessed: " + date.today().strftime("%d %B %Y") + "."
    )

    out_path = os.path.join(_HERE, "O2_01_WorldBank_Macro_Nigeria.pdf")
    pdf.output(out_path)
    ok = os.path.exists(out_path) and os.path.getsize(out_path) > 3000
    print(f"{'[OK]' if ok else '[FAIL]'}  O2_01_WorldBank_Macro_Nigeria.pdf")
    return ok


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print("Fetching World Bank macro data for Nigeria (2000-2024)...")
    df, fetch_ok = build_dataframe()

    # Raw CSV (long format)
    raw_rows = []
    for code, (col, label) in INDICATORS.items():
        for _, row in df.iterrows():
            raw_rows.append({
                'country': 'Nigeria', 'iso3': 'NGA',
                'indicator_code': code, 'indicator_name': label,
                'year': int(row['year']), 'value': row[col],
            })
    raw_path = os.path.join(RAW_DIR, 'worldbank_nigeria.csv')
    pd.DataFrame(raw_rows).to_csv(raw_path, index=False)
    print(f"  Saved raw CSV:       {raw_path}")

    # Processed CSV (wide format)
    proc_path = os.path.join(PROC_DIR, 'worldbank_nigeria_processed.csv')
    df.to_csv(proc_path, index=False)
    print(f"  Saved processed CSV: {proc_path}")

    chart_path = make_chart(df)
    generate_pdf(df, fetch_ok, chart_path)
    try:
        os.unlink(chart_path)
    except OSError:
        pass


if __name__ == "__main__":
    main()

