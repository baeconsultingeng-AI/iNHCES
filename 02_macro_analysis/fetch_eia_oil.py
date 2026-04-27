"""
iNHCES O2 Step 1 -- Brent Crude Oil Price Fetcher
Fetches monthly Brent crude oil spot prices (USD/barrel) with three-tier fallback:
  1. EIA API v1  (set env var EIA_API_KEY  -- free at eia.gov/opendata)
  2. FRED API    (set env var FRED_API_KEY -- free at fred.stlouisfed.org/docs/api)
  3. Synthetic   (hardcoded annual estimates with WARNING banner)

Outputs:
  data/raw/eia_brent_oil.csv                -- raw monthly/annual data
  data/processed/eia_brent_oil_processed.csv -- annual averages, year-indexed
  O2_02_Brent_Oil_Prices.pdf                -- PDF report with chart

Run: .venv\Scripts\python.exe 02_macro_analysis\fetch_eia_oil.py
EIA:  https://api.eia.gov/series/?api_key=KEY&series_id=RBRTE
FRED: https://api.stlouisfed.org/fred/series/observations?series_id=DCOILBRENTEU

TETFund NRF 2025 | Department of Quantity Surveying, ABU Zaria
"""

import sys
import os
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

START_YEAR = 2000
END_YEAR   = 2024

# ── Synthetic fallback: annual average Brent crude (USD/barrel) ───────────────
# Sources: EIA, BP Statistical Review, OPEC Annual Statistics
SYNTHETIC_ANNUAL = {
    2000: 28.5,  2001: 24.4,  2002: 25.0,  2003: 28.8,  2004: 38.3,
    2005: 54.6,  2006: 65.1,  2007: 72.5,  2008: 97.0,  2009: 61.7,
    2010: 79.6,  2011: 111.3, 2012: 111.6, 2013: 108.7, 2014: 98.9,
    2015: 52.4,  2016: 43.7,  2017: 54.2,  2018: 71.7,  2019: 64.2,
    2020: 41.8,  2021: 70.9,  2022: 99.0,  2023: 82.6,  2024: 80.0,
}


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
def fetch_eia(api_key):
    """Try EIA API v1. Returns (DataFrame monthly, 'EIA') or None."""
    url = (f"https://api.eia.gov/series/"
           f"?api_key={api_key}&series_id=RBRTE&out=json")
    try:
        resp = requests.get(url, timeout=25)
        resp.raise_for_status()
        js   = resp.json()
        data = js.get('series', [{}])[0].get('data', [])
        if not data:
            return None
        rows = []
        for period, value in data:
            try:
                yr  = int(str(period)[:4])
                mo  = int(str(period)[4:6]) if len(str(period)) >= 6 else 1
                val = float(value)
                rows.append({'year': yr, 'month': mo, 'brent_usd': val})
            except (ValueError, TypeError):
                continue
        if not rows:
            return None
        return pd.DataFrame(rows), 'EIA API (series: RBRTE)'
    except Exception as exc:
        print(f"  EIA API unavailable: {exc}")
        return None


def fetch_fred(api_key):
    """Try FRED API for DCOILBRENTEU. Returns (DataFrame monthly, 'FRED') or None."""
    url = (f"https://api.stlouisfed.org/fred/series/observations"
           f"?series_id=DCOILBRENTEU&api_key={api_key}&file_type=json"
           f"&observation_start={START_YEAR}-01-01"
           f"&observation_end={END_YEAR}-12-31")
    try:
        resp = requests.get(url, timeout=25)
        resp.raise_for_status()
        obs  = resp.json().get('observations', [])
        if not obs:
            return None
        rows = []
        for o in obs:
            try:
                val = float(o['value'])   # raises ValueError for '.'
                d   = o['date']           # "YYYY-MM-DD"
                rows.append({'year': int(d[:4]), 'month': int(d[5:7]), 'brent_usd': val})
            except (ValueError, TypeError):
                continue
        if not rows:
            return None
        return pd.DataFrame(rows), 'FRED API (series: DCOILBRENTEU)'
    except Exception as exc:
        print(f"  FRED API unavailable: {exc}")
        return None


def get_data():
    """
    Return (df_annual, df_monthly_or_none, source_label, is_synthetic).
    df_annual has columns: year, brent_usd_annual_avg.
    """
    eia_key  = os.environ.get('EIA_API_KEY', '').strip()
    fred_key = os.environ.get('FRED_API_KEY', '').strip()

    # Tier 1: EIA
    if eia_key:
        print("  Trying EIA API...")
        result = fetch_eia(eia_key)
        if result:
            df_m, src = result
            df_m   = df_m[(df_m['year'] >= START_YEAR) & (df_m['year'] <= END_YEAR)]
            df_ann = (df_m.groupby('year')['brent_usd']
                         .mean().reset_index()
                         .rename(columns={'brent_usd': 'brent_usd_annual_avg'}))
            print(f"  EIA OK: {len(df_m)} monthly observations")
            return df_ann, df_m, src, False

    # Tier 2: FRED
    if fred_key:
        print("  Trying FRED API...")
        result = fetch_fred(fred_key)
        if result:
            df_m, src = result
            df_m   = df_m[(df_m['year'] >= START_YEAR) & (df_m['year'] <= END_YEAR)]
            df_ann = (df_m.groupby('year')['brent_usd']
                         .mean().reset_index()
                         .rename(columns={'brent_usd': 'brent_usd_annual_avg'}))
            print(f"  FRED OK: {len(df_m)} monthly observations")
            return df_ann, df_m, src, False

    # Tier 3: Synthetic fallback
    print("  No API keys set. Using synthetic fallback data.")
    years  = list(range(START_YEAR, END_YEAR + 1))
    values = [SYNTHETIC_ANNUAL.get(y, np.nan) for y in years]
    df_ann = pd.DataFrame({'year': years, 'brent_usd_annual_avg': values})
    return df_ann, None, 'SYNTHETIC (hardcoded estimates -- replace with live data)', True


# ── Chart ─────────────────────────────────────────────────────────────────────
def make_chart(df_ann, df_monthly):
    """Return path to a temp PNG of Brent crude price chart."""
    fig, ax = plt.subplots(figsize=(9, 4))
    fig.patch.set_facecolor('#F7F9FC')
    ax.set_facecolor('#FDF5E6')

    if df_monthly is not None and not df_monthly.empty:
        # Monthly line
        dm = df_monthly.sort_values(['year', 'month']).copy()
        dm['period'] = dm['year'] + (dm['month'] - 1) / 12
        ax.plot(dm['period'], dm['brent_usd'], color='#8B4513', linewidth=0.8,
                alpha=0.5, label='Monthly')
        # Annual overlay
        ax.plot(df_ann['year'], df_ann['brent_usd_annual_avg'],
                color='#C0392B', linewidth=2.0, marker='o', markersize=4,
                markerfacecolor='white', markeredgecolor='#C0392B',
                markeredgewidth=1.2, label='Annual avg', zorder=5)
    else:
        ax.plot(df_ann['year'], df_ann['brent_usd_annual_avg'],
                color='#C0392B', linewidth=2.0, marker='o', markersize=5,
                markerfacecolor='white', markeredgecolor='#C0392B',
                markeredgewidth=1.5, label='Annual avg (synthetic)')
        ax.fill_between(df_ann['year'], df_ann['brent_usd_annual_avg'],
                        alpha=0.15, color='#C0392B')

    # Key events
    events = {2008: '2008 GFC', 2014: '2014 Oil crash', 2020: 'COVID-19', 2022: 'Ukraine conflict'}
    for yr, label in events.items():
        if START_YEAR <= yr <= END_YEAR:
            ax.axvline(yr, color='grey', linewidth=0.7, linestyle='--', alpha=0.6)
            ax.text(yr + 0.2, ax.get_ylim()[1] * 0.9 if ax.get_ylim()[1] > 0 else 90,
                    label, fontsize=6.5, color='grey', rotation=90, va='top')

    ax.set_xlabel('Year', fontsize=8)
    ax.set_ylabel('Brent Crude (USD/barrel)', fontsize=8)
    ax.set_title('Brent Crude Oil Spot Price (2000-2024)\nSource: ' +
                 ('EIA/FRED API' if df_monthly is not None else 'Synthetic fallback estimates'),
                 fontsize=9, fontweight='bold', color='#0F2850')
    ax.legend(fontsize=7.5, framealpha=0.7)
    ax.tick_params(labelsize=7)
    ax.spines[['top', 'right']].set_visible(False)
    ax.grid(axis='y', alpha=0.4, linewidth=0.5)
    fig.tight_layout()

    tmp = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    fig.savefig(tmp.name, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close(fig)
    return tmp.name


# ── PDF ───────────────────────────────────────────────────────────────────────
def generate_pdf(df_ann, source_label, is_synthetic, chart_path):
    pdf = O2PDF("O2_02_Brent_Oil_Prices.pdf", "O2 Step 1 - Brent Crude Oil Prices")

    # ── Cover ─────────────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.set_fill_color(*DARK_NAVY)
    pdf.rect(0, 18, 210, 55, 'F')
    pdf.set_xy(0, 26)
    pdf.set_font("Helvetica", "B", 15)
    pdf.set_text_color(*WHITE)
    pdf.cell(210, 9, "Brent Crude Oil Prices (2000-2024)", align="C", ln=True)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(200, 215, 235)
    pdf.cell(210, 7, "EIA / FRED Data -- O2 Step 1 Data Collection Report",
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

    pdf.set_xy(LEFT, 84)
    for label, val in [
        ("Document:",      "O2_02_Brent_Oil_Prices.pdf"),
        ("Objective:",     "O2 -- Macroeconomic Variable Analysis"),
        ("Series:",        "Brent Crude Oil Spot Price (USD/barrel, monthly average)"),
        ("Primary source:","EIA API v1 (series: RBRTE) -- set EIA_API_KEY env var"),
        ("Secondary:",     "FRED API (series: DCOILBRENTEU) -- set FRED_API_KEY env var"),
        ("Actual source:", source_label),
        ("Date range:",    f"{START_YEAR}-{END_YEAR}"),
        ("Raw CSV:",       "02_macro_analysis/data/raw/eia_brent_oil.csv"),
        ("Processed CSV:", "02_macro_analysis/data/processed/eia_brent_oil_processed.csv"),
        ("Date:",          date.today().strftime("%d %B %Y")),
    ]:
        pdf.set_x(LEFT)
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*DARK_NAVY)
        pdf.cell(42, 6.2, sanitize(label))
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*DARK_GREY)
        pdf.cell(PAGE_W - 42, 6.2, sanitize(val), ln=True)

    if is_synthetic:
        pdf.ln(2)
        pdf.set_fill_color(245, 210, 210)
        pdf.set_draw_color(140, 20, 20)
        pdf.set_line_width(0.5)
        pdf.set_x(LEFT)
        pdf.set_font("Helvetica", "B", 8.5)
        pdf.set_text_color(120, 10, 10)
        pdf.multi_cell(PAGE_W, 5.5, sanitize(
            "  DATA SOURCE: SYNTHETIC FALLBACK -- No API key was detected "
            "(EIA_API_KEY or FRED_API_KEY). The values used are hardcoded annual "
            "estimates based on published EIA/BP statistical reviews. "
            "To use live data: (1) Register free at eia.gov/opendata or "
            "fred.stlouisfed.org/docs/api, (2) set the env var, (3) re-run this script."
        ), border=1, fill=True)
        pdf.set_text_color(*DARK_GREY)
    else:
        pdf.ln(2)
        pdf.set_fill_color(200, 235, 200)
        pdf.set_draw_color(20, 90, 20)
        pdf.set_line_width(0.4)
        pdf.set_x(LEFT)
        pdf.set_font("Helvetica", "B", 8.5)
        pdf.set_text_color(20, 90, 20)
        pdf.cell(PAGE_W, 6, sanitize(
            f"  DATA SOURCE: LIVE -- Fetched from {source_label}"
        ), border=1, fill=True, ln=True)
        pdf.set_text_color(*DARK_GREY)

    # ── Data Source Declaration ──────────────────────────────────────────────────
    _ds_page(pdf, 'amber' if is_synthetic else 'green',
        "DATA SOURCE: SYNTHETIC FALLBACK -- Hardcoded estimates (no API key set)"
        if is_synthetic else
        f"DATA SOURCE: LIVE -- {source_label}",
        (
            "INTENDED SOURCE: U.S. Energy Information Administration (EIA) Brent Crude Spot Price\n"
            "  Primary: EIA API v1 -- series RBRTE (monthly USD/barrel) -- requires EIA_API_KEY env var\n"
            "  Secondary: FRED API (St Louis Fed) -- series DCOILBRENTEU -- requires FRED_API_KEY env var\n\n"
            "ACTUAL SOURCE THIS RUN: " + source_label + "\n\n"
            + (
            "SYNTHETIC DATA WARNING:\n"
            "No API key (EIA_API_KEY or FRED_API_KEY) was detected at time of generation. "
            "All Brent crude values in this document are HARDCODED ANNUAL ESTIMATES "
            "taken from published EIA/BP Statistical Review of World Energy historical tables. "
            "These values are broadly accurate historical benchmarks but were entered manually "
            "by the script author -- they were NOT retrieved from a live API call.\n\n"
            "TO UPGRADE TO LIVE DATA:\n"
            "  1. Register free at eia.gov/opendata (EIA) or fred.stlouisfed.org (FRED)\n"
            "  2. Set env var: $env:EIA_API_KEY='your-key' (or FRED_API_KEY)\n"
            "  3. Re-run: .venv\\Scripts\\python.exe 02_macro_analysis\\fetch_eia_oil.py\n\n"
            if is_synthetic else
            "LIVE DATA CONFIRMED:\n"
            "Values were retrieved from the API at time of generation. "
            "No values were invented or substituted by an AI model.\n\n"
            ) +
            "WHAT IS AI-AUTHORED (methodology/framing only, not the data):\n"
            "  * iNHCES relevance explanations, chart design, and report structure were authored "
            "by GitHub Copilot / Claude as part of the iNHCES TETFund NRF 2025 pipeline.\n\n"
            "CITATION FOR USE:\n"
            "  EIA (2025). Brent Crude Oil Spot Price (RBRTE). U.S. Energy Information Administration. "
            "Retrieved " + date.today().strftime("%d %B %Y") + ". eia.gov/opendata  |  "
            "OR: Federal Reserve Bank of St. Louis (FRED). DCOILBRENTEU. fred.stlouisfed.org"
        )
    )

    # ── iNHCES relevance ──────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.section_title("iNHCES Relevance: Why Brent Crude Matters for Nigerian Housing Costs")
    pdf.body(
        "Nigeria is a petroleum-dependent economy. Brent crude oil price is a primary "
        "macroeconomic driver of construction costs through multiple channels:"
    )
    pdf.bullet([
        "PMS (petrol) price: Nigeria's domestic fuel prices are administratively linked to "
        "crude oil values. Higher crude = higher petrol price = higher transport costs for "
        "all construction materials (cement, iron rods, sand, granite).",
        "Government revenue: Oil revenue funds public construction budgets. Price crashes "
        "(2015-16, 2020) triggered austerity and construction sector contractions.",
        "Exchange rate transmission: Crude oil export revenue is the primary source of "
        "NGN/USD supply. Price shocks directly transmit to NGN depreciation, amplifying "
        "import-cost inflation for steel, aluminium, and electrical materials.",
        "Cement cost: Nigerian cement production uses heavy fuel oil (HFO) for kiln firing. "
        "Brent crude price changes are directly reflected in cement factory gate prices.",
        "SHAP analysis in O2 Step 4 will quantify Brent crude's marginal contribution to "
        "cost_per_sqm prediction versus other macro variables.",
    ])

    pdf.ln(3)
    pdf.section_title("Summary Statistics -- Annual Average Brent Crude (2000-2024)")
    s = df_ann['brent_usd_annual_avg'].dropna()
    sw = [60, 35, 35, 35, 21]
    pdf.thead(["Metric", "Value", "Year", "Context", "Source"], sw)
    rows = [
        ("Minimum",            f"${s.min():.2f}/bbl", str(int(df_ann.loc[df_ann['brent_usd_annual_avg'].idxmin(), 'year'])),
         "Post-dot-com / Iraq uncertainty", "Hist."),
        ("Maximum",            f"${s.max():.2f}/bbl", str(int(df_ann.loc[df_ann['brent_usd_annual_avg'].idxmax(), 'year'])),
         "Global commodity super-cycle peak", "Hist."),
        ("Mean (2000-2024)",   f"${s.mean():.2f}/bbl", "2000-2024", "25-year average", "Calc."),
        ("Std deviation",      f"${s.std():.2f}/bbl",  "2000-2024", "High volatility", "Calc."),
        ("2024 (latest)",      f"${df_ann.loc[df_ann['year']==2024, 'brent_usd_annual_avg'].values[0]:.2f}/bbl",
         "2024", "Post-Ukraine conflict level", "Est." if is_synthetic else "Live"),
    ]
    for i, row in enumerate(rows):
        pdf.mrow(row, sw, fill=(i % 2 == 0), bold_first=True)

    # ── Chart ──────────────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.section_title("Brent Crude Oil Price Chart (2000-2024)")
    pdf.body(
        "Annual average prices with key market inflection events annotated. "
        "The 2008 peak (USD 97/bbl) coincided with the highest Nigerian construction "
        "cost growth recorded in the NIQS Cost Index. The 2015-16 crash (-55%) "
        "triggered Nigeria's worst recession since 1987."
    )
    pdf.ln(2)
    if os.path.exists(chart_path):
        pdf.image(chart_path, x=LEFT, y=None, w=PAGE_W)
    pdf.ln(3)
    pdf.info_box(
        "For the iNHCES ML model: Brent crude price will be included as a continuous "
        "numeric feature (annual average, USD/barrel). The lag structure (t-1, t-2) "
        "will be tested in VAR/VECM modelling (O2 Step 3) to determine the optimal "
        "transmission delay from oil price shock to construction cost impact."
    )

    # ── Annual data table ──────────────────────────────────────────────────────
    pdf.add_page()
    pdf.section_title("Annual Average Brent Crude Oil Price Data Table")
    tw = [28, 60, 98]
    pdf.thead(["Year", "Annual Avg (USD/barrel)", "Market Context"], tw)
    contexts = {
        2000: "Post-1998 recovery; Iraq uncertainty",
        2001: "9/11 economic slowdown; OPEC cuts",
        2002: "Iraq War fears; Venezuela strike",
        2003: "Iraq invasion; supply disruptions",
        2004: "China demand surge; capacity constraints",
        2005: "Katrina; Nigerian Delta disruptions",
        2006: "Iran nuclear concerns; strong demand",
        2007: "Dollar weakness; supply fears",
        2008: "Super-cycle peak; GFC crash Q4",
        2009: "Global Financial Crisis demand collapse",
        2010: "Recovery; Arab Spring beginnings",
        2011: "Libya civil war; Fukushima impact",
        2012: "Iran sanctions; Eurozone debt crisis",
        2013: "Libyan supply outages",
        2014: "OPEC no-cut decision; shale surge",
        2015: "Price war; Nigeria enters recession",
        2016: "OPEC Vienna deal; NGN floated",
        2017: "OPEC-Russia cuts; Nigeria emerges recession",
        2018: "US Iran sanctions; WH pressure on OPEC",
        2019: "US-China trade war; Saudi attacks",
        2020: "COVID-19 demand collapse; brief negative WTI",
        2021: "Vaccine recovery; supply underinvestment",
        2022: "Russia-Ukraine war; global sanctions",
        2023: "OPEC+ voluntary cuts; demand softening",
        2024: "Geopolitical tensions; demand moderation",
    }
    src_note = "(estimated)" if is_synthetic else "(live)"
    for i, row in df_ann.iterrows():
        yr   = int(row['year'])
        val  = row['brent_usd_annual_avg']
        vstr = f"${val:.2f} {src_note}" if pd.notna(val) else "N/A"
        ctx  = contexts.get(yr, "")
        pdf.mrow((str(yr), vstr, ctx), tw, fill=(i % 2 == 0))

    if is_synthetic:
        pdf.ln(3)
        pdf.info_box(
            "DATA NOTE: Values above are hardcoded annual estimates based on EIA, "
            "BP Statistical Review of World Energy, and OPEC Annual Statistical Bulletin. "
            "To replace with live API data: set EIA_API_KEY or FRED_API_KEY environment "
            "variable and re-run fetch_eia_oil.py. Live data will auto-overwrite both "
            "the CSV files and this PDF."
        )

    out_path = os.path.join(_HERE, "O2_02_Brent_Oil_Prices.pdf")
    pdf.output(out_path)
    ok = os.path.exists(out_path) and os.path.getsize(out_path) > 3000
    print(f"{'[OK]' if ok else '[FAIL]'}  O2_02_Brent_Oil_Prices.pdf")
    return ok


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print("Fetching Brent crude oil price data...")
    df_ann, df_monthly, source_label, is_synthetic = get_data()

    # Raw CSV
    if df_monthly is not None:
        raw_path = os.path.join(RAW_DIR, 'eia_brent_oil.csv')
        df_monthly.to_csv(raw_path, index=False)
        print(f"  Saved raw CSV (monthly): {raw_path}")
    else:
        # Save synthetic annual data as raw CSV
        raw_path = os.path.join(RAW_DIR, 'eia_brent_oil.csv')
        df_ann.to_csv(raw_path, index=False)
        print(f"  Saved raw CSV (synthetic annual): {raw_path}")

    # Processed CSV (annual averages)
    proc_path = os.path.join(PROC_DIR, 'eia_brent_oil_processed.csv')
    df_ann.to_csv(proc_path, index=False)
    print(f"  Saved processed CSV: {proc_path}")

    chart_path = make_chart(df_ann, df_monthly)
    generate_pdf(df_ann, source_label, is_synthetic, chart_path)
    try:
        os.unlink(chart_path)
    except OSError:
        pass


if __name__ == "__main__":
    main()

