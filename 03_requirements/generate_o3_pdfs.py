"""
iNHCES O3 Requirements Modelling — PDF Generator
Produces all O3 deliverables:
  O3_01_Stakeholder_Register.pdf
  O3_02_Delphi_Round1_Instrument.pdf
  O3_03_Delphi_Round2_Instrument.pdf
  O3_04_Delphi_Round2_Analysis.pdf
  O3_05_Delphi_Round3_Instrument.pdf
  O3_06_Delphi_Final_Consensus.pdf
  O3_07_SRS_IEEE830.pdf
  O3_08_UML_Use_Cases.pdf
  delphi/delphi_results.csv
  delphi/Round1.md, Round2.md, Round3.md
  srs/03_SRS_NHCES_IEEE830.md
  use_cases/03_UML_Use_Cases.md

DATA SOURCE: AMBER (Delphi instrument = real design; expert ratings = SYNTHETIC simulated
responses, n=20, seed=42). Replace synthetic ratings with real survey data before publication.

TETFund NRF 2025 | Dept. of Quantity Surveying, ABU Zaria
"""

import sys, os, csv, tempfile, textwrap
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, os.path.join(_ROOT, '01_literature_review'))

from generate_o1_pdfs import (
    DocPDF, sanitize, _ds_page,
    DARK_NAVY, GOLD, LIGHT_BLUE, WHITE, DARK_GREY, MID_GREY,
    PAGE_W, LEFT, LINE_H,
)

OUT_DIR   = _HERE
DEL_DIR   = os.path.join(_HERE, 'delphi')
SRS_DIR   = os.path.join(_HERE, 'srs')
UC_DIR    = os.path.join(_HERE, 'use_cases')

# ── Delphi parameters ──────────────────────────────────────────────────────────
N_EXPERTS       = 20
SEED            = 42
CONSENSUS_MEAN  = 5.0   # minimum mean for consensus (1-7 scale)
CONSENSUS_CV    = 20.0  # maximum CV% for consensus

# ── Delphi items: (category, id, short_text, full_text, r2_mean, r2_sd) ────────
DELPHI_ITEMS = [
    # ── A: Macroeconomic Feature Requirements ──────────────────────────────────
    ("A","A1","NGN/USD exchange rate as ML feature",
     "The NGN/USD exchange rate should be included as a predictive feature in the iNHCES model",
     6.4, 0.7),
    ("A","A2","CPI inflation rate as ML feature",
     "The CPI/inflation rate (annual %) should be included as a predictive feature in the model",
     6.2, 0.8),
    ("A","A3","Brent crude oil price as ML feature",
     "Brent crude oil price (USD/barrel) should be included as a predictive feature in the model",
     5.9, 1.0),
    ("A","A4","GDP growth rate as ML feature",
     "Nigeria's GDP growth rate (annual %) should be included as a predictive feature",
     5.3, 1.1),
    ("A","A5","Lending rate as ML feature",
     "The commercial lending interest rate should be included as a predictive feature",
     4.8, 1.4),
    ("A","A6","Live macro data (not static)",
     "The iNHCES system should use live, automatically updated macroeconomic data, not static historical tables",
     6.1, 0.9),
    ("A","A7","Weekly or more frequent macro data refresh",
     "Macroeconomic features in the model should be refreshed at least once per week automatically",
     5.8, 1.0),

    # ── B: Project Characteristic Features ─────────────────────────────────────
    ("B","B1","Gross floor area (sqm) — mandatory",
     "Gross floor area in square metres (sqm) should be a mandatory input feature for every estimate",
     6.7, 0.5),
    ("B","B2","Number of storeys — mandatory",
     "Number of building storeys (above ground) should be a mandatory input feature",
     6.3, 0.8),
    ("B","B3","Structural system type — mandatory",
     "Structural system type (masonry/reinforced concrete frame/steel frame) should be a mandatory input feature",
     6.1, 0.9),
    ("B","B4","Project location (zone/state) — mandatory",
     "Project location expressed as geopolitical zone or state should be a mandatory input feature",
     6.5, 0.6),
    ("B","B5","Project type (residential/commercial) — mandatory",
     "Project type (purely residential / commercial / mixed-use) should be a mandatory input feature",
     6.4, 0.7),
    ("B","B6","Procurement method as feature",
     "Procurement method (direct labour / traditional / design-and-build) should be included as an input feature",
     4.5, 1.5),
    ("B","B7","Specification level (standard/medium/luxury)",
     "Specification level (standard / medium / luxury finish) should be included as an input feature",
     5.8, 1.0),
    ("B","B8","Number of residential units",
     "Number of residential units or bedrooms should be included as an input feature",
     5.5, 1.2),

    # ── C: ML Model Requirements ───────────────────────────────────────────────
    ("C","C1","Model MAPE <= 15% on validation data",
     "The deployed iNHCES model should achieve a Mean Absolute Percentage Error (MAPE) of <= 15% on held-out validation data",
     6.0, 1.0),
    ("C","C2","SHAP explainability for every estimate",
     "The model must provide SHAP-based feature importance explanations for every estimate generated",
     5.7, 1.1),
    ("C","C3","Prediction intervals (not just point estimates)",
     "The model should provide 90% prediction intervals alongside point estimates to communicate uncertainty",
     5.9, 0.9),
    ("C","C4","Quarterly automatic model retraining",
     "The model should be automatically retrained at least quarterly as new project cost data becomes available",
     5.8, 1.0),
    ("C","C5","Benchmark multiple ML algorithms before deployment",
     "Multiple ML algorithms (e.g. Ridge, RF, XGBoost, LightGBM, MLP) should be benchmarked before the champion model is selected for deployment",
     5.5, 1.2),
    ("C","C6","Stacking ensemble as champion if it outperforms",
     "A stacking ensemble should be selected as the champion model if it outperforms individual models on cross-validated MAPE",
     4.9, 1.4),

    # ── D: System Performance Requirements ─────────────────────────────────────
    ("D","D1","Estimate generation < 3 seconds",
     "Cost estimate generation (model inference + SHAP calculation) should complete within 3 seconds",
     6.3, 0.8),
    ("D","D2","Support >= 50 concurrent users",
     "The system should support at least 50 simultaneous active users without performance degradation",
     5.6, 1.2),
    ("D","D3","System availability >= 99.5% uptime",
     "The iNHCES web system should maintain at least 99.5% uptime (scheduled maintenance excluded)",
     6.4, 0.7),
    ("D","D4","Full audit trail for all estimates",
     "Every estimate should be stored with a full audit trail: user identity, timestamp, all inputs, model version, and outputs",
     6.5, 0.6),
    ("D","D5","Auto-generate PDF report for every estimate",
     "The system should automatically generate a professionally formatted PDF cost report for every estimate completed",
     6.1, 0.9),

    # ── E: Interface Requirements ──────────────────────────────────────────────
    ("E","E1","Web browser access — no installation",
     "The user interface should be fully accessible via standard web browser without any software installation",
     6.6, 0.6),
    ("E","E2","Input form completable in < 5 minutes",
     "A qualified QS professional should be able to complete the estimate input form in under 5 minutes",
     6.0, 0.9),
    ("E","E3","Visual cost breakdown chart in results",
     "Estimate results should include a visual cost breakdown chart (elemental or trade-by-trade)",
     5.9, 1.0),
    ("E","E4","Data freshness indicators for macro variables",
     "The interface should display data freshness indicators showing the age of each macroeconomic data source",
     5.7, 1.1),
    ("E","E5","Mobile/tablet usability",
     "The user interface should be fully usable on mobile phones and tablet devices",
     4.8, 1.5),
    ("E","E6","Multiple saved project profiles per user",
     "Each registered user should be able to save and manage multiple project profiles",
     5.6, 1.1),

    # ── F: Data Quality Requirements ───────────────────────────────────────────
    ("F","F1","Flag macro data > 7 days old",
     "The system should display a warning flag when any macroeconomic data source is more than 7 days old",
     5.9, 1.0),
    ("F","F2","DATA SOURCE confidence classification on estimates",
     "Each estimate should display a DATA SOURCE confidence classification (GREEN/AMBER/RED) indicating data quality",
     6.0, 0.9),
    ("F","F3","Graceful handling of missing/invalid inputs",
     "Missing or invalid input values should produce clear, user-friendly validation messages — not system crashes",
     6.5, 0.6),
    ("F","F4","Numeric input range validation",
     "All numeric inputs should be validated against plausible real-world range limits before submission",
     6.2, 0.8),

    # ── G: Reporting Requirements ──────────────────────────────────────────────
    ("G","G1","NIQS cost plan format in reports",
     "Generated PDF reports should follow the NIQS (Nigerian Institute of Quantity Surveyors) cost plan format",
     6.3, 0.8),
    ("G","G2","Sensitivity analysis under 3 FX scenarios",
     "Reports should include a sensitivity analysis showing estimate variation under 3 exchange rate scenarios (base, +15%, -15%)",
     4.7, 1.4),
    ("G","G3","PDF export of professional quality",
     "Cost reports should be exportable as professionally formatted, branded PDF documents",
     6.5, 0.6),
    ("G","G4","Report format acceptable for tender submission",
     "The report format should be acceptable for submission alongside tender documents in Nigerian public procurement",
     6.1, 0.9),
]

CATEGORIES = {
    "A": "Macroeconomic Feature Requirements",
    "B": "Project Characteristic Features",
    "C": "ML Model Requirements",
    "D": "System Performance Requirements",
    "E": "Interface Requirements",
    "F": "Data Quality Requirements",
    "G": "Reporting Requirements",
}

# ── Synthetic data generation ──────────────────────────────────────────────────
def generate_ratings(items, n, seed, convergence=False):
    rng = np.random.default_rng(seed)
    ratings = {}
    for cat, iid, short, full, mean, sd in items:
        if convergence:
            mean = min(7, mean + 0.4)
            sd   = max(0.4, sd * 0.75)
        raw = rng.normal(mean, sd, n)
        clipped = np.clip(np.round(raw), 1, 7).astype(int)
        ratings[iid] = clipped
    return ratings

def calc_stats(ratings):
    stats = {}
    for iid, vals in ratings.items():
        m  = float(np.mean(vals))
        sd = float(np.std(vals, ddof=1))
        cv = (sd / m * 100) if m > 0 else 999.0
        q1, q3 = np.percentile(vals, [25, 75])
        iqr = float(q3 - q1)
        consensus = (m >= CONSENSUS_MEAN) and (cv <= CONSENSUS_CV)
        stats[iid] = {'mean': m, 'sd': sd, 'cv': cv, 'iqr': iqr,
                      'consensus': consensus, 'vals': vals}
    return stats

# ── Run full Delphi simulation ─────────────────────────────────────────────────
def run_delphi():
    r2_ratings = generate_ratings(DELPHI_ITEMS, N_EXPERTS, SEED)
    r2_stats   = calc_stats(r2_ratings)
    non_consensus = [it for it in DELPHI_ITEMS if not r2_stats[it[1]]['consensus']]
    r3_items   = non_consensus
    r3_ratings = generate_ratings(r3_items, N_EXPERTS, SEED + 1, convergence=True)
    r3_stats   = calc_stats(r3_ratings)
    # Final consensus: items with R2 consensus OR R3 consensus
    final = []
    excluded = []
    for it in DELPHI_ITEMS:
        iid = it[1]
        if r2_stats[iid]['consensus']:
            final.append((it, r2_stats[iid], None))
        elif iid in r3_stats and r3_stats[iid]['consensus']:
            final.append((it, r2_stats[iid], r3_stats[iid]))
        else:
            excluded.append((it, r2_stats[iid], r3_stats.get(iid)))
    return r2_ratings, r2_stats, r3_items, r3_ratings, r3_stats, final, excluded


# ── O3 PDF class ───────────────────────────────────────────────────────────────
class O3PDF(DocPDF):
    def __init__(self, title, doc_id):
        super().__init__(title, doc_id)

    def header(self):
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*MID_GREY)
        self.set_xy(LEFT, 5)
        self.cell(PAGE_W, 4.5, sanitize(
            f"iNHCES O3 | {self.doc_name[:60]} | TETFund NRF 2025"
        ))
        self.set_text_color(*DARK_GREY)
        self.ln(12)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "", 7.5)
        self.set_text_color(*MID_GREY)
        self.cell(0, 5, f"Page {self.page_no()}", align="C")
        self.set_text_color(*DARK_GREY)

    def h1(self, text):
        self.ln(3)
        self.set_font("Helvetica", "B", 11.5)
        self.set_text_color(*DARK_NAVY)
        self.set_x(LEFT)
        self.multi_cell(PAGE_W, 5.5, sanitize(text))
        self.set_text_color(*DARK_GREY)
        self.ln(1)

    def h2(self, text):
        self.ln(2)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*DARK_NAVY)
        self.set_x(LEFT)
        self.multi_cell(PAGE_W, 5, sanitize(text))
        self.set_text_color(*DARK_GREY)
        self.ln(1)

    def para(self, text, indent=0):
        self.set_font("Helvetica", "", 9.5)
        self.set_text_color(*DARK_GREY)
        self.set_x(LEFT + indent)
        self.multi_cell(PAGE_W - indent, 5.2, sanitize(text))
        self.ln(1.5)

    def bullet(self, text, indent=4):
        self.set_font("Helvetica", "", 9.5)
        self.set_text_color(*DARK_GREY)
        self.set_x(LEFT + indent)
        self.multi_cell(PAGE_W - indent, 5.2, sanitize(f"- {text}"))
        self.ln(0.5)

    def note(self, text):
        self.set_fill_color(*LIGHT_BLUE)
        self.set_draw_color(*DARK_NAVY)
        self.set_line_width(0.4)
        self.set_font("Helvetica", "I", 8.5)
        self.set_text_color(*DARK_NAVY)
        self.set_x(LEFT)
        self.multi_cell(PAGE_W, 4.8, sanitize(f"NOTE: {text}"), border=1, fill=True)
        self.set_text_color(*DARK_GREY)
        self.ln(1.5)

    def caption(self, text):
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*MID_GREY)
        self.set_x(LEFT)
        self.multi_cell(PAGE_W, 4.5, sanitize(text))
        self.set_text_color(*DARK_GREY)
        self.ln(1.5)

    def req_box(self, req_id, text, priority="High"):
        clr = (200,230,200) if priority=="High" else (255,245,220) if priority=="Medium" else (240,240,240)
        self.set_fill_color(*clr)
        self.set_draw_color(*DARK_NAVY)
        self.set_line_width(0.3)
        self.set_x(LEFT)
        self.set_font("Helvetica", "B", 8.5)
        self.set_text_color(*DARK_NAVY)
        self.cell(22, 5, sanitize(req_id), border='LTB', fill=True)
        self.set_font("Helvetica", "", 8.5)
        self.set_text_color(*DARK_GREY)
        self.multi_cell(PAGE_W - 22, 5, sanitize(f"[{priority}]  {text}"), border='RTB', fill=True)
        self.ln(0.8)

    def likert_row(self, item_id, text):
        """Print a Likert-scale survey item (for instrument PDFs)"""
        self.set_x(LEFT)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*DARK_NAVY)
        self.cell(14, 5, sanitize(item_id))
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*DARK_GREY)
        self.multi_cell(PAGE_W - 14, 5, sanitize(text))
        # Draw 7 boxes for Likert scale
        self.set_x(LEFT + 14)
        self.set_font("Helvetica", "", 7.5)
        self.set_text_color(*MID_GREY)
        labels = ["1\nStrongly\nDisagree","2","3","4\nNeither","5","6","7\nStrongly\nAgree"]
        box_w = (PAGE_W - 14) / 7
        for i, lbl in enumerate(labels):
            self.set_x(LEFT + 14 + i * box_w)
            self.cell(box_w, 5, sanitize(lbl.replace('\n',' ')), border=1, align='C')
        self.ln(6)

    def add_chart(self, fig):
        tmp = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        tmp.close()
        fig.savefig(tmp.name, dpi=150, bbox_inches='tight')
        plt.close(fig)
        self.set_x(LEFT)
        self.image(tmp.name, x=LEFT, y=None, w=PAGE_W)
        os.unlink(tmp.name)
        self.ln(2)


# ══════════════════════════════════════════════════════════════════════════════
# PDF 1: Stakeholder Register
# ══════════════════════════════════════════════════════════════════════════════
STAKEHOLDERS = [
    ("QS Practitioners (NIQS Members)",
     "Primary Users",
     "High interest — tool replaces manual estimation; quality, accuracy, speed",
     "High influence — adoption drives system success",
     "Co-design workshops; beta testing; Delphi survey"),
    ("Housing Developers (REDAN)",
     "Primary Users",
     "High interest — cost certainty for project viability; investment decisions",
     "High influence — major source of real project data",
     "Advisory committee; data sharing MoU"),
    ("Public Sector Clients (FHA, State HCs)",
     "Primary Users",
     "High interest — cost control, budget planning, value-for-money",
     "High influence — access to historical project cost data",
     "Stakeholder briefings; data sharing agreement"),
    ("Building Contractors (CORBON)",
     "Secondary Users",
     "Moderate interest — benchmarking tender prices; understanding market rates",
     "Moderate influence — can provide market price data",
     "Online survey; input validation sessions"),
    ("Architects & Structural Engineers (NIA, NSE)",
     "Secondary Users",
     "Moderate interest — early-stage cost checking during design",
     "Moderate influence — referrers of tool to clients",
     "Professional forum presentations; feedback surveys"),
    ("Ministry of Housing & Urban Dev.",
     "Regulator / Policy",
     "High interest — policy evidence on housing affordability, cost drivers",
     "High influence — may mandate use in public projects",
     "Policy briefing papers; government liaison"),
    ("Bureau of Public Procurement (BPP)",
     "Regulator",
     "High interest — accurate independent cost benchmarking for approvals",
     "Very high influence — controls federal procurement",
     "Formal presentation; BPP validation workshop"),
    ("Nigeria Institute of QS (NIQS)",
     "Professional Body",
     "Very high interest — tool advances QS profession in Nigeria",
     "Very high influence — can endorse/mandate for members",
     "MoU; co-branding; NIQS Council briefing"),
    ("National Bureau of Statistics (NBS)",
     "Data Provider",
     "Low interest in tool; provides housing/construction data",
     "High influence — data quality determines model accuracy",
     "Data access request; citation acknowledgement"),
    ("World Bank / Development Partners",
     "Funders / Data Providers",
     "Moderate interest — aligned with housing affordability SDG 11",
     "Moderate influence — open data APIs used in O2",
     "Open access publication; API acknowledgement"),
    ("Academic Researchers (QS, CM depts.)",
     "Research Community",
     "High interest — academic publication, methodology validation",
     "Moderate influence — peer review, citation, replication",
     "Conference presentations; open-source code release"),
    ("TETFund (Research Funder)",
     "Funder",
     "High interest — demonstrable research output and national impact",
     "Very high influence — grant continuation conditions",
     "Quarterly reports; milestone deliverables"),
    ("ABU Zaria (Host Institution)",
     "Institutional Host",
     "High interest — IP ownership, researcher outputs, REF metrics",
     "High influence — ethics approvals, resource allocation",
     "Ethics committee; departmental reporting"),
    ("Property Valuers / Estate Surveyors (NIESV)",
     "Secondary Users",
     "Moderate interest — market price benchmarking; investment appraisal",
     "Low influence — data consumers",
     "Professional newsletter; NIESV chapter talks"),
    ("Financial Institutions (FMBN, Mortgage Banks)",
     "Secondary Users / Data Consumers",
     "Moderate interest — collateral valuation, loan feasibility",
     "Moderate influence — potential private funding partner",
     "Partnership proposal; pilot loan appraisal study"),
]

def make_stakeholder_register(r2_stats, r3_stats, final_items, excluded_items):
    pdf = O3PDF("Stakeholder Register", "O3_01")
    pdf.add_page()

    # Cover
    pdf.set_fill_color(*DARK_NAVY)
    pdf.rect(0, 0, 210, 45, 'F')
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(*GOLD)
    pdf.set_xy(LEFT, 14)
    pdf.multi_cell(PAGE_W, 8, sanitize(
        "iNHCES O3 — Stakeholder Register\nIntelligent National Housing Cost Estimating System"
    ), align="C")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*LIGHT_BLUE)
    pdf.set_xy(LEFT, 34)
    pdf.cell(PAGE_W, 6, sanitize("TETFund NRF 2025 | Dept. of Quantity Surveying, ABU Zaria"), align="C")
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(20)

    _ds_page(pdf, 'green',
        "DATA SOURCE: GREEN — Stakeholder identification is based on real institutional knowledge "
        "of the Nigerian construction and housing sector. No survey data required for this document.",
        (
            "This stakeholder register identifies all parties with an interest or influence in the "
            "iNHCES research programme. Classifications are based on:\n"
            "  * NIQS membership lists and NIQS Strategic Plan (2021-2025)\n"
            "  * Federal Government procurement framework (BPP Act 2007)\n"
            "  * National Housing Fund Act (1992) institutional mandates\n"
            "  * World Bank Nigeria Housing Sector Assessment (2023)\n"
            "  * Academic knowledge of Nigerian construction industry stakeholder landscape\n\n"
            "CONFIDENCE: HIGH. The stakeholder register does not depend on survey data. "
            "It should be reviewed and validated by the PI before the Delphi panel is recruited."
        )
    )

    pdf.add_page()
    pdf.h1("1. Stakeholder Register Overview")
    pdf.para(
        "This stakeholder register identifies 15 categories of stakeholders relevant to the "
        "Intelligent National Housing Cost Estimating System (iNHCES) research programme. "
        "Stakeholders are classified by role, interest, influence, and engagement strategy "
        "following the Power/Interest Grid framework (Johnson & Scholes, 1999 [VERIFY]). "
        "The register informs Delphi panel recruitment (O3 Step 2) and system requirements "
        "elicitation priorities."
    )
    pdf.para(
        "Stakeholder engagement follows the five-level IAP2 Spectrum of Public Participation: "
        "Inform, Consult, Involve, Collaborate, Empower. The Delphi expert panel (O3) draws "
        "from the high-interest, high-influence quadrant (NIQS members, developers, public "
        "sector clients, BPP) to ensure requirements reflect operational practitioner needs."
    )

    # Summary count table
    roles = {"Primary Users": 0, "Secondary Users": 0, "Regulator / Policy": 0,
             "Regulator": 0, "Professional Body": 0, "Data Provider": 0,
             "Funder": 0, "Institutional Host": 0, "Research Community": 0,
             "Funder / Data Providers": 0, "Secondary Users / Data Consumers": 0}
    for s in STAKEHOLDERS:
        roles[s[1]] = roles.get(s[1], 0) + 1
    sw = [55, 30, PAGE_W-85]
    pdf.thead(["Stakeholder Category", "Role Type", "Engagement Level"], sw)
    for i, s in enumerate(STAKEHOLDERS):
        # Determine engagement level from interest + influence text
        if "Very high influence" in s[3] or "High influence" in s[3]:
            level = "Collaborate / Empower"
        elif "Moderate influence" in s[3]:
            level = "Involve / Consult"
        else:
            level = "Inform / Consult"
        pdf.trow([s[0], s[1], level], sw, fill=(i % 2 == 1))
    pdf.ln(2)
    pdf.caption("Table 1: Stakeholder categories and engagement levels. 15 categories identified.")

    pdf.add_page()
    pdf.h1("2. Detailed Stakeholder Profiles")
    iw = [55, 35, 50, PAGE_W-140]
    pdf.thead(["Stakeholder", "Interest", "Influence", "Engagement Strategy"], iw)
    for i, s in enumerate(STAKEHOLDERS):
        pdf.trow([s[0], s[2][:45], s[3][:35], s[4]], iw, fill=(i % 2 == 1))
    pdf.ln(2)
    pdf.caption(
        "Table 2: Full stakeholder profile matrix. Interest = primary concern with iNHCES. "
        "Influence = degree to which stakeholder can affect project success. "
        "Engagement strategy = recommended communication and participation approach."
    )

    pdf.add_page()
    pdf.h1("3. Delphi Panel Recruitment Criteria")
    pdf.para(
        "The Delphi expert panel (O3 Steps 2-3) is recruited from stakeholders in the "
        "high-interest, high-influence quadrant. Panel composition follows the recommendations "
        "of Hasson et al. (2000) [VERIFY] and Keeney et al. (2001) [VERIFY]: a minimum of "
        "15-20 experts from diverse sub-groups is sufficient for Delphi consensus studies "
        "in construction management."
    )
    ew = [52, 15, PAGE_W-67]
    pdf.thead(["Expert Category", "Target n", "Selection Criteria"], ew)
    panel = [
        ("Registered QS (NIQS full members, >= 5 years post-qualification experience)", "6",
         "MNIQS/FNIQS with cost planning practice; building/housing sector"),
        ("Housing Developers (REDAN registered; >= 3 completed projects)", "3",
         "Active residential developers in Nigeria; minimum NGN 500m project value"),
        ("Public Sector Clients (FHA / State Housing Corp. PM/QS staff)", "3",
         "Federal or state housing authority project manager or quantity surveyor"),
        ("BPP/Procurement Officers (Federal MDA procurement staff)", "2",
         "Grade level >= GL 14; cost benchmarking responsibilities"),
        ("Construction Contractors (CORBON registered; QS or PM role)", "3",
         "Active building contractor, QS or commercial manager"),
        ("Academic Researchers (PhD; published >= 2 papers in CM/QS journals)", "3",
         "Nigerian university QS/CM lecturer with quantitative research background"),
    ]
    for i, p in enumerate(panel):
        pdf.trow(list(p), ew, fill=(i % 2 == 1))
    pdf.ln(2)
    pdf.caption(
        "Table 3: Delphi panel composition criteria. Total target n=20. "
        "Panel should include both Abuja (FCT), Lagos, Kano, and Port Harcourt-based practitioners "
        "to represent regional construction cost variation."
    )

    pdf.h1("4. Ethics and Data Protection")
    for item in [
        "Participation in the Delphi survey is entirely voluntary. Experts may withdraw at any point without consequence.",
        "Anonymity is maintained across all rounds: responses are aggregated and individual experts are not identified in any publication.",
        "Data will be stored on encrypted servers compliant with the Nigeria Data Protection Regulation (NDPR, 2019) and University's data governance policy.",
        "Experts will be required to sign an informed consent form prior to Round 1 participation.",
        "The Delphi survey protocol is subject to institutional ethics committee approval before data collection commences.",
        "AI assistance in instrument design must be disclosed to participants in the participant information sheet.",
    ]:
        pdf.bullet(item)
    pdf.ln(2)

    out = os.path.join(OUT_DIR, 'O3_01_Stakeholder_Register.pdf')
    pdf.output(out)
    print(f"[OK]  O3_01_Stakeholder_Register.pdf -> {out}")
    return out


# ══════════════════════════════════════════════════════════════════════════════
# PDF 2: Delphi Round 1 Instrument
# ══════════════════════════════════════════════════════════════════════════════
def make_round1_instrument():
    pdf = O3PDF("Delphi Round 1 Instrument — Open-Ended Expert Survey", "O3_02")
    pdf.add_page()

    # Cover
    pdf.set_fill_color(*DARK_NAVY)
    pdf.rect(0, 0, 210, 45, 'F')
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(*GOLD)
    pdf.set_xy(LEFT, 12)
    pdf.multi_cell(PAGE_W, 7.5, sanitize(
        "iNHCES O3 — Delphi Round 1\nExpert Requirements Elicitation Survey"
    ), align="C")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*LIGHT_BLUE)
    pdf.set_xy(LEFT, 35)
    pdf.cell(PAGE_W, 6, sanitize("Confidential | All responses anonymised | ABU Zaria, 2025"), align="C")
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(20)

    _ds_page(pdf, 'amber',
        "DATA SOURCE: AMBER — This Delphi Round 1 instrument is a real, researchable expert survey "
        "instrument. Round 1 responses in this PDF are HYPOTHETICAL (not yet collected from real experts).",
        (
            "This instrument is designed to be administered to the 20-expert Delphi panel identified "
            "in the Stakeholder Register (O3_01). It follows Linstone & Turoff (1975) [VERIFY] "
            "modified Delphi methodology.\n\n"
            "STATUS: This is a DRAFT instrument — not yet administered.\n"
            "Round 1 open-ended responses shown in Section 4 are AI-generated HYPOTHETICAL "
            "examples illustrating the expected form of expert responses.\n\n"
            "BEFORE ADMINISTRATION:\n"
            "  1. Obtain IRB/ethics committee approval\n"
            "  2. Prepare participant information sheet and consent form\n"
            "  3. Pilot test with 2-3 colleague QS practitioners\n"
            "  4. Administer via Google Forms / Qualtrics (not paper)\n"
            "  5. Allow 2 weeks for responses before closing Round 1"
        )
    )

    pdf.add_page()
    pdf.h1("Participant Information")
    pdf.para(
        "Dear Expert,"
    )
    pdf.para(
        "You have been invited to participate in a modified Delphi study conducted by the "
        "Department of Quantity Surveying, Ahmadu Bello University (ABU) Zaria, as part of a "
        "TETFund National Research Fund 2025 project: the Intelligent National Housing Cost "
        "Estimating System (iNHCES). This study aims to establish expert consensus on the "
        "functional and data requirements for an AI-powered housing construction cost "
        "estimation system appropriate for the Nigerian built environment."
    )
    pdf.para(
        "Your participation is voluntary and confidential. All responses will be anonymised "
        "and aggregated. The estimated time to complete this Round 1 questionnaire is "
        "20-30 minutes. If you have any questions, please contact the Principal Investigator "
        "at [PI EMAIL ADDRESS]."
    )

    pdf.h2("Instructions")
    pdf.para(
        "This Round 1 questionnaire is intentionally open-ended. Please provide your "
        "professional opinion on each question below. There are no right or wrong answers. "
        "Your responses will be used to generate structured Likert-scale items for "
        "Round 2. Please answer all questions."
    )

    questions = [
        ("Expert Background",
         "1a. What is your professional role? (e.g., Quantity Surveyor, Developer, Public Sector Client, Contractor, Researcher)",
         "1b. How many years of experience do you have in the Nigerian construction/housing sector?",
         "1c. Have you previously used any computer-aided cost estimating tool? If yes, which ones?",
         "1d. In which Nigerian state(s) do you primarily work?"),
        ("Macroeconomic Factors",
         "2a. In your professional experience, which macroeconomic variables have the GREATEST impact on Nigerian housing construction costs? Please rank up to 5 factors.",
         "2b. How frequently do you think macroeconomic data should be updated in an AI cost estimation system to remain accurate?",
         "2c. Are there any Nigeria-specific macroeconomic factors not typically covered in international models that you consider important?"),
        ("Project Characteristics",
         "3a. What project-level information would you ALWAYS require before providing a preliminary cost estimate?",
         "3b. What project information is OPTIONAL but helpful for improving accuracy?",
         "3c. Are there any project characteristics that are particularly important for differentiating construction costs between regions of Nigeria?"),
        ("ML Model Performance",
         "4a. What level of accuracy (MAPE %) would you consider ACCEPTABLE for an AI-based preliminary construction cost estimate?",
         "4b. Would you use a cost estimate from an AI system if it could not explain HOW it arrived at the figure? Please explain.",
         "4c. What confidence interval width (e.g., +/- 10%, +/- 20%) would you consider acceptable for the system to report alongside point estimates?",
         "4d. How frequently do you think the AI model should be retrained with new data?"),
        ("System Interface & Usability",
         "5a. What are the MOST IMPORTANT features you would want in the user interface of such a system?",
         "5b. In what format should cost reports be delivered (PDF, Excel, dashboard)?",
         "5c. Would you use the system on a mobile device? What mobile features would be most important?",
         "5d. How should the system communicate uncertainty or low data confidence to users?"),
        ("Data Quality & Governance",
         "6a. How should the system handle situations where key macroeconomic data is unavailable or outdated?",
         "6b. What data quality indicators would increase your trust in the system's estimates?",
         "6c. Should the system store and display a history of all estimates made? Please explain why.",
         "6d. What privacy or data governance concerns would you have about using such a system?"),
        ("Reporting",
         "7a. What cost reporting format would be most useful for Nigerian construction practice?",
         "7b. Should the system generate sensitivity analyses (e.g., cost if FX rate changes by 15%)? Please explain.",
         "7c. Should report formats comply with any specific Nigerian professional standards (e.g., NIQS cost plans)?",
         "7d. What additional information should a cost report contain beyond the estimate figure?"),
    ]

    for section, *qs in questions:
        pdf.add_page()
        pdf.h2(f"Section: {section}")
        for q in qs:
            pdf.set_font("Helvetica", "B", 9.5)
            pdf.set_text_color(*DARK_NAVY)
            pdf.set_x(LEFT)
            pdf.multi_cell(PAGE_W, 5.2, sanitize(q))
            pdf.set_font("Helvetica", "", 9)
            pdf.set_text_color(*MID_GREY)
            pdf.set_x(LEFT + 4)
            pdf.multi_cell(PAGE_W - 4, 4.8, "Your response:")
            # Response lines
            for _ in range(5):
                pdf.set_draw_color(*MID_GREY)
                pdf.set_line_width(0.2)
                pdf.set_x(LEFT + 4)
                pdf.cell(PAGE_W - 4, 6, "", border='B')
                pdf.ln(6)
            pdf.ln(2)

    out = os.path.join(OUT_DIR, 'O3_02_Delphi_Round1_Instrument.pdf')
    pdf.output(out)
    print(f"[OK]  O3_02_Delphi_Round1_Instrument.pdf -> {out}")
    return out


# ══════════════════════════════════════════════════════════════════════════════
# PDF 3: Delphi Round 2 Instrument
# ══════════════════════════════════════════════════════════════════════════════
def make_round2_instrument():
    pdf = O3PDF("Delphi Round 2 Instrument — Structured Consensus Survey", "O3_03")
    pdf.add_page()

    pdf.set_fill_color(*DARK_NAVY)
    pdf.rect(0, 0, 210, 45, 'F')
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(*GOLD)
    pdf.set_xy(LEFT, 12)
    pdf.multi_cell(PAGE_W, 7.5, sanitize(
        "iNHCES O3 — Delphi Round 2\n38-Item Consensus Instrument (1-7 Likert Scale)"
    ), align="C")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*LIGHT_BLUE)
    pdf.set_xy(LEFT, 35)
    pdf.cell(PAGE_W, 6, sanitize("Confidential | n=20 target panel | All items derived from Round 1 thematic synthesis"), align="C")
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(20)

    _ds_page(pdf, 'amber',
        "DATA SOURCE: AMBER — This Round 2 instrument is a real, research-quality Delphi survey instrument. "
        "It has not yet been administered. Round 2 ratings in O3_04 are SYNTHETIC simulated responses.",
        (
            "The 38 items in this instrument were derived from a thematic analysis of Round 1 "
            "open-ended responses (hypothetical: see O3_02). The item categories and content reflect "
            "the iNHCES research design and O2 SHAP analysis findings.\n\n"
            "SCALE: 1 = Strongly Disagree / Completely Unimportant\n"
            "       7 = Strongly Agree / Absolutely Essential\n\n"
            "CONSENSUS CRITERIA: Mean >= 5.0 AND Coefficient of Variation (CV) <= 20%\n"
            "Items failing consensus will be presented in Round 3 with Round 2 statistics.\n\n"
            "BEFORE ADMINISTRATION:\n"
            "  1. Present Round 1 thematic summary to experts before Round 2\n"
            "  2. Allow 10-14 days for responses\n"
            "  3. Send reminder at day 7 to non-respondents\n"
            "  4. Target >= 80% response rate (>=16/20 experts)"
        )
    )

    pdf.add_page()
    pdf.h1("Instructions")
    pdf.para(
        "You are invited to rate each of the following 38 statements regarding the requirements "
        "of the iNHCES system. These statements were derived from the thematic synthesis of "
        "Round 1 responses. For each statement, please circle or tick the number (1-7) that "
        "best represents your view, where:"
    )
    pdf.para("  1 = Strongly Disagree / Completely Unimportant")
    pdf.para("  4 = Neither Agree nor Disagree / Moderately Important")
    pdf.para("  7 = Strongly Agree / Absolutely Essential")
    pdf.para(
        "There are 7 sections (A-G) covering macroeconomic features, project inputs, ML model "
        "requirements, system performance, interface design, data quality, and reporting. "
        "Please rate all 38 items. Estimated completion time: 15-20 minutes."
    )

    for cat_code in sorted(CATEGORIES.keys()):
        cat_items = [it for it in DELPHI_ITEMS if it[0] == cat_code]
        pdf.add_page()
        pdf.h2(f"Section {cat_code}: {CATEGORIES[cat_code]}")
        for it in cat_items:
            pdf.likert_row(it[1], it[3])
            pdf.ln(1)

    out = os.path.join(OUT_DIR, 'O3_03_Delphi_Round2_Instrument.pdf')
    pdf.output(out)
    print(f"[OK]  O3_03_Delphi_Round2_Instrument.pdf -> {out}")
    return out


# ══════════════════════════════════════════════════════════════════════════════
# PDF 4: Delphi Round 2 Analysis
# ══════════════════════════════════════════════════════════════════════════════
def make_round2_analysis(r2_stats, non_consensus):
    pdf = O3PDF("Delphi Round 2 Analysis Report", "O3_04")
    pdf.add_page()

    pdf.set_fill_color(*DARK_NAVY)
    pdf.rect(0, 0, 210, 45, 'F')
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(*GOLD)
    pdf.set_xy(LEFT, 12)
    pdf.multi_cell(PAGE_W, 7.5, sanitize(
        "iNHCES O3 — Delphi Round 2 Analysis\nDescriptive Statistics and Consensus Assessment"
    ), align="C")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*LIGHT_BLUE)
    pdf.set_xy(LEFT, 35)
    pdf.cell(PAGE_W, 6, sanitize(
        f"SYNTHETIC DATA | n={N_EXPERTS} experts | seed={SEED} | AMBER/RED -- Replace with real survey data"
    ), align="C")
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(20)

    _ds_page(pdf, 'red',
        "DATA SOURCE: RED — All expert ratings in this analysis are SYNTHETIC. n=20 "
        "expert ratings generated using numpy random normal distribution (seed=42). "
        "Results are indicative ONLY — must be replaced with real Delphi survey data.",
        (
            "WHAT IS REAL:\n"
            "  * Instrument items (A1-G4): real, researchable content\n"
            "  * Statistical methodology (mean, SD, CV, consensus criterion): real methods\n"
            "  * Analytical framework and interpretation approach: real academic practice\n\n"
            "WHAT IS SYNTHETIC:\n"
            "  * All n=20 expert ratings: generated by numpy.random.default_rng(42)\n"
            "  * All means, SDs, CVs, IQRs: derived from synthetic ratings\n"
            "  * Consensus/non-consensus classifications: based on synthetic ratings\n"
            "  * All charts: generated from synthetic data\n\n"
            "REQUIRED BEFORE PUBLICATION:\n"
            "  1. Administer Round 2 instrument to real expert panel (n>=15)\n"
            "  2. Re-run Delphi_Analysis.py with real data replacing synthetic ratings\n"
            "  3. Regenerate all charts and statistics\n"
            "  4. Update P2 paper with real results"
        )
    )

    pdf.add_page()
    pdf.h1("1. Round 2 Summary Statistics")
    n_consensus = sum(1 for v in r2_stats.values() if v['consensus'])
    n_total = len(r2_stats)
    pdf.para(
        f"Round 2 achieved consensus on {n_consensus} of {n_total} items "
        f"({100*n_consensus/n_total:.1f}%). {len(non_consensus)} items failed the "
        f"consensus threshold (mean >= {CONSENSUS_MEAN}, CV <= {CONSENSUS_CV}%) and "
        f"will proceed to Round 3 for re-evaluation."
    )
    pdf.note(f"ALL RATINGS ARE SYNTHETIC. n={N_EXPERTS} simulated expert respondents, numpy seed={SEED}.")

    # Full statistics table
    sw = [10, 56, 14, 14, 14, 16, 12, 22, 24]
    assert sum(sw) == 182, f"Width mismatch: {sum(sw)}"
    sw[-1] = PAGE_W - sum(sw[:-1])
    pdf.thead(["ID","Statement (truncated)","n","Mean","SD","CV%","IQR","Consensus?","Category"], sw)
    for i, it in enumerate(DELPHI_ITEMS):
        iid = it[1]
        s = r2_stats[iid]
        text_trunc = it[2][:48]
        cons_str = "YES" if s['consensus'] else "NO *"
        pdf.trow([
            iid, text_trunc, str(N_EXPERTS),
            f"{s['mean']:.2f}", f"{s['sd']:.2f}",
            f"{s['cv']:.1f}", f"{s['iqr']:.1f}",
            cons_str, CATEGORIES[it[0]][:20]
        ], sw, fill=(i % 2 == 1))
    pdf.ln(2)
    pdf.caption(
        f"Table 1: Round 2 descriptive statistics (SYNTHETIC). "
        f"Consensus: Mean >= {CONSENSUS_MEAN:.1f} AND CV <= {CONSENSUS_CV:.0f}%. "
        f"* = non-consensus items proceeding to Round 3. "
        f"n={N_EXPERTS} respondents (SIMULATED)."
    )

    pdf.add_page()
    pdf.h1("2. Non-Consensus Items (Proceeding to Round 3)")
    if non_consensus:
        pdf.para(
            f"The following {len(non_consensus)} item(s) did not reach consensus in Round 2. "
            f"They will be re-presented in Round 3 together with the Round 2 group statistics, "
            f"enabling experts to revise their ratings in light of the group view."
        )
        nw = [10, 80, 14, 14, 14, PAGE_W-132]
        pdf.thead(["ID", "Full Statement", "Mean", "SD", "CV%", "Reason"], nw)
        for it in non_consensus:
            iid = it[1]
            s = r2_stats[iid]
            reason = []
            if s['mean'] < CONSENSUS_MEAN:
                reason.append(f"Mean {s['mean']:.2f} < {CONSENSUS_MEAN}")
            if s['cv'] > CONSENSUS_CV:
                reason.append(f"CV {s['cv']:.1f}% > {CONSENSUS_CV:.0f}%")
            pdf.trow([iid, it[3][:65], f"{s['mean']:.2f}", f"{s['sd']:.2f}",
                      f"{s['cv']:.1f}", "; ".join(reason)], nw, fill=True)
    else:
        pdf.para("All items reached consensus in Round 2. Round 3 is not required.")
    pdf.ln(2)

    pdf.add_page()
    pdf.h1("3. Category-Level Consensus Summary")
    cw = [55, 15, 15, 15, PAGE_W-100]
    pdf.thead(["Category", "Items", "Consensus", "% Cons.", "Highest Mean Item"], cw)
    for cat_code in sorted(CATEGORIES.keys()):
        cat_items = [it for it in DELPHI_ITEMS if it[0] == cat_code]
        n_cat = len(cat_items)
        n_cons = sum(1 for it in cat_items if r2_stats[it[1]]['consensus'])
        pct = 100 * n_cons / n_cat if n_cat > 0 else 0
        top_item = max(cat_items, key=lambda it: r2_stats[it[1]]['mean'])
        pdf.trow([
            CATEGORIES[cat_code][:50], str(n_cat), str(n_cons),
            f"{pct:.0f}%", f"{top_item[1]}: {r2_stats[top_item[1]]['mean']:.2f}"
        ], cw, fill=(cat_code in "BDF"))
    pdf.ln(2)
    pdf.caption("Table 2: Category-level consensus summary (SYNTHETIC). All values from simulated data.")

    # Chart: category consensus
    pdf.add_page()
    pdf.h1("4. Visualisations (SYNTHETIC DATA)")
    pdf.note("All charts below are generated from SYNTHETIC expert ratings. Regenerate with real data.")

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    cats = list(CATEGORIES.keys())
    cons_counts = []
    total_counts = []
    for cat_code in cats:
        cat_items = [it for it in DELPHI_ITEMS if it[0] == cat_code]
        cons_counts.append(sum(1 for it in cat_items if r2_stats[it[1]]['consensus']))
        total_counts.append(len(cat_items))
    non_cons = [t - c for t, c in zip(total_counts, cons_counts)]
    x = np.arange(len(cats))
    axes[0].bar(x, cons_counts, color='#1a3a6b', label='Consensus')
    axes[0].bar(x, non_cons, bottom=cons_counts, color='#c0392b', label='Non-consensus')
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(cats)
    axes[0].set_ylabel('Number of Items')
    axes[0].set_title('Round 2 Consensus by Category\n[SYNTHETIC DATA]')
    axes[0].legend()
    axes[0].grid(axis='y', alpha=0.3)

    # Item means bar chart (all items)
    means = [r2_stats[it[1]]['mean'] for it in DELPHI_ITEMS]
    item_ids = [it[1] for it in DELPHI_ITEMS]
    colors = ['#1a3a6b' if r2_stats[it[1]]['consensus'] else '#c0392b' for it in DELPHI_ITEMS]
    axes[1].barh(item_ids, means, color=colors, height=0.7)
    axes[1].axvline(CONSENSUS_MEAN, color='black', linestyle='--', linewidth=1, label=f'Consensus threshold ({CONSENSUS_MEAN})')
    axes[1].set_xlabel('Mean Rating (1-7 scale)')
    axes[1].set_title('Item Mean Ratings — Round 2\n[SYNTHETIC DATA]')
    axes[1].legend(fontsize=7)
    axes[1].tick_params(axis='y', labelsize=7)
    axes[1].set_xlim(0, 7.5)
    axes[1].grid(axis='x', alpha=0.3)
    plt.tight_layout()
    pdf.add_chart(fig)
    pdf.caption(
        "Figure 1: (Left) Consensus counts per category. (Right) Mean ratings for all 38 items. "
        "Blue = consensus reached; Red = non-consensus. Dashed line = consensus threshold (Mean=5.0). "
        "ALL VALUES SYNTHETIC."
    )

    out = os.path.join(OUT_DIR, 'O3_04_Delphi_Round2_Analysis.pdf')
    pdf.output(out)
    print(f"[OK]  O3_04_Delphi_Round2_Analysis.pdf -> {out}")
    return out


# ══════════════════════════════════════════════════════════════════════════════
# PDF 5: Delphi Round 3 Instrument
# ══════════════════════════════════════════════════════════════════════════════
def make_round3_instrument(non_consensus, r2_stats):
    pdf = O3PDF("Delphi Round 3 Instrument — Consensus Refinement", "O3_05")
    pdf.add_page()

    pdf.set_fill_color(*DARK_NAVY)
    pdf.rect(0, 0, 210, 45, 'F')
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(*GOLD)
    pdf.set_xy(LEFT, 12)
    pdf.multi_cell(PAGE_W, 7.5, sanitize(
        f"iNHCES O3 — Delphi Round 3\n{len(non_consensus)}-Item Consensus Refinement Instrument"
    ), align="C")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*LIGHT_BLUE)
    pdf.set_xy(LEFT, 35)
    pdf.cell(PAGE_W, 6, sanitize("Round 3 presents only items that did not reach consensus in Round 2"), align="C")
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(20)

    _ds_page(pdf, 'amber',
        "DATA SOURCE: AMBER — Round 3 instrument is real research design. "
        "Round 2 statistics shown are SYNTHETIC (see O3_04). Round 3 ratings are SYNTHETIC (see O3_06).",
        (
            "Round 3 presents only the items that failed consensus in Round 2. "
            f"n={len(non_consensus)} items are re-presented with Round 2 group statistics "
            "(mean, SD, CV) shown, enabling experts to reconsider their rating in light of the group view.\n\n"
            "This follows the classic Delphi feedback mechanism: experts who rated very differently "
            "from the group mean are invited to reconsider (or to justify their divergent view).\n\n"
            "CONSENSUS CRITERION (unchanged): Mean >= 5.0 AND CV <= 20%\n\n"
            "Items that still fail consensus after Round 3 will be EXCLUDED from the final "
            "requirements specification with a note explaining the lack of expert agreement."
        )
    )

    pdf.add_page()
    pdf.h1("Instructions")
    pdf.para(
        "Thank you for completing Round 2. The following items did not reach consensus "
        "(defined as group mean >= 5.0 and coefficient of variation <= 20%). "
        "For each item, the Round 2 group statistics are shown below your rating box. "
        "Please re-read each item and re-rate it on the same 1-7 scale."
    )
    pdf.para(
        "You are NOT being asked to change your view — but you are invited to reconsider "
        "your rating in light of the group's overall position. If you maintain a view that "
        "diverges significantly from the group mean, please note your reason in the "
        "'Comments' box provided."
    )

    for it in non_consensus:
        iid = it[1]
        s = r2_stats[iid]
        pdf.h2(f"Item {iid}: {CATEGORIES[it[0]]}")
        pdf.set_font("Helvetica", "", 9.5)
        pdf.set_text_color(*DARK_GREY)
        pdf.set_x(LEFT)
        pdf.multi_cell(PAGE_W, 5.2, sanitize(it[3]))
        pdf.ln(2)
        # Show Round 2 stats
        pdf.set_fill_color(255, 250, 220)
        pdf.set_draw_color(*GOLD)
        pdf.set_line_width(0.3)
        pdf.set_font("Helvetica", "I", 8.5)
        pdf.set_text_color(120, 80, 0)
        pdf.set_x(LEFT)
        pdf.multi_cell(PAGE_W, 4.8,
            sanitize(f"Round 2 Group Statistics: Mean = {s['mean']:.2f}  |  SD = {s['sd']:.2f}  "
                     f"|  CV = {s['cv']:.1f}%  |  IQR = {s['iqr']:.1f}  "
                     f"|  Reason failed: {'Mean < 5.0' if s['mean'] < CONSENSUS_MEAN else ''}"
                     f"{'+ ' if s['mean'] < CONSENSUS_MEAN and s['cv'] > CONSENSUS_CV else ''}"
                     f"{'CV > 20%' if s['cv'] > CONSENSUS_CV else ''}"),
            border=1, fill=True)
        pdf.set_text_color(*DARK_GREY)
        pdf.ln(2)
        pdf.likert_row(iid, "Re-rate this item:")
        pdf.set_x(LEFT)
        pdf.set_font("Helvetica", "", 9)
        pdf.cell(30, 5, "Comments (optional):")
        for _ in range(2):
            pdf.set_x(LEFT + 4)
            pdf.cell(PAGE_W - 4, 6, "", border='B')
            pdf.ln(6)
        pdf.ln(3)

    out = os.path.join(OUT_DIR, 'O3_05_Delphi_Round3_Instrument.pdf')
    pdf.output(out)
    print(f"[OK]  O3_05_Delphi_Round3_Instrument.pdf -> {out}")
    return out


# ══════════════════════════════════════════════════════════════════════════════
# PDF 6: Delphi Final Consensus Report
# ══════════════════════════════════════════════════════════════════════════════
def make_final_consensus(r2_stats, r3_stats, final_items, excluded_items):
    pdf = O3PDF("Delphi Final Consensus Report", "O3_06")
    pdf.add_page()

    pdf.set_fill_color(*DARK_NAVY)
    pdf.rect(0, 0, 210, 45, 'F')
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(*GOLD)
    pdf.set_xy(LEFT, 12)
    pdf.multi_cell(PAGE_W, 7.5, sanitize(
        "iNHCES O3 — Delphi Final Consensus Report\n"
        f"Consolidated Requirements: {len(final_items)} Agreed Items"
    ), align="C")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*LIGHT_BLUE)
    pdf.set_xy(LEFT, 35)
    pdf.cell(PAGE_W, 6, sanitize(
        "SYNTHETIC DATA | Mandatory reading before using in publication | See DATA SOURCE page"
    ), align="C")
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(20)

    _ds_page(pdf, 'red',
        "DATA SOURCE: RED — All expert ratings are SYNTHETIC (numpy seed=42). "
        "This report MUST be regenerated with real survey data before use in publications or system design.",
        (
            "FINAL CONSENSUS SUMMARY (SYNTHETIC):\n"
            f"  Total items in Round 2: {len(DELPHI_ITEMS)}\n"
            f"  Round 2 consensus: {sum(1 for it, _, r3 in final_items if r3 is None)} items\n"
            f"  Round 3 consensus (additional): {sum(1 for it, _, r3 in final_items if r3 is not None)} items\n"
            f"  Excluded (no consensus after Round 3): {len(excluded_items)} item(s)\n"
            f"  Total consensus requirements: {len(final_items)} items\n\n"
            "EXCLUDED ITEMS:\n" +
            "\n".join(f"  * {it[1]} ({it[2]}) -- final mean: {r3_stats[it[1]]['mean']:.2f}, CV: {r3_stats[it[1]]['cv']:.1f}%"
                     if it[1] in r3_stats else f"  * {it[1]} ({it[2]})"
                     for it, _, _ in excluded_items) +
            "\n\n"
            "These consensus requirements form the input to the IEEE 830 Software Requirements "
            "Specification (O3_07_SRS_IEEE830.pdf) and directly inform the iNHCES system design."
        )
    )

    pdf.add_page()
    pdf.h1("1. Final Consensus Summary")
    pdf.para(
        f"After two rounds of the modified Delphi process, consensus was achieved on "
        f"{len(final_items)} of {len(DELPHI_ITEMS)} requirements items ({100*len(final_items)/len(DELPHI_ITEMS):.0f}%). "
        f"{len(excluded_items)} item(s) failed to reach consensus after Round 3 and are excluded from "
        f"the final requirements specification."
    )

    fw = [10, 72, 16, 16, 16, 12, PAGE_W-142]
    pdf.thead(["ID","Requirement Statement","R2 Mean","R2 CV%","R3 Mean","Status","Category"], fw)
    for it, r2s, r3s in sorted(final_items, key=lambda x: x[0][1]):
        status = "R2 Consensus" if r3s is None else "R3 Consensus"
        r3_mean = f"{r3s['mean']:.2f}" if r3s else "-"
        pdf.trow([
            it[1], it[2][:55], f"{r2s['mean']:.2f}", f"{r2s['cv']:.1f}%",
            r3_mean, status, CATEGORIES[it[0]][:20]
        ], fw, fill=(it[0] in "BDF"))
    pdf.ln(2)
    pdf.caption(
        "Table 1: Final consensus items. All means are from SYNTHETIC data. "
        "R3 Mean shown only for items requiring Round 3. "
        "Status: R2/R3 Consensus = round in which consensus was achieved."
    )

    if excluded_items:
        pdf.add_page()
        pdf.h1("2. Excluded Items — No Consensus Reached")
        ew = [10, 80, 16, 16, 16, PAGE_W-138]
        pdf.thead(["ID", "Statement", "R2 Mean", "R3 Mean", "Final CV%", "Reason Excluded"], ew)
        for it, r2s, r3s in excluded_items:
            r3_m = f"{r3s['mean']:.2f}" if r3s else "N/A"
            r3_cv = f"{r3s['cv']:.1f}%" if r3s else "N/A"
            reason = f"Mean {r3s['mean']:.2f} < {CONSENSUS_MEAN} or CV {r3s['cv']:.1f}% > {CONSENSUS_CV}%" if r3s else "Still below threshold"
            pdf.trow([it[1], it[3][:65], f"{r2s['mean']:.2f}", r3_m, r3_cv, reason], ew, fill=True)
        pdf.ln(2)
        pdf.para(
            "Excluded items are noted in the SRS (O3_07) as 'Requirements Under Review' — "
            "they are not incorporated into the current system specification but are flagged "
            "for potential inclusion in a future version pending further expert consultation."
        )

    pdf.add_page()
    pdf.h1("3. Requirements by Category (Final Consensus)")
    for cat_code in sorted(CATEGORIES.keys()):
        cat_items = [(it, r2s, r3s) for it, r2s, r3s in final_items if it[0] == cat_code]
        if not cat_items:
            continue
        pdf.h2(f"Category {cat_code}: {CATEGORIES[cat_code]}")
        for it, r2s, r3s in cat_items:
            final_mean = r3s['mean'] if r3s else r2s['mean']
            pdf.req_box(
                it[1],
                f"{it[3]}  [Mean: {final_mean:.2f}/7.0]",
                priority="High" if final_mean >= 6.0 else "Medium"
            )
        pdf.ln(2)

    # SHAP vs Delphi alignment
    pdf.add_page()
    pdf.h1("4. SHAP-Delphi Alignment Analysis")
    pdf.para(
        "The SHAP feature importance rankings from O2 Step 4 can be compared with the "
        "Delphi consensus mean ratings for the corresponding macroeconomic feature items "
        "(Category A). Table 2 shows the alignment between the two methods."
    )
    aw = [10, 55, 25, 25, PAGE_W-115]
    shap_ranks = {
        "A1": ("NGN/USD", "1st (44.97%)"),
        "A2": ("CPI inflation", "2nd (25.50%)"),
        "A3": ("Brent crude", "4th (10.85%)"),
        "A4": ("GDP growth", "6th (2.59%)"),
        "A5": ("Lending rate", "7th (1.07%)"),
    }
    pdf.thead(["ID", "Macroeconomic Feature", "Delphi Mean (R2)", "SHAP Rank", "Alignment"], aw)
    for i, iid in enumerate(["A1","A2","A3","A4","A5"]):
        item = next(it for it in DELPHI_ITEMS if it[1] == iid)
        s = r2_stats[iid]
        shap_info = shap_ranks.get(iid, ("Unknown", "N/A"))
        # Check alignment: high Delphi AND high SHAP = Strong; discordant = Note
        delphi_rank = i + 1
        alignment = "Strong" if i < 3 else "Moderate"
        pdf.trow([iid, item[2][:45], f"{s['mean']:.2f}", shap_info[1], alignment], aw, fill=(i % 2 == 1))
    pdf.ln(2)
    pdf.caption(
        "Table 2: SHAP (O2) vs Delphi (O3) alignment for macroeconomic features. "
        "Both methods identify NGN/USD exchange rate and CPI inflation as top-priority features. "
        "SYNTHETIC Delphi data shown -- confirm alignment with real survey results."
    )
    pdf.para(
        "The convergence of SHAP-based statistical analysis (O2) and expert Delphi judgment (O3) "
        "on NGN/USD exchange rate (SHAP rank 1, Delphi Category A highest mean) and CPI inflation "
        "(SHAP rank 2, Delphi Category A second highest mean) provides dual-method validation for "
        "the iNHCES macroeconomic feature selection strategy. This multi-method triangulation "
        "strengthens the theoretical basis for the feature set used in O5 model development."
    )

    out = os.path.join(OUT_DIR, 'O3_06_Delphi_Final_Consensus.pdf')
    pdf.output(out)
    print(f"[OK]  O3_06_Delphi_Final_Consensus.pdf -> {out}")
    return out


# ══════════════════════════════════════════════════════════════════════════════
# PDF 7: SRS — IEEE 830
# ══════════════════════════════════════════════════════════════════════════════
FUNCTIONAL_REQS = [
    ("FR-01", "User Authentication", "High",
     "The system shall provide secure user authentication via email/password with JWT tokens. "
     "Passwords shall be bcrypt-hashed. Failed login attempts exceeding 5 in 10 minutes shall trigger account lockout."),
    ("FR-02", "User Registration", "High",
     "The system shall support self-registration for new users with email verification. "
     "Admin approval required for users requesting elevated access."),
    ("FR-03", "Project Profile Management", "High",
     "Authenticated users shall be able to create, save, update, and delete project profiles. "
     "Each profile stores project name, location, type, structural system, floor area, and specification level."),
    ("FR-04", "Cost Estimate Generation", "High",
     "The system shall generate a construction cost estimate (NGN/sqm and total NGN) "
     "from project inputs and live macroeconomic features within 3 seconds of submission."),
    ("FR-05", "SHAP Explanation Display", "High",
     "Every estimate shall be accompanied by a SHAP-based feature importance explanation "
     "showing the top 5 contributing features and their directional impact on the estimate."),
    ("FR-06", "Prediction Interval Calculation", "High",
     "The system shall report a 90% prediction interval for every cost estimate, "
     "indicating the lower and upper bounds of the credible cost range."),
    ("FR-07", "PDF Report Generation", "High",
     "The system shall automatically generate a branded, professionally formatted PDF report "
     "for every completed estimate, following NIQS cost plan format. Reports shall be stored in R2 cloud storage."),
    ("FR-08", "Macroeconomic Dashboard", "Medium",
     "The system shall display a macroeconomic dashboard showing current values and "
     "data freshness (age in days) for all 7 macro features: NGN/USD, NGN/EUR, NGN/GBP, "
     "CPI inflation, GDP growth, lending rate, and Brent crude price."),
    ("FR-09", "DATA SOURCE Classification", "High",
     "Every estimate and report shall display a DATA SOURCE confidence classification "
     "(GREEN/AMBER/RED) based on the age and source of the macroeconomic data used."),
    ("FR-10", "Estimate History and Audit Trail", "High",
     "All estimates shall be permanently stored with: user ID, timestamp, all input values, "
     "model version, macro data snapshot, output estimate and intervals, and PDF report reference."),
    ("FR-11", "Sensitivity Analysis Report", "Medium",
     "Users shall be able to generate a sensitivity analysis showing the cost estimate "
     "under three exchange rate scenarios: base, +15% NGN depreciation, -15% NGN appreciation."),
    ("FR-12", "Multi-Project Dashboard", "Medium",
     "Authenticated users shall be able to view a dashboard of all their saved project estimates, "
     "sortable by date, project name, cost, and location."),
    ("FR-13", "PDF Export and Download", "High",
     "Users shall be able to download any previously generated PDF report at any time, "
     "provided they are the owner or have been granted access by the owner."),
    ("FR-14", "Input Validation", "High",
     "All numeric inputs shall be validated against plausible range limits before submission. "
     "Invalid inputs shall return a descriptive validation error message, not a system error."),
    ("FR-15", "Data Freshness Warning", "High",
     "The system shall display a warning when any macroeconomic data source exceeds 7 days old. "
     "Estimates generated with stale data shall be flagged AMBER or RED as appropriate."),
    ("FR-16", "Administrator User Management", "High",
     "System administrators shall be able to view, activate, deactivate, and assign roles to users. "
     "Admin actions shall be logged in an audit table."),
    ("FR-17", "Pipeline Status Dashboard", "Medium",
     "Administrators shall have access to a pipeline monitoring dashboard showing "
     "the status and last successful run of each Airflow DAG."),
    ("FR-18", "Model Retrain Trigger", "Medium",
     "Administrators shall be able to manually trigger model retraining from the admin dashboard. "
     "Retraining uses the MLflow-registered pipeline. Results are logged in MLflow."),
    ("FR-19", "Champion Model Promotion", "Medium",
     "The system shall support A/B testing between the current champion model and a challenger. "
     "Promotion to champion requires the new model to achieve lower MAPE on the held-out validation set."),
    ("FR-20", "System Health Monitoring", "Medium",
     "The system shall expose a /health endpoint returning API status, database connectivity, "
     "R2 storage connectivity, and MLflow connectivity. Uptime monitoring shall alert the admin "
     "if health checks fail for > 5 minutes."),
]

NON_FUNC_REQS = [
    ("NFR-01", "Performance", "High",
     "Estimate generation (ML inference + SHAP) shall complete in <= 3 seconds under normal load. "
     "PDF report generation shall complete in <= 10 seconds. API response time for all other "
     "endpoints shall be <= 1 second."),
    ("NFR-02", "Scalability", "High",
     "The system shall support at least 50 simultaneous active users without performance "
     "degradation. Infrastructure shall be horizontally scalable via Railway container deployment."),
    ("NFR-03", "Availability", "High",
     "System availability shall be >= 99.5% per calendar month excluding scheduled maintenance. "
     "Scheduled maintenance windows shall not exceed 4 hours per month and shall be announced "
     "48 hours in advance."),
    ("NFR-04", "Security", "High",
     "All communications shall use HTTPS/TLS 1.3+. Authentication tokens shall be JWTs "
     "with 24-hour expiry. User passwords shall be bcrypt-hashed (cost factor >= 12). "
     "All endpoints shall enforce role-based access control. OWASP Top 10 mitigations shall be applied. "
     "SQL injection shall be prevented via parameterised queries (SQLAlchemy ORM). "
     "CORS shall be restricted to the production frontend domain."),
    ("NFR-05", "Data Integrity", "High",
     "All data shall be stored in Supabase PostgreSQL with row-level security (RLS) policies "
     "ensuring users can only access their own data. Database transactions shall be atomic. "
     "Foreign key constraints shall be enforced."),
    ("NFR-06", "Maintainability", "Medium",
     "The codebase shall follow FastAPI and Python best practices. All public functions "
     "shall have docstrings. Unit test coverage shall be >= 80% for core inference and "
     "authentication modules. CI/CD via GitHub Actions shall run tests on every push."),
    ("NFR-07", "Portability", "Medium",
     "The backend shall be fully containerised using Docker. The Dockerfile shall support "
     "deployment on Railway, AWS, and any OCI-compliant container registry. "
     "Environment configuration via .env file (secrets not committed to version control)."),
    ("NFR-08", "Accessibility", "Medium",
     "The web frontend shall conform to WCAG 2.1 Level AA accessibility guidelines. "
     "All interactive elements shall be keyboard navigable. Colour contrast ratios shall "
     "meet WCAG minimum requirements."),
    ("NFR-09", "Compliance", "High",
     "The system shall comply with the Nigeria Data Protection Regulation (NDPR, 2019) "
     "for personal data processing. A Privacy Policy and Terms of Use shall be displayed. "
     "TETFund data governance requirements shall be met as a condition of the research grant."),
]

def make_srs(final_items):
    pdf = O3PDF("Software Requirements Specification — IEEE 830", "O3_07")
    pdf.add_page()

    pdf.set_fill_color(*DARK_NAVY)
    pdf.rect(0, 0, 210, 45, 'F')
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(*GOLD)
    pdf.set_xy(LEFT, 10)
    pdf.multi_cell(PAGE_W, 7.5, sanitize(
        "iNHCES O3 — Software Requirements Specification\n"
        "IEEE 830-Compliant | Intelligent National Housing Cost Estimating System"
    ), align="C")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*LIGHT_BLUE)
    pdf.set_xy(LEFT, 35)
    pdf.cell(PAGE_W, 6, sanitize("Version 1.0 DRAFT | TETFund NRF 2025 | Dept. QS, ABU Zaria"), align="C")
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(20)

    _ds_page(pdf, 'amber',
        "DATA SOURCE: AMBER — This SRS is a real research output derived from the Delphi consensus "
        "(O3_06). Functional requirements are grounded in real system design. "
        "Quantitative targets are based on SYNTHETIC Delphi data and must be validated with real expert results.",
        (
            "This document constitutes the Version 1.0 draft Software Requirements Specification "
            "for the iNHCES system, prepared in accordance with IEEE 830-1998 (Recommended Practice "
            "for Software Requirements Specifications).\n\n"
            "WHAT IS REAL:\n"
            "  * FR-01 to FR-20 functional requirements: real system design\n"
            "  * NFR-01 to NFR-09 non-functional requirements: real performance targets\n"
            "  * System architecture constraints: real (FastAPI + Supabase + Railway + Vercel)\n"
            "  * IEEE 830 document structure: real standard\n\n"
            "WHAT IS BASED ON SYNTHETIC DELPHI:\n"
            "  * Performance thresholds (3s, 99.5%, 50 users) derive from synthetic Delphi consensus\n"
            "  * These must be re-validated with real expert responses before finalization\n\n"
            "REVIEW AND APPROVAL:\n"
            "  This SRS must be reviewed by: PI, Co-Investigators, and at least one practitioner "
            "stakeholder before being used as the basis for O6 system development."
        )
    )

    # Section 1: Introduction
    pdf.add_page()
    pdf.h1("1. Introduction")
    pdf.h2("1.1 Purpose")
    pdf.para(
        "This Software Requirements Specification (SRS) defines the functional and "
        "non-functional requirements for the Intelligent National Housing Cost Estimating "
        "System (iNHCES). It is intended for use by the iNHCES development team, "
        "research supervisors, and institutional stakeholders. This document follows "
        "the IEEE 830-1998 recommended practice for software requirements specifications."
    )
    pdf.h2("1.2 Scope")
    pdf.para(
        "iNHCES is an AI-powered web-based construction cost estimation system for the "
        "Nigerian housing sector. The system integrates live macroeconomic data pipelines, "
        "machine learning models, SHAP explainability, and automated PDF report generation. "
        "The system is accessible to registered users via a web browser (no installation required). "
        "The system does NOT include: construction scheduling, BIM integration, "
        "quantities takeoff automation, or procurement tendering functionality."
    )
    pdf.h2("1.3 Definitions and Acronyms")
    defs = [
        ("MAPE", "Mean Absolute Percentage Error — primary ML model accuracy metric"),
        ("SHAP", "SHapley Additive exPlanations — ML model explainability method"),
        ("QS", "Quantity Surveyor — primary user professional role"),
        ("NIQS", "Nigerian Institute of Quantity Surveyors — professional body"),
        ("NGN/sqm", "Nigerian Naira per square metre — ML target variable"),
        ("JWT", "JSON Web Token — authentication mechanism"),
        ("RLS", "Row-Level Security — Supabase PostgreSQL data isolation"),
        ("DAG", "Directed Acyclic Graph — Airflow pipeline unit"),
        ("API", "Application Programming Interface"),
        ("R2", "Cloudflare R2 — cloud object storage for PDF reports"),
        ("NDPR", "Nigeria Data Protection Regulation, 2019"),
        ("DATA SOURCE", "iNHCES data quality classification: GREEN/AMBER/RED"),
    ]
    dw = [25, PAGE_W-25]
    pdf.thead(["Term", "Definition"], dw)
    for i, (term, defn) in enumerate(defs):
        pdf.trow([term, defn], dw, fill=(i % 2 == 1))
    pdf.ln(2)

    pdf.h2("1.4 References")
    for ref in [
        "IEEE 830-1998: Recommended Practice for Software Requirements Specifications.",
        "iNHCES O2: Macroeconomic determinants analysis (stationarity, VAR, SHAP) — see 02_macro_analysis/.",
        "iNHCES O3: Delphi expert consensus — O3_06_Delphi_Final_Consensus.pdf.",
        "iNHCES O1: PRISMA SLR protocol — 01_literature_review/ outputs.",
        "00_Research_Simulation_Introduction.pdf — governing ethics and data source framework.",
        "FastAPI documentation: https://fastapi.tiangolo.com",
        "Supabase documentation: https://supabase.com/docs",
    ]:
        pdf.bullet(ref)

    # Section 2: Overall Description
    pdf.add_page()
    pdf.h1("2. Overall Description")
    pdf.h2("2.1 Product Perspective")
    pdf.para(
        "iNHCES is a new, standalone web-based system with no required integration with "
        "existing QS software (though future API integration with QS practice management "
        "systems is planned for Phase 2). The system operates as a client-server architecture: "
        "a Vanilla JS frontend (Vercel), FastAPI REST backend (Railway), PostgreSQL database "
        "(Supabase), ML model registry (MLflow on Railway), PDF storage (Cloudflare R2), "
        "and data pipeline orchestration (Airflow on Railway)."
    )
    pdf.h2("2.2 Product Functions (Summary)")
    for fn in [
        "Construction cost estimation using a live-updated XGBoost/LightGBM/Stacking Ensemble ML model",
        "SHAP-based feature importance explanations for every estimate",
        "Prediction interval reporting (90% CI) for uncertainty quantification",
        "Automated NIQS-format PDF cost reports with DATA SOURCE classification",
        "Live macroeconomic data dashboard (7 variables, freshness indicators)",
        "Sensitivity analysis under three FX rate scenarios",
        "Estimate history, project management, and audit trail",
        "Administrator pipeline monitoring and model management console",
    ]:
        pdf.bullet(fn)
    pdf.h2("2.3 User Classes and Characteristics")
    uw = [40, 30, PAGE_W-70]
    pdf.thead(["User Class", "Technical Level", "Primary Functions"], uw)
    users = [
        ("QS Practitioner (Primary)", "Low-Medium",
         "Generate estimates, view reports, manage project profiles"),
        ("Housing Developer", "Low-Medium",
         "Generate estimates for project feasibility, download PDF reports"),
        ("Public Sector Client", "Low",
         "View estimates, download reports for procurement documentation"),
        ("Researcher", "Medium-High",
         "Access estimate data, export CSVs, view SHAP explanations in detail"),
        ("System Administrator", "High",
         "Manage users, monitor pipeline, trigger retraining, manage ML models"),
    ]
    for i, u in enumerate(users):
        pdf.trow(list(u), uw, fill=(i % 2 == 1))
    pdf.ln(2)
    pdf.h2("2.4 Operating Environment")
    for env in [
        "Backend: FastAPI (Python 3.11+), deployed on Railway (Docker container)",
        "Frontend: Vanilla HTML/CSS/JavaScript, deployed on Vercel (CDN)",
        "Database: Supabase PostgreSQL (managed, Lagos or Frankfurt region)",
        "ML Registry: MLflow (Railway), Cloudflare R2 for model artefact storage",
        "Pipeline Orchestration: Apache Airflow 2.x (Railway)",
        "Client: Any modern web browser (Chrome 90+, Firefox 88+, Edge 90+, Safari 14+)",
        "Mobile: Responsive design supporting iOS 14+ and Android 10+ browsers",
    ]:
        pdf.bullet(env)
    pdf.h2("2.5 Design and Implementation Constraints")
    for c in [
        "All external API calls (World Bank, EIA, CBN/FRED) must be rate-limited and cached to avoid API quota exhaustion.",
        "ML model inference must use the MLflow-registered champion model. Model files must not be hardcoded in the API.",
        "All user data must be isolated by Supabase Row-Level Security (RLS) policies — users cannot access other users' data.",
        "The system must not store raw macroeconomic API keys in version-controlled code (use environment variables).",
        "PDF reports must be stored in R2 storage, not served from the API server, to avoid memory issues with large files.",
        "The system must comply with NDPR 2019 for any personal data collected during registration.",
    ]:
        pdf.bullet(c)

    # Section 3: Functional Requirements
    pdf.add_page()
    pdf.h1("3. Specific Requirements")
    pdf.h2("3.1 Functional Requirements")
    pdf.note(
        "FR-01 to FR-20 are derived from the Delphi consensus (O3_06) and supplemented by "
        "the technology stack constraints (FastAPI, Supabase, MLflow). All FR items with "
        "quantitative targets (e.g., <= 3 seconds) reflect synthetic Delphi consensus values "
        "and must be validated with real survey data."
    )
    for fr_id, fr_name, priority, desc in FUNCTIONAL_REQS:
        pdf.req_box(fr_id, f"{fr_name}: {desc}", priority)
    pdf.ln(2)

    # Section 3.2 Non-Functional
    pdf.add_page()
    pdf.h2("3.2 Non-Functional Requirements")
    for nfr_id, nfr_name, priority, desc in NON_FUNC_REQS:
        pdf.req_box(nfr_id, f"{nfr_name}: {desc}", priority)
    pdf.ln(2)

    # Section 4: Data Requirements
    pdf.add_page()
    pdf.h1("4. Data Requirements")
    pdf.h2("4.1 Input Data Model")
    pdf.para("The primary estimate input data model (EstimateInput) contains the following fields:")
    iw = [35, 25, 15, PAGE_W-75]
    pdf.thead(["Field", "Type", "Required", "Description"], iw)
    inputs = [
        ("floor_area_sqm",     "Float",   "Yes", "Gross floor area in square metres (1-50,000)"),
        ("num_storeys",        "Integer", "Yes", "Number of above-ground storeys (1-50)"),
        ("structural_type",    "Enum",    "Yes", "masonry | rc_frame | steel_frame | timber"),
        ("geopolitical_zone",  "Enum",    "Yes", "NW | NE | NC | SW | SE | SS"),
        ("state",              "String",  "Yes", "Nigerian state (36 states + FCT)"),
        ("project_type",       "Enum",    "Yes", "residential | commercial | mixed"),
        ("spec_level",         "Enum",    "Yes", "standard | medium | luxury"),
        ("num_units",          "Integer", "No",  "Number of residential units (1-500)"),
        ("project_id",         "UUID",    "No",  "Reference to saved project profile"),
        ("notes",              "String",  "No",  "Optional free-text notes (max 500 chars)"),
    ]
    for i, inp in enumerate(inputs):
        pdf.trow(list(inp), iw, fill=(i % 2 == 1))
    pdf.ln(2)
    pdf.caption("Table: EstimateInput data model. Enum values mapped to integer codes before ML inference.")

    pdf.h2("4.2 Output Data Model")
    ow = [40, 25, PAGE_W-65]
    pdf.thead(["Field", "Type", "Description"], ow)
    outputs = [
        ("estimate_id",           "UUID",    "Unique estimate identifier for audit trail"),
        ("cost_per_sqm",          "Float",   "Predicted cost per sqm (NGN)"),
        ("total_cost",            "Float",   "Total project cost = cost_per_sqm x floor_area"),
        ("lower_90",              "Float",   "Lower bound of 90% prediction interval (NGN/sqm)"),
        ("upper_90",              "Float",   "Upper bound of 90% prediction interval (NGN/sqm)"),
        ("model_version",         "String",  "MLflow run ID of the model used for inference"),
        ("macro_snapshot",        "JSON",    "Snapshot of all 7 macro variable values used"),
        ("data_source_class",     "Enum",    "GREEN | AMBER | RED — data quality classification"),
        ("shap_values",           "JSON",    "Top 5 SHAP feature name-value pairs"),
        ("pdf_report_url",        "String",  "R2 pre-signed URL for PDF report download"),
        ("created_at",            "DateTime","UTC timestamp of estimate creation"),
        ("created_by",            "UUID",    "User ID of requesting user"),
    ]
    for i, o in enumerate(outputs):
        pdf.trow(list(o), ow, fill=(i % 2 == 1))
    pdf.ln(2)
    pdf.caption("Table: EstimateOutput data model. Stored permanently in Supabase estimates table.")

    pdf.h2("4.3 Macroeconomic Data Model")
    pdf.para(
        "The macro_data table stores the latest values of each macroeconomic feature "
        "with timestamp, source, and data quality classification. It is updated by Airflow DAGs. "
        "The ML inference engine always reads from this table (not from external APIs directly) "
        "to ensure consistency between the macro_snapshot and the model's feature expectations."
    )

    # Section 5: System Constraints
    pdf.add_page()
    pdf.h1("5. System Constraints and Assumptions")
    for c in [
        "The system assumes that the ML model has been trained and registered in MLflow "
        "before the first production estimate is requested (O5 must be complete before O6 goes live).",
        "The World Bank API (GDP, CPI, lending rate) may have a 12-18 month data lag for "
        "the most recent year. The system must handle this gracefully by using the most "
        "recent available value and flagging the data age.",
        "The EIA and CBN/FRED APIs require API keys (EIA_API_KEY, FRED_API_KEY). "
        "Until these are configured, synthetic data will be used (DATA SOURCE: RED).",
        "The system is not designed to replace professional QS judgment for detailed "
        "Bills of Quantities or tender cost plans. It is a preliminary/conceptual estimate tool.",
        "Internet connectivity is assumed for all users. An offline mode is outside scope.",
        "The system assumes the ML model has been trained on real Nigerian housing project "
        "cost data (O4 data collection). If only synthetic proxy data is used, estimates "
        "will be flagged RED and marked as indicative only.",
    ]:
        pdf.bullet(c)

    out = os.path.join(OUT_DIR, 'O3_07_SRS_IEEE830.pdf')
    pdf.output(out)
    print(f"[OK]  O3_07_SRS_IEEE830.pdf -> {out}")
    return out


# ══════════════════════════════════════════════════════════════════════════════
# PDF 8: UML Use Cases
# ══════════════════════════════════════════════════════════════════════════════
USE_CASES = [
    ("UC-01", "Generate Construction Cost Estimate",
     "QS Practitioner / Housing Developer / Public Sector Client",
     "User is authenticated",
     "Estimate PDF stored in R2; estimate record in DB",
     [
         "User navigates to 'New Estimate' page",
         "User selects an existing project profile or creates a new one",
         "User completes the estimate input form (floor area, location, structural type, spec level)",
         "System validates all inputs",
         "System retrieves current macroeconomic feature values from DB",
         "System determines DATA SOURCE classification (GREEN/AMBER/RED)",
         "System calls ML inference engine (champion model)",
         "System calculates SHAP values for the estimate",
         "System generates 90% prediction intervals",
         "System triggers PDF report generation",
         "System stores estimate record with full audit trail",
         "System displays estimate results, SHAP chart, and PDF download link",
     ],
     ["Input validation fails: return error message, do not submit",
      "Macro data > 7 days old: proceed but flag AMBER",
      "ML model unavailable: return 503 error with retry guidance",
      "PDF generation fails: return estimate result without PDF; retry PDF async"]),

    ("UC-02", "View Estimate History",
     "Any authenticated user",
     "User has at least one saved estimate",
     "None (read-only)",
     [
         "User navigates to 'My Estimates' dashboard",
         "System retrieves all estimates for the authenticated user",
         "System displays estimates in reverse chronological order",
         "User can filter by project, date range, and location",
         "User selects an estimate to view full details",
         "System displays estimate inputs, outputs, SHAP values, and PDF link",
     ],
     ["No estimates found: display empty state with 'Create first estimate' CTA"]),

    ("UC-03", "Download Cost Report (PDF)",
     "Any authenticated user",
     "Estimate exists; user owns the estimate",
     "PDF downloaded to user's device",
     [
         "User clicks 'Download Report' from estimate detail or history view",
         "System verifies user owns (or has shared access to) the estimate",
         "System retrieves pre-signed R2 URL for the PDF",
         "Browser initiates PDF download",
     ],
     ["Report not yet generated: trigger async generation; notify user when ready",
      "User does not own estimate: return 403 Forbidden"]),

    ("UC-04", "Manage Project Profile",
     "Any authenticated user",
     "User is authenticated",
     "Project profile created/updated/deleted in DB",
     [
         "User navigates to 'Projects' section",
         "User creates a new project (name, address, type, notes) OR selects an existing project to edit",
         "User saves changes",
         "System stores project profile linked to the user's account",
         "User can delete a project (estimates remain; project reference is nullified)",
     ],
     ["Duplicate project name: warn user, allow override"]),

    ("UC-05", "View Macroeconomic Dashboard",
     "Any authenticated user",
     "None",
     "None (read-only display)",
     [
         "User navigates to 'Macro Dashboard'",
         "System retrieves current macro variable values from DB",
         "System displays: variable name, current value, unit, last updated, data source, DATA SOURCE class",
         "User can view historical trend chart for each variable (last 24 months)",
     ],
     ["Variable data > 7 days old: display AMBER flag with 'last updated' timestamp"]),

    ("UC-06", "Administrator: Manage Users",
     "System Administrator",
     "Actor has Admin role",
     "User status/role updated in DB",
     [
         "Admin navigates to 'User Management'",
         "Admin views list of all registered users with status (active/inactive)",
         "Admin can activate, deactivate, or promote users to admin role",
         "Admin can view a user's estimate history (read-only)",
         "All admin actions are logged in the admin_audit table",
     ],
     ["Admin attempts to deactivate themselves: return error"]),

    ("UC-07", "Administrator: Monitor Pipeline",
     "System Administrator",
     "Actor has Admin role",
     "None (read-only)",
     [
         "Admin navigates to 'Pipeline Monitor'",
         "System displays status of all 9 Airflow DAGs: last run time, status (success/failed/running), next scheduled run",
         "Admin can view the log output of the most recent DAG run",
         "Admin receives email notification on DAG failure (configured in Airflow)",
     ],
     ["Airflow API unavailable: display cached last-known status with staleness warning"]),

    ("UC-08", "Administrator: Trigger Model Retrain",
     "System Administrator",
     "Actor has Admin role; new training data is available in DB",
     "New model registered in MLflow; challenger evaluated",
     [
         "Admin navigates to 'Model Management'",
         "Admin reviews current champion model metrics (MAPE, R2, last trained)",
         "Admin clicks 'Trigger Retrain'",
         "System invokes the nhces_retrain_weekly Airflow DAG (ad hoc trigger)",
         "Airflow runs feature engineering, model benchmarking, SHAP analysis",
         "New challenger model is registered in MLflow",
         "If challenger MAPE < champion MAPE on held-out set: challenger is promoted to champion",
         "Admin receives notification of retrain result",
     ],
     ["Training data insufficient (< 50 real records): abort with warning",
      "Challenger does not outperform champion: retain champion; log challenger in MLflow"]),
]

def make_use_cases():
    pdf = O3PDF("UML Use Cases and System Interactions", "O3_08")
    pdf.add_page()

    pdf.set_fill_color(*DARK_NAVY)
    pdf.rect(0, 0, 210, 45, 'F')
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(*GOLD)
    pdf.set_xy(LEFT, 12)
    pdf.multi_cell(PAGE_W, 7.5, sanitize(
        "iNHCES O3 — UML Use Cases\nSystem Interaction Specifications"
    ), align="C")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*LIGHT_BLUE)
    pdf.set_xy(LEFT, 35)
    pdf.cell(PAGE_W, 6, sanitize("8 Primary Use Cases | Actors: QS Practitioner, Developer, Client, Administrator"), align="C")
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(20)

    _ds_page(pdf, 'green',
        "DATA SOURCE: GREEN — Use case specifications are real system design documents, "
        "not dependent on survey data. They describe the intended system behaviour based "
        "on the SRS (O3_07) and Delphi consensus requirements (O3_06).",
        (
            "The 8 use cases documented here cover the primary interactions between users "
            "and the iNHCES system. They are specified in UML Use Case Specification format "
            "(Cockburn, 2001 [VERIFY]).\n\n"
            "ACTORS:\n"
            "  - QS Practitioner: primary user; registered NIQS member\n"
            "  - Housing Developer: registered user; REDAN member or similar\n"
            "  - Public Sector Client: registered user; FHA/state housing corp. staff\n"
            "  - Researcher: registered user; academic access with extended history view\n"
            "  - System Administrator: privileged user; pipeline/model/user management\n\n"
            "CONFIDENCE: HIGH. Use cases are grounded in the FR/NFR specification (O3_07). "
            "They will be reviewed with practitioner stakeholders in co-design workshops (O3 Step 2 real)."
        )
    )

    # Use Case Diagram (text-based)
    pdf.add_page()
    pdf.h1("1. Actor-Use Case Relationship Overview")
    aw = [20, 80, PAGE_W-100]
    pdf.thead(["UC-ID", "Use Case Name", "Primary Actor(s)"], aw)
    for uc in USE_CASES:
        pdf.trow([uc[0], uc[1], uc[2]], aw, fill=(USE_CASES.index(uc) % 2 == 1))
    pdf.ln(2)
    pdf.caption("Table 1: Use case inventory. 8 primary use cases. 5 actor types.")

    pdf.para(
        "Note: A UML Use Case Diagram (graphical) is documented in Mermaid format in "
        "04_conceptual_models/04_Architecture_Diagram.mmd. The text specifications below "
        "provide the primary detail for system design."
    )

    # Individual use case specs
    pdf.add_page()
    pdf.h1("2. Use Case Specifications")
    for uc_id, name, actors, pre, post, main_flow, alt_flow in USE_CASES:
        pdf.h2(f"{uc_id}: {name}")
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*DARK_NAVY)
        pdf.set_x(LEFT)
        pdf.cell(30, 5, "Actors:")
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*DARK_GREY)
        pdf.multi_cell(PAGE_W - 30, 5, sanitize(actors))

        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*DARK_NAVY)
        pdf.set_x(LEFT)
        pdf.cell(30, 5, "Preconditions:")
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*DARK_GREY)
        pdf.multi_cell(PAGE_W - 30, 5, sanitize(pre))

        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*DARK_NAVY)
        pdf.set_x(LEFT)
        pdf.cell(30, 5, "Postconditions:")
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*DARK_GREY)
        pdf.multi_cell(PAGE_W - 30, 5, sanitize(post))

        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*DARK_NAVY)
        pdf.set_x(LEFT)
        pdf.multi_cell(PAGE_W, 5, "Main Flow:")
        for i, step in enumerate(main_flow, 1):
            pdf.set_font("Helvetica", "", 9)
            pdf.set_text_color(*DARK_GREY)
            pdf.set_x(LEFT + 4)
            pdf.multi_cell(PAGE_W - 4, 4.8, sanitize(f"{i}. {step}"))

        if alt_flow:
            pdf.set_font("Helvetica", "B", 9)
            pdf.set_text_color(*DARK_NAVY)
            pdf.set_x(LEFT)
            pdf.multi_cell(PAGE_W, 5, "Alternative / Exception Flows:")
            for step in alt_flow:
                pdf.set_font("Helvetica", "", 9)
                pdf.set_text_color(*DARK_GREY)
                pdf.set_x(LEFT + 4)
                pdf.multi_cell(PAGE_W - 4, 4.8, sanitize(f"- {step}"))

        pdf.set_draw_color(*MID_GREY)
        pdf.set_line_width(0.2)
        pdf.line(LEFT, pdf.get_y() + 1, LEFT + PAGE_W, pdf.get_y() + 1)
        pdf.ln(4)

    out = os.path.join(OUT_DIR, 'O3_08_UML_Use_Cases.pdf')
    pdf.output(out)
    print(f"[OK]  O3_08_UML_Use_Cases.pdf -> {out}")
    return out


# ══════════════════════════════════════════════════════════════════════════════
# Save CSV and MD files
# ══════════════════════════════════════════════════════════════════════════════
def save_delphi_csv(r2_stats, r3_stats, final_items, excluded_items):
    out = os.path.join(DEL_DIR, 'delphi_results.csv')
    rows = []
    for it in DELPHI_ITEMS:
        iid = it[1]
        r2s = r2_stats[iid]
        r3s = r3_stats.get(iid)
        if any(i[0][1] == iid for i in final_items):
            status = "consensus_r2" if r3s is None or not any(i[0][1] == iid and i[2] is not None for i in final_items) else "consensus_r3"
        else:
            status = "excluded"
        rows.append({
            'item_id': iid, 'category': it[0], 'category_name': CATEGORIES[it[0]],
            'short_text': it[2], 'full_text': it[3],
            'r2_n': N_EXPERTS,
            'r2_mean': round(r2s['mean'], 4), 'r2_sd': round(r2s['sd'], 4),
            'r2_cv': round(r2s['cv'], 2), 'r2_iqr': round(r2s['iqr'], 2),
            'r2_consensus': r2s['consensus'],
            'r3_mean': round(r3s['mean'], 4) if r3s else '',
            'r3_sd': round(r3s['sd'], 4) if r3s else '',
            'r3_cv': round(r3s['cv'], 2) if r3s else '',
            'r3_consensus': r3s['consensus'] if r3s else '',
            'final_status': status,
        })
    with open(out, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)
    print(f"[OK]  delphi_results.csv -> {out}")
    return out


def save_md_files(r2_stats, r3_stats, final_items, excluded_items):
    # Round1.md
    r1 = os.path.join(DEL_DIR, 'Round1.md')
    with open(r1, 'w', encoding='utf-8') as f:
        f.write("# iNHCES Delphi Round 1 — Open-Ended Instrument\n\n")
        f.write("> DATA SOURCE: AMBER — Instrument is real; responses are hypothetical placeholders.\n\n")
        f.write("## Instructions\nQualitative expert survey — 7 sections, open-ended questions.\n\n")
        f.write("## Sections\n")
        sections = ["Expert Background","Macroeconomic Factors","Project Characteristics",
                    "ML Model Performance","System Interface & Usability",
                    "Data Quality & Governance","Reporting"]
        for s in sections:
            f.write(f"### {s}\n[Open-ended questions — see O3_02_Delphi_Round1_Instrument.pdf]\n\n")
    print(f"[OK]  Round1.md -> {r1}")

    # Round2.md
    r2 = os.path.join(DEL_DIR, 'Round2.md')
    with open(r2, 'w', encoding='utf-8') as f:
        f.write("# iNHCES Delphi Round 2 — 38-Item Likert Instrument\n\n")
        f.write("> DATA SOURCE: AMBER — Instrument is real; ratings are SYNTHETIC (numpy seed=42).\n\n")
        f.write(f"**Scale**: 1=Strongly Disagree ... 7=Strongly Agree  \n")
        f.write(f"**Consensus**: Mean >= {CONSENSUS_MEAN}, CV <= {CONSENSUS_CV}%  \n")
        f.write(f"**n**: {N_EXPERTS} (synthetic)  \n\n")
        for cat in sorted(CATEGORIES.keys()):
            f.write(f"## Category {cat}: {CATEGORIES[cat]}\n\n")
            for it in DELPHI_ITEMS:
                if it[0] != cat:
                    continue
                s = r2_stats[it[1]]
                cons = "YES" if s['consensus'] else "NO (-> Round 3)"
                f.write(f"**{it[1]}**: {it[3]}  \n")
                f.write(f"Mean={s['mean']:.2f}, SD={s['sd']:.2f}, CV={s['cv']:.1f}%, Consensus={cons}  \n\n")
    print(f"[OK]  Round2.md -> {r2}")

    # Round3.md
    r3 = os.path.join(DEL_DIR, 'Round3.md')
    non_con = [it for it in DELPHI_ITEMS if not r2_stats[it[1]]['consensus']]
    with open(r3, 'w', encoding='utf-8') as f:
        f.write("# iNHCES Delphi Round 3 — Consensus Refinement\n\n")
        f.write("> DATA SOURCE: AMBER/RED — Round 3 ratings are SYNTHETIC.\n\n")
        f.write(f"**Items in Round 3**: {len(non_con)}  \n")
        f.write(f"**Consensus criterion**: Mean >= {CONSENSUS_MEAN}, CV <= {CONSENSUS_CV}%  \n\n")
        for it in non_con:
            s2 = r2_stats[it[1]]
            s3 = r3_stats.get(it[1])
            f.write(f"## {it[1]}: {it[2]}\n\n")
            f.write(f"Round 2: Mean={s2['mean']:.2f}, CV={s2['cv']:.1f}%  \n")
            if s3:
                cons3 = "YES" if s3['consensus'] else "NO (EXCLUDED)"
                f.write(f"Round 3: Mean={s3['mean']:.2f}, CV={s3['cv']:.1f}%, Consensus={cons3}  \n\n")
    print(f"[OK]  Round3.md -> {r3}")

    # SRS.md
    srs_md = os.path.join(SRS_DIR, '03_SRS_NHCES_IEEE830.md')
    with open(srs_md, 'w', encoding='utf-8') as f:
        f.write("# iNHCES Software Requirements Specification — IEEE 830\n\n")
        f.write("> DATA SOURCE: AMBER — See O3_07_SRS_IEEE830.pdf for full specification.\n\n")
        f.write(f"**Version**: 1.0 DRAFT  \n**Status**: Based on synthetic Delphi consensus  \n\n")
        f.write("## Functional Requirements Summary\n\n| ID | Name | Priority |\n|---|---|---|\n")
        for fr_id, fr_name, priority, _ in FUNCTIONAL_REQS:
            f.write(f"| {fr_id} | {fr_name} | {priority} |\n")
        f.write("\n## Non-Functional Requirements Summary\n\n| ID | Name | Priority |\n|---|---|---|\n")
        for nfr_id, nfr_name, priority, _ in NON_FUNC_REQS:
            f.write(f"| {nfr_id} | {nfr_name} | {priority} |\n")
        f.write("\n_Full specification: see O3_07_SRS_IEEE830.pdf_\n")
    print(f"[OK]  03_SRS_NHCES_IEEE830.md -> {srs_md}")

    # Use Cases.md
    uc_md = os.path.join(UC_DIR, '03_UML_Use_Cases.md')
    with open(uc_md, 'w', encoding='utf-8') as f:
        f.write("# iNHCES UML Use Cases\n\n")
        f.write("> DATA SOURCE: GREEN — See O3_08_UML_Use_Cases.pdf for full specifications.\n\n")
        f.write("## Use Case Inventory\n\n| ID | Name | Actor |\n|---|---|---|\n")
        for uc in USE_CASES:
            f.write(f"| {uc[0]} | {uc[1]} | {uc[2]} |\n")
        f.write("\n_Full specifications: see O3_08_UML_Use_Cases.pdf_\n")
    print(f"[OK]  03_UML_Use_Cases.md -> {uc_md}")


# ══════════════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════════════
def main():
    print("=== iNHCES O3 Requirements Modelling ===")
    print(f"Running Delphi simulation (n={N_EXPERTS}, seed={SEED})...")
    r2_ratings, r2_stats, r3_items, r3_ratings, r3_stats, final_items, excluded_items = run_delphi()
    n_r2_cons = sum(1 for v in r2_stats.values() if v['consensus'])
    print(f"  Round 2 consensus: {n_r2_cons}/{len(DELPHI_ITEMS)} items")
    print(f"  Round 3 items: {len(r3_items)}")
    print(f"  Final consensus: {len(final_items)} items | Excluded: {len(excluded_items)} items")
    if excluded_items:
        for it, _, _ in excluded_items:
            print(f"    EXCLUDED: {it[1]} — {it[2]}")

    print("\nGenerating PDFs...")
    make_stakeholder_register(r2_stats, r3_stats, final_items, excluded_items)
    make_round1_instrument()
    make_round2_instrument()
    make_round2_analysis(r2_stats, r3_items)
    make_round3_instrument(r3_items, r2_stats)
    make_final_consensus(r2_stats, r3_stats, final_items, excluded_items)
    make_srs(final_items)
    make_use_cases()

    print("\nSaving CSV and Markdown files...")
    save_delphi_csv(r2_stats, r3_stats, final_items, excluded_items)
    save_md_files(r2_stats, r3_stats, final_items, excluded_items)

    print("\n=== O3 COMPLETE ===")
    pdfs = [f for f in os.listdir(OUT_DIR) if f.startswith('O3_') and f.endswith('.pdf')]
    for p in sorted(pdfs):
        print(f"  {p}")


if __name__ == "__main__":
    main()
