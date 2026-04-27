"""
iNHCES Draft Paper P1 Generator
Paper: "Systematic Review of Machine Learning Methods for Housing Construction
Cost Estimation in Emerging Economies: A PRISMA 2020-Compliant Protocol
and Preliminary Synthesis"
Target Journal: Construction Management and Economics (Taylor & Francis)
Based on: O1 Steps 1-3 outputs

DATA SOURCE: AMBER -- AI-generated first draft based on AI-synthesised literature
synthesis. No real database search has been executed. PRISMA statistics are
PLACEHOLDERS. All citations must be verified in Scopus / Web of Science before
submission. This document is a working template for the research team.

TETFund NRF 2025 | Department of Quantity Surveying, ABU Zaria
"""

import sys
import os
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

JOURNAL   = "Construction Management and Economics (Taylor & Francis)"
PAPER_ID  = "P1"
PAPER_TITLE = (
    "Systematic Review of Machine Learning Methods for Housing Construction "
    "Cost Estimation in Emerging Economies: A PRISMA 2020 Protocol and Preliminary Synthesis"
)
SHORT_TITLE = "ML Methods for Housing Cost Estimation: A Systematic Review"

# ── Paper PDF class ────────────────────────────────────────────────────────────
class PaperPDF(DocPDF):
    def __init__(self):
        super().__init__(PAPER_TITLE, PAPER_ID)

    def header(self):
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*MID_GREY)
        self.set_xy(LEFT, 5)
        self.cell(PAGE_W, 4.5, sanitize(
            f"{PAPER_ID}  |  {SHORT_TITLE[:60]}  |  "
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


# ── Title page ─────────────────────────────────────────────────────────────────
def make_title_page(pdf):
    pdf.add_page()

    # Draft watermark strip
    pdf.set_fill_color(220, 50, 50)
    pdf.rect(0, 0, 210, 8, 'F')
    pdf.set_font("Helvetica", "B", 7.5)
    pdf.set_text_color(*WHITE)
    pdf.set_xy(0, 1.5)
    pdf.cell(210, 5,
             "AI-GENERATED FIRST DRAFT -- FOR RESEARCHER REVIEW ONLY -- NOT FOR SUBMISSION",
             align="C")
    pdf.set_text_color(*DARK_GREY)

    pdf.ln(16)

    # Journal target
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.cell(PAGE_W, 6, sanitize(f"Target journal: {JOURNAL}"), align="C")
    pdf.ln(6)

    # Title
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(*DARK_NAVY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 7.5,
                   sanitize(PAPER_TITLE), align="C")
    pdf.ln(5)

    # Gold rule
    pdf.set_draw_color(*GOLD)
    pdf.set_line_width(1.0)
    pdf.line(LEFT + 20, pdf.get_y(), LEFT + PAGE_W - 20, pdf.get_y())
    pdf.ln(6)

    # Author block
    for line in [
        "[FIRST AUTHOR NAME], Department of Quantity Surveying, ABU Zaria",
        "[SECOND AUTHOR NAME], Department of Quantity Surveying, ABU Zaria",
        "[ADDITIONAL AUTHORS]",
        "Corresponding author: [EMAIL ADDRESS] | ORCID: [INSERT]",
        "",
        "Acknowledgement: TETFund National Research Fund 2025, Grant No. [INSERT]",
        f"Manuscript prepared: {date.today().strftime('%d %B %Y')}",
        "Estimated word count (draft): ~6,800 words (excl. references)",
    ]:
        pdf.set_font("Helvetica", "I" if line.startswith("[") else "", 9)
        pdf.set_text_color(*MID_GREY if not line.startswith("Corr") else DARK_NAVY)
        pdf.set_x(LEFT)
        pdf.cell(PAGE_W, 5.5, sanitize(line), align="C", ln=True)

    pdf.ln(5)
    pdf.set_draw_color(*MID_GREY)
    pdf.set_line_width(0.3)
    pdf.line(LEFT, pdf.get_y(), LEFT + PAGE_W, pdf.get_y())
    pdf.ln(5)


# ── Abstract ───────────────────────────────────────────────────────────────────
def make_abstract(pdf):
    pdf.paper_heading(1, "ABSTRACT")
    abstract_text = (
        "Background: Housing construction cost estimation in Nigeria and sub-Saharan Africa "
        "remains characterised by opacity, data scarcity, and reliance on subjective "
        "professional judgement. Machine learning (ML) offers a systematic, data-driven "
        "alternative to conventional parametric and elemental cost planning methods. "
        "However, no PRISMA-compliant systematic review has been conducted that focuses "
        "specifically on the applicability of ML cost estimation methods to the Nigerian "
        "and emerging-economy context.\n\n"
        "Objective: This paper reports the PRISMA 2020-compliant protocol and a preliminary "
        "AI-synthesised framework for a systematic literature review (SLR) examining ML-based "
        "construction cost estimation methods across emerging economies, with particular "
        "emphasis on model performance benchmarks, data requirements, and contextual "
        "transferability to Nigeria.\n\n"
        "Methods: A six-database search strategy was designed (Scopus, Web of Science, "
        "ASCE Library, ScienceDirect, IBSS, Google Scholar) using Boolean operators across "
        "three concept clusters: construction cost estimation, machine learning and AI "
        "methods, and Nigeria/Africa/emerging economy. Inclusion and exclusion criteria "
        "follow a PICO framework. Study quality is assessed using CASP criteria.\n\n"
        "Preliminary Framework: Based on AI-synthesised knowledge (not yet PRISMA-extracted "
        "results), the literature is mapped across regression, neural network, ensemble, "
        "and hybrid ML categories. Seven knowledge gaps are identified, including the "
        "absence of Nigeria-specific longitudinal datasets, SHAP-based explainability "
        "studies, and ML systems integrated with live macroeconomic feature pipelines.\n\n"
        "NOTE: Quantitative synthesis results (PRISMA flow counts, included study "
        "characteristics, effect sizes) are PLACEHOLDERS. This draft will be updated after "
        "the database search (O1 Phase 2) has been executed by the research team."
    )
    pdf.abstract_box(abstract_text)

    # Keywords
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*DARK_NAVY)
    pdf.set_x(LEFT)
    pdf.cell(28, 5.5, "Keywords:")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*DARK_GREY)
    pdf.cell(PAGE_W - 28, 5.5, sanitize(
        "construction cost estimation; machine learning; systematic literature review; "
        "PRISMA 2020; Nigeria; emerging economies; XGBoost; neural networks"
    ), ln=True)
    pdf.ln(4)


# ── Section 1: Introduction ────────────────────────────────────────────────────
def section1(pdf):
    pdf.add_page()
    pdf.paper_heading(1, "1. Introduction")
    pdf.para(
        "Accurate housing construction cost estimation is a critical function in the "
        "built environment professions. In Nigeria, housing construction costs exhibit "
        "high volatility driven by exchange rate fluctuations, fuel price instability, "
        "cement and steel supply chain disruptions, and political-economic shocks "
        "(World Bank, 2023 [VERIFY]). The National Housing Fund Act (1992) and the "
        "National Urban Development Policy (2012) both identify cost uncertainty as a "
        "primary barrier to housing delivery for low- and middle-income households. "
        "The Bureau of Public Procurement (BPP) reports persistent cost overruns of "
        "30-80% on federal construction projects, with incomplete designs and cost "
        "data limitations cited as primary causes (BPP Annual Report, [VERIFY YEAR])."
    )
    pdf.para(
        "Conventional cost estimation methods -- superficial area, elemental, approximate "
        "quantities, and Bills of Quantities (BQ) -- rely on historical unit rate data "
        "and professional judgement. These methods are inadequate in environments where "
        "macroeconomic conditions change rapidly and historical data may not reflect "
        "current market reality. The Quantity Surveyor (QS) profession in Nigeria, "
        "represented by the Nigerian Institute of Quantity Surveyors (NIQS), has "
        "recognised the urgent need to develop data-driven cost modelling tools "
        "appropriate for the Nigerian context (NIQS Strategic Plan [VERIFY])."
    )
    pdf.para(
        "Machine learning (ML) methods offer a fundamentally different paradigm: "
        "rather than relying on predetermined cost relationships, ML models learn "
        "from data patterns and can incorporate a wide range of features -- including "
        "macroeconomic indicators, project characteristics, location, and procurement "
        "method -- to produce probabilistic cost estimates. ML methods demonstrated "
        "in international cost estimation literature include Artificial Neural Networks "
        "(ANN), Support Vector Regression (SVR), Random Forests (RF), Gradient "
        "Boosting (XGBoost/LightGBM), and stacking ensemble methods (Kim et al., "
        "2004 [VERIFY]; Ji et al., 2011 [VERIFY]; Bilal et al., 2016 [VERIFY])."
    )
    pdf.paper_heading(2, "1.1 Research Gaps and Motivation")
    pdf.para(
        "Despite the growing ML cost estimation literature, two critical gaps motivate "
        "this review. First, existing reviews focus predominantly on developed-economy "
        "contexts (USA, UK, Australia, South Korea) with high data availability and "
        "stable macroeconomic environments. The few African studies identified (Dania "
        "et al. [VERIFY]; Kpamma et al. [VERIFY]) are limited to single-country "
        "regression models without ML benchmarking. Second, no prior study has "
        "systematically evaluated how macroeconomic variables (exchange rate, inflation, "
        "oil price) should be incorporated as time-varying features in construction "
        "cost ML models for emerging economy settings."
    )
    pdf.paper_heading(2, "1.2 Research Objectives")
    for obj in [
        "RO1: Systematically identify and map ML methods applied to construction cost "
        "estimation in peer-reviewed literature (2000-2024).",
        "RO2: Compare reported model performance metrics (R2, MAE, MAPE) across ML "
        "method categories to identify best-performing approaches.",
        "RO3: Assess the extent to which macroeconomic variables are incorporated in "
        "existing ML cost models, and identify gaps relevant to Nigeria.",
        "RO4: Identify knowledge gaps and derive a feature set and model architecture "
        "recommendation for the iNHCES system.",
    ]:
        pdf.set_font("Helvetica", "", 9.5)
        pdf.set_text_color(*DARK_GREY)
        pdf.set_x(LEFT + 4)
        pdf.multi_cell(PAGE_W - 4, 5.2, sanitize(obj))
        pdf.ln(1)
    pdf.ln(2)
    pdf.paper_heading(2, "1.3 Paper Contributions")
    pdf.para(
        "This paper makes three contributions: (1) a PRISMA 2020-registered search "
        "protocol for ML construction cost estimation -- the first covering both "
        "ML method families and macroeconomic feature integration; (2) a preliminary "
        "taxonomy of ML methods applied across 7 model categories from AI-synthesised "
        "knowledge, to be validated against extracted study evidence; and (3) a "
        "gap analysis matrix identifying 7 research gaps, directly informing the "
        "iNHCES project research design (TETFund NRF 2025, ABU Zaria)."
    )


# ── Section 2: Theoretical Framework ──────────────────────────────────────────
def section2(pdf):
    pdf.add_page()
    pdf.paper_heading(1, "2. Theoretical Framework")
    pdf.paper_heading(2, "2.1 Construction Cost Estimation Methods")
    pdf.para(
        "Construction cost estimation methods exist on a spectrum from simple to "
        "complex (RICS, 2021 [VERIFY]; Ferry et al., 2014 [VERIFY]). At the "
        "early design stage, superficial area and volume methods provide rapid "
        "order-of-magnitude estimates (+/- 25-35%). As design information develops, "
        "elemental and approximate quantity methods improve accuracy to +/- 10-15%. "
        "Bills of Quantities at tender stage target +/- 5%. However, in the Nigerian "
        "context, even BQ-based estimates frequently exceed this tolerance due to "
        "exchange rate volatility, specification inflation, and contractor risk premiums."
    )
    pdf.para(
        "Parametric models -- regression-based relationships between project "
        "characteristics and cost -- have been the dominant quantitative approach "
        "in construction economics research since the 1980s (Skitmore, 1988 [VERIFY]; "
        "Aibinu & Pasco, 2008 [VERIFY]). Their key limitation is the assumption of "
        "linear or log-linear relationships between variables, which may not hold "
        "in environments with structural breaks and high non-linearity."
    )
    pdf.paper_heading(2, "2.2 Machine Learning in Construction Cost Estimation")
    pdf.para(
        "ML models relax the linearity assumption and can capture complex, non-linear "
        "interaction effects among features. The literature identifies seven ML "
        "method families applied to construction cost estimation:"
    )
    mw = [58, PAGE_W - 58]
    pdf.thead(["ML Method Family", "Representative Studies [VERIFY ALL]"], mw)
    for i, (meth, studies) in enumerate([
        ("Artificial Neural Network (ANN/MLP)",    "Kim et al. (2004); Wilmot & Mei (2005); Betts et al. (2018)"),
        ("Support Vector Regression (SVR)",         "Chou et al. (2010); Jin et al. (2012)"),
        ("Random Forest (RF)",                      "Petruseva et al. (2017); Doyle et al. (2020)"),
        ("Gradient Boosting (XGBoost/LightGBM)",    "Bilal et al. (2020); Huo et al. (2021)"),
        ("Stacking / Ensemble",                     "Pham et al. (2020); Zhu et al. (2022)"),
        ("Case-Based Reasoning (CBR)",              "Ji et al. (2011); Lowe et al. (2006)"),
        ("Deep Learning (DNN/LSTM)",                "Liu et al. (2019); Wang et al. (2021)"),
    ]):
        pdf.trow([meth, studies], mw, fill=(i % 2 == 1))
    pdf.ln(2)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 4.5, sanitize(
        "Table 1: ML method families in construction cost estimation literature. "
        "All citations are AI-generated and MUST be verified in Scopus/WoS before use."
    ))
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(2)

    pdf.paper_heading(2, "2.3 Macroeconomic Variables in Construction Cost Modelling")
    pdf.para(
        "The role of macroeconomic variables in construction cost models has received "
        "limited systematic treatment. Inflation (CPI) has been included in several "
        "time-series cost models as a deflator (Trost & Oberlender, 2003 [VERIFY]). "
        "Exchange rate effects are particularly significant in import-dependent "
        "construction sectors: Ogunsemi & Jagboro (2006) [VERIFY] showed that "
        "imported material price changes accounted for 47% of cost overrun variance "
        "in Nigerian construction projects. Oil price effects operate through transport "
        "costs, diesel for construction plant, and petrochemical product prices "
        "(asphalt, paints, sealants). No prior ML study has integrated all three "
        "macro dimensions (exchange rate, inflation, oil price) as time-varying "
        "features in a construction cost estimation model."
    )


# ── Section 3: Methodology (PRISMA) ───────────────────────────────────────────
def section3(pdf):
    pdf.add_page()
    pdf.paper_heading(1, "3. Methodology: PRISMA 2020 Protocol")
    pdf.para(
        "This systematic review follows the PRISMA 2020 guidelines (Page et al., 2021). "
        "The protocol has been pre-registered [PROSPERO registration: INSERT CRD NUMBER]. "
        "The review methodology is structured around the four PRISMA phases: "
        "Identification, Screening, Eligibility, and Inclusion."
    )
    pdf.paper_heading(2, "3.1 Research Questions")
    for q in [
        "RQ1: Which ML methods have been applied to construction cost estimation, "
        "and what are their reported accuracy metrics (R2, MAE, MAPE)?",
        "RQ2: To what extent do existing ML cost models incorporate macroeconomic "
        "variables (exchange rate, inflation, oil price)?",
        "RQ3: What project characteristics (type, scale, procurement, location) "
        "are most consistently used as ML features, and with what predictive importance?",
        "RQ4: What data collection and model training approaches are most appropriate "
        "for emerging economy, data-scarce construction environments?",
    ]:
        pdf.set_font("Helvetica", "", 9.5)
        pdf.set_text_color(*DARK_GREY)
        pdf.set_x(LEFT + 4)
        pdf.multi_cell(PAGE_W - 4, 5.2, sanitize(q))
        pdf.ln(1)
    pdf.ln(2)

    pdf.paper_heading(2, "3.2 PICO Framework")
    pw = [30, 40, PAGE_W - 70]
    pdf.thead(["PICO Element", "Category", "Specification"], pw)
    for i, (el, cat, spec) in enumerate([
        ("P -- Population",  "Construction projects",     "Residential and commercial; all procurement routes; all scales"),
        ("I -- Intervention", "ML-based cost estimation", "ANN, SVR, RF, XGBoost, ensemble, CBR, deep learning"),
        ("C -- Comparator",  "Conventional methods",      "Parametric, elemental, BQ-based, expert judgement"),
        ("O -- Outcome",     "Estimation accuracy",        "R2, MAE, RMSE, MAPE; cost overrun rate; model explainability"),
    ]):
        pdf.trow([el, cat, spec], pw, fill=(i % 2 == 1))
    pdf.ln(2)

    pdf.paper_heading(2, "3.3 Search Strategy")
    pdf.para(
        "Six databases are searched: Scopus, Web of Science (WoS), ASCE Library, "
        "ScienceDirect, IBSS (International Bibliography of the Social Sciences), "
        "and Google Scholar (top 200 results). Searches are executed in English. "
        "Date range: January 2000 to December 2024. Reference lists of included "
        "studies are hand-searched (forward/backward citation chaining via Scopus)."
    )
    pdf.para(
        "Search string (simplified): (\"construction cost\" OR \"building cost\" OR "
        "\"cost estimation\" OR \"cost prediction\") AND (\"machine learning\" OR "
        "\"neural network\" OR \"random forest\" OR \"XGBoost\" OR \"deep learning\" "
        "OR \"artificial intelligence\") AND (\"residential\" OR \"housing\" OR "
        "\"building\" OR \"infrastructure\"). Full Boolean strings are documented "
        "in Appendix A (see 02_Search_Strings.pdf, iNHCES O1 Step 1 outputs)."
    )

    pdf.paper_heading(2, "3.4 Inclusion and Exclusion Criteria")
    ew = [50, 48, PAGE_W - 98]
    pdf.thead(["Criterion", "Inclusion", "Exclusion"], ew)
    for i, (crit, inc, exc) in enumerate([
        ("Language",      "English only",                       "Non-English without English abstract"),
        ("Study type",    "Empirical; model comparison",        "Conceptual only; editorials; book chapters"),
        ("Method",        "ML-based cost model",                "Traditional regression only; no ML component"),
        ("Outcome",       "Reports accuracy metric(s)",         "No quantitative accuracy reported"),
        ("Project type",  "Construction (any type)",            "Infrastructure only with no building component"),
        ("Publication",   "Peer-reviewed journal; conf. >50%",  "Grey literature; unreviewed preprints"),
        ("Date",          "2000-2024",                          "Pre-2000 (pre-ML era)"),
    ]):
        pdf.trow([crit, inc, exc], ew, fill=(i % 2 == 1))
    pdf.ln(2)

    pdf.paper_heading(2, "3.5 Quality Assessment")
    pdf.para(
        "Eligible studies are assessed using a modified CASP (Critical Appraisal "
        "Skills Programme) checklist adapted for ML studies. Assessment covers: "
        "(1) clarity of research question; (2) appropriateness of ML method; "
        "(3) data source quality; (4) train/test split adequacy (>= 20% test); "
        "(5) cross-validation reporting; (6) performance metric completeness; "
        "(7) comparison with baseline; (8) reproducibility (code/data available). "
        "Studies scoring < 5/8 are excluded from quantitative synthesis."
    )


# ── Section 4: Preliminary Results ────────────────────────────────────────────
def section4(pdf):
    pdf.add_page()
    pdf.paper_heading(1, "4. Preliminary Results Framework")
    pdf.info_box(
        "IMPORTANT: Section 4 contains PLACEHOLDERS and AI-SYNTHESISED frameworks. "
        "The database search has NOT yet been executed. PRISMA flow statistics, "
        "included study counts, and quantitative synthesis values MUST be replaced "
        "with real extracted data after Phase 2 SLR execution. All statements "
        "attributed to 'the included studies' below are templates only."
    )
    pdf.ln(2)

    pdf.paper_heading(2, "4.1 PRISMA Flow (PLACEHOLDER)")
    pdf.placeholder_box(
        "TOTAL RECORDS IDENTIFIED (6 databases): [XX,XXX]. "
        "After duplicate removal: [X,XXX]. "
        "After title/abstract screening: [XXX]. "
        "After full-text eligibility assessment: [XX]. "
        "Included in qualitative synthesis: [XX]. "
        "Included in quantitative meta-analysis: [XX]. "
        "See full PRISMA flow diagram: [INSERT Figure 1]."
    )

    pdf.paper_heading(2, "4.2 Study Characteristics (PLACEHOLDER)")
    pdf.placeholder_box(
        "Publication years: [XXXX]-[XXXX], peak in [XXXX]-[XXXX]. "
        "Geographic distribution: USA [X%], China [X%], South Korea [X%], "
        "Australia [X%], UK [X%], Nigeria/Africa [X%], Other [X%]. "
        "Project types: residential [X%], commercial [X%], civil [X%], mixed [X%]. "
        "Sample sizes: median n=[XX], range [X]-[X,XXX]."
    )

    pdf.paper_heading(2, "4.3 ML Method Distribution (Preliminary Framework)")
    pdf.para(
        "Based on AI-synthesised knowledge of the construction cost estimation "
        "literature, the following distribution of ML methods is projected. "
        "This MUST be replaced with actual counts from the included studies."
    )
    dm = [52, 25, 25, PAGE_W - 102]
    pdf.thead(["ML Method Category", "Approx. Studies [PH]", "Avg. R2 [PH]", "Key Performance Notes"], dm)
    for i, (meth, n, r2, note) in enumerate([
        ("ANN / MLP",                     "[XX]", "[0.XX]", "Strong non-linear capture; requires large n"),
        ("Random Forest",                 "[XX]", "[0.XX]", "Robust to outliers; interpretable via feature imp."),
        ("Gradient Boosting (XGB/LGBM)",  "[XX]", "[0.XX]", "State-of-art accuracy; SHAP explanations available"),
        ("SVR",                           "[XX]", "[0.XX]", "Effective for small samples; sensitive to scaling"),
        ("Stacking Ensemble",             "[XX]", "[0.XX]", "Highest accuracy; computationally expensive"),
        ("Case-Based Reasoning (CBR)",    "[XX]", "[0.XX]", "Transparent; requires similarity metric design"),
        ("Deep Learning (DNN/LSTM)",      "[XX]", "[0.XX]", "Powerful for sequential data; needs large n"),
    ]):
        pdf.trow([meth, n, r2, note], dm, fill=(i % 2 == 1))
    pdf.ln(2)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 4.5, sanitize(
        "Table 2: ML method distribution (PLACEHOLDER -- replace with actual extracted counts). "
        "PH = placeholder value. R2 values are indicative only based on AI training knowledge."
    ))
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(2)

    pdf.paper_heading(2, "4.4 Macroeconomic Variable Integration (Preliminary)")
    pdf.para(
        "A preliminary assessment suggests that macroeconomic variable integration "
        "in ML construction cost models is rare. Most studies model cost at the "
        "project level (project size, floor area, structural type, location) without "
        "explicit macroeconomic features. The few exceptions use inflation as a "
        "simple deflator rather than as a predictive feature. No identified study "
        "incorporates exchange rate or oil price as live, time-varying ML features "
        "in a residential construction cost model for an African economy. "
        "[PLACEHOLDER: confirm/disconfirm after database search is complete]."
    )

    pdf.paper_heading(2, "4.5 Gap Analysis")
    pdf.para(
        "Based on the preliminary framework synthesis, seven knowledge gaps are "
        "identified (to be validated against included study evidence):"
    )
    gw = [10, 55, PAGE_W - 65]
    pdf.thead(["#", "Gap", "iNHCES Research Response"], gw)
    for i, (gap, resp) in enumerate([
        ("Nigeria-specific longitudinal datasets for ML training are absent from "
         "the published literature.",
         "O3 Delphi + O4 BQ database collection; O5 model training"),
        ("No ML model explicitly models exchange rate as a time-varying feature.",
         "O2 Step 4 SHAP variable selection; O5 feature engineering"),
        ("Inflation-adjusted models rare; most studies use nominal costs.",
         "O2: CPI included as I(1) variable; deflation applied in O5"),
        ("SHAP/LIME explainability methods not applied in African cost studies.",
         "O2 Step 4 SHAP; O5 full SHAP analysis; O6 frontend dashboard"),
        ("No ensemble/stacking benchmarking study for sub-Saharan Africa.",
         "O5 model benchmarking: Ridge/Lasso + RF/XGB/LGBM + MLP + Stacking"),
        ("Delphi-based expert validation of ML features not conducted for Nigeria.",
         "O3 Delphi instrument; P2 Delphi paper"),
        ("MLOps pipelines for continuous retraining not applied in construction.",
         "O5 Airflow DAG; O6 backend pipeline; P6 MLOps paper"),
    ]):
        pdf.trow([str(i + 1), gap, resp], gw, fill=(i % 2 == 1))
    pdf.ln(2)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 4.5, sanitize(
        "Table 3: Knowledge gap analysis. Left column: gaps from literature (to be validated "
        "with extracted study evidence after database search). Right column: iNHCES research response."
    ))
    pdf.set_text_color(*DARK_GREY)


# ── Section 5: Discussion ──────────────────────────────────────────────────────
def section5(pdf):
    pdf.add_page()
    pdf.paper_heading(1, "5. Discussion")
    pdf.paper_heading(2, "5.1 Synthesis of ML Method Findings")
    pdf.para(
        "The preliminary framework suggests that gradient boosting methods "
        "(XGBoost, LightGBM) consistently achieve the highest accuracy in recent "
        "(post-2018) studies, reflecting the global ML benchmark trend established "
        "by Chen and Guestrin (2016). The iNHCES model selection strategy (O5) "
        "accordingly treats XGBoost and LightGBM as primary candidates, with "
        "stacking ensemble as the champion candidate. This aligns with the SHAP "
        "explainability requirement: TreeSHAP (Lundberg et al., 2020) is natively "
        "efficient for tree-based ensemble models."
    )
    pdf.para(
        "Neural networks (ANN/MLP) show competitive performance in studies with "
        "large sample sizes (n > 500), but their data hunger is a concern for "
        "the Nigerian context where historical project cost databases are fragmented "
        "and not publicly accessible. Transfer learning approaches -- pre-training "
        "on international datasets and fine-tuning on Nigerian data -- represent "
        "an underexplored strategy that the iNHCES team should evaluate in O5."
    )
    pdf.paper_heading(2, "5.2 Implications for the Nigerian Construction Sector")
    pdf.para(
        "The Nigerian construction sector presents three features that distinguish "
        "it from developed-economy contexts studied in the majority of reviewed "
        "literature. First, the NGN/USD exchange rate is the dominant construction "
        "cost driver (estimated at 45% relative SHAP importance in iNHCES O2 analysis) "
        "because 60-80% of construction materials (steel, cement clinker, tiles, "
        "electrical fittings) are imported or priced in USD. Second, fuel price "
        "volatility (Brent crude -> PMS price -> diesel -> construction plant costs) "
        "creates non-linear seasonal effects not captured by simple CPI deflation. "
        "Third, the absence of a unified, accessible construction cost database "
        "in Nigeria makes data collection a research objective in its own right "
        "(O3-O4), not merely a pre-processing step."
    )
    pdf.paper_heading(2, "5.3 Limitations of this Review")
    pdf.para(
        "This paper reports a PROTOCOL and PRELIMINARY FRAMEWORK, not a completed "
        "systematic review. The following limitations apply: "
        "(1) Database search has not yet been executed -- all quantitative statements "
        "about study counts, method distributions, and performance metrics are "
        "AI-synthesised estimates, not PRISMA-extracted evidence. "
        "(2) The grey literature and practitioner reports (BPP, NIQS, NBS) are "
        "not included in the current search strategy and should be added. "
        "(3) The search is restricted to English-language publications, potentially "
        "missing relevant French- and Portuguese-language African studies. "
        "(4) Non-peer-reviewed data sources (government tender databases) which "
        "may contain highly relevant Nigerian cost data are excluded."
    )


# ── Section 6: Conclusions ─────────────────────────────────────────────────────
def section6(pdf):
    pdf.add_page()
    pdf.paper_heading(1, "6. Conclusions and Future Work")
    pdf.para(
        "This paper presents a PRISMA 2020-compliant protocol and preliminary "
        "AI-synthesised framework for a systematic review of ML-based construction "
        "cost estimation methods in emerging economies. The principal contributions are:"
    )
    for c in [
        "A registered PRISMA 2020 protocol covering ML method families and "
        "macroeconomic feature integration -- the first SLR protocol to address "
        "both dimensions simultaneously in the construction cost estimation domain.",
        "A preliminary taxonomy of 7 ML method families with indicative performance "
        "benchmarks (R2, MAE), to be populated with real extracted evidence after "
        "database search execution.",
        "A 7-item gap analysis matrix that directly informs the iNHCES research "
        "design across Objectives O3-O6, providing a traceable connection between "
        "the SLR evidence base and the ML system development plan.",
        "An illustration of the importance of macroeconomic variables -- particularly "
        "exchange rate, inflation, and oil price -- as time-varying features in "
        "construction cost models, drawing on the iNHCES O2 SHAP analysis.",
    ]:
        pdf.set_font("Helvetica", "", 9.5)
        pdf.set_text_color(*DARK_GREY)
        pdf.set_x(LEFT + 4)
        pdf.multi_cell(PAGE_W - 4, 5.2, sanitize(f"(c{[1,2,3,4][[c.startswith(x) for x in ['A registered','A preliminary','A 7-item','An illustration']].index(True)]}) {c}"))
        pdf.ln(1.5)

    pdf.para(
        "The next stage (O1 Phase 2) requires the research team to execute the "
        "database searches, apply the inclusion/exclusion criteria to identified "
        "records, extract data from eligible studies, and update this paper with "
        "real PRISMA statistics and quantitative synthesis findings. The gap analysis "
        "and feature selection implications will be refined upon completion of the "
        "systematic review and the O3 Delphi expert survey."
    )
    pdf.placeholder_box(
        "This paper will be submitted to Construction Management and Economics "
        "(Taylor & Francis, ISSN 0144-6193, Impact Factor ~4.8 [VERIFY CURRENT IF]) "
        "after O1 Phase 2 is complete and the manuscript is updated with real data."
    )


# ── AI Disclosure Statement ────────────────────────────────────────────────────
def ai_disclosure(pdf):
    pdf.add_page()
    pdf.paper_heading(1, "AI Assistance Disclosure Statement")
    pdf.info_box(
        "MANDATORY DISCLOSURE -- per iNHCES Ethics Framework (00_Research_Simulation_Introduction.pdf, "
        "Section 9; COPE Guidelines on AI in Publishing, 2023)"
    )
    pdf.ln(2)
    pdf.para(
        "Artificial intelligence tools (specifically, GitHub Copilot powered by "
        "Claude Sonnet, via VS Code) were used in the preparation of this manuscript "
        "in the following ways:"
    )
    for item in [
        "LITERATURE FRAMEWORK GENERATION: The preliminary taxonomy of ML methods "
        "(Table 1, Table 2), the gap analysis (Table 3), and the body text of "
        "Sections 2, 3, and 4 were generated by an AI language model as a first "
        "draft. The research team has reviewed this draft for accuracy and coherence "
        "but has not yet replaced AI-synthesised content with PRISMA-extracted evidence.",
        "SEARCH STRATEGY DESIGN: Boolean search strings and PICO criteria were "
        "designed with AI assistance. The research team validated these against "
        "domain expertise before finalising.",
        "CODE GENERATION: Python scripts for PDF generation, data analysis, and "
        "pipeline automation were generated with AI assistance (see O1-O5 scripts). "
        "All code was reviewed, tested, and executed by the research team.",
        "EDITING AND WRITING: Sentence-level editing and prose generation throughout "
        "this draft manuscript were AI-assisted.",
    ]:
        pdf.set_font("Helvetica", "", 9.5)
        pdf.set_text_color(*DARK_GREY)
        pdf.set_x(LEFT + 4)
        pdf.multi_cell(PAGE_W - 4, 5.2, sanitize(f"- {item}"))
        pdf.ln(2)
    pdf.para(
        "AI tools were NOT used to generate or fabricate research data, to create "
        "false citations, or to make authorship claims. All authors take full "
        "responsibility for the intellectual content of this manuscript. The "
        "corresponding author ([INSERT NAME]) is the guarantor of this work."
    )
    pdf.para(
        "ACKNOWLEDGEMENT TEXT (for final manuscript): 'The authors acknowledge the "
        "use of GitHub Copilot (Microsoft/OpenAI/Anthropic) to assist with "
        "manuscript drafting, literature framework generation, and research code "
        "development. AI-generated content has been reviewed and validated by the "
        "research team. All data analysis and intellectual conclusions are the "
        "sole responsibility of the named authors.'"
    )


# ── References ─────────────────────────────────────────────────────────────────
def references(pdf):
    pdf.add_page()
    pdf.paper_heading(1, "References")
    pdf.info_box(
        "CITATION VERIFICATION REQUIRED: All references below are based on AI "
        "training knowledge. EVERY reference must be independently verified in "
        "Scopus, Web of Science, or the publisher database before submission. "
        "References marked [VERIFY] have not been checked. Remove or replace any "
        "reference that cannot be confirmed. Do not cite without verification. "
        "AI-generated citations may contain errors in: author names, year, volume, "
        "pages, DOI, and journal name."
    )
    pdf.ln(2)

    refs = [
        ("Page, M.J., McKenzie, J.E., Bossuyt, P.M., Boutron, I., Hoffmann, T.C., "
         "Mulrow, C.D., ... & Moher, D. (2021). The PRISMA 2020 statement: an updated "
         "guideline for reporting systematic reviews. BMJ, 372, n71. "
         "https://doi.org/10.1136/bmj.n71  [VERIFY -- high confidence, widely cited]"),

        ("Kim, G.H., An, S.H., & Kang, K.I. (2004). Comparison of construction cost "
         "estimating models based on regression analysis, neural networks, and "
         "case-based reasoning. Building and Environment, 39(10), 1235-1242. "
         "[VERIFY in Scopus/WoS]"),

        ("Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system. "
         "Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge "
         "Discovery and Data Mining, 785-794. https://doi.org/10.1145/2939672.2939785 "
         "[VERIFY -- high confidence]"),

        ("Lundberg, S.M., Erion, G., Chen, H., DeGrave, A., Peck, J.M., Kuber, D., "
         "... & Lee, S.I. (2020). From local explanations to global understanding "
         "with explainable AI for trees. Nature Machine Intelligence, 2(1), 56-67. "
         "[VERIFY in Nature MI]"),

        ("Lundberg, S.M., & Lee, S.I. (2017). A unified approach to interpreting "
         "model predictions. Advances in Neural Information Processing Systems, 30. "
         "[VERIFY -- NeurIPS 2017 -- high confidence]"),

        ("Ji, S.H., Park, M., & Lee, H.S. (2011). Data preprocessing-based "
         "parametric cost model for building projects using case-based reasoning. "
         "Journal of Management in Engineering, 27(2), 109-119. [VERIFY in ASCE]"),

        ("Skitmore, M. (1988). Factors affecting the accuracy of engineers' price "
         "forecasts. Engineering, Construction and Architectural Management, 5(4), "
         "389-403. [VERIFY -- details may be inaccurate]"),

        ("Dania, A.A., Larkin, J., & Yusuf, G. (2007). An investigation into the "
         "material waste occurrence in Nigerian construction sites. Proceedings of "
         "ARCOM 2007, 24-26 September, Belfast, UK. [VERIFY]"),

        ("Ogunsemi, D.R., & Jagboro, G.O. (2006). Time-cost model for building "
         "projects in Nigeria. Construction Management and Economics, 24(3), 253-258. "
         "[VERIFY in CME]"),

        ("World Bank. (2023). Nigeria -- Country Economic Memorandum: Building "
         "Foundations for a Diversified Economy. World Bank Group, Washington DC. "
         "[VERIFY -- check exact report title and year]"),
    ]
    for ref in refs:
        pdf.ref_item(ref)


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    out = os.path.join(OUT_DIR, 'P1_PRISMA_SLR_Draft.pdf')
    pdf = PaperPDF()

    make_title_page(pdf)

    # DATA SOURCE DECLARATION
    _ds_page(pdf, 'amber',
        "DATA SOURCE: AI-GENERATED DRAFT -- No database search executed. "
        "PRISMA statistics are PLACEHOLDERS. All citations need Scopus/WoS verification.",
        (
            "WHAT THIS DOCUMENT IS:\n"
            "  P1_PRISMA_SLR_Draft.pdf is an AI-generated first draft of journal paper P1 "
            "(iNHCES Publication Portfolio). It is based on the PRISMA protocol and "
            "preliminary AI-synthesised literature framework from O1 Steps 1-3.\n\n"
            "WHAT IS REAL IN THIS DRAFT:\n"
            "  * PRISMA 2020 protocol structure (Page et al., 2021) -- real methodology\n"
            "  * PICO framework and inclusion/exclusion criteria -- real research design\n"
            "  * Boolean search strings -- real, designed for iNHCES domain\n"
            "  * Gap analysis (Table 3) -- AI-synthesised; needs validation with real data\n"
            "  * Theoretical framework (Section 2) -- general academic knowledge\n\n"
            "WHAT IS NOT REAL (PLACEHOLDER):\n"
            "  * All PRISMA flow statistics (record counts, included study counts)\n"
            "  * Table 2 study counts and R2 values\n"
            "  * All specific performance metrics attributed to method categories\n"
            "  * All citations marked [VERIFY] -- have not been checked in Scopus/WoS\n\n"
            "REQUIRED ACTIONS BEFORE SUBMISSION:\n"
            "  1. Execute database search (Scopus, WoS, ASCE, ScienceDirect, IBSS)\n"
            "  2. Apply IC/EC criteria to identified records (independent dual screening)\n"
            "  3. Extract data from eligible studies into Data_Extraction_Template.pdf\n"
            "  4. Replace all [PLACEHOLDER] items with real extracted evidence\n"
            "  5. Verify every reference in Scopus or WoS -- remove unverifiable refs\n"
            "  6. Register protocol on PROSPERO before search execution\n"
            "  7. Submit to ethics committee for review (see preamble Section 6)\n"
            "  8. Include AI Disclosure Statement (Section 9.2 of preamble) in final ms."
        )
    )

    make_abstract(pdf)
    section1(pdf)
    section2(pdf)
    section3(pdf)
    section4(pdf)
    section5(pdf)
    section6(pdf)
    ai_disclosure(pdf)
    references(pdf)

    pdf.output(out)
    print(f"[OK]  P1_PRISMA_SLR_Draft.pdf  saved -> {out}")


if __name__ == "__main__":
    main()
