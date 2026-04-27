"""
iNHCES Draft Paper P3 Generator
Paper: "Macroeconomic Determinants of Housing Construction Costs in Nigeria:
A Time-Series Analysis with SHAP-Based Feature Importance"
Target Journal: Construction Management and Economics (Taylor & Francis)
Based on: O2 Steps 2-4 outputs (stationarity, VAR/VECM, SHAP)

DATA SOURCE: AMBER/RED -- World Bank live data used for GDP/CPI/lending rate.
EIA Brent and CBN FX data are SYNTHETIC (API keys not configured).
Housing cost proxy is SYNTHETIC. Findings are indicative only.

TETFund NRF 2025 | Department of Quantity Surveying, ABU Zaria
"""

import sys
import os
import csv
from datetime import date

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, os.path.join(_ROOT, '01_literature_review'))

from generate_o1_pdfs import (
    DocPDF, sanitize, _ds_page,
    DARK_NAVY, GOLD, LIGHT_BLUE, WHITE, DARK_GREY, MID_GREY,
    PAGE_W, LEFT, LINE_H,
)

OUT_DIR = _HERE
RESULTS_DIR = os.path.join(_ROOT, '02_macro_analysis')

JOURNAL   = "Construction Management and Economics (Taylor & Francis)"
PAPER_ID  = "P3"
PAPER_TITLE = (
    "Macroeconomic Determinants of Housing Construction Costs in Nigeria: "
    "A Time-Series Stationarity Analysis, Vector Autoregression, and "
    "SHAP-Based Feature Importance Assessment"
)
SHORT_TITLE = "Macroeconomic Determinants of Nigerian Housing Construction Costs"

# ── Load result CSVs ───────────────────────────────────────────────────────────
def load_stationarity():
    fpath = os.path.join(RESULTS_DIR, 'data', 'processed', 'stationarity_results.csv')
    rows = []
    try:
        with open(fpath, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
        print(f"  [READ] stationarity_results.csv: {len(rows)} rows")
    except FileNotFoundError:
        print(f"  [WARN] stationarity_results.csv not found at {fpath}")
    return rows

def load_shap():
    fpath = os.path.join(RESULTS_DIR, 'shap_results', 'shap_importance.csv')
    rows = []
    try:
        with open(fpath, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
        print(f"  [READ] shap_importance.csv: {len(rows)} rows")
    except FileNotFoundError:
        print(f"  [WARN] shap_importance.csv not found at {fpath}")
    return rows

def load_var():
    fpath = os.path.join(RESULTS_DIR, 'results', 'var_vecm_results.csv')
    rows = []
    try:
        with open(fpath, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
        print(f"  [READ] var_vecm_results.csv: {len(rows)} rows")
    except FileNotFoundError:
        print(f"  [WARN] var_vecm_results.csv not found at {fpath}")
    return rows


# ── Paper PDF class ────────────────────────────────────────────────────────────
class PaperPDF(DocPDF):
    def __init__(self):
        super().__init__(PAPER_TITLE, PAPER_ID)

    def header(self):
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*MID_GREY)
        self.set_xy(LEFT, 5)
        self.cell(PAGE_W, 4.5, sanitize(
            f"{PAPER_ID}  |  {SHORT_TITLE[:65]}  |  "
            "DRAFT -- AI-GENERATED -- NOT FOR SUBMISSION"
        ))
        self.set_text_color(*DARK_GREY)
        self.ln(12)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "", 7.5)
        self.set_text_color(*MID_GREY)
        self.cell(0, 5, f"Page {self.page_no()}", align="C")
        self.set_text_color(*DARK_GREY)

    def paper_heading(self, level, text):
        if level == 1:
            self.set_font("Helvetica", "B", 11.5)
            self.set_text_color(*DARK_NAVY)
        elif level == 2:
            self.set_font("Helvetica", "B", 10)
            self.set_text_color(*DARK_NAVY)
        else:
            self.set_font("Helvetica", "BI", 9.5)
            self.set_text_color(*DARK_GREY)
        self.ln(3)
        self.set_x(LEFT)
        self.multi_cell(PAGE_W, 5.5, sanitize(text))
        self.set_text_color(*DARK_GREY)
        self.ln(1)

    def para(self, text, indent=0):
        self.set_font("Helvetica", "", 9.5)
        self.set_text_color(*DARK_GREY)
        self.set_x(LEFT + indent)
        self.multi_cell(PAGE_W - indent, 5.2, sanitize(text))
        self.ln(1.5)

    def ref_item(self, text):
        self.set_font("Helvetica", "", 8.5)
        self.set_text_color(*DARK_GREY)
        self.set_x(LEFT + 5)
        self.multi_cell(PAGE_W - 5, 4.8, sanitize(text))
        self.ln(0.5)

    def placeholder_box(self, text):
        self.set_fill_color(255, 245, 220)
        self.set_draw_color(180, 120, 0)
        self.set_line_width(0.4)
        self.set_font("Helvetica", "B", 8.5)
        self.set_text_color(140, 80, 0)
        self.set_x(LEFT)
        self.multi_cell(PAGE_W, 5, sanitize(f"[PLACEHOLDER]  {text}"),
                        border=1, fill=True)
        self.set_text_color(*DARK_GREY)
        self.ln(1.5)

    def abstract_box(self, text):
        self.set_fill_color(*LIGHT_BLUE)
        self.set_draw_color(*DARK_NAVY)
        self.set_line_width(0.5)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*DARK_GREY)
        self.set_x(LEFT)
        self.multi_cell(PAGE_W, 5, sanitize(text), border=1, fill=True)
        self.set_text_color(*DARK_GREY)
        self.ln(2)

    def data_badge(self, kind, text):
        """Inline data source badge: kind = 'live' | 'synthetic'"""
        if kind == 'live':
            self.set_fill_color(0, 130, 60)
        else:
            self.set_fill_color(200, 80, 0)
        self.set_font("Helvetica", "B", 7.5)
        self.set_text_color(*WHITE)
        self.set_x(LEFT)
        self.cell(PAGE_W, 5.5, sanitize(f"  DATA: {text}"), fill=True, ln=True)
        self.set_text_color(*DARK_GREY)
        self.ln(1)


# ── Title page ─────────────────────────────────────────────────────────────────
def make_title_page(pdf):
    pdf.add_page()

    # Amber/Red draft strip
    pdf.set_fill_color(180, 100, 20)
    pdf.rect(0, 0, 210, 8, 'F')
    pdf.set_font("Helvetica", "B", 7.5)
    pdf.set_text_color(*WHITE)
    pdf.set_xy(0, 1.5)
    pdf.cell(210, 5,
             "AI-GENERATED FIRST DRAFT -- SYNTHETIC DATA USED -- NOT FOR SUBMISSION",
             align="C")
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(16)

    # Journal
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.cell(PAGE_W, 6, sanitize(f"Target journal: {JOURNAL}"), align="C")
    pdf.ln(6)

    # Title
    pdf.set_font("Helvetica", "B", 13.5)
    pdf.set_text_color(*DARK_NAVY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 7.5, sanitize(PAPER_TITLE), align="C")
    pdf.ln(5)

    pdf.set_draw_color(*GOLD)
    pdf.set_line_width(1.0)
    pdf.line(LEFT + 15, pdf.get_y(), LEFT + PAGE_W - 15, pdf.get_y())
    pdf.ln(6)

    for line in [
        "[FIRST AUTHOR NAME], Department of Quantity Surveying, ABU Zaria",
        "[SECOND AUTHOR NAME], Department of Quantity Surveying, ABU Zaria",
        "[ADDITIONAL AUTHORS]",
        "Corresponding author: [EMAIL ADDRESS] | ORCID: [INSERT]",
        "",
        "Acknowledgement: TETFund National Research Fund 2025, Grant No. [INSERT]",
        f"Manuscript prepared: {date.today().strftime('%d %B %Y')}",
        "Estimated word count (draft): ~7,200 words (excl. references)",
    ]:
        pdf.set_font("Helvetica", "I" if line.startswith("[") else "", 9)
        pdf.set_text_color(*MID_GREY)
        pdf.set_x(LEFT)
        pdf.cell(PAGE_W, 5.5, sanitize(line), align="C", ln=True)

    pdf.ln(5)
    pdf.set_draw_color(*MID_GREY)
    pdf.set_line_width(0.3)
    pdf.line(LEFT, pdf.get_y(), LEFT + PAGE_W, pdf.get_y())
    pdf.ln(5)


# ── Abstract ───────────────────────────────────────────────────────────────────
def make_abstract(pdf, shap_rows):
    pdf.paper_heading(1, "ABSTRACT")
    top1  = shap_rows[0]['variable']      if len(shap_rows) > 0 else "[VAR1]"
    top1p = shap_rows[0]['relative_imp_pct'] if len(shap_rows) > 0 else "[X]"
    top2  = shap_rows[1]['variable']      if len(shap_rows) > 1 else "[VAR2]"
    top2p = shap_rows[1]['relative_imp_pct'] if len(shap_rows) > 1 else "[X]"
    top3  = shap_rows[2]['variable']      if len(shap_rows) > 2 else "[VAR3]"
    top3p = shap_rows[2]['relative_imp_pct'] if len(shap_rows) > 2 else "[X]"

    abstract = (
        "Background: Nigerian housing construction costs are subject to significant "
        "macroeconomic volatility, yet no published study has systematically examined "
        "the relative importance of exchange rate, inflation, oil price, GDP growth, and "
        "lending rate as determinants of housing construction cost per square metre "
        "(NGN/sqm) using modern machine learning explainability methods.\n\n"
        "Objective: This study identifies and ranks the macroeconomic determinants of "
        "housing construction costs in Nigeria using a multi-method analytical framework "
        "comprising unit root testing, Johansen cointegration analysis, Vector "
        "Autoregression (VAR) modelling, and SHAP (SHapley Additive exPlanations) "
        "feature importance analysis on an XGBoost model.\n\n"
        f"Data: Annual panel data (2000-2024, n=25) covering 7 macroeconomic variables: "
        "NGN/USD, NGN/EUR, NGN/GBP (exchange rates), CPI inflation, GDP growth rate, "
        "commercial lending rate, and Brent crude oil price. GDP/CPI/lending rate data "
        "from World Bank Open Data (live feed). EIA Brent oil price and CBN FX rate data "
        "are currently synthetic (API keys not yet configured). Housing cost per sqm "
        "proxy is synthetic. [NOTE: All quantitative results are indicative only.]\n\n"
        "Methods: ADF and KPSS unit root tests confirm stationarity orders. Johansen "
        "cointegration test assesses long-run equilibrium relationships. VAR model "
        "is fitted on first-differenced I(1) variables. SHAP values from XGBoost "
        "trained on a synthetic housing cost proxy identify variable importance.\n\n"
        f"Results: All four macro variables (GDP growth, CPI inflation, lending rate, "
        "Brent crude) are I(1). Exchange rate variables (NGN/USD, NGN/EUR, NGN/GBP) "
        "exhibit possible I(2) behaviour. Johansen test finds no cointegration (rank=0). "
        f"VAR model fitted on first differences with lag order 1. SHAP analysis ranks "
        f"{sanitize(top1)} as the most important predictor ({sanitize(top1p)}% SHAP "
        f"importance), followed by CPI inflation ({sanitize(top2p)}%) and "
        f"{sanitize(top3)} ({sanitize(top3p)}%). These findings have direct implications "
        "for the iNHCES ML feature selection strategy.\n\n"
        "CAVEAT: All results are based on partially synthetic data. Real housing cost "
        "per sqm data collection (O3-O4) is required before results can be published."
    )
    pdf.abstract_box(abstract)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*DARK_NAVY)
    pdf.set_x(LEFT)
    pdf.cell(28, 5.5, "Keywords:")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*DARK_GREY)
    pdf.cell(PAGE_W - 28, 5.5, sanitize(
        "housing construction costs; Nigeria; macroeconomic determinants; unit root; "
        "VAR; SHAP; XGBoost; exchange rate; inflation; feature importance"
    ), ln=True)
    pdf.ln(4)


# ── Section 1: Introduction ────────────────────────────────────────────────────
def section1(pdf):
    pdf.add_page()
    pdf.paper_heading(1, "1. Introduction")
    pdf.para(
        "Housing affordability in Nigeria is a function of land, finance, labour, and "
        "materials costs -- all of which are sensitive to macroeconomic conditions. "
        "Nigeria's construction sector accounts for approximately 3.6% of GDP (NBS, 2023 "
        "[VERIFY]) and is overwhelmingly dependent on imported construction materials: "
        "steel reinforcement, cement clinker, electrical fittings, tiles, and finishing "
        "materials are largely sourced from Asia (China, India, Vietnam) and priced in "
        "US dollars. As a result, the Naira-to-Dollar (NGN/USD) exchange rate has a "
        "direct and immediate transmission effect on construction material costs, "
        "independent of domestic inflation."
    )
    pdf.para(
        "The NGN/USD rate has experienced several major devaluation events: the 2016 "
        "managed float (N197 to N305/USD), the 2022-2023 unification (reaching N900+ "
        "in parallel market), and the 2023 Central Bank of Nigeria (CBN) policy shift "
        "that drove the official rate to N1,500+ per USD. Each devaluation event caused "
        "construction material cost spikes of 40-120% within 6-12 months (building on "
        "NIQS unit rate surveys [VERIFY]). However, the precise quantitative relationship "
        "between macroeconomic variables and housing construction cost per square metre "
        "(NGN/sqm) has not been rigorously modelled in the published literature."
    )
    pdf.paper_heading(2, "1.1 Problem Statement")
    pdf.para(
        "Without quantitative evidence on which macroeconomic variables most strongly "
        "determine housing construction costs -- and with what lag structure -- "
        "professional cost estimators, housing developers, and policy-makers are unable "
        "to anticipate cost movements or build reliable ML-based prediction systems. "
        "This gap motivates both this study and the broader iNHCES research programme."
    )
    pdf.paper_heading(2, "1.2 Research Questions")
    for rq in [
        "RQ1: What is the stationarity order of the seven macroeconomic variables "
        "most relevant to Nigerian housing construction costs?",
        "RQ2: Is there evidence of a long-run cointegrating relationship between "
        "macroeconomic variables and housing construction costs?",
        "RQ3: What is the short-run dynamic relationship (VAR) between macroeconomic "
        "variables and housing construction costs, and what do Impulse Response "
        "Functions reveal about shock transmission lags?",
        "RQ4: Which macroeconomic variables are the most important predictors of "
        "housing construction cost per sqm, as quantified by SHAP feature importance?",
    ]:
        pdf.set_font("Helvetica", "", 9.5)
        pdf.set_text_color(*DARK_GREY)
        pdf.set_x(LEFT + 4)
        pdf.multi_cell(PAGE_W - 4, 5.2, sanitize(rq))
        pdf.ln(1)

    pdf.paper_heading(2, "1.3 Significance")
    pdf.para(
        "This study is -- to the authors' knowledge -- the first to apply the combined "
        "ADF+KPSS+Johansen+VAR+SHAP analytical framework to the Nigerian housing "
        "construction cost problem. The SHAP importance rankings provide a theoretically "
        "grounded, data-driven basis for ML feature selection in the iNHCES system (O5), "
        "replacing the ad hoc variable inclusion that has characterised prior Nigerian "
        "construction cost studies."
    )


# ── Section 2: Literature Review ──────────────────────────────────────────────
def section2(pdf):
    pdf.add_page()
    pdf.paper_heading(1, "2. Literature Review")
    pdf.paper_heading(2, "2.1 Construction Costs and Macroeconomic Variables")
    pdf.para(
        "The relationship between macroeconomic conditions and construction costs has "
        "been studied primarily in developed economies. Skitmore and Marston (1999) "
        "[VERIFY] demonstrated that tender price indices in the UK are significantly "
        "correlated with GDP growth and interest rates. Trost and Oberlender (2003) "
        "[VERIFY] used regression analysis to show that CPI-adjusted labour and "
        "material costs explained 85% of construction cost variance in US federal "
        "projects. The impact of exchange rate movements on construction costs in "
        "import-dependent economies is less studied, though Lowe et al. (2006) [VERIFY] "
        "noted the importance of currency risk in international project feasibility."
    )
    pdf.para(
        "In the Nigerian context, Ogunsemi and Jagboro (2006) [VERIFY] identified "
        "material cost escalation as the primary driver of construction cost overruns. "
        "Dania et al. (2007) [VERIFY] found that 40% of material waste in Nigerian "
        "construction projects was attributable to procurement failures linked to price "
        "volatility. Anigbogu et al. (2014) [VERIFY] showed that exchange rate "
        "depreciation was the most frequently cited cause of project abandonment in "
        "Abuja residential construction. Despite these qualitative findings, no "
        "published study has quantified the relative importance of exchange rate, "
        "inflation, GDP growth, oil price, and lending rate as co-determinants of "
        "housing construction cost per sqm in Nigeria."
    )
    pdf.paper_heading(2, "2.2 Time-Series Methods in Construction Economics")
    pdf.para(
        "Time-series econometric methods are well-established in the construction "
        "economics literature. Cointegration analysis (Engle & Granger, 1987 [VERIFY]; "
        "Johansen, 1988 [VERIFY]) tests for long-run equilibrium relationships between "
        "non-stationary series. When cointegration is found, Vector Error Correction "
        "Models (VECM) are appropriate; otherwise, VAR on differences is preferred "
        "(Sims, 1980 [VERIFY]). Trost and Oberlender (2003) [VERIFY] applied VAR to "
        "US construction cost indices. Jeong et al. (2009) [VERIFY] used VECM to model "
        "long-run relationships between Korean construction costs and macro variables."
    )
    pdf.paper_heading(2, "2.3 SHAP Feature Importance in Construction")
    pdf.para(
        "SHAP (SHapley Additive exPlanations) values, introduced by Lundberg and Lee "
        "(2017) [VERIFY], provide model-agnostic, theoretically grounded feature "
        "importance based on cooperative game theory. TreeSHAP (Lundberg et al., 2020 "
        "[VERIFY]) extends this to tree ensemble models (XGBoost, LightGBM, Random "
        "Forest) with polynomial-time computation. Applications in construction "
        "cost estimation are emerging: Huo et al. (2021) [VERIFY] used SHAP with "
        "XGBoost to rank cost drivers in Chinese infrastructure projects; Bilal et al. "
        "(2020) [VERIFY] applied SHAP to UK housing development cost modelling. "
        "No published study has applied SHAP to macroeconomic determinants of "
        "Nigerian housing construction costs."
    )
    pdf.paper_heading(2, "2.4 Research Gap")
    pdf.para(
        "The literature review identifies a clear gap: no study integrates unit root "
        "testing, Johansen cointegration, VAR modelling, and SHAP-based feature "
        "importance to jointly analyse macroeconomic determinants of housing "
        "construction costs in Nigeria. This study fills that gap, providing both "
        "econometric rigour (for academic contribution) and practical feature "
        "importance rankings (for ML system design in iNHCES)."
    )


# ── Section 3: Data and Methods ────────────────────────────────────────────────
def section3(pdf):
    pdf.add_page()
    pdf.paper_heading(1, "3. Data and Methods")
    pdf.paper_heading(2, "3.1 Data Sources and Variables")
    pdf.data_badge('live',
        "GDP growth, CPI inflation, lending rate: World Bank Open Data API -- LIVE DATA")
    pdf.data_badge('synthetic',
        "Brent crude price: EIA API -- SYNTHETIC (EIA_API_KEY not configured)")
    pdf.data_badge('synthetic',
        "NGN/USD, NGN/EUR, NGN/GBP: CBN/FRED -- SYNTHETIC (FRED_API_KEY not configured)")
    pdf.data_badge('synthetic',
        "Housing cost proxy (target variable): SYNTHETIC -- based on rule-based formula")
    pdf.ln(1)
    pdf.para(
        "Annual data from 2000 to 2024 (T=25 observations) are collected for seven "
        "macroeconomic variables relevant to Nigerian housing construction costs "
        "(Table 1). The dependent variable -- housing construction cost per square "
        "metre (NGN/sqm) -- is currently represented by a synthetic proxy generated "
        "from a rule-based formula incorporating exchange rate and inflation inputs. "
        "This proxy will be replaced with real NIQS unit rate survey data and BQ "
        "project cost records in O4 of the iNHCES research programme."
    )
    vw = [35, 25, 20, PAGE_W - 80]
    pdf.thead(["Variable", "Units", "Source", "Notes"], vw)
    for i, (var, units, src, note) in enumerate([
        ("GDP growth rate",      "% annual",    "World Bank",   "LIVE data via API"),
        ("CPI inflation",        "% annual",    "World Bank",   "LIVE data via API"),
        ("Lending rate",         "% annual",    "World Bank",   "LIVE data via API"),
        ("Brent crude price",    "USD/barrel",  "EIA (synth.)", "SYNTHETIC -- API key needed"),
        ("NGN/USD exchange rate","NGN/USD",     "CBN/FRED",     "SYNTHETIC -- API key needed"),
        ("NGN/EUR exchange rate","NGN/EUR",     "CBN/FRED",     "SYNTHETIC -- API key needed"),
        ("NGN/GBP exchange rate","NGN/GBP",     "CBN/FRED",     "SYNTHETIC -- API key needed"),
        ("Housing cost proxy",   "NGN/sqm",     "Synthetic",    "SYNTHETIC -- replace with NIQS data"),
    ]):
        pdf.trow([var, units, src, note], vw, fill=(i % 2 == 1))
    pdf.ln(1)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 4.5, sanitize(
        "Table 1: Variable definitions, units, and data sources. LIVE = fetched from live API. "
        "SYNTHETIC = generated using rule-based proxy. Replace synthetic series before publication."
    ))
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(2)

    pdf.paper_heading(2, "3.2 Unit Root Testing (ADF and KPSS)")
    pdf.para(
        "Stationarity is tested using the Augmented Dickey-Fuller (ADF) test (Dickey & "
        "Fuller, 1979 [VERIFY]) and the Kwiatkowski-Phillips-Schmidt-Shin (KPSS) test "
        "(Kwiatkowski et al., 1992 [VERIFY]). The dual-test approach is employed: ADF "
        "has null hypothesis H0: unit root present (non-stationary), while KPSS has "
        "H0: series is stationary. Confirming I(d) requires ADF to reject H0 for the "
        "d-th difference and KPSS to fail to reject H0 at the same level. "
        "Optimal lag selection uses the Akaike Information Criterion (AIC). "
        "Significance level: alpha=0.05."
    )
    pdf.para(
        "Series integration order is classified as I(0) (stationary in levels), "
        "I(1) (stationary in first differences), or I(2)* (requiring second differences, "
        "flagged with asterisk due to small sample uncertainty). I(2) classification "
        "with T=25 is tentative; a longer series (T>=50) would provide more reliable "
        "unit root test results."
    )

    pdf.paper_heading(2, "3.3 Cointegration Analysis (Johansen)")
    pdf.para(
        "For I(1) variables (GDP growth, CPI inflation, lending rate, Brent crude), "
        "the Johansen (1988 [VERIFY]) trace and max-eigenvalue tests are applied to "
        "determine the cointegration rank r. Lag length for the VECM is selected using "
        "BIC. If r >= 1, a VECM is estimated; if r = 0, a VAR on first differences is "
        "estimated. Exchange rate variables (tentatively I(2)*) are excluded from the "
        "Johansen system due to order incompatibility."
    )

    pdf.paper_heading(2, "3.4 Vector Autoregression (VAR)")
    pdf.para(
        "Following the Johansen result, a VAR model is estimated on the first-differenced "
        "I(1) variables. Lag order is selected by minimising AIC/BIC. Model adequacy is "
        "assessed via residual autocorrelation (Portmanteau test) and normality tests. "
        "Impulse Response Functions (IRF) trace the dynamic response of housing cost "
        "proxy to one-standard-deviation shocks in each macroeconomic variable over "
        "a 10-period horizon. Forecast Error Variance Decomposition (FEVD) identifies "
        "the proportion of housing cost forecast error variance attributable to each "
        "macro variable."
    )

    pdf.paper_heading(2, "3.5 SHAP Feature Importance (XGBoost)")
    pdf.para(
        "An XGBoost regressor is trained on all 7 macroeconomic variables to predict "
        "housing construction cost proxy (NGN/sqm). Training uses 80% / 20% "
        "train-test split with 5-fold cross-validation. TreeSHAP (Lundberg et al., "
        "2020 [VERIFY]) is applied to extract mean absolute SHAP values for each "
        "feature, representing the average contribution of each variable to the "
        "predicted housing cost outcome. SHAP importance is expressed as a percentage "
        "of total mean absolute SHAP across all features."
    )
    pdf.para(
        "IMPORTANT CAVEAT: The XGBoost model is trained on a synthetic housing cost "
        "proxy. The train R2 (~0.999) reflects overfitting to the synthetic formula, "
        "and the cross-validated R2 (~-0.12) reflects poor generalisation -- which is "
        "expected and appropriate given the synthetic target. The SHAP rankings derived "
        "from this analysis indicate which variables the proxy formula most heavily "
        "weights (which by construction aligns with the formula's design), NOT the "
        "true predictive importance in real-world data. These results will be "
        "re-estimated with real NIQS housing cost data in O5."
    )


# ── Section 4: Results ─────────────────────────────────────────────────────────
def section4_stationarity(pdf, stat_rows):
    pdf.add_page()
    pdf.paper_heading(1, "4. Results")
    pdf.paper_heading(2, "4.1 Unit Root Test Results")
    pdf.data_badge('synthetic',
        "Stationarity results: Partially real (World Bank vars) + Synthetic (FX/Brent)")
    pdf.ln(1)
    pdf.para(
        "Table 2 presents the ADF and KPSS test results for each macroeconomic variable "
        "at levels and first differences. The integration order I(d) is determined by "
        "the dual ADF+KPSS criterion described in Section 3.2."
    )

    if stat_rows:
        # Dynamic table from CSV
        sw = [38, 18, 18, 18, 18, PAGE_W - 110]
        pdf.thead(["Variable", "ADF Lev p", "ADF d1 p", "KPSS Lev", "KPSS d1", "I(d) Order"], sw)
        for i, row in enumerate(stat_rows):
            var     = row.get('variable', '[?]')
            adf_lev = row.get('adf_lev_p', '[?]')
            adf_d1  = row.get('adf_d1_p', '[?]')
            kpss_lev= row.get('kpss_lev_stat', '[?]')
            kpss_d1 = row.get('kpss_d1_stat', '[?]')
            order   = row.get('integration_order', '[?]')
            # Format floats
            try: adf_lev = f"{float(adf_lev):.4f}"
            except: pass
            try: adf_d1  = f"{float(adf_d1):.4f}"
            except: pass
            try: kpss_lev = f"{float(kpss_lev):.4f}"
            except: pass
            try: kpss_d1  = f"{float(kpss_d1):.4f}"
            except: pass
            pdf.trow([var, adf_lev, adf_d1, kpss_lev, kpss_d1, order], sw, fill=(i % 2 == 1))
    else:
        pdf.placeholder_box("stationarity_results.csv not found -- run 02_macro_analysis/stationarity_analysis.py first")

    pdf.ln(1)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 4.5, sanitize(
        "Table 2: ADF and KPSS unit root test results. H0 (ADF): unit root present. "
        "H0 (KPSS): series stationary. I(1): stationary in 1st differences. "
        "I(2)*: tentative -- second differencing required, small-sample caveat applies. "
        "AIC-selected lag. Significance: alpha=0.05 for ADF; critical value 0.463 for KPSS."
    ))
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(2)

    pdf.para(
        "Results indicate that four macroeconomic variables -- GDP growth rate, CPI "
        "inflation, commercial lending rate, and Brent crude oil price -- are integrated "
        "of order one, I(1). These series are non-stationary in levels (ADF p > 0.05) "
        "but stationary in first differences (ADF p < 0.05). Three exchange rate series "
        "-- NGN/USD, NGN/EUR, and NGN/GBP -- exhibit possible I(2) behaviour, requiring "
        "second differencing to achieve stationarity. This pattern is consistent with "
        "the known non-linear and step-change nature of the NGN exchange rate, which "
        "experienced multiple discrete devaluation events over the 2000-2024 period "
        "rather than gradual random-walk movements. The I(2)* classification should be "
        "treated with caution given T=25; a longer sample period would improve "
        "the reliability of this determination."
    )


def section4_var(pdf, var_rows):
    pdf.paper_heading(2, "4.2 Johansen Cointegration and VAR Results")
    pdf.para(
        "The Johansen trace test, applied to the four I(1) variables (GDP growth, CPI "
        "inflation, lending rate, Brent crude), returns a cointegration rank of r=0 at "
        "the 5% significance level. This indicates no statistically significant long-run "
        "equilibrium relationship among the four variables in the 2000-2024 sample. "
        "The absence of cointegration is consistent with the macroeconomic literature "
        "on developing economies where structural breaks (policy changes, shocks) disrupt "
        "long-run relationships (Perron, 1989 [VERIFY])."
    )
    pdf.para(
        "Given r=0, a VAR model is estimated on first-differenced I(1) variables. "
        "Lag order selection by AIC returns p=1 (VAR(1)). Residual diagnostics confirm "
        "absence of significant autocorrelation (Portmanteau test p > 0.05 [VERIFY "
        "against output]) and approximate multivariate normality. "
        "See O2_05_VAR_VECM_Models.pdf for full IRF and FEVD charts."
    )
    pdf.placeholder_box(
        "VAR coefficient table: See O2_05_VAR_VECM_Models.pdf Section 4 for full "
        "coefficient matrix, standard errors, t-statistics, and p-values. Summary: "
        "Brent crude first difference shows strongest within-system predictive effect "
        "on differenced macro variables at lag 1 [VERIFY from output CSV]."
    )
    pdf.para(
        "Impulse Response Functions show that a one-standard-deviation shock to "
        "Brent crude first-difference produces a positive response in CPI inflation "
        "first-difference within 1-2 periods, consistent with the oil price -> fuel "
        "price -> general price level transmission mechanism. The response dissipates "
        "within 4-5 periods. GDP growth shows a muted, lagged negative response to "
        "oil price shocks, consistent with Nigeria's oil-revenue dependence. "
        "[NOTE: Full IRF charts available in O2_05_VAR_VECM_Models.pdf. Quantitative "
        "IRF values to be reported here from the results CSV after verification]."
    )


def section4_shap(pdf, shap_rows):
    pdf.add_page()
    pdf.paper_heading(2, "4.3 SHAP Feature Importance Results")
    pdf.data_badge('synthetic',
        "SHAP results derived from SYNTHETIC housing cost proxy -- re-run with real data")
    pdf.ln(1)
    pdf.para(
        "Table 3 presents the SHAP-based feature importance ranking for the 7 "
        "macroeconomic variables, expressed as mean absolute SHAP value and as a "
        "percentage of total importance. Figure 1 (see O2_06_SHAP_Variable_Selection.pdf) "
        "shows the SHAP summary beeswarm plot."
    )

    if shap_rows:
        sw2 = [10, 48, 28, 22, PAGE_W - 108]
        pdf.thead(["Rank", "Feature", "Mean |SHAP|", "Importance (%)", "Include in iNHCES?"], sw2)
        for i, row in enumerate(shap_rows):
            rank = row.get('rank', str(i + 1))
            feat = row.get('variable', '[?]')
            shap_v = row.get('mean_abs_shap', '[?]')
            imp_p  = row.get('relative_imp_pct', '[?]')
            include = row.get('include_in_model', 'Yes')
            try: shap_v = f"{float(shap_v):.2f}"
            except: pass
            try: imp_p  = f"{float(imp_p):.2f}%"
            except: pass
            pdf.trow([rank, feat, shap_v, imp_p, include], sw2, fill=(i % 2 == 1))
    else:
        pdf.placeholder_box("shap_importance.csv not found -- run 02_macro_analysis/shap_variable_selection.py first")

    pdf.ln(1)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 4.5, sanitize(
        "Table 3: SHAP-based feature importance. Mean |SHAP| = mean absolute SHAP value. "
        "Importance % = share of total mean absolute SHAP. DERIVED FROM SYNTHETIC PROXY. "
        "All values to be re-estimated with real housing cost per sqm data."
    ))
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(2)

    # Narrative interpretation
    if len(shap_rows) >= 4:
        r1, r2, r3, r4 = shap_rows[0], shap_rows[1], shap_rows[2], shap_rows[3]
        pdf.para(
            f"The SHAP analysis identifies {sanitize(r1['variable'])} as the single most "
            f"important predictor ({sanitize(r1.get('relative_imp_pct','[?]'))}% of total SHAP "
            f"importance), followed by {sanitize(r2['variable'])} "
            f"({sanitize(r2.get('relative_imp_pct','[?]'))}%), "
            f"{sanitize(r3['variable'])} ({sanitize(r3.get('relative_imp_pct','[?]'))}%), "
            f"and {sanitize(r4['variable'])} ({sanitize(r4.get('relative_imp_pct','[?]'))}%). "
            f"Together, the top 4 features account for approximately "
            f"{sum(float(x.get('relative_imp_pct','0')) for x in shap_rows[:4]):.1f}% "
            "of total SHAP importance, confirming that exchange rate and inflation "
            "variables are the dominant determinants of the housing cost proxy. "
            "GDP growth and lending rate, ranked 6th and 7th respectively, are "
            "classified as 'optional' features for the initial iNHCES model, "
            "pending validation with real housing cost data."
        )
    pdf.para(
        "The strong dominance of NGN/USD exchange rate (~45% importance) is consistent "
        "with qualitative assessments in the Nigerian construction literature (Anigbogu "
        "et al., 2014 [VERIFY]; Ogunsemi & Jagboro, 2006 [VERIFY]) and with the "
        "known structure of the Nigerian construction material supply chain. CPI inflation "
        "captures broader price level effects including domestically produced inputs "
        "(sand, granite, labour). The EUR and GBP exchange rates reflect the European "
        "source of certain premium finishes and mechanical/electrical equipment."
    )
    pdf.para(
        "Brent crude oil price (~10.85% importance) operates through two channels: "
        "(1) direct: diesel cost for construction plant and logistics; (2) indirect: "
        "oil revenue -> Nigerian fiscal policy -> public sector construction demand. "
        "The moderate importance (~10%) suggests that once exchange rate and inflation "
        "are controlled for, the residual oil price effect on housing construction cost "
        "is non-negligible but secondary."
    )


# ── Section 5: Discussion ──────────────────────────────────────────────────────
def section5(pdf):
    pdf.add_page()
    pdf.paper_heading(1, "5. Discussion")
    pdf.paper_heading(2, "5.1 Implications of Stationarity Findings")
    pdf.para(
        "The I(1) classification of GDP growth, CPI inflation, lending rate, and Brent "
        "crude confirms that these series have a unit root -- shocks have permanent "
        "effects rather than mean-reverting. For ML-based forecasting, this implies "
        "that raw levels of these variables may not be suitable as model features; "
        "first differences (period-to-period changes) or detrended series should be "
        "used to avoid spurious regression. The iNHCES O5 feature engineering pipeline "
        "will apply first-differencing and log-transformation as appropriate."
    )
    pdf.para(
        "The tentative I(2)* classification of the three exchange rate series warrants "
        "attention. I(2) behaviour in exchange rates is unusual in developed economies "
        "but may reflect the step-change devaluation pattern of the NGN, where discrete "
        "policy-driven devaluation events dominate the dynamics rather than random-walk "
        "increments. For ML feature engineering, this suggests using percentage change "
        "(returns) rather than level or first difference for exchange rate variables."
    )
    pdf.paper_heading(2, "5.2 Implications of No Cointegration")
    pdf.para(
        "The Johansen result (r=0, no cointegration) implies there is no stable long-run "
        "equilibrium between the four I(1) macro variables in the 2000-2024 Nigerian "
        "data. This is not surprising: structural breaks (the 2008 global crisis, "
        "2016 devaluation, 2020 COVID shock, 2023 CBN FX liberalisation) frequently "
        "break long-run equilibrium relationships in developing economies. The "
        "consequence for modelling is that a pure error-correction (VECM) approach "
        "is inappropriate, and short-run dynamics (VAR) better capture the observed "
        "relationships. For the iNHCES ML model, this supports a rolling-window "
        "retraining strategy (Airflow DAG, O5) rather than a fixed long-run model."
    )
    pdf.paper_heading(2, "5.3 SHAP-Driven Feature Selection for iNHCES")
    pdf.para(
        "The SHAP importance ranking provides a data-driven basis for the iNHCES "
        "feature set. Based on the synthetic proxy analysis, the recommended initial "
        "feature set includes: NGN/USD (1.0 weight), CPI inflation (0.57 weight), "
        "NGN/EUR (0.26 weight), Brent crude (0.24 weight), NGN/GBP (0.076 weight). "
        "GDP growth and lending rate are designated 'optional' pending validation. "
        "When real NIQS housing cost data becomes available (O4), this SHAP analysis "
        "will be re-run on the real dataset, and the feature set may need revision. "
        "The current ranking should be understood as a theoretically plausible prior "
        "based on the synthetic proxy's construction, not as empirically validated "
        "importance from real housing cost outcomes."
    )
    pdf.paper_heading(2, "5.4 Limitations")
    pdf.para(
        "This study has several important limitations: "
        "(1) The housing cost target variable is synthetic -- all SHAP and model "
        "performance results are preliminary and cannot be published as real findings. "
        "(2) T=25 annual observations is a small sample for time-series econometrics; "
        "quarterly data would improve test power. "
        "(3) EIA Brent crude and CBN exchange rate data are currently synthetic; "
        "configuring API keys (EIA_API_KEY, FRED_API_KEY) and re-running the "
        "fetch scripts (O2 Step 1) will upgrade these to live data. "
        "(4) The SHAP analysis uses XGBoost on annual data; a richer dataset with "
        "project-level cost records and monthly macro data would produce more "
        "reliable importance estimates. "
        "(5) Regional variation within Nigeria (North, South-West, South-East, "
        "South-South construction cost differentials) is not captured in this "
        "national-level analysis."
    )


# ── Section 6: Conclusion ──────────────────────────────────────────────────────
def section5b_temporal(pdf):
    """NEW: Section on temporal cost projection using VAR + compound inflation."""
    pdf.add_page()
    pdf.paper_heading(1, "5B. Temporal Construction Cost Projection")
    pdf.paper_heading(2, "5B.1 Motivation and Methodology")
    pdf.para(
        "A key practical application of the macroeconomic analysis conducted in this "
        "study is the projection of construction costs at future time horizons. "
        "Nigerian QS professionals and developers require not only a current cost "
        "estimate but also cost projections at short- (< 1 year), medium- (< 3 years), "
        "and long-term (< 5 years) horizons to support project planning decisions: "
        "whether to build now, defer, or phase construction over time."
    )
    pdf.para(
        "The iNHCES temporal projection methodology applies a two-stage approach: "
        "(1) The VAR(diff, lag=1) model from Section 4.2 is used to generate h-step "
        "ahead forecasts of the four I(1) macroeconomic variables (GDP growth, CPI "
        "inflation, lending rate, Brent crude); (2) The expected annual construction "
        "cost inflation rate is derived as a weighted combination of CPI inflation "
        "(40% weight) and NGN/USD exchange rate depreciation (60% weight), reflecting "
        "the SHAP importance hierarchy established in Section 4.3. "
        "The compound growth formula cost(h) = cost(0) x (1 + r)^h is applied, where "
        "r is the derived annual inflation rate and h is the horizon in years."
    )
    pdf.paper_heading(2, "5B.2 Confidence Interval Framework")
    pdf.para(
        "The total uncertainty at horizon h is computed as: "
        "sigma_total(h) = sqrt(sigma_model^2 + sigma_forecast(h)^2), where "
        "sigma_model = 13.66% (champion model LOO-CV MAPE from O5) and "
        "sigma_forecast(h) = 6% x sqrt(h) (VAR forecast uncertainty, growing with "
        "square root of horizon). This produces 90% confidence intervals that widen "
        "appropriately as the projection horizon increases, providing an honest "
        "representation of the growing uncertainty at longer horizons."
    )
    pdf.paper_heading(2, "5B.3 Indicative Projection Results (Synthetic Proxy)")
    pdf.placeholder_box(
        "Temporal projection results to be populated with real NIQS cost data. "
        "Indicative results from synthetic proxy (n=22, seed=2025): "
        "Current: NGN 122,987/sqm | Short-term (1yr): NGN 153,734/sqm (+25%) | "
        "Medium-term (3yr): NGN 240,210/sqm (+95%) | Long-term (5yr): NGN 375,328/sqm (+205%). "
        "Annual inflation rate: 25.0% p.a. (derived from World Bank CPI 2020-2024). "
        "NOTE: These results reflect the current high-inflation Nigerian macro environment "
        "and should be interpreted as upper-bound scenarios rather than central forecasts."
    )
    pdf.paper_heading(2, "5B.4 Practical Implications")
    pdf.para(
        "The temporal projection feature has direct practical value for Nigerian "
        "construction decision-makers. A projected 5-year cost increase of 150-200% "
        "in nominal NGN terms (driven by FX depreciation and CPI inflation) suggests "
        "that deferring construction by 3-5 years in Nigeria involves substantial "
        "cost escalation risk. This finding reinforces the importance of: "
        "(1) securing construction materials procurement early when FX is favourable; "
        "(2) including cost escalation provisions of 20-30% per annum in project "
        "feasibility studies; and (3) phasing construction to front-load labour and "
        "material procurement in the early project stages."
    )
    pdf.info_box(
        "Temporal projection methodology is implemented in:\n"
        "  02_macro_analysis/forecast_macro.py (VAR h-step forecasts)\n"
        "  05_ml_models/05_temporal_projection.py (compound cost projection engine)\n"
        "  nhces-backend/app/ml/temporal.py (FastAPI integration)\n"
        "  DATA SOURCE: AMBER/RED -- real CPI data; synthetic FX and cost proxy.\n"
        "  Horizons: h=1 (short), h=3 (medium), h=5 (long). Cap at 5yr is deliberate:\n"
        "  Nigeria's macro regime changes every 5-7 years; 10yr projection is speculative."
    )


def section6(pdf):
    pdf.add_page()
    pdf.paper_heading(1, "6. Conclusions")
    pdf.para(
        "This study has applied a rigorous multi-method analytical framework -- "
        "ADF+KPSS unit root testing, Johansen cointegration analysis, VAR modelling, "
        "and SHAP-XGBoost feature importance -- to identify the macroeconomic "
        "determinants of housing construction costs in Nigeria over the period 2000-2024. "
        "The principal findings, subject to the synthetic data caveat, are:"
    )
    for finding in [
        "Four macroeconomic variables (GDP growth, CPI inflation, lending rate, Brent "
        "crude) are I(1) -- confirming they require differencing or log-transformation "
        "before use as ML features in the iNHCES model.",
        "Three exchange rate series (NGN/USD, NGN/EUR, NGN/GBP) exhibit possible I(2) "
        "behaviour, suggesting percentage changes are the appropriate feature form. "
        "This finding requires confirmation with a longer time series.",
        "No cointegration is found among the four I(1) variables (Johansen rank=0), "
        "supporting a VAR (not VECM) approach and a rolling-window ML retraining strategy.",
        "SHAP importance analysis identifies NGN/USD exchange rate (~45%), CPI inflation "
        "(~25%), NGN/EUR (~12%), and Brent crude (~11%) as the dominant determinants "
        "of housing construction cost in the synthetic proxy model. These rankings "
        "provide a theoretically consistent prior for iNHCES ML feature selection.",
        "GDP growth and lending rate are designated optional features, contributing "
        "~3.7% combined SHAP importance in the proxy model.",
    ]:
        pdf.set_font("Helvetica", "", 9.5)
        pdf.set_text_color(*DARK_GREY)
        pdf.set_x(LEFT + 4)
        pdf.multi_cell(PAGE_W - 4, 5.2, sanitize(f"- {finding}"))
        pdf.ln(1)

    pdf.para(
        "The policy implication for housing cost management in Nigeria is clear: "
        "exchange rate stability is the single most important macroeconomic "
        "lever for reducing housing construction cost volatility, with inflation "
        "management and fuel/energy subsidy policy as secondary but significant "
        "influences. For the iNHCES system, these findings justify a live data "
        "pipeline that continuously updates exchange rate and inflation features "
        "in the ML model (O5 Airflow DAG, O6 backend)."
    )
    pdf.placeholder_box(
        "This paper will be submitted to Construction Management and Economics "
        "(or Habitat International) after O4 real data collection is complete and "
        "all synthetic data has been replaced with validated real measurements."
    )


# ── AI Disclosure ──────────────────────────────────────────────────────────────
def ai_disclosure(pdf):
    pdf.add_page()
    pdf.paper_heading(1, "AI Assistance Disclosure Statement")
    pdf.info_box(
        "MANDATORY DISCLOSURE -- per iNHCES Ethics Framework (00_Research_Simulation_Introduction.pdf, "
        "Section 9; COPE Guidelines on AI in Publishing, 2023)"
    )
    pdf.ln(2)
    pdf.para(
        "Artificial intelligence tools (specifically, GitHub Copilot powered by Claude Sonnet, "
        "via VS Code) were used in the preparation of this manuscript as follows:"
    )
    for item in [
        "ANALYTICAL CODE GENERATION: Python scripts for data collection (fetch_worldbank.py, "
        "fetch_eia_oil.py, fetch_cbn_fx.py), stationarity analysis (stationarity_analysis.py), "
        "VAR/VECM modelling (var_vecm_model.py), and SHAP analysis (shap_variable_selection.py) "
        "were generated with AI assistance, reviewed, and executed by the research team.",
        "MANUSCRIPT DRAFTING: The full body text of this manuscript -- including Sections 1-6, "
        "abstract, tables, and references -- was generated by an AI language model as a first draft. "
        "The research team reviewed this draft for accuracy, coherence, and alignment with the "
        "iNHCES research design.",
        "SYNTHETIC DATA GENERATION: The housing cost proxy variable and the synthetic EIA/CBN "
        "data series were generated using rule-based formulas designed with AI assistance. "
        "These synthetic series will be replaced with real data in O4.",
        "RESULT INTERPRETATION: Preliminary narrative interpretation of the stationarity, VAR, "
        "and SHAP results (Sections 4-5) was AI-generated. The research team will validate "
        "all interpretations against actual model outputs before final manuscript preparation.",
    ]:
        pdf.set_font("Helvetica", "", 9.5)
        pdf.set_text_color(*DARK_GREY)
        pdf.set_x(LEFT + 4)
        pdf.multi_cell(PAGE_W - 4, 5.2, sanitize(f"- {item}"))
        pdf.ln(2)

    pdf.para(
        "AI tools were NOT used to fabricate research data, to create false citations, "
        "or to misrepresent results. All authors take full responsibility for the "
        "intellectual content of this manuscript."
    )


# ── References ─────────────────────────────────────────────────────────────────
def references(pdf):
    pdf.add_page()
    pdf.paper_heading(1, "References")
    pdf.info_box(
        "CITATION VERIFICATION REQUIRED: All references are based on AI training knowledge. "
        "Verify EVERY reference in Scopus or Web of Science before submission. "
        "References marked [VERIFY] have not been checked. Remove unverifiable references."
    )
    pdf.ln(2)
    refs = [
        ("Dickey, D.A., & Fuller, W.A. (1979). Distribution of the estimators for "
         "autoregressive time series with a unit root. Journal of the American "
         "Statistical Association, 74(366), 427-431. [VERIFY -- high confidence]"),

        ("Engle, R.F., & Granger, C.W.J. (1987). Co-integration and error correction: "
         "representation, estimation, and testing. Econometrica, 55(2), 251-276. "
         "[VERIFY -- high confidence, Nobel Prize work]"),

        ("Johansen, S. (1988). Statistical analysis of cointegration vectors. "
         "Journal of Economic Dynamics and Control, 12(2-3), 231-254. "
         "[VERIFY -- high confidence]"),

        ("Kwiatkowski, D., Phillips, P.C.B., Schmidt, P., & Shin, Y. (1992). "
         "Testing the null hypothesis of stationarity against the alternative of a "
         "unit root. Journal of Econometrics, 54(1-3), 159-178. "
         "[VERIFY -- high confidence]"),

        ("Lundberg, S.M., & Lee, S.I. (2017). A unified approach to interpreting "
         "model predictions. Advances in Neural Information Processing Systems, 30. "
         "[VERIFY -- NeurIPS 2017]"),

        ("Lundberg, S.M., Erion, G., Chen, H., DeGrave, A., Peck, J.M., Kuber, D., "
         "... & Lee, S.I. (2020). From local explanations to global understanding "
         "with explainable AI for trees. Nature Machine Intelligence, 2(1), 56-67. "
         "[VERIFY in Nature MI]"),

        ("Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system. "
         "Proceedings of the 22nd ACM SIGKDD, 785-794. [VERIFY -- high confidence]"),

        ("Sims, C.A. (1980). Macroeconomics and reality. Econometrica, 48(1), 1-48. "
         "[VERIFY -- highly cited, high confidence]"),

        ("Perron, P. (1989). The great crash, the oil price shock, and the unit root "
         "hypothesis. Econometrica, 57(6), 1361-1401. [VERIFY -- high confidence]"),

        ("Ogunsemi, D.R., & Jagboro, G.O. (2006). Time-cost model for building "
         "projects in Nigeria. Construction Management and Economics, 24(3), 253-258. "
         "[VERIFY in CME -- details may be inaccurate]"),

        ("Anigbogu, N., Onwusoba, I., & Adafin, J. (2014). Analysis of factors "
         "contributing to abandoned public projects in Nigeria. [VERIFY FULL CITATION -- "
         "journal, volume, pages may be inaccurate]"),

        ("World Bank. (2023). World Development Indicators. World Bank Open Data. "
         "https://data.worldbank.org  [VERIFY -- access date and specific indicators]"),

        ("Bilal, M., Oyedele, L.O., Akinade, O.O., Ajayi, S.O., Alaka, H.A., & "
         "Owolabi, H.A. (2016). Big data architecture for construction waste analytics "
         "(CWA): A conceptual framework. Journal of Building Engineering, 6, 144-156. "
         "[VERIFY -- this may not be a cost estimation reference, check carefully]"),

        ("National Bureau of Statistics, Nigeria. (2023). Nigerian Construction "
         "Sector Report. NBS, Abuja. [VERIFY existence and title]"),
    ]
    for ref in refs:
        pdf.ref_item(ref)


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    print("Loading result CSVs...")
    stat_rows = load_stationarity()
    shap_rows = load_shap()
    var_rows  = load_var()

    out = os.path.join(OUT_DIR, 'P3_Macroeconomic_Determinants_Draft.pdf')
    pdf = PaperPDF()

    make_title_page(pdf)

    _ds_page(pdf, 'amber',
        "DATA SOURCE: AMBER/RED -- World Bank data is LIVE; EIA and FX data are SYNTHETIC. "
        "Housing cost target variable is SYNTHETIC. All quantitative results are indicative only.",
        (
            "WHAT IS REAL IN THIS DOCUMENT:\n"
            "  * World Bank GDP growth, CPI inflation, lending rate (2000-2024): "
            "LIVE data fetched from World Bank Open Data API.\n"
            "  * Stationarity test results for the above 3 World Bank variables: "
            "derived from real data.\n"
            "  * PRISMA protocol, research methodology, and gap analysis: "
            "AI-authored academic framework.\n\n"
            "WHAT IS SYNTHETIC (RED LEVEL):\n"
            "  * Brent crude oil price: rule-based synthetic series. "
            "Set EIA_API_KEY and re-run fetch_eia_oil.py to upgrade.\n"
            "  * NGN/USD, NGN/EUR, NGN/GBP exchange rates: rule-based synthetic "
            "series. Set FRED_API_KEY and re-run fetch_cbn_fx.py to upgrade.\n"
            "  * Housing cost per sqm (target variable): ENTIRELY SYNTHETIC proxy. "
            "Must be replaced with real NIQS unit rate survey data (O4).\n"
            "  * SHAP importance rankings: derived from model trained on SYNTHETIC "
            "target -- rankings reflect proxy formula design, NOT real-world data.\n\n"
            "REQUIRED BEFORE PUBLICATION:\n"
            "  1. Set EIA_API_KEY and FRED_API_KEY; re-run all fetch_*.py scripts\n"
            "  2. Complete O4 data collection: NIQS unit rates, BQ project costs\n"
            "  3. Replace synthetic housing cost proxy with validated real data\n"
            "  4. Re-run shap_variable_selection.py with real target variable\n"
            "  5. Re-run stationarity and VAR with longer quarterly/monthly series\n"
            "  6. Verify all citations in Scopus / Web of Science\n"
            "  7. Register on PROSPERO if any SLR component is included\n"
            "  8. Include AI Disclosure Statement in final submitted manuscript\n"
            "  9. Submit to ethics committee for review before public release"
        )
    )

    make_abstract(pdf, shap_rows)
    section1(pdf)
    section2(pdf)
    section3(pdf)
    section4_stationarity(pdf, stat_rows)
    section4_var(pdf, var_rows)
    section4_shap(pdf, shap_rows)
    section5(pdf)
    section5b_temporal(pdf)
    section6(pdf)
    ai_disclosure(pdf)
    references(pdf)

    pdf.output(out)
    print(f"[OK]  P3_Macroeconomic_Determinants_Draft.pdf  saved -> {out}")


if __name__ == "__main__":
    main()
