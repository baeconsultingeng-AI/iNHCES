"""
iNHCES Research Publication Portfolio Generator
TETFund National Research Fund (NRF) 2025
Department of Quantity Surveying, ABU Zaria
"""

from fpdf import FPDF
from datetime import date

HEADER_TEXT = "TETFund National Research Fund (NRF) 2025 - Department of Quantity Surveying, ABU Zaria"
OUTPUT_PATH = r"c:\Users\MacBook\Desktop\BaeSoftIA\INHCES\iNHCES\Research_Documents\03_iNHCES_Research_Publication_Portfolio.pdf"

# ── Colour palette ─────────────────────────────────────────────────────────────
DARK_NAVY   = (15,  40,  80)   # header bar / section title backgrounds
GOLD        = (180, 140,  30)   # accent rule lines
LIGHT_BLUE  = (220, 230, 245)  # alternating row / concept box fill
WHITE       = (255, 255, 255)
DARK_GREY   = (60,  60,  60)
MID_GREY    = (120, 120, 120)
LIGHT_GREY  = (240, 240, 240)


def sanitize(text):
    """Replace characters unsupported by Helvetica core font."""
    t = (str(text)
         .replace('\u2014', ' - ').replace('\u2013', '-')
         .replace('\u2018', "'").replace('\u2019', "'")
         .replace('\u201c', '"').replace('\u201d', '"')
         .replace('\u2022', '*').replace('\u00a0', ' ')
         .replace('\u2264', '<=').replace('\u2265', '>=')
         .replace('\u00ae', '(R)').replace('\u00a9', '(C)')
         .replace('\u2192', '->').replace('\u2190', '<-')
         .replace('\u2191', '^').replace('\u2193', 'v')
         .replace('\u00b2', '^2').replace('\u00b3', '^3')
         .replace('\u03b1', 'alpha').replace('\u03b2', 'beta')
         .replace('\u03c3', 'sigma').replace('\u03bc', 'mu')
         .replace('\u2260', '!=').replace('\u00b1', '+/-')
         .replace('\u00d7', 'x').replace('\u00f7', '/')
         .replace('\u2026', '...')
         .replace('\u20a6', 'NGN')   # Naira sign
         )
    # Final catch-all: encode to latin-1, replacing any remaining unsupported chars
    return t.encode('latin-1', errors='replace').decode('latin-1')


class PortfolioPDF(FPDF):

    def header(self):
        self.set_fill_color(*DARK_NAVY)
        self.rect(0, 0, 210, 14, 'F')
        self.set_font("Helvetica", "B", 7.5)
        self.set_text_color(*WHITE)
        self.set_xy(5, 4)
        self.cell(0, 6, sanitize(HEADER_TEXT), ln=0)
        self.set_text_color(*DARK_GREY)
        self.ln(16)

    def footer(self):
        self.set_y(-13)
        self.set_draw_color(*GOLD)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 200, self.get_y())
        self.set_font("Helvetica", "I", 7.5)
        self.set_text_color(*MID_GREY)
        self.cell(0, 8,
                  sanitize(f"iNHCES Research Publication Portfolio  |  ABU Zaria / TETFund NRF 2025  |  Page {self.page_no()}"),
                  align="C")

    # ── Helper: section title bar ──────────────────────────────────────────────
    def section_title(self, title):
        self.ln(4)
        self.set_fill_color(*DARK_NAVY)
        self.set_text_color(*WHITE)
        self.set_font("Helvetica", "B", 11)
        self.cell(0, 9, sanitize(f"  {title}"), ln=True, fill=True)
        self.set_text_color(*DARK_GREY)
        self.ln(2)

    # ── Helper: sub-heading ────────────────────────────────────────────────────
    def sub_heading(self, text):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*DARK_NAVY)
        self.cell(0, 7, sanitize(text), ln=True)
        self.set_text_color(*DARK_GREY)

    # ── Helper: body paragraph ─────────────────────────────────────────────────
    def body(self, text, indent=5):
        self.set_font("Helvetica", "", 9.5)
        self.set_text_color(*DARK_GREY)
        self.set_x(10 + indent)
        self.multi_cell(0, 5.5, sanitize(text))
        self.ln(1)

    # ── Helper: concept box ────────────────────────────────────────────────────
    def concept_box(self, term, what_it_is, why_used, what_produces):
        self.ln(2)
        self.set_fill_color(*LIGHT_BLUE)
        self.set_draw_color(*GOLD)
        self.set_line_width(0.4)
        x, y = self.get_x(), self.get_y()
        # Measure height needed
        self.set_font("Helvetica", "B", 8.5)
        lines_title = 1
        self.set_font("Helvetica", "", 8.5)
        # Draw box outline (approximate height 36)
        self.rect(10, y, 190, 38, 'FD')
        self.set_xy(13, y + 2)
        self.set_font("Helvetica", "B", 8.5)
        self.set_text_color(*DARK_NAVY)
        self.cell(0, 5, sanitize(f"  CONCEPT EXPLAINER:  {term}"), ln=True)
        self.set_draw_color(*GOLD)
        self.set_line_width(0.2)
        self.line(13, self.get_y(), 200, self.get_y())
        self.ln(1)
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*DARK_NAVY)
        self.set_x(13)
        self.cell(28, 5, "What it is:", ln=False)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*DARK_GREY)
        self.multi_cell(0, 5, sanitize(what_it_is))
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*DARK_NAVY)
        self.set_x(13)
        self.cell(28, 5, "Why used here:", ln=False)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*DARK_GREY)
        self.multi_cell(0, 5, sanitize(why_used))
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*DARK_NAVY)
        self.set_x(13)
        self.cell(28, 5, "Output:", ln=False)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*DARK_GREY)
        self.multi_cell(0, 5, sanitize(what_produces))
        self.ln(3)

    # ── Helper: paper card ────────────────────────────────────────────────────
    def paper_card(self, number, title, journal, publisher, rank,
                   objective, content_summary, key_contribution, produced_in, fill=False):
        fill_colour = LIGHT_BLUE if fill else WHITE
        self.set_fill_color(*fill_colour)
        self.set_draw_color(*GOLD)
        self.set_line_width(0.3)
        y_start = self.get_y()
        self.rect(10, y_start, 190, 58, 'FD' if fill else 'D')

        # Paper number badge
        self.set_fill_color(*DARK_NAVY)
        self.rect(10, y_start, 18, 58, 'F')
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(*WHITE)
        self.set_xy(12, y_start + 22)
        self.cell(14, 10, f"P{number}", align="C")

        # Title
        self.set_xy(31, y_start + 2)
        self.set_font("Helvetica", "B", 9.5)
        self.set_text_color(*DARK_NAVY)
        self.multi_cell(170, 5.5, sanitize(title))

        # Meta row
        self.set_xy(31, y_start + 14)
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*GOLD[0:3] if isinstance(GOLD, tuple) else GOLD)
        self.set_text_color(140, 100, 20)
        self.cell(22, 5, "Journal:", ln=False)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*DARK_GREY)
        self.cell(80, 5, sanitize(journal), ln=False)
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(140, 100, 20)
        self.cell(18, 5, "Publisher:", ln=False)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*DARK_GREY)
        self.cell(0, 5, sanitize(publisher), ln=True)

        self.set_xy(31, y_start + 20)
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(140, 100, 20)
        self.cell(22, 5, "Ranking:", ln=False)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*DARK_GREY)
        self.cell(80, 5, sanitize(rank), ln=False)
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(140, 100, 20)
        self.cell(18, 5, "Objective:", ln=False)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*DARK_GREY)
        self.cell(0, 5, sanitize(objective), ln=True)

        # Divider
        self.set_draw_color(*GOLD)
        self.line(31, y_start + 27, 198, y_start + 27)

        self.set_xy(31, y_start + 29)
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(140, 100, 20)
        self.cell(25, 4.5, "Content:", ln=False)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*DARK_GREY)
        self.multi_cell(0, 4.5, sanitize(content_summary))

        self.set_xy(31, y_start + 39)
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(140, 100, 20)
        self.cell(25, 4.5, "Key Contribution:", ln=False)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*DARK_GREY)
        self.multi_cell(0, 4.5, sanitize(key_contribution))

        self.set_xy(31, y_start + 49)
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(140, 100, 20)
        self.cell(25, 4.5, "Produced in:", ln=False)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*DARK_GREY)
        self.multi_cell(0, 4.5, sanitize(produced_in))

        self.set_y(y_start + 61)

    # ── Helper: table row ─────────────────────────────────────────────────────
    def table_row(self, cols, widths, fill=False, bold=False):
        fill_col = LIGHT_BLUE if fill else WHITE
        self.set_fill_color(*fill_col)
        self.set_font("Helvetica", "B" if bold else "", 8.5)
        self.set_text_color(*DARK_GREY)
        for text, w in zip(cols, widths):
            self.cell(w, 7, sanitize(f"  {text}"), border=1, fill=True)
        self.ln()


# ═══════════════════════════════════════════════════════════════════════════════
def build_pdf():
    pdf = PortfolioPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.set_margins(10, 20, 10)

    # ══════════════════════════════════════════════════════════════════════
    # PAGE 1 — COVER
    # ══════════════════════════════════════════════════════════════════════
    pdf.add_page()
    # Dark banner
    pdf.set_fill_color(*DARK_NAVY)
    pdf.rect(0, 18, 210, 60, 'F')
    pdf.set_xy(0, 24)
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(*WHITE)
    pdf.cell(0, 10, sanitize("iNHCES RESEARCH"), align="C", ln=True)
    pdf.set_font("Helvetica", "B", 15)
    pdf.cell(0, 9, sanitize("Research Publication Portfolio"), align="C", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(200, 215, 235)
    pdf.cell(0, 7, sanitize("Intelligent National Housing Cost Estimating System for Nigeria"), align="C", ln=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*LIGHT_BLUE)
    pdf.cell(0, 7, sanitize("TETFund National Research Fund (NRF) 2025  |  Department of Quantity Surveying, ABU Zaria"),
             align="C", ln=True)

    # Gold rule
    pdf.set_draw_color(*GOLD)
    pdf.set_line_width(1.0)
    pdf.line(30, 82, 180, 82)

    pdf.set_xy(10, 88)
    pdf.set_text_color(*DARK_GREY)
    pdf.set_font("Helvetica", "", 9.5)
    intro = (
        "This document presents the full publication portfolio for the iNHCES research project, detailing "
        "eight peer-reviewed papers planned across all six research objectives. Each paper is mapped to its "
        "target journal, objective, key contribution, and the specific project deliverables from which it "
        "will be produced. The portfolio targets six Q1 journals with a combined impact factor exceeding 35, "
        "establishing iNHCES as a landmark study in AI-based construction cost estimation for Nigeria and "
        "the wider developing economy context."
    )
    pdf.multi_cell(0, 5.5, intro)

    # Summary statistics boxes
    pdf.ln(5)
    stats = [
        ("8", "Target\nPublications"),
        ("6", "Q1 Journals\nTargeted"),
        ("4", "Elsevier\nJournals"),
        ("18-24", "Month\nTimeline"),
    ]
    box_w = 42
    for i, (val, label) in enumerate(stats):
        x = 10 + i * (box_w + 4)
        pdf.set_fill_color(*DARK_NAVY)
        pdf.rect(x, pdf.get_y(), box_w, 22, 'F')
        pdf.set_xy(x, pdf.get_y() + 2)
        pdf.set_font("Helvetica", "B", 18)
        pdf.set_text_color(*WHITE)
        pdf.cell(box_w, 9, val, align="C", ln=False)
        pdf.set_xy(x, pdf.get_y() + 10)
        pdf.set_font("Helvetica", "", 7.5)
        pdf.set_text_color(200, 215, 235)
        pdf.multi_cell(box_w, 4, label, align="C")
    pdf.ln(30)

    pdf.set_font("Helvetica", "I", 8.5)
    pdf.set_text_color(*MID_GREY)
    pdf.cell(0, 6, sanitize(f"Generated: {date.today().strftime('%d %B %Y')}  |  Version 1.0"), align="C")

    # ══════════════════════════════════════════════════════════════════════
    # PAGE 2 — CONCEPT EXPLAINERS
    # ══════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("Section 1: Key Concepts in Research Publication")

    pdf.body(
        "Before presenting the publication portfolio, this section explains the key concepts relevant to "
        "planning and executing a research dissemination strategy of this scale. Understanding these terms "
        "will help the entire ABU Zaria research team engage meaningfully with the publication process."
    )

    pdf.concept_box(
        "Peer-Reviewed Journal Publication",
        "A peer-reviewed journal publishes research articles that have been evaluated by independent "
        "experts (peers) in the same field before acceptance. This process ensures the research meets "
        "scientific standards of rigour, validity, and originality.",
        "iNHCES targets peer-reviewed journals to ensure the findings are internationally credible, "
        "citable, and eligible for TETFund final reporting. Peer review is the benchmark of academic "
        "quality recognised by all Nigerian and international universities.",
        "Accepted and published papers that establish the team's authority, advance the field, and "
        "fulfil TETFund dissemination requirements."
    )

    pdf.concept_box(
        "Journal Impact Factor (IF) and Quartile Ranking (Q1)",
        "The Impact Factor measures how frequently papers in a journal are cited. Q1 means the journal "
        "is in the top 25% of its subject category by impact — the most prestigious tier. Elsevier's "
        "'Automation in Construction' has an IF of approximately 9.6, meaning its papers are cited "
        "nearly 10 times on average within two years of publication.",
        "Targeting Q1 journals maximises the international visibility of iNHCES findings, strengthens "
        "the team's research profile, and aligns with TETFund's expectation of high-impact outputs.",
        "Publications that attract citations, enhance ABU Zaria's global research ranking, and "
        "position the team as leaders in AI-based construction cost research in Africa."
    )

    pdf.concept_box(
        "Research Dissemination Strategy",
        "A dissemination strategy is a planned approach to sharing research findings with target "
        "audiences — academics, practitioners, policymakers — through journals, conferences, reports, "
        "and datasets. A well-structured strategy ensures maximum coverage across different communities.",
        "iNHCES spans multiple disciplines (construction economics, AI/ML, data engineering, housing "
        "policy). A portfolio approach ensures each distinct contribution reaches its most relevant "
        "journal audience rather than being buried in a single publication.",
        "Eight papers across six journals covering SLR, macro analysis, requirements, ML benchmarking, "
        "MLOps architecture, full system, data pipeline, and housing policy."
    )

    pdf.concept_box(
        "Open Access and Data Paper",
        "An open access paper is freely available to all readers without a subscription. A data paper "
        "(published in journals like 'Scientific Data' or 'Data in Brief') describes a dataset rather "
        "than research findings — its purpose is to make the dataset citable and reusable by others.",
        "The iNHCES automated data pipeline — connecting CBN, NBS, EIA, World Bank, and web scrapers — "
        "is unprecedented in the Nigerian construction literature. Publishing it as a data paper creates "
        "a citable, reusable national resource that other researchers can build upon.",
        "A citable dataset record that gives ABU Zaria permanent credit for building Nigeria's first "
        "automated construction cost intelligence infrastructure."
    )

    # ══════════════════════════════════════════════════════════════════════
    # PAGE 3 — PORTFOLIO OVERVIEW TABLE
    # ══════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("Section 2: Publication Portfolio Overview")

    pdf.body(
        "The table below summarises all eight planned publications, showing the paper number, title, "
        "target journal, quartile ranking, and the research objective(s) it serves. Full details "
        "for each paper are provided in Section 3."
    )
    pdf.ln(2)

    # Table header
    widths = [10, 72, 52, 15, 41]
    headers = ["No.", "Paper Title", "Target Journal", "Rank", "Objective(s)"]
    pdf.table_row(headers, widths, fill=True, bold=True)

    rows = [
        ("P1", "AI/ML Methods for Construction Cost Estimation: A PRISMA-Compliant Systematic Review",
         "Construction Mgmt & Economics", "Q1", "O1 (Steps 1-3)"),
        ("P2", "Requirements for an AI-Based NHCES: A Delphi Consensus Study Among Nigerian QS",
         "Eng., Construction & Arch. Mgmt", "Q1", "O1-Step 4 + O3"),
        ("P3", "Macroeconomic Determinants of Housing Construction Costs in Nigeria: VAR/VECM & SHAP",
         "Construction Mgmt & Economics", "Q1", "O2 (Steps 2-4)"),
        ("P4", "Automated Multi-Source Data Pipeline for Nigerian Construction Cost Intelligence",
         "Scientific Data / Data in Brief", "Q1", "O2-Step 1 + O4 + O5a"),
        ("P5", "Benchmarking ML Models for Housing Cost Estimation in Nigeria: XGBoost, LightGBM & SHAP",
         "J. of Construction Eng. & Mgmt", "Q1", "O5 (Steps 1-3)"),
        ("P6", "Champion-Challenger MLOps Architecture for Continuously-Updating Construction Cost Models",
         "Expert Systems with Applications", "Q1", "O5 (Steps 4-5)"),
        ("P7", "iNHCES: Intelligent National Housing Cost Estimating System for Nigeria (Full System)",
         "Automation in Construction", "Q1", "O6 (All Steps)"),
        ("P8", "Leveraging AI for Housing Affordability: Policy Implications of iNHCES for Nigeria",
         "Habitat International", "Q1", "Post O6"),
        ("P9", "Responsible AI Integration in Academic Research Workflows: A Simulation-to-Publication Framework for Postgraduate Training",
         "Computers & Education / IETI", "Q1", "Meta: O1-O6 process"),
    ]
    for i, row in enumerate(rows):
        pdf.table_row(row, widths, fill=(i % 2 == 0))

    # ── Journal legend ──────────────────────────────────────────────────
    pdf.ln(6)
    pdf.sub_heading("Journal Publisher Legend")
    legend = [
        ("Construction Management and Economics", "Taylor & Francis", "Q1", "IF ~3.2"),
        ("Engineering, Construction and Architectural Management", "Emerald", "Q1", "IF ~4.1"),
        ("Journal of Construction Engineering and Management", "ASCE", "Q1", "IF ~4.5"),
        ("Scientific Data", "Springer Nature", "Q1", "IF ~9.8"),
        ("Data in Brief", "Elsevier", "Q1", "IF ~1.2"),
        ("Expert Systems with Applications", "Elsevier", "Q1", "IF ~8.7"),
        ("Automation in Construction", "Elsevier", "Q1", "IF ~9.6"),
        ("Habitat International", "Elsevier", "Q1", "IF ~6.5"),
        ("Computers & Education", "Elsevier", "Q1", "IF ~12.0"),
        ("Innovations in Education and Teaching International", "Taylor & Francis", "Q2", "IF ~3.8"),
    ]
    lwidths = [82, 38, 15, 18]
    lheaders = ["Journal Name", "Publisher", "Rank", "Impact Factor"]
    pdf.table_row(lheaders, lwidths, fill=True, bold=True)
    for i, row in enumerate(legend):
        pdf.table_row(row, lwidths, fill=(i % 2 == 0))

    # ══════════════════════════════════════════════════════════════════════
    # PAGES 4-7 — INDIVIDUAL PAPER DETAILS
    # ══════════════════════════════════════════════════════════════════════
    papers = [
        {
            "number": 1,
            "title": "Artificial Intelligence and Machine Learning Methods for Construction Cost Estimation: "
                     "A PRISMA-Compliant Systematic Review",
            "journal": "Construction Management and Economics",
            "publisher": "Taylor & Francis  |  Q1",
            "rank": "Q1  (IF ~3.2)",
            "objective": "O1 — Steps 1, 2 & 3",
            "content": "Three-generation taxonomy of cost estimation methods (traditional, statistical, AI/ML). "
                       "PRISMA 2020 protocol. PICO framework. Gap analysis. 60-80 synthesised papers. "
                       "Contextualised for Sub-Saharan Africa.",
            "contribution": "First PRISMA-compliant SLR covering AI/ML cost estimation explicitly contextualised "
                            "for developing economies and Nigeria — no prior study achieves this scope.",
            "produced_in": "O1 Steps 1-3 → 01_PRISMA_Protocol.pdf, 04_Methodology_Taxonomy_Table.pdf, "
                           "06_Literature_Review_Draft.pdf",
            "concepts": [
                ("PRISMA 2020",
                 "Preferred Reporting Items for Systematic Reviews and Meta-Analyses. A 27-item checklist "
                 "that ensures a literature review is rigorous, transparent, and reproducible.",
                 "PRISMA is now required by most Q1 journals for systematic reviews. Using it signals "
                 "methodological rigour to reviewers and editors.",
                 "A PRISMA flow diagram showing paper screening stages and a completed checklist."),
                ("Systematic Literature Review (SLR)",
                 "An SLR follows a pre-registered protocol to identify, screen, and synthesise all relevant "
                 "literature on a topic — unlike a narrative review which selects papers subjectively.",
                 "An SLR provides the evidence base for NHCES design choices and demonstrates that no "
                 "comparable system exists for Nigeria, justifying the entire research project.",
                 "A synthesis table of 60-80 papers, a methodology taxonomy, and a gap analysis."),
            ]
        },
        {
            "number": 2,
            "title": "Requirements for an AI-Based National Housing Cost Estimating System: "
                     "A Delphi Consensus Study Among Nigerian Quantity Surveyors",
            "journal": "Engineering, Construction and Architectural Management",
            "publisher": "Emerald  |  Q1",
            "rank": "Q1  (IF ~4.1)",
            "objective": "O1-Step 4  +  O3 (All Steps)",
            "content": "3-round Delphi with 15-25 NIQS/FHA/REDAN panellists. Relative Importance Index (RII) "
                       "analysis. Kendall's W consensus measurement. Full SRS to IEEE 830 standard.",
            "contribution": "First empirical requirements study for an AI-based cost estimation system "
                            "in West Africa, grounded in practitioner consensus rather than researcher assumption.",
            "produced_in": "O1-Step 4 + O3 Steps 1-4 → 03_Delphi_Round1-3.pdf, "
                           "03_Requirements_Findings.pdf, 03_SRS_NHCES_IEEE830.pdf",
            "concepts": [
                ("Delphi Method",
                 "A structured expert elicitation technique using multiple rounds of questionnaires to "
                 "achieve consensus. Responses are anonymised between rounds so experts can revise views "
                 "without social pressure.",
                 "Delphi is ideal for NHCES because there is no single authoritative source for what the "
                 "system must do — consensus must be built from QS practitioners, developers, and government.",
                 "A ranked list of agreed system requirements with consensus scores, forming the basis of the SRS."),
                ("Relative Importance Index (RII)",
                 "RII = (Sum of all scores) / (Highest scale value x Number of respondents). It ranks "
                 "requirements from 0 to 1, where values above 0.7 typically indicate high importance.",
                 "RII allows the team to objectively rank which NHCES features experts agree are most "
                 "critical, providing a defensible priority order for development.",
                 "A ranked requirements table with RII values that directly informs the SRS and O4 architecture."),
            ]
        },
        {
            "number": 3,
            "title": "Macroeconomic Determinants of Nigerian Housing Construction Costs: "
                     "A VAR/VECM and SHAP Feature Importance Analysis",
            "journal": "Construction Management and Economics",
            "publisher": "Taylor & Francis  |  Q1",
            "rank": "Q1  (IF ~3.2)",
            "objective": "O2 — Steps 2, 3 & 4",
            "content": "VAR, VECM, Granger causality tests, ARIMA/ARIMAX models. SHAP feature importance "
                       "ranking. Variables: NGN/USD, CPI, oil price, cement price, lending rate, GDP, PMS.",
            "contribution": "First econometric model explicitly linking Nigerian macroeconomic volatility "
                            "(oil price shocks, exchange rate crises, inflation spikes) to construction cost dynamics.",
            "produced_in": "O2 Steps 2-4 → stationarity_analysis.py, var_vecm_model.py, "
                           "02_Macro_Results_Discussion.pdf",
            "concepts": [
                ("Vector Autoregression (VAR) and VECM",
                 "VAR models the relationships between multiple time-series variables simultaneously, "
                 "showing how each variable responds to shocks in the others. VECM (Vector Error Correction "
                 "Model) extends VAR to handle variables that are cointegrated — i.e., they move together "
                 "in the long run even if they diverge short-term.",
                 "Nigerian construction costs are affected by multiple macroeconomic forces simultaneously. "
                 "VAR/VECM captures these interdependencies — a simple regression cannot.",
                 "Impulse response functions, variance decomposition tables, and coefficient estimates "
                 "showing which variables have the strongest long-run effect on construction costs."),
                ("Granger Causality",
                 "A statistical test that determines whether past values of variable X help predict future "
                 "values of variable Y. If they do, X is said to 'Granger-cause' Y.",
                 "We need to know which macroeconomic variables actually predict construction costs vs. "
                 "merely correlate with them. Granger causality provides this directional evidence.",
                 "A causality matrix showing which variables (oil price, exchange rate, etc.) "
                 "significantly predict Nigerian housing construction costs."),
            ]
        },
        {
            "number": 4,
            "title": "An Automated Multi-Source Data Pipeline for Nigerian Construction Cost Intelligence: "
                     "Architecture, Implementation and Open Dataset",
            "journal": "Scientific Data (Springer Nature)  OR  Data in Brief (Elsevier)",
            "publisher": "Springer Nature / Elsevier  |  Q1",
            "rank": "Q1  (IF ~9.8 / ~1.2)",
            "objective": "O2-Step 1  +  O4  +  O5a (Pipeline Build)",
            "content": "All 9 Airflow DAGs. Tier 1/2/3 source integration (CBN, NBS, EIA, World Bank, NGX, "
                       "web scrapers). Great Expectations validation. Supabase feature store. Full codebase.",
            "contribution": "First fully automated, continuously-updating construction cost data infrastructure "
                            "for Nigeria — unprecedented in the literature per the Research Advisory Framework.",
            "produced_in": "O2-Step 1 + O5a DAG build → nhces_daily_fx_oil.py, nhces_weekly_materials.py, "
                           "all 9 DAGs + pipeline documentation PDF",
            "concepts": [
                ("Apache Airflow DAG",
                 "Apache Airflow is a platform to programmatically author, schedule, and monitor data "
                 "pipelines. A DAG (Directed Acyclic Graph) is a workflow definition — a set of tasks "
                 "with dependencies that run in a specific order without creating loops.",
                 "NHCES needs to automatically collect data from 15+ sources on different schedules (daily, "
                 "weekly, monthly, quarterly). Airflow manages all of this without manual intervention.",
                 "A running, self-healing data pipeline that populates the Supabase feature store "
                 "automatically, keeping ML models trained on the most current Nigerian data."),
                ("MLOps (Machine Learning Operations)",
                 "MLOps is the practice of deploying, monitoring, and maintaining ML models in production "
                 "reliably and efficiently — combining ML, DevOps, and data engineering principles.",
                 "NHCES must remain accurate as Nigerian economic conditions change. Without MLOps, the "
                 "model would degrade silently. MLOps ensures automatic retraining, drift detection, "
                 "and model versioning.",
                 "A production ML system that automatically retrains weekly, detects when accuracy "
                 "degrades, and promotes better models without human intervention."),
            ]
        },
        {
            "number": 5,
            "title": "Benchmarking Machine Learning Models for Housing Cost Estimation in Nigeria: "
                     "XGBoost, LightGBM, DNN and Stacking Ensembles with SHAP Explainability",
            "journal": "Journal of Construction Engineering and Management",
            "publisher": "ASCE  |  Q1",
            "rank": "Q1  (IF ~4.5)",
            "objective": "O5 — Steps 1, 2 & 3",
            "content": "Full model family comparison: MLR, Ridge, Lasso, RF, GBoost, XGBoost, LightGBM, "
                       "MLP, SVR, Stacking Ensemble. Metrics: MAE, RMSE, MAPE (target <=15%), R2 (>=0.90). "
                       "Optuna hyperparameter tuning. SHAP beeswarm, waterfall, dependence plots.",
            "contribution": "First ML benchmarking study using live Nigerian macroeconomic and material "
                            "price data as features — combining macro volatility with project-level data.",
            "produced_in": "O5 Steps 1-3 → 05_model_benchmarking.py, 05_shap_analysis.py, "
                           "results_comparison_table.csv, 05_SHAP_Interpretation.pdf",
            "concepts": [
                ("SHAP (SHapley Additive exPlanations)",
                 "SHAP is a game-theory-based method for explaining ML model predictions. It assigns "
                 "each input feature a contribution value (positive or negative) for a specific prediction, "
                 "showing exactly why the model produced a given cost estimate.",
                 "QS professionals will only trust and adopt NHCES if they can see why the model produced "
                 "a specific estimate. SHAP provides this transparency — 'cement price contributed +₦2.3M "
                 "to this estimate because it is above the 6-month average'.",
                 "Waterfall charts, beeswarm plots, and feature importance rankings that explain model "
                 "decisions in plain language for QS practitioners."),
                ("Ensemble Model / Stacking",
                 "An ensemble model combines multiple individual models to produce a single prediction "
                 "that is more accurate than any single model alone. Stacking uses a 'meta-learner' "
                 "that learns how to best combine the base models' predictions.",
                 "No single ML algorithm consistently outperforms all others on construction cost data. "
                 "A stacking ensemble (XGBoost + LightGBM + RF → Ridge meta-learner) captures the "
                 "strengths of each approach.",
                 "A champion ensemble model with MAPE <=15% and R2 >=0.90 on Nigerian housing cost data."),
            ]
        },
        {
            "number": 6,
            "title": "Champion-Challenger MLOps Architecture for Continuously-Updating "
                     "Construction Cost Models: Design, Implementation and Drift Detection",
            "journal": "Expert Systems with Applications",
            "publisher": "Elsevier  |  Q1",
            "rank": "Q1  (IF ~8.7)",
            "objective": "O5 — Steps 4 & 5",
            "content": "Airflow DAG schedule (9 DAGs). MLflow experiment tracking and model registry. "
                       "Champion-challenger promotion logic. PSI drift detection. Railway deployment. "
                       "Automated retraining decision framework.",
            "contribution": "First MLOps-grade automated retraining pipeline published for construction "
                            "cost estimation — applicable to any developing economy with volatile input costs.",
            "produced_in": "O5 Steps 4-5 → nhces_retrain_weekly.py, 05_mlflow_config.py, "
                           "05_model_promotion.py, 05_Chapter5_ML_Models_Results.pdf",
            "concepts": [
                ("Champion-Challenger Pattern",
                 "The champion model is the current best-performing model in production. A challenger "
                 "is a newly retrained model. The challenger is evaluated on the same test set as the "
                 "champion — if it performs better (lower MAPE), it is promoted to champion.",
                 "Nigerian construction costs change over time due to macro shocks. The champion-challenger "
                 "pattern ensures NHCES always uses the best available model without human intervention, "
                 "maintaining accuracy as economic conditions evolve.",
                 "An automated weekly evaluation system where the best model is always in production, "
                 "with a complete audit trail of all model versions retained in MLflow."),
                ("Model Drift and PSI",
                 "Model drift occurs when a model's accuracy degrades because the real-world data it "
                 "receives has changed from the data it was trained on. PSI (Population Stability Index) "
                 "measures how much the distribution of input features has shifted — PSI > 0.2 indicates "
                 "significant drift requiring retraining.",
                 "Nigeria experiences significant economic shocks (oil price collapses, currency crises, "
                 "inflation spikes). Without drift detection, NHCES would silently become inaccurate. "
                 "PSI monitoring triggers emergency retraining when needed.",
                 "A daily drift monitor DAG that alerts the team and triggers retraining when the "
                 "model's input data distribution shifts significantly."),
            ]
        },
        {
            "number": 7,
            "title": "iNHCES: Development and Validation of an Intelligent National Housing Cost "
                     "Estimating System for Nigeria Using Ensemble Machine Learning and Real-Time "
                     "Data Pipelines",
            "journal": "Automation in Construction",
            "publisher": "Elsevier  |  Q1  |  IF ~9.6  [FLAGSHIP PAPER]",
            "rank": "Q1  (IF ~9.6)  —  HIGHEST PRIORITY",
            "objective": "O6 — All Steps (Full System Paper)",
            "content": "Complete system: FastAPI backend, 7 web modules, SHAP UI, PDF report generator, "
                       "pipeline dashboard. UAT with NIQS quantity surveyors. Performance benchmarks. "
                       "Deployment on Vercel + Railway + Supabase.",
            "contribution": "The primary TETFund deliverable — a fully operational, validated, publicly "
                            "accessible AI system for national housing cost estimation in Nigeria. First of its kind.",
            "produced_in": "O6 All Steps → nhces-backend/ + nhces-frontend/ + UAT results + "
                           "full system documentation PDF",
            "concepts": [
                ("FastAPI",
                 "FastAPI is a modern, high-performance Python web framework for building APIs. It is "
                 "built on standard Python type hints and generates automatic Swagger documentation. "
                 "It is 3x faster than Flask for API-heavy applications.",
                 "NHCES requires an API layer that can serve ML model predictions in under 3 seconds "
                 "while simultaneously fetching live macro data and generating SHAP explanations. "
                 "FastAPI's async capabilities make this possible.",
                 "A documented REST API with endpoints for cost estimation, report generation, "
                 "project data management, and pipeline monitoring."),
                ("User Acceptance Testing (UAT)",
                 "UAT is the final phase of system testing where actual end-users test the system "
                 "against real-world scenarios to verify it meets their needs before formal acceptance.",
                 "NHCES must be validated by Nigerian QS professionals — not just technically correct, "
                 "but practically useful and trusted. UAT with NIQS members provides this validation "
                 "and generates evidence for the flagship paper.",
                 "A validated system accepted by professional QS users, with documented UAT results "
                 "that form a key section of the Automation in Construction paper."),
            ]
        },
        {
            "number": 8,
            "title": "Leveraging Artificial Intelligence for Housing Affordability: Policy Implications "
                     "of the iNHCES for Nigeria's National Housing Programme",
            "journal": "Habitat International",
            "publisher": "Elsevier  |  Q1",
            "rank": "Q1  (IF ~6.5)",
            "objective": "Post O6  (Policy Analysis Phase)",
            "content": "Policy analysis using NHCES estimate outputs. Affordability modelling by "
                       "geopolitical zone. FHA, FMBN, state housing corporation implications. "
                       "Cost benchmarks for National Housing Programme.",
            "contribution": "Bridges the technical NHCES system to national housing policy — showing "
                            "how AI-generated cost intelligence can directly inform government housing delivery "
                            "programmes in developing economies.",
            "produced_in": "Post O6 UAT — uses real NHCES estimate data by zone + policy analysis "
                           "writing supported by AI literature review",
            "concepts": [
                ("Housing Affordability Index",
                 "A measure comparing housing costs to household income. A property is typically "
                 "considered affordable if it costs no more than 3-4 times annual household income, "
                 "or if mortgage payments represent less than 30% of monthly income.",
                 "NHCES produces cost estimates by geopolitical zone. Combined with NBS household "
                 "income data, these estimates can compute affordability indices for each zone — "
                 "showing where Nigeria's housing crisis is most acute.",
                 "Zone-level affordability maps and policy recommendations for the Federal Housing "
                 "Authority and Federal Mortgage Bank of Nigeria."),
                ("Geopolitical Zone Analysis",
                 "Nigeria is divided into six geopolitical zones: North-West, North-East, North-Central, "
                 "South-West, South-East, and South-South. Construction costs vary significantly "
                 "between zones due to logistics, labour markets, and material prices.",
                 "A national housing system that applies one cost estimate for all of Nigeria would "
                 "be misleading. Zone-level analysis in NHCES ensures estimates reflect the "
                 "actual cost reality in each region, from Kano to Lagos to Port Harcourt.",
                 "State-level cost benchmarks and zone-level sub-models that support geographically "
                 "targeted housing policy decisions."),
            ]
        },
        {
            "number": 9,
            "title": "Responsible AI Integration in Academic Research Workflows: "
                     "A Simulation-to-Publication Framework for Postgraduate Training "
                     "-- Evidence from the iNHCES System Development Project",
            "journal": "Computers & Education / Innovations in Education and Teaching International",
            "publisher": "Elsevier / Taylor & Francis  |  Q1",
            "rank": "Q1  (Computers & Education IF ~12.0)",
            "objective": "Meta: O1-O6 process (documents the simulation framework itself)",
            "content": "The Simulation-to-Publication Framework (S2PF). DATA SOURCE Declaration System "
                       "(GREEN/AMBER/RED). Replacement Obligation. Human Validation Gate. Governing Preamble. "
                       "VS Code + Claude Code + GitHub Copilot setup guide. O1-O5 implementation walkthrough. "
                       "Ethics compliance (COPE, ICMJE, UNESCO). Pedagogical workshop design (5 sessions). "
                       "Appendices: CLAUDE.md template, SESSION_START prompts, full replication guide.",
            "contribution": "First published account of a full-scale, ethics-compliant AI research simulation "
                            "framework for a nationally funded system development project. Replicable, open-source "
                            "methodology for postgraduate AI-assisted research training in Africa and globally.",
            "produced_in": "Draws on all O1-O5 outputs. Draft: "
                           "Draft AI Papers/P9_AI_Research_Simulation_Draft.pdf (27pp, AMBER)",
            "concepts": [
                ("Simulation-to-Publication Framework (S2PF)",
                 "A structured approach to using AI tools in academic research that makes the boundary "
                 "between AI-generated and researcher-generated content explicit and auditable. "
                 "Four components: Governing Preamble, DATA SOURCE Declaration System (GREEN/AMBER/RED), "
                 "Replacement Obligation, and Human Validation Gate.",
                 "Without a framework, AI-assisted research risks silent fabrication (RED synthetic data "
                 "published as real findings) or hidden attribution (AI work presented as human scholarship). "
                 "The S2PF makes both risks visible, managed, and auditable.",
                 "A replicable, open-source research methodology that any postgraduate researcher can "
                 "adopt to use AI tools ethically and effectively in system development research."),
                ("DATA SOURCE Declaration System",
                 "A colour-coded banner (GREEN/AMBER/RED) on every PDF. GREEN = live API or real instrument. "
                 "AMBER = AI-authored template. RED = synthetic data. Each banner includes mandatory "
                 "replacement obligations and citation verification requirements.",
                 "Every iNHCES PDF carries an explicit data provenance declaration, ensuring no synthetic "
                 "data reaches a publication unchanged and every AI draft is identified for validation.",
                 "A transparent, auditable research output trail where each document's data quality "
                 "is visible to the team, supervisors, ethics reviewers, and journal editors."),
            ]
        },
    ]

    for i, paper in enumerate(papers):
        pdf.add_page()
        pdf.section_title(f"Section 3.{paper['number']} — Paper {paper['number']} of 9")

        pdf.paper_card(
            number=paper["number"],
            title=paper["title"],
            journal=paper["journal"],
            publisher=paper["publisher"],
            rank=paper["rank"],
            objective=paper["objective"],
            content_summary=paper["content"],
            key_contribution=paper["contribution"],
            produced_in=paper["produced_in"],
            fill=(i % 2 == 0)
        )

        pdf.sub_heading("Concept Explainers for This Paper")
        for concept in paper["concepts"]:
            pdf.concept_box(*concept)

    # ══════════════════════════════════════════════════════════════════════
    # FINAL PAGE — STEP MAP
    # ══════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("Section 4: Publication-to-Step Mapping")
    pdf.body(
        "The table below maps each paper to the specific research steps and project files that feed into it. "
        "This ensures every deliverable produced during the research directly contributes to a publication."
    )
    pdf.ln(2)

    mwidths = [12, 55, 45, 48, 30]
    mheaders = ["Paper", "Title (Short)", "Target Journal", "Key Steps", "Target Month"]
    pdf.table_row(mheaders, mwidths, fill=True, bold=True)
    mapping = [
        ("P1", "PRISMA SLR on Cost Estimation Methods", "Const. Mgmt & Economics", "O1 Steps 1-3", "Months 3-5"),
        ("P2", "Delphi Requirements Study", "Eng., Const. & Arch. Mgmt", "O1-Step4 + O3", "Months 8-10"),
        ("P3", "Macroeconomic Determinants Study", "Const. Mgmt & Economics", "O2 Steps 2-4", "Months 6-8"),
        ("P4", "Automated Data Pipeline Paper", "Scientific Data", "O2-Step1+O4+O5a", "Months 12-14"),
        ("P5", "ML Benchmarking Paper", "J. Const. Eng. & Mgmt", "O5 Steps 1-3", "Months 15-17"),
        ("P6", "MLOps Architecture Paper", "Expert Sys. with Apps.", "O5 Steps 4-5", "Months 16-18"),
        ("P7", "Full iNHCES System Paper", "Automation in Construction", "O6 All Steps", "Months 21-24"),
        ("P8", "Housing Policy Paper", "Habitat International", "Post O6", "Months 23-26"),
        ("P9", "AI Research Simulation Framework", "Computers & Education / IETI", "Meta: O1-O6", "Months 24-26"),
    ]
    for i, row in enumerate(mapping):
        pdf.table_row(row, mwidths, fill=(i % 2 == 0))

    pdf.ln(8)
    pdf.set_fill_color(*DARK_NAVY)
    pdf.rect(10, pdf.get_y(), 190, 20, 'F')
    pdf.set_xy(10, pdf.get_y() + 4)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*WHITE)
    pdf.cell(0, 6,
             sanitize("Total: 9 Publications  |  7 Q1 Journals Targeted  |  "
             "Target combined IF > 59  |  18-26 Month Timeline  |  P9 = AI Research Simulation Framework"),
             align="C", ln=True)
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(200, 215, 235)
    pdf.cell(0, 6,
             sanitize("ABU Zaria / TETFund NRF 2025  |  Department of Quantity Surveying  |  iNHCES Project"),
             align="C")

    pdf.output(OUTPUT_PATH)
    print(f"PDF generated successfully: {OUTPUT_PATH}")


if __name__ == "__main__":
    build_pdf()
