"""
P2 — Draft Paper: Delphi-Based Requirements Engineering for an AI Construction Cost
     Estimating System: Expert Consensus on Feature, Model, and Interface Requirements

Target Journal: Engineering, Construction and Architectural Management (ECAM)
               Emerald Publishing | Scopus/SSCI Q1 (Construction Management)

DATA SOURCE: AMBER/RED
  - Delphi instrument design: REAL (AMBER)
  - Expert ratings n=20: SYNTHETIC (RED) — numpy seed=42
  - Do NOT submit this paper with synthetic data

iNHCES TETFund NRF 2025 | Dept. of Quantity Surveying, ABU Zaria
"""

import sys, os, csv, textwrap
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import tempfile

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
_O3   = os.path.join(_ROOT, '03_requirements')
_DEL  = os.path.join(_O3, 'delphi')

sys.path.insert(0, os.path.join(_ROOT, '01_literature_review'))
from generate_o1_pdfs import (
    DocPDF, sanitize, _ds_page,
    DARK_NAVY, GOLD, LIGHT_BLUE, WHITE, DARK_GREY, MID_GREY,
    PAGE_W, LEFT, LINE_H,
)

OUT = os.path.join(_HERE, 'P2_Delphi_Requirements_Draft.pdf')

# ── Load Delphi results CSV ────────────────────────────────────────────────────
def load_delphi_results():
    csv_path = os.path.join(_DEL, 'delphi_results.csv')
    rows = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['r2_mean']    = float(row['r2_mean'])
            row['r2_sd']      = float(row['r2_sd'])
            row['r2_cv']      = float(row['r2_cv'])
            row['r2_iqr']     = float(row['r2_iqr'])
            row['r2_consensus'] = row['r2_consensus'] == 'True'
            row['r3_mean']    = float(row['r3_mean']) if row['r3_mean'] else None
            row['r3_sd']      = float(row['r3_sd'])   if row['r3_sd']   else None
            row['r3_cv']      = float(row['r3_cv'])   if row['r3_cv']   else None
            row['r3_consensus'] = row['r3_consensus'] == 'True' if row['r3_consensus'] else None
            rows.append(row)
    return rows


# ── Paper PDF class ────────────────────────────────────────────────────────────
class PaperPDF(DocPDF):
    def __init__(self):
        super().__init__("P2 - Delphi Requirements Draft", "DRAFT")

    def header(self):
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*MID_GREY)
        self.set_xy(LEFT, 4)
        self.cell(PAGE_W/2, 4.5,
            sanitize("P2 DRAFT -- Delphi Requirements | ECAM Target | iNHCES TETFund NRF 2025"))
        self.set_x(LEFT + PAGE_W/2)
        self.cell(PAGE_W/2, 4.5, sanitize("SYNTHETIC DATA -- NOT FOR SUBMISSION"), align="R")
        self.set_draw_color(*GOLD)
        self.set_line_width(0.3)
        self.line(LEFT, 10, LEFT + PAGE_W, 10)
        self.set_text_color(*DARK_GREY)
        self.ln(14)

    def footer(self):
        self.set_draw_color(*GOLD)
        self.set_line_width(0.3)
        self.line(LEFT, self.get_y()-3, LEFT + PAGE_W, self.get_y()-3)
        self.set_y(-12)
        self.set_font("Helvetica", "", 7.5)
        self.set_text_color(*MID_GREY)
        self.cell(0, 5, f"Page {self.page_no()}", align="C")
        self.set_text_color(*DARK_GREY)

    def title_block(self, title, authors, affil, journal, wordcount, keywords):
        self.add_page()
        self.set_fill_color(*DARK_NAVY)
        self.rect(0, 0, 210, 52, 'F')
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(*GOLD)
        self.set_xy(LEFT, 13)
        self.multi_cell(PAGE_W, 7, sanitize(title), align="C")
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*LIGHT_BLUE)
        self.set_x(LEFT)
        self.multi_cell(PAGE_W, 5, sanitize(authors), align="C")
        self.set_font("Helvetica", "I", 8)
        self.set_x(LEFT)
        self.multi_cell(PAGE_W, 4.5, sanitize(affil), align="C")
        self.set_text_color(*DARK_GREY)
        self.ln(12)

        self.set_x(LEFT)
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*DARK_NAVY)
        self.cell(35, 5, "Target Journal:")
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*DARK_GREY)
        self.cell(PAGE_W - 35, 5, sanitize(journal))
        self.ln(5)
        self.set_x(LEFT)
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*DARK_NAVY)
        self.cell(35, 5, "Word Count:")
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*DARK_GREY)
        self.cell(PAGE_W - 35, 5, sanitize(wordcount))
        self.ln(5)
        self.set_x(LEFT)
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*DARK_NAVY)
        self.cell(35, 5, "Keywords:")
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*DARK_GREY)
        self.multi_cell(PAGE_W - 35, 5, sanitize(keywords))
        self.ln(2)

    def h1(self, text):
        self.ln(3)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*DARK_NAVY)
        self.set_x(LEFT)
        self.multi_cell(PAGE_W, 5.5, sanitize(text))
        self.set_draw_color(*GOLD)
        self.set_line_width(0.5)
        self.line(LEFT, self.get_y(), LEFT + PAGE_W, self.get_y())
        self.set_text_color(*DARK_GREY)
        self.ln(2)

    def h2(self, text):
        self.ln(2)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*DARK_NAVY)
        self.set_x(LEFT)
        self.multi_cell(PAGE_W, 5, sanitize(text))
        self.set_text_color(*DARK_GREY)
        self.ln(1)

    def h3(self, text):
        self.ln(1)
        self.set_font("Helvetica", "BI", 9.5)
        self.set_text_color(*DARK_NAVY)
        self.set_x(LEFT)
        self.multi_cell(PAGE_W, 5, sanitize(text))
        self.set_text_color(*DARK_GREY)
        self.ln(0.5)

    def para(self, text, indent=0):
        self.set_font("Helvetica", "", 9.5)
        self.set_text_color(*DARK_GREY)
        self.set_x(LEFT + indent)
        self.multi_cell(PAGE_W - indent, 5.2, sanitize(text))
        self.ln(1.5)

    def abstract_box(self, text):
        self.set_fill_color(*LIGHT_BLUE)
        self.set_draw_color(*DARK_NAVY)
        self.set_line_width(0.4)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*DARK_GREY)
        self.set_x(LEFT)
        self.multi_cell(PAGE_W, 5, sanitize(text), border=1, fill=True)
        self.ln(2)

    def cite(self, text):
        """Inline citation marker in brackets"""
        return f"[{text}]"

    def add_chart(self, fig, w=None):
        tmp = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        tmp.close()
        fig.savefig(tmp.name, dpi=150, bbox_inches='tight')
        plt.close(fig)
        self.set_x(LEFT)
        self.image(tmp.name, x=LEFT, y=None, w=w or PAGE_W)
        os.unlink(tmp.name)
        self.ln(2)

    def caption(self, text):
        self.set_font("Helvetica", "I", 8.5)
        self.set_text_color(*MID_GREY)
        self.set_x(LEFT)
        self.multi_cell(PAGE_W, 4.5, sanitize(text))
        self.set_text_color(*DARK_GREY)
        self.ln(2)

    def note_box(self, text):
        self.set_fill_color(255, 245, 210)
        self.set_draw_color(180, 120, 0)
        self.set_line_width(0.3)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(100, 60, 0)
        self.set_x(LEFT)
        self.multi_cell(PAGE_W, 4.8, sanitize(text), border=1, fill=True)
        self.set_text_color(*DARK_GREY)
        self.ln(1.5)


# ══════════════════════════════════════════════════════════════════════════════
# GENERATE PAPER
# ══════════════════════════════════════════════════════════════════════════════
def generate_p2():
    data = load_delphi_results()
    consensus_items = [r for r in data if r['final_status'] != 'excluded']
    excluded_items  = [r for r in data if r['final_status'] == 'excluded']

    pdf = PaperPDF()

    # ── Cover / Title Block ─────────────────────────────────────────────────
    pdf.title_block(
        title=(
            "Delphi-Based Requirements Engineering for an AI-Powered Housing Construction "
            "Cost Estimating System: Expert Consensus on Feature Selection, Model Performance, "
            "and Interface Requirements for the Nigerian Built Environment"
        ),
        authors=(
            "[Author 1 Name, Author 2 Name, Author 3 Name — ANONYMISED FOR PEER REVIEW]"
        ),
        affil=(
            "Department of Quantity Surveying, Faculty of Environmental Design, "
            "Ahmadu Bello University, Zaria, Kaduna State, Nigeria"
        ),
        journal=(
            "Engineering, Construction and Architectural Management (ECAM) — "
            "Emerald Publishing | ISSN: 0969-9988 | Scopus/SSCI Q1"
        ),
        wordcount="~8,500 words (target; this draft: indicative structure)",
        keywords=(
            "Delphi method; requirements engineering; construction cost estimation; "
            "machine learning; intelligent systems; Nigeria; quantity surveying; "
            "housing; expert consensus; software requirements"
        ),
    )

    _ds_page(pdf, 'red',
        "DATA SOURCE: RED — All Delphi expert ratings (n=20) used in this paper are SYNTHETIC "
        "(numpy normal distribution, seed=42). This paper is a DRAFT TEMPLATE ONLY. "
        "DO NOT SUBMIT TO JOURNAL WITH SYNTHETIC DATA.",
        (
            "This paper draft was generated as part of the iNHCES research simulation framework "
            "(see 00_Research_Simulation_Introduction.pdf). All content marked [VERIFY], "
            "[ADD CITATION], or similar requires real literature review and referencing.\n\n"
            "WHAT REQUIRES REPLACEMENT BEFORE SUBMISSION:\n"
            "  1. All Delphi statistics (means, SDs, CVs, consensus classifications)\n"
            "     -> Re-run 03_requirements/generate_o3_pdfs.py after real survey data is collected\n"
            "  2. All citations marked [VERIFY] or [ADD CITATION]\n"
            "     -> Conduct real literature search using PRISMA protocol (O1 outputs)\n"
            "  3. Author names, ORCID IDs, corresponding author details\n"
            "  4. Ethics approval number (institutional IRB)\n"
            "  5. Data availability statement (real survey data will be archived)\n"
            "  6. Acknowledgements (TETFund grant number, expert panel acknowledgement)\n\n"
            "TARGET JOURNAL NOTE:\n"
            "ECAM word limit: 8,000-10,000 words (excludes references, tables, figures).\n"
            "Submission requirements: structured abstract (purpose, design, findings, "
            "practical implications, originality); max 6 keywords; APA referencing.\n"
            "Declare use of AI tools in methods section per Emerald AI policy."
        )
    )

    # ── Abstract ────────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.h1("Abstract")
    pdf.note_box(
        "DRAFT ABSTRACT — Replace all statistics and findings with real survey results. "
        "ECAM structured abstract format: Purpose | Design/methodology | Findings | "
        "Practical implications | Originality/value. Max 250 words."
    )
    pdf.abstract_box(
        "PURPOSE: This study establishes expert consensus on the functional requirements, "
        "feature selection priorities, and performance standards for an AI-powered housing "
        "construction cost estimating system (iNHCES) tailored to the Nigerian built environment. "
        "The research addresses the absence of a validated, context-specific requirements "
        "specification for intelligent construction cost estimation in sub-Saharan Africa.\n\n"
        "DESIGN/METHODOLOGY/APPROACH: A modified three-round Delphi study was conducted with a "
        "purposively selected panel of [n=XX REAL] expert practitioners drawn from quantity "
        "surveying, housing development, public sector procurement, and academic research "
        "backgrounds. A 38-item structured instrument covering seven requirement categories "
        "(macroeconomic features, project characteristics, ML model performance, system "
        "performance, interface, data quality, and reporting) was administered. Consensus was "
        "defined as a group mean >= 5.0 (on a 1-7 Likert scale) and coefficient of variation "
        "<= 20%.\n\n"
        "FINDINGS [SYNTHETIC]: Consensus was achieved on [XX/38] requirements items across all "
        "seven categories. The NGN/USD exchange rate, CPI inflation rate, and project gross "
        "floor area received the highest consensus mean ratings ([>6.0/7.0]). Experts required "
        "SHAP-based explainability for all estimates, a maximum MAPE of 15%, and prediction "
        "interval reporting as high-priority ML model requirements. Four items — including "
        "mobile usability and sensitivity analysis reporting — failed to reach consensus and "
        "are treated as aspirational features pending future research.\n\n"
        "PRACTICAL IMPLICATIONS: The validated requirements specification provides a replicable "
        "evidence base for AI-powered cost estimating systems in emerging economies. The findings "
        "directly inform the iNHCES software requirements specification (SRS) and ML model "
        "development pipeline.\n\n"
        "ORIGINALITY/VALUE: This is the first Delphi study to systematically establish expert "
        "consensus on requirements for an AI construction cost estimating system in the Nigerian "
        "built environment, filling a gap identified in the O1 PRISMA systematic review."
    )

    # ── 1. Introduction ──────────────────────────────────────────────────────
    pdf.add_page()
    pdf.h1("1. Introduction")
    pdf.para(
        "Construction cost estimation is a critical early-stage activity in project management, "
        "enabling developers, public sector clients, and quantity surveyors to assess project "
        "viability and allocate budgets before detailed design is complete (Ferry et al., 2019 "
        "[VERIFY]). In Nigeria, the accuracy of preliminary cost estimates is fundamentally "
        "compromised by macroeconomic volatility: the NGN/USD exchange rate has depreciated "
        "by over 70% since 2020, CPI inflation in the construction sector has exceeded 25% "
        "per annum in 2022-2024, and material costs — heavily import-dependent — fluctuate "
        "with global crude oil price movements (CBN, 2024 [VERIFY]). These dynamics create "
        "a context in which static cost data books and manual estimation methods are "
        "systematically unreliable (Aibinu & Jagboro, 2002 [VERIFY])."
    )
    pdf.para(
        "Artificial intelligence (AI) and machine learning (ML) offer promising pathways to "
        "dynamic, data-driven construction cost estimation. A growing body of international "
        "literature demonstrates that ensemble ML models — particularly gradient boosting "
        "algorithms such as XGBoost and LightGBM — can achieve prediction accuracy (MAPE) "
        "of 10-15% on historical project data, outperforming traditional regression and "
        "parametric methods (Dogan & Arditi, 2020 [VERIFY]; Kim et al., 2004 [VERIFY]). "
        "However, the majority of published AI cost estimation models are trained on "
        "datasets from developed economies (USA, UK, South Korea, China) and fail to "
        "incorporate Nigeria-specific macroeconomic drivers (Eke et al., 2022 [VERIFY]; "
        "iNHCES O1 PRISMA SLR, 2025)."
    )
    pdf.para(
        "The development of any AI system that will be used in professional practice requires "
        "a structured requirements engineering process to ensure that the system meets the "
        "actual operational needs of its intended users (Sommerville, 2016 [VERIFY]). In the "
        "construction informatics literature, the Delphi method — a structured iterative "
        "expert elicitation technique — has been widely used to establish consensus on "
        "complex, multi-dimensional research questions where established standards are absent "
        "(Hasson et al., 2000 [VERIFY]; Hallowell & Gambatese, 2010 [VERIFY]). Despite this, "
        "no Delphi study has systematically elicited requirements for an AI-powered "
        "construction cost estimating system in any African context."
    )
    pdf.para(
        "This paper addresses that gap. The Intelligent National Housing Cost Estimating "
        "System (iNHCES) is a TETFund NRF 2025-funded research programme at the Department "
        "of Quantity Surveying, Ahmadu Bello University (ABU) Zaria. This study presents the "
        "results of a three-round modified Delphi expert consensus process establishing "
        "agreed requirements for the iNHCES system across seven dimensions: macroeconomic "
        "feature selection, project characteristic inputs, ML model performance standards, "
        "system performance, interface design, data quality governance, and cost reporting format."
    )

    pdf.h2("1.1 Research Objectives")
    objectives = [
        "To identify the macroeconomic and project-level features that Nigerian built environment "
        "practitioners consider most important for inclusion in an AI construction cost estimating model.",
        "To establish expert consensus on acceptable ML model performance standards (accuracy, "
        "explainability, uncertainty quantification) for AI-based cost estimation.",
        "To determine the minimum functional and non-functional requirements for an AI cost "
        "estimation web system that practitioners would trust and adopt.",
        "To identify areas of expert disagreement requiring further research before system "
        "requirements can be finalised.",
    ]
    for i, obj in enumerate(objectives, 1):
        pdf.set_x(LEFT + 4)
        pdf.set_font("Helvetica", "", 9.5)
        pdf.set_text_color(*DARK_GREY)
        pdf.multi_cell(PAGE_W - 4, 5.2, sanitize(f"RO{i}. {obj}"))
        pdf.ln(1)
    pdf.ln(2)

    pdf.h2("1.2 Contribution")
    pdf.para(
        "This paper makes three original contributions to the construction informatics literature: "
        "(1) it produces the first published expert consensus on requirements for AI-powered "
        "cost estimation in the Nigerian built environment; (2) it validates the convergence "
        "between data-driven SHAP feature importance (O2 analysis, [CITE iNHCES O2 working paper]) "
        "and expert professional judgment through a triangulated multi-method approach; and "
        "(3) it produces an IEEE 830-compliant Software Requirements Specification (SRS) that "
        "directly links Delphi consensus to system design, providing a replicable framework for "
        "requirements engineering of AI construction tools in emerging economy contexts."
    )

    # ── 2. Literature Review ─────────────────────────────────────────────────
    pdf.add_page()
    pdf.h1("2. Literature Review")
    pdf.h2("2.1 AI in Construction Cost Estimation: State of the Art")
    pdf.para(
        "The application of AI and ML to preliminary construction cost estimation has grown "
        "substantially since Boussabaine & Elhag (1999) [VERIFY] first applied neural networks "
        "to building cost data. Recent systematic reviews (Eke et al., 2022 [VERIFY]; "
        "Pham et al., 2023 [VERIFY]) document a consistent pattern: ensemble methods "
        "(Random Forest, XGBoost, Gradient Boosting) outperform individual algorithms on "
        "heterogeneous construction datasets, achieving MAPE of 8-18% depending on data "
        "quality and feature set. Key features identified across studies include: "
        "gross floor area, number of storeys, structural type, project type, and location — "
        "findings broadly consistent with the Delphi consensus reported in this study."
    )
    pdf.para(
        "A critical limitation of existing models is their reliance on static historical "
        "datasets without dynamic macroeconomic feature integration. Wilmot & Cheng (2003) "
        "[VERIFY] demonstrated that incorporating economic indicators (CPI, GDP) improved "
        "cost prediction accuracy by 12-18% in South African road construction. "
        "Ali et al. (2021) [VERIFY] showed that exchange rate volatility significantly "
        "moderates construction cost escalation in import-dependent economies. These findings "
        "support the iNHCES design decision to integrate live macroeconomic APIs, "
        "a requirement that received strong expert consensus in this study "
        "(NGN/USD: Mean=[SYNTHETIC 6.4], GDP growth: Mean=[SYNTHETIC 5.3])."
    )
    pdf.para(
        "Model explainability has emerged as a critical adoption barrier for AI cost tools. "
        "Mathews et al. (2019) [VERIFY] found that QS practitioners distrusted 'black box' "
        "ML outputs without interpretable justification. The integration of SHapley Additive "
        "exPlanations (SHAP; Lundberg & Lee, 2017 [VERIFY]) into construction cost models "
        "has been demonstrated to significantly improve practitioner acceptance "
        "(Petruseva et al., 2017 [VERIFY]; [ADD SHAP+CONSTRUCTION CITATION]). "
        "The high consensus rating for SHAP explainability (FR-05, Mean=[SYNTHETIC 5.7]) "
        "in this study corroborates this finding for the Nigerian context."
    )
    pdf.h2("2.2 Delphi Method in Construction Research")
    pdf.para(
        "The Delphi method, developed at the RAND Corporation (Dalkey & Helmer, 1963 [VERIFY]), "
        "is a structured iterative expert elicitation technique particularly suited to complex "
        "problems where no established empirical standards exist and where practitioner judgment "
        "is essential (Linstone & Turoff, 1975 [VERIFY]). In construction management research, "
        "Delphi has been applied to: risk assessment criteria (Tah & Carr, 2000 [VERIFY]), "
        "critical success factors for IT adoption (Eadie et al., 2013 [VERIFY]), "
        "sustainability rating criteria (Alyami & Rezgui, 2012 [VERIFY]), and "
        "BIM implementation requirements (Hosseini et al., 2016 [VERIFY]). "
        "Hallowell & Gambatese (2010) [VERIFY] provide the most cited guidance for Delphi "
        "design in construction research, recommending a minimum panel size of 15-20 experts, "
        "a consensus threshold defined as mean >= 4.0 on a 5-point scale (or equivalent), "
        "and a maximum of three rounds."
    )
    pdf.para(
        "Panel composition is critical to Delphi validity. The deliberate inclusion of "
        "practitioners from diverse sub-sectors — rather than relying solely on academic "
        "experts — is particularly important for requirements engineering, where operational "
        "context determines system adoption (Hasson et al., 2000 [VERIFY]). This study "
        "recruited experts from six practitioner categories (Table 1), reflecting the "
        "multi-stakeholder reality of the Nigerian housing cost estimation ecosystem."
    )
    pdf.h2("2.3 Requirements Engineering for AI Construction Systems")
    pdf.para(
        "Software Requirements Engineering (SRE) for AI systems presents unique challenges "
        "compared to traditional software: ML model behaviour is emergent and data-dependent, "
        "performance targets must be defined in terms of statistical metrics rather than "
        "deterministic correctness, and explainability requirements are not captured in "
        "standard functional specification frameworks such as IEEE 830 "
        "(Sommerville, 2016 [VERIFY]; Habibullah & Weyns, 2023 [VERIFY]). "
        "The combination of Delphi expert consensus with IEEE 830 SRS documentation — "
        "as employed in this study — provides a practical bridge between practitioner "
        "requirements and formal system specification, an approach recently advocated by "
        "Zeng et al. (2022) [VERIFY] for construction AI systems."
    )
    pdf.para(
        "In the Nigerian context, requirements engineering for construction IT systems "
        "must additionally account for: infrastructure constraints (variable internet "
        "connectivity), professional capacity (variable digital literacy), regulatory "
        "context (BPP procurement framework, NIQS practice standards), and "
        "data availability constraints (limited digital project cost records). "
        "This study is the first to explicitly address these context-specific factors "
        "through a requirements consensus process."
    )

    # ── 3. Methodology ───────────────────────────────────────────────────────
    pdf.add_page()
    pdf.h1("3. Methodology")
    pdf.h2("3.1 Research Design")
    pdf.para(
        "A modified three-round Delphi design was adopted. The 'modified' Delphi variant "
        "(Okoli & Pawlowski, 2004 [VERIFY]) differs from the classical Delphi in that Round 1 "
        "provides an a priori structured item set derived from a systematic literature review "
        "(O1 outputs) and SHAP variable analysis (O2 outputs), supplemented by open-ended "
        "questions to capture Nigeria-specific factors not identified in the literature. "
        "This design was selected over a standard expert survey because: (1) the research "
        "question requires iterative convergence rather than a single-point measurement; "
        "(2) anonymity preserves the independence of expert judgment; and (3) the controlled "
        "feedback mechanism in Rounds 2-3 enables genuine consensus formation rather than "
        "majority opinion (Hasson et al., 2000 [VERIFY])."
    )
    pdf.h2("3.2 Expert Panel Composition and Recruitment")
    pdf.para(
        "Panel composition followed the purposive sampling criteria of Hallowell & Gambatese "
        "(2010) [VERIFY]. A minimum of 15 responses per round was targeted for adequate "
        "statistical analysis; [n=XX REAL] experts completed all three rounds (Round 1 "
        "response rate: [XX]%; Round 2: [XX]%; Round 3: [XX]%). [UPDATE WITH REAL DATA]"
    )

    # Panel table
    pw = [52, 10, PAGE_W-62]
    pdf.thead(["Expert Category", "n", "Selection Criteria"], pw)
    panel = [
        ("Registered QS (MNIQS/FNIQS, >= 5 years post-qual.)", "6",
         "Cost planning practice; building/housing sector"),
        ("Housing Developers (REDAN registered; >= 3 projects)", "3",
         "Active residential developer; min NGN 500m project value"),
        ("Public Sector Clients (FHA / State Housing Corp.)", "3",
         "Federal/state housing authority PM or QS staff"),
        ("BPP/Procurement Officers (Federal MDA)", "2",
         "GL >= 14; cost benchmarking responsibilities"),
        ("Construction Contractors (CORBON registered)", "3",
         "Active building contractor, QS or commercial manager"),
        ("Academic Researchers (PhD; >= 2 CM/QS publications)", "3",
         "Nigerian university QS/CM lecturer, quantitative background"),
    ]
    for i, p in enumerate(panel):
        pdf.trow(list(p), pw, fill=(i % 2 == 1))
    pdf.ln(2)
    pdf.caption(
        "Table 1: Delphi panel composition (n=20 target; actual n=[XX] REAL). "
        "Recruitment via NIQS chapter contacts, REDAN secretariat, and university QS departments. "
        "Experts based in Abuja (FCT), Lagos, Kano, Kaduna, and Port Harcourt."
    )
    pdf.note_box("SYNTHETIC STUDY NOTE: Panel sizes and response rates above are PLACEHOLDERS. "
                 "Replace with real panel data before submission.")

    pdf.h2("3.3 Instrument Development")
    pdf.para(
        "The Round 1 open-ended questionnaire comprised 28 questions across seven thematic "
        "sections. Round 1 responses were analysed using NVivo thematic analysis "
        "(Braun & Clarke, 2006 [VERIFY]) to generate the 38-item Round 2 structured instrument. "
        "Items were classified into seven categories corresponding to the iNHCES system "
        "design dimensions: macroeconomic features (A, n=7), project characteristics (B, n=8), "
        "ML model requirements (C, n=6), system performance (D, n=5), interface (E, n=6), "
        "data quality (F, n=4), and reporting (G, n=4). Items were rated on a 7-point Likert "
        "scale (1 = Strongly Disagree/Completely Unimportant; 7 = Strongly Agree/Absolutely "
        "Essential) following the recommendation of Joshi et al. (2015) [VERIFY] for "
        "requirements elicitation studies."
    )
    pdf.h2("3.4 Consensus Criterion")
    pdf.para(
        "Consensus was defined as: group mean >= 5.0 (out of 7) AND coefficient of "
        "variation (CV) <= 20%. This dual criterion is more stringent than the single-metric "
        "thresholds used in many Delphi studies (e.g., mean >= 4.0/5.0; IQR <= 1.0) and "
        "was selected to ensure both central tendency (importance) and agreement (homogeneity) "
        "before a requirement is accepted into the specification. This approach follows "
        "Grime & Wright (2016) [VERIFY] who recommend a CV-based criterion for "
        "Likert-scale Delphi studies to avoid conflating high importance with high disagreement."
    )
    pdf.h2("3.5 Ethical Considerations")
    pdf.para(
        "The study received ethical approval from [INSTITUTION ETHICS COMMITTEE REF: XX/XXXX]. "
        "All participants provided written informed consent. Anonymity was maintained "
        "throughout all rounds; individual responses are not identifiable in any reported "
        "data. Data are stored on encrypted institutional servers in compliance with the "
        "Nigeria Data Protection Regulation (NDPR, 2019). Use of AI assistance in instrument "
        "design was disclosed to participants in the participant information sheet."
    )
    pdf.note_box("DRAFT NOTE: Ethics committee reference number must be obtained and inserted before submission.")

    # ── 4. Results ───────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.h1("4. Results")
    pdf.note_box(
        "ALL RESULTS ARE BASED ON SYNTHETIC DATA (numpy seed=42, n=20 simulated). "
        "Replace all means, SDs, CVs, and consensus classifications with real survey results."
    )

    n_total = len(data)
    n_consensus = len(consensus_items)
    n_excl = len(excluded_items)

    pdf.h2("4.1 Overview of Consensus Achievement")
    pdf.para(
        f"After three rounds of the Delphi process, consensus was achieved on "
        f"{n_consensus} of {n_total} items ({100*n_consensus/n_total:.1f}%). "
        f"{n_excl} item(s) failed to reach consensus after Round 3 and are excluded from "
        f"the final requirements specification (Table 2). Round 2 achieved consensus on "
        f"{sum(1 for r in data if r['r2_consensus'])} items directly; "
        f"{sum(1 for r in data if r['final_status'] == 'consensus_r3')} additional items "
        f"reached consensus in Round 3 following controlled feedback."
    )

    # Overview table
    ow = [12, 42, 12, 12, 12, 14, PAGE_W-104]
    pdf.thead(["Cat.", "Category Name", "Items", "R2 Cons.", "R3 Cons.", "Excl.", "Key Finding"], ow)
    cats = ["A","B","C","D","E","F","G"]
    cat_names = {
        "A": "Macroeconomic Features",
        "B": "Project Characteristics",
        "C": "ML Model Requirements",
        "D": "System Performance",
        "E": "Interface Requirements",
        "F": "Data Quality",
        "G": "Reporting",
    }
    key_findings = {
        "A": "NGN/USD & CPI top-ranked; GDP & lending rate lower",
        "B": "Floor area, location, structural type highest priority",
        "C": "SHAP explainability & MAPE<=15% high consensus",
        "D": "All 5 items: consensus. <3s response time required",
        "E": "Web browser access essential; mobile aspirational",
        "F": "All 4 items: full consensus. Data freshness critical",
        "G": "NIQS format & PDF quality required; sensitivity debated",
    }
    for i, cat in enumerate(cats):
        cat_data = [r for r in data if r['category'] == cat]
        r2c = sum(1 for r in cat_data if r['r2_consensus'])
        r3c = sum(1 for r in cat_data if r['final_status'] == 'consensus_r3')
        exl = sum(1 for r in cat_data if r['final_status'] == 'excluded')
        pdf.trow([cat, cat_names[cat], str(len(cat_data)), str(r2c),
                  str(r3c), str(exl), key_findings[cat]], ow, fill=(i % 2 == 1))
    pdf.ln(2)
    pdf.caption(
        "Table 2: Consensus overview by category (SYNTHETIC DATA). "
        "R2 Cons. = consensus achieved in Round 2. R3 Cons. = achieved after Round 3. "
        "Excl. = failed consensus after Round 3."
    )

    # ── Mean ratings chart ─────────────────────────────────────────────────
    pdf.add_page()
    pdf.h2("4.2 Item-Level Results: Mean Ratings and Consensus Classification")

    # Chart: mean ratings with consensus threshold
    fig, ax = plt.subplots(figsize=(11, 8))
    colors = {'consensus_r2': '#1a3a6b', 'consensus_r3': '#2e7d32', 'excluded': '#c0392b'}
    color_labels = {'consensus_r2': 'Consensus R2', 'consensus_r3': 'Consensus R3 (revised)', 'excluded': 'No consensus'}
    for status in ['excluded', 'consensus_r3', 'consensus_r2']:
        items = [r for r in data if r['final_status'] == status]
        ax.barh([r['item_id'] for r in items],
                [r['r2_mean'] for r in items],
                color=colors[status], label=color_labels[status], height=0.7)
    ax.axvline(5.0, color='black', linestyle='--', linewidth=1.5, label='Consensus threshold (5.0)')
    ax.set_xlabel('Mean Rating (1-7 scale)', fontsize=10)
    ax.set_title(f'Delphi Round 2 Mean Ratings — All {n_total} Items\n[SYNTHETIC DATA — n=20 simulated experts, seed=42]',
                 fontsize=10)
    ax.legend(fontsize=8)
    ax.tick_params(axis='y', labelsize=8)
    ax.set_xlim(0, 7.5)
    ax.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    pdf.add_chart(fig, w=PAGE_W)
    pdf.caption(
        "Figure 1: Item mean ratings across all 38 Delphi items (Round 2, SYNTHETIC DATA). "
        "Dark blue = consensus achieved in Round 2; Green = consensus in Round 3; "
        "Red = no consensus after Round 3. Dashed line = consensus threshold (mean=5.0/7.0)."
    )

    pdf.h2("4.3 Top-Priority Requirements by Category")

    # Category A: Macro features
    pdf.h3("Category A: Macroeconomic Feature Requirements (n=7 items, n=[X] consensus)")
    cat_a = sorted([r for r in data if r['category'] == 'A'], key=lambda x: -x['r2_mean'])
    aw = [10, 80, 14, 14, 14, PAGE_W-132]
    pdf.thead(["ID", "Requirement", "Mean", "SD", "CV%", "Consensus"], aw)
    for i, r in enumerate(cat_a):
        c = "YES" if r['final_status'] != 'excluded' else "NO"
        pdf.trow([r['item_id'], r['short_text'][:60], f"{r['r2_mean']:.2f}",
                  f"{r['r2_sd']:.2f}", f"{r['r2_cv']:.1f}", c], aw, fill=(i%2==1))
    pdf.ln(1)
    pdf.para(
        "NGN/USD exchange rate (A1, Mean=[SYN: 6.4]) and CPI inflation (A2, Mean=[SYN: 6.2]) "
        "received the highest consensus ratings, consistent with the SHAP importance analysis "
        "(O2) identifying these variables as the first and second most important predictors "
        "(relative importance: 44.97% and 25.50% respectively). This convergence between "
        "statistical SHAP analysis and expert judgment provides strong dual-method support "
        "for the iNHCES macroeconomic feature set. The commercial lending rate (A5, "
        "Mean=[SYN: 4.8]) was the only macroeconomic feature approaching the consensus "
        "threshold boundary, reflecting expert uncertainty about the direct relevance of "
        "interest rates to construction costs (as distinct from project financing costs)."
    )

    pdf.add_page()
    pdf.h3("Category B: Project Characteristic Features (n=8 items, n=[X] consensus)")
    cat_b = sorted([r for r in data if r['category'] == 'B'], key=lambda x: -x['r2_mean'])
    pdf.thead(["ID", "Requirement", "Mean", "SD", "CV%", "Consensus"], aw)
    for i, r in enumerate(cat_b):
        c = "YES" if r['final_status'] != 'excluded' else "NO"
        pdf.trow([r['item_id'], r['short_text'][:60], f"{r['r2_mean']:.2f}",
                  f"{r['r2_sd']:.2f}", f"{r['r2_cv']:.1f}", c], aw, fill=(i%2==1))
    pdf.ln(1)
    pdf.para(
        "Gross floor area (B1, Mean=[SYN: 6.7]) was the highest-rated feature across all "
        "38 items, reflecting its fundamental role as a primary cost driver in all "
        "parametric estimation methods. Project location (B4, Mean=[SYN: 6.5]) and project "
        "type (B5, Mean=[SYN: 6.4]) also achieved very high ratings, underscoring the "
        "importance of geopolitical zone as a proxy for regional cost variation in Nigeria "
        "(a pattern confirmed by the SHAP analysis in O2). Procurement method (B6) was the "
        "only Category B item excluded — experts were divided on whether procurement route "
        "affects cost levels (as distinct from tender competitiveness), consistent with "
        "contradictory findings in the international literature (Ling & Liu, 2004 [VERIFY])."
    )

    pdf.h3("Category C: ML Model Requirements (n=6 items, n=[X] consensus)")
    cat_c = sorted([r for r in data if r['category'] == 'C'], key=lambda x: -x['r2_mean'])
    pdf.thead(["ID", "Requirement", "Mean", "SD", "CV%", "Consensus"], aw)
    for i, r in enumerate(cat_c):
        c = "YES" if r['final_status'] != 'excluded' else "NO"
        pdf.trow([r['item_id'], r['short_text'][:60], f"{r['r2_mean']:.2f}",
                  f"{r['r2_sd']:.2f}", f"{r['r2_cv']:.1f}", c], aw, fill=(i%2==1))
    pdf.ln(1)
    pdf.para(
        "MAPE <= 15% (C1, Mean=[SYN: 6.0]) and SHAP explainability (C2, Mean=[SYN: 5.7]) "
        "were the top-ranked ML requirements, both achieving clear consensus. The 15% MAPE "
        "threshold is consistent with international benchmarks for preliminary AI-based "
        "construction cost estimation (Dogan & Arditi, 2020 [VERIFY]). The high consensus "
        "for SHAP explainability (C2) corroborates Mathews et al. (2019) [VERIFY] on the "
        "importance of explainability for professional adoption of AI estimation tools. "
        "Stacking ensemble as champion (C6) was excluded, with experts preferring to specify "
        "a performance-based selection criterion rather than mandate a specific architecture."
    )

    pdf.add_page()
    pdf.h3("Categories D-G: Performance, Interface, Data Quality, Reporting")
    cat_dg = sorted([r for r in data if r['category'] in 'DEFG'], key=lambda x: (x['category'], -x['r2_mean']))
    dw = [10, 8, 68, 14, 14, PAGE_W-114]
    pdf.thead(["Cat.", "ID", "Requirement", "Mean", "CV%", "Consensus"], dw)
    for i, r in enumerate(cat_dg):
        c = "YES" if r['final_status'] != 'excluded' else "NO"
        pdf.trow([r['category'], r['item_id'], r['short_text'][:55],
                  f"{r['r2_mean']:.2f}", f"{r['r2_cv']:.1f}", c], dw, fill=(i%2==1))
    pdf.ln(1)
    pdf.caption(
        "Table 3: Category D-G results (SYNTHETIC DATA). All performance (D), data quality (F), "
        "and most interface (E) and reporting (G) items achieved consensus. "
        "Mobile usability (E5) and sensitivity analysis (G2) failed consensus."
    )
    pdf.para(
        "All five system performance items (D1-D5) achieved consensus, establishing clear "
        "quantitative targets: < 3 second estimate generation (D1), >= 50 concurrent users "
        "(D2), >= 99.5% uptime (D3). All four data quality items (F1-F4) achieved consensus, "
        "indicating strong expert alignment on the critical importance of DATA SOURCE "
        "classification and data freshness indicators — a context-specific requirement "
        "reflecting Nigeria's variable data infrastructure. Mobile usability (E5) failed "
        "consensus (Mean=[SYN: 4.8], CV=[SYN: high]), with experts divided on whether "
        "mobile-first design was necessary for professional QS use cases (as distinct "
        "from client-facing access)."
    )

    # ── Non-consensus table ─────────────────────────────────────────────────
    pdf.add_page()
    pdf.h2("4.4 Non-Consensus Items: Analysis and Implications")
    pdf.para(
        f"Four items failed to reach consensus after Round 3 (Table 4). These are classified as "
        f"'aspirational requirements' — features that may be included in future system versions "
        f"pending additional evidence or user testing, but are not included in the v1.0 SRS."
    )
    nw = [10, 62, 14, 14, 14, PAGE_W-114]
    pdf.thead(["ID", "Requirement", "R2 Mean", "R3 Mean", "Final CV%", "Interpretation"], nw)
    for r in excluded_items:
        r3m = f"{r['r3_mean']:.2f}" if r['r3_mean'] else "N/A"
        r3cv = f"{r['r3_cv']:.1f}" if r['r3_cv'] else "N/A"
        interp = {
            "B6": "Context-dependent; procurement route not universally cost-determining",
            "C6": "Experts prefer performance-based selection over mandating architecture",
            "E5": "Mobile QS use cases not universal; future version consideration",
            "G2": "Sensitivity analysis valued by some experts; not universal need",
        }.get(r['item_id'], "Insufficient consensus — aspirational feature")
        pdf.trow([r['item_id'], r['short_text'][:50], f"{r['r2_mean']:.2f}",
                  r3m, r3cv, interp], nw, fill=True)
    pdf.ln(2)
    pdf.caption(
        "Table 4: Non-consensus items after Round 3 (SYNTHETIC DATA). "
        "These items are excluded from v1.0 SRS but flagged for future research."
    )

    # ── 5. Discussion ─────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.h1("5. Discussion")
    pdf.h2("5.1 Convergence of Delphi and SHAP Methods")
    pdf.para(
        "A notable finding of this study is the strong convergence between Delphi expert "
        "consensus (this paper) and SHAP-based statistical importance (O2 [CITE iNHCES "
        "working paper]). The top three macroeconomic features by Delphi consensus mean — "
        "NGN/USD (A1), CPI inflation (A2), and Brent crude (A3) — correspond precisely to "
        "the top three features by SHAP relative importance (44.97%, 25.50%, 10.85% "
        "respectively). This triangulation across two independent methodological approaches "
        "provides unusually strong support for the iNHCES macroeconomic feature set, "
        "addressing a key limitation of prior AI construction cost models that rely "
        "exclusively on statistical feature selection without expert validation."
    )
    pdf.para(
        "The only notable divergence was for GDP growth rate (A4): SHAP placed it "
        "7th by importance (2.59%) while Delphi rated it modestly high (Mean=[SYN: 5.3]). "
        "This discrepancy may reflect the multicollinearity between GDP growth and "
        "exchange rate in the Nigerian context (both partly driven by oil revenue cycles), "
        "which SHAP's additive attribution framework distributes across correlated features. "
        "Practitioners, however, may intuit GDP growth as a broader economic health indicator "
        "worth including regardless of marginal statistical contribution."
    )
    pdf.h2("5.2 Explainability as a Non-Negotiable Requirement")
    pdf.para(
        "The high consensus rating for SHAP explainability (C2, Mean=[SYN: 5.7]) stands "
        "out as a practically significant finding. Professional QS practice in Nigeria "
        "requires defensible, auditable cost estimates — practitioners cannot present "
        "clients or approval bodies with a figure they cannot explain. This study provides "
        "the first quantitative evidence that Nigerian QS practitioners would reject an "
        "AI cost tool without explanation capabilities, a finding with direct implications "
        "for the design of all construction AI systems in the African built environment."
    )
    pdf.para(
        "The practical implication is clear: explainability is not an optional 'nice-to-have' "
        "feature but a professional necessity. System designers who prioritise model accuracy "
        "over explainability — a common pattern in ML literature — risk building tools that "
        "practitioners will not adopt. The iNHCES design response (SHAP waterfall plots for "
        "every estimate, integrated into the PDF report) directly reflects this consensus finding."
    )
    pdf.h2("5.3 DATA SOURCE Governance as a Nigerian Context-Specific Requirement")
    pdf.para(
        "The full consensus on all four data quality requirements (F1-F4), particularly "
        "the DATA SOURCE confidence classification (F2, Mean=[SYN: 6.0]) and macro data "
        "freshness flags (F1, F15), reflects the specific institutional context of "
        "Nigerian construction practice. Unlike high-income economies with reliable, "
        "frequently updated official statistics, Nigeria's macroeconomic data environment "
        "is characterised by: NBS data releases with 6-12 month lags; CBN FX data that "
        "diverges from parallel market rates; and EIA oil price data that may not reflect "
        "ex-refinery prices in Nigeria. Expert consensus on making data confidence "
        "explicitly visible to users — rather than opaque — represents a context-specific "
        "requirement unlikely to appear in requirements studies from data-rich economies."
    )
    pdf.h2("5.4 Excluded Items: Mobile and Sensitivity Analysis")
    pdf.para(
        "The exclusion of mobile usability (E5) and sensitivity analysis (G2) from the "
        "v1.0 requirements specification deserves interpretation. The mobile usability "
        "result is consistent with the primary user profile: registered NIQS members "
        "conducting professional cost estimates are likely to use desktop/laptop workstations "
        "in office settings, not mobile phones. The expert panel appears to distinguish "
        "between QS professionals (desktop users) and a potential future client-facing "
        "interface (mobile-appropriate), suggesting a two-tier system architecture for "
        "future development."
    )
    pdf.para(
        "The sensitivity analysis result is more nuanced. Several experts who rated G2 "
        "highly noted (in Round 3 open-ended comments) that sensitivity analysis under "
        "FX scenarios is highly valued for feasibility studies but less relevant for "
        "standard project cost plans. This suggests sensitivity analysis should be "
        "available as an optional module rather than a core feature — a design decision "
        "incorporated in the iNHCES SRS as FR-11 (optional, medium priority)."
    )

    # ── 6. Conclusion ─────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.h1("6. Conclusion")
    pdf.para(
        "This study has produced the first validated, expert consensus-based requirements "
        "specification for an AI-powered housing construction cost estimating system in the "
        "Nigerian built environment. A three-round modified Delphi process with [n=XX REAL] "
        "expert practitioners established consensus on [XX/38 REAL] requirements across seven "
        "system dimensions, yielding a rigorous evidence base for the iNHCES Software "
        "Requirements Specification (IEEE 830)."
    )
    pdf.para(
        "Three key contributions emerge from this research: (1) The dual-method convergence "
        "of SHAP statistical importance and Delphi expert consensus on the macroeconomic "
        "feature set provides unusually robust justification for the iNHCES feature "
        "selection, directly addressing the feature engineering challenge identified in "
        "the O1 systematic literature review. (2) The unanimous expert consensus on SHAP "
        "explainability as a non-negotiable requirement establishes a new precedent for "
        "AI construction tool design in the African context: explainability must be "
        "treated as a functional requirement, not a post-hoc addition. (3) The full "
        "consensus on DATA SOURCE confidence classification represents a Nigeria-specific "
        "innovation in AI system design — a transparent data quality governance framework "
        "embedded in the user interface — that addresses the macro data reliability "
        "challenges unique to the Nigerian institutional context."
    )
    pdf.para(
        "This study is limited by its use of a purposive sample from a single research "
        "programme ecosystem; future research should replicate the requirements consensus "
        "process with independently recruited panels in other African construction markets. "
        "The synthetic data used in this draft must be replaced with real expert survey "
        "data before the findings can be considered substantive."
    )
    pdf.para(
        "The validated requirements specification directly informs the next phase of the "
        "iNHCES programme: O4 (historical project data collection) and O5 (ML model "
        "development), ensuring that all system design decisions from this point forward "
        "are grounded in expert-validated, evidence-based requirements."
    )

    # ── 7. References ──────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.h1("7. References (DRAFT — All Citations Must Be Verified)")
    pdf.note_box(
        "ALL REFERENCES BELOW ARE PLACEHOLDER TEMPLATES. They must be verified against "
        "real publications, correctly formatted in APA style, and all [VERIFY] tags removed. "
        "Do not include unchecked references in the submitted manuscript."
    )
    refs = [
        "Aibinu, A.A. & Jagboro, G.O. (2002). The effects of construction delays on project "
        "delivery in Nigerian construction industry. International Journal of Project Management, "
        "20(8), 593-599. [VERIFY DOI]",
        "Ali, Z., Zhu, F., Hussain, S., & Shirani, H. (2021). Construction cost "
        "escalation and exchange rate: evidence from Pakistan. Construction Economics and "
        "Building, 21(2), 1-18. [VERIFY — CONFIRM EXACT PAPER]",
        "Alyami, S.H. & Rezgui, Y. (2012). Sustainable building assessment tool development "
        "approach. Sustainable Cities and Society, 5, 52-62. [VERIFY DOI]",
        "Boussabaine, A.H. & Elhag, T. (1999). Applying fuzzy techniques to cash flow analysis. "
        "Construction Management and Economics, 17(6), 745-755. [VERIFY DOI]",
        "Braun, V. & Clarke, V. (2006). Using thematic analysis in psychology. "
        "Qualitative Research in Psychology, 3(2), 77-101. [VERIFY DOI]",
        "CBN (2024). Central Bank of Nigeria: Statistical Bulletin. Abuja: CBN. "
        "[VERIFY EDITION AND DATE]",
        "Dalkey, N. & Helmer, O. (1963). An experimental application of the Delphi method to "
        "the use of experts. Management Science, 9(3), 458-467. [VERIFY DOI]",
        "Dogan, S.Z. & Arditi, D. (2020). Expert systems and neural networks in cost "
        "estimation for early design. Journal of Construction Engineering and Management, "
        "146(7). [VERIFY — CONFIRM THIS IS THE RIGHT PAPER]",
        "Eadie, R. et al. (2013). BIM implementation throughout the UK construction "
        "project lifecycle: An analysis. Automation in Construction, 36, 145-151. [VERIFY]",
        "Eke, C.I. et al. (2022). Machine learning for construction cost prediction: "
        "A systematic review. Journal of Engineering, Design and Technology. [VERIFY — CONFIRM THIS EXISTS]",
        "Ferry, D.J., Brandon, P.S. & Ferry, J.D. (2019). Cost Planning of Buildings (9th ed.). "
        "Oxford: Blackwell. [VERIFY EDITION]",
        "Grime, M.M. & Wright, G. (2016). Delphi method. In Wiley StatsRef: Statistics "
        "Reference Online. [VERIFY]",
        "Habibullah, M.S. & Weyns, D. (2023). Requirements engineering for AI systems. "
        "IEEE Software. [VERIFY — CONFIRM EXISTENCE]",
        "Hallowell, M.R. & Gambatese, J.A. (2010). Qualitative research: Application of the "
        "Delphi method to CEM research. Journal of Construction Engineering and Management, "
        "136(1), 99-107. [VERIFY DOI]",
        "Hasson, F., Keeney, S. & McKenna, H. (2000). Research guidelines for the Delphi "
        "survey technique. Journal of Advanced Nursing, 32(4), 1008-1015. [VERIFY DOI]",
        "Hosseini, M.R. et al. (2016). BIM adoption within Australian Small and Medium-sized "
        "Enterprises (SMEs): An innovation diffusion model. Construction Economics and "
        "Building, 16(3), 71-86. [VERIFY]",
        "Joshi, A. et al. (2015). Likert scale: Explored and explained. British Journal of "
        "Applied Science & Technology, 7(4), 396-403. [VERIFY]",
        "Kim, G.H., An, S.H. & Kang, K.I. (2004). Comparison of construction cost estimating "
        "models based on regression analysis, neural networks, and case-based reasoning. "
        "Building and Environment, 39(10), 1235-1242. [VERIFY DOI]",
        "Ling, F.Y.Y. & Liu, M. (2004). Using neural network to predict performance of "
        "design-build projects in Singapore. Building and Environment, 39(10), 1263-1274. [VERIFY]",
        "Linstone, H.A. & Turoff, M. (Eds.) (1975). The Delphi Method: Techniques and "
        "Applications. Reading, MA: Addison-Wesley. [VERIFY PUBLISHER]",
        "Lundberg, S.M. & Lee, S.I. (2017). A unified approach to interpreting model "
        "predictions. Advances in Neural Information Processing Systems, 30. [VERIFY]",
        "Mathews, M. et al. (2019). Machine learning for cost estimation in construction: "
        "a practitioner perspective. [VERIFY — CONFIRM THIS EXISTS OR REMOVE]",
        "Okoli, C. & Pawlowski, S.D. (2004). The Delphi method as a research tool: An "
        "example, design considerations and applications. Information and Management, "
        "42(1), 15-29. [VERIFY DOI]",
        "Petruseva, S. et al. (2017). Construction costs prediction with machine learning. "
        "Slovak Journal of Civil Engineering, 25(3), 13-19. [VERIFY]",
        "Pham, T.D. et al. (2023). A comprehensive review of machine learning for construction "
        "cost estimation. [ADD REAL CITATION]",
        "Sommerville, I. (2016). Software Engineering (10th ed.). Boston: Pearson. [VERIFY EDITION]",
        "Tah, J.H.M. & Carr, V. (2000). A proposal for construction project risk assessment "
        "using fuzzy fault trees. Construction Management and Economics, 18(4), 491-500. [VERIFY]",
        "Wilmot, C.G. & Cheng, G. (2003). Estimating future highway construction costs. "
        "Journal of Construction Engineering and Management, 129(3), 272-279. [VERIFY DOI]",
        "Zeng, W. et al. (2022). Requirements engineering for AI-based systems: current "
        "state and challenges. [VERIFY — CONFIRM THIS EXISTS]",
    ]
    for i, ref in enumerate(refs, 1):
        pdf.set_x(LEFT)
        pdf.set_font("Helvetica", "", 8.5)
        pdf.set_text_color(*DARK_GREY)
        pdf.multi_cell(PAGE_W, 4.8, sanitize(f"{i}. {ref}"))
        pdf.ln(0.5)

    # ── Appendices ─────────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.h1("Appendix A: Delphi Round 2 Instrument Items (Full Text)")
    pdf.note_box("See O3_03_Delphi_Round2_Instrument.pdf for the full administered instrument.")

    aw2 = [10, PAGE_W-10]
    pdf.thead(["ID", "Full Statement (1-7 Likert scale)"], aw2)
    for i, r in enumerate(data):
        pdf.trow([r['item_id'], r['full_text'][:120]], aw2, fill=(i%2==1))
    pdf.ln(2)

    pdf.add_page()
    pdf.h1("Appendix B: Complete Round 2 Statistics (All 38 Items)")
    bw = [10, 58, 12, 12, 12, 12, 10, 15, PAGE_W-141]
    pdf.thead(["ID","Requirement","n","Mean","SD","CV%","IQR","Cons.","Category"], bw)
    for i, r in enumerate(data):
        c = "YES" if r['r2_consensus'] else "NO"
        pdf.trow([
            r['item_id'], r['short_text'][:45], str(20),
            f"{r['r2_mean']:.2f}", f"{r['r2_sd']:.2f}",
            f"{r['r2_cv']:.1f}", f"{r['r2_iqr']:.1f}",
            c, r['category_name'][:20]
        ], bw, fill=(i%2==1))
    pdf.ln(2)
    pdf.caption(
        "Appendix B: Full Round 2 statistics for all 38 items (SYNTHETIC DATA, n=20 simulated). "
        "Replace with real survey data before submission."
    )

    # Save
    pdf.output(OUT)
    print(f"[OK]  P2_Delphi_Requirements_Draft.pdf -> {OUT}")
    return OUT


if __name__ == "__main__":
    print("=== iNHCES P2 — Delphi Requirements Paper Draft ===")
    out = generate_p2()
    print(f"\nOutput: {out}")
    print("NOTE: All statistics are SYNTHETIC. Replace with real Delphi survey data before submission.")
