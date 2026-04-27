"""
iNHCES Research Simulation Introduction Document
Generates: 00_Research_Simulation_Introduction.pdf
TETFund NRF 2025 | Department of Quantity Surveying, ABU Zaria

PURPOSE:
    This script generates the official preamble document for the entire iNHCES
    research project.  It explains that the development pipeline is a SIMULATION
    using AI assistance (Claude / GitHub Copilot) to scaffold a real research
    programme -- and sets out the ethics and integrity obligations that govern
    every subsequent deliverable.
"""

from fpdf import FPDF
from datetime import date
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, _HERE)

from generate_o1_pdfs import (
    DocPDF, sanitize, _ds_page,
    DARK_NAVY, GOLD, LIGHT_BLUE, WHITE, DARK_GREY, MID_GREY,
    PAGE_W, LEFT, LINE_H,
)

OUTPUT_DIR = os.path.join(_ROOT, "Research_Documents")

# ── Custom cover colour for this preamble document ────────────────────────────
DEEP_GREEN  = (10,  70,  40)
PALE_GREEN  = (230, 248, 235)
WARN_AMBER  = (255, 235, 185)
WARN_BORDER = (180, 100,  0)


# ─────────────────────────────────────────────────────────────────────────────
class IntroPDF(DocPDF):
    """Custom header for the introduction / preamble document."""
    def header(self):
        self.set_fill_color(*DEEP_GREEN)
        self.rect(0, 0, 210, 14, 'F')
        self.set_font("Helvetica", "B", 7)
        self.set_text_color(*WHITE)
        self.set_xy(5, 4)
        self.cell(PAGE_W, 6, sanitize(
            "iNHCES | TETFund NRF 2025 | ABU Zaria  |  "
            "S2RF Governing Preamble -- Simulation to Research Framework (S2RF)"
        ))
        self.set_text_color(*DARK_GREY)
        self.ln(16)

    def highlight_box(self, text, color=None, border_color=None):
        """Full-width highlight box with custom colour."""
        if color is None:
            color = PALE_GREEN
        if border_color is None:
            border_color = DEEP_GREEN
        self.ln(2)
        self.set_fill_color(*color)
        self.set_draw_color(*border_color)
        self.set_line_width(0.5)
        self.set_x(LEFT)
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(*DARK_GREY)
        self.multi_cell(PAGE_W, 5.2, sanitize(text), border=1, fill=True)
        self.set_text_color(*DARK_GREY)
        self.ln(2)

    def warn_box(self, text):
        """Amber warning / important notice box."""
        self.highlight_box(text, color=WARN_AMBER, border_color=WARN_BORDER)

    def numbered_item(self, number, title, body):
        """Numbered list item with bold title and indented body."""
        self.ln(1)
        self.set_x(LEFT + 2)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*DARK_NAVY)
        self.cell(8, 6, sanitize(f"{number}."), ln=False)
        self.set_font("Helvetica", "B", 9)
        self.multi_cell(PAGE_W - 10, 6, sanitize(title), ln=True)
        self.set_x(LEFT + 10)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*DARK_GREY)
        self.multi_cell(PAGE_W - 10, 5.2, sanitize(body))
        self.ln(1)

    def principle_row(self, label, detail, fill=False):
        """Two-column principle row."""
        w1, w2 = 55, PAGE_W - 55
        self.set_fill_color(*(LIGHT_BLUE if fill else WHITE))
        self.set_x(LEFT)
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*DARK_NAVY)
        y0 = self.get_y()
        # Draw label cell
        self.set_xy(LEFT, y0)
        self.multi_cell(w1, LINE_H, sanitize(f" {label}"), border=1, fill=True)
        y1 = self.get_y()
        # Draw body cell
        self.set_xy(LEFT + w1, y0)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*DARK_GREY)
        self.multi_cell(w2, LINE_H, sanitize(f" {detail}"), border=1, fill=True)
        y2 = self.get_y()
        self.set_y(max(y1, y2))


# ─────────────────────────────────────────────────────────────────────────────
def generate_intro():
    out_path = os.path.join(OUTPUT_DIR, "00_S2RF_Governing_Preamble_iNHCES.pdf")
    pdf = IntroPDF("00_S2RF_Governing_Preamble_iNHCES.pdf",
                   "Simulation to Research Framework (S2RF) -- Governing Preamble")

    # =========================================================================
    # COVER PAGE
    # =========================================================================
    pdf.add_page()
    pdf.set_fill_color(*DEEP_GREEN)
    pdf.rect(0, 18, 210, 62, 'F')
    pdf.set_xy(0, 24)
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(*WHITE)
    pdf.cell(210, 8,  "Simulation to Research Framework (S2RF)", align="C", ln=True)
    pdf.cell(210, 8,  "for AI-Assisted Academic Research -- An iNHCES Case Study", align="C", ln=True)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(195, 230, 210)
    pdf.cell(210, 7,  "Governing Preamble, Ethics & Process Documentation", align="C", ln=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(195, 220, 205)
    pdf.cell(210, 6,  "Intelligent National Housing Cost Estimating System (iNHCES)", align="C", ln=True)
    pdf.cell(210, 6,  "TETFund NRF 2025  |  Department of Quantity Surveying, ABU Zaria", align="C", ln=True)
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(*GOLD)
    pdf.cell(210, 5,  "S2R Architect:  Dr. Bello Abdullahi", align="C", ln=True)
    pdf.set_draw_color(*GOLD)
    pdf.set_line_width(0.8)
    pdf.line(30, 87, 180, 87)

    pdf.set_xy(LEFT, 93)
    for label, val in [
        ("Document:",      "00_S2RF_Governing_Preamble_iNHCES.pdf"),
        ("Type:",          "Governing Preamble / Policy & Ethics Framework"),
        ("Scope:",         "Entire iNHCES Research Development Pipeline (O1 - O6)"),
        ("AI Tool:",       "Claude (Anthropic) via GitHub Copilot -- Microsoft VS Code"),
        ("Grant:",         "TETFund National Research Fund (NRF) 2025"),
        ("S2R Architect:", "Dr. Bello Abdullahi"),
    ]:
        pdf.set_x(LEFT)
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*DARK_NAVY)
        pdf.cell(44, 6.5, sanitize(label))
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*DARK_GREY)
        pdf.cell(PAGE_W - 44, 6.5, sanitize(val), ln=True)
    # Researchers multi-line entry
    pdf.set_x(LEFT)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*DARK_NAVY)
    pdf.cell(44, 5.5, sanitize("Researchers:"), ln=False)
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(*DARK_GREY)
    pdf.multi_cell(PAGE_W - 44, 5.0, sanitize(
        "Hassan Adaviriku Ahmadu (Reader, Dept. of QS, ABU Zaria) -- Principal Researcher  |  "
        "Prof. Yahaya Makarfi Ibrahim (Professor of QS, ABU Zaria)  |  "
        "Prof. Joy Joshua Maina (Professor of Architecture, ABU Zaria)  |  "
        "Dr. Bello Abdullahi (PhD, BAE Consulting Engineers, Abuja)  |  "
        "Muhammad Aliyu Yamusa (Lecturer II, Dept. of QS, ABU Zaria)"
    ))
    # Version and Date after Researchers
    for label, val in [
        ("Version:", "1.0"),
        ("Date:",    date.today().strftime("%d %B %Y")),
    ]:
        pdf.set_x(LEFT)
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*DARK_NAVY)
        pdf.cell(44, 6.5, sanitize(label))
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*DARK_GREY)
        pdf.cell(PAGE_W - 44, 6.5, sanitize(val), ln=True)

    # =========================================================================
    # DATA SOURCE DECLARATION
    # =========================================================================
    _ds_page(pdf, 'green',
        "DATA SOURCE: AI-AUTHORED POLICY & ETHICS DOCUMENT -- "
        "Based on Established Academic Integrity Principles",
        (
            "This document was authored by an AI assistant (Claude / GitHub Copilot) under the "
            "direction and intellectual oversight of the research team at the Department of Quantity "
            "Surveying, Ahmadu Bello University (ABU) Zaria, as part of the iNHCES TETFund NRF 2025 "
            "research project.\n\n"
            "WHAT THIS DOCUMENT IS:\n"
            "  * A policy and ethics framework document -- not a data-bearing research output.\n"
            "  * A transparent declaration of the AI-simulation methodology used throughout iNHCES.\n"
            "  * A statement of researcher obligations and academic integrity commitments.\n"
            "  * Structured with reference to: COPE (Committee on Publication Ethics) guidelines, "
            "IEEE/ACM AI ethics statements, ICMJE authorship criteria, NRF (South Africa) AI use "
            "policy 2024, and UNESCO Recommendation on the Ethics of AI (2021).\n\n"
            "WHAT CONTAINS NO FABRICATED DATA:\n"
            "  * All institutional statements, ethics principles, and guidelines cited in this "
            "document refer to real, publicly available policy frameworks. Where specific policy "
            "documents are cited, the researcher should verify the current version applies at the "
            "time of submission.\n\n"
            "INTELLECTUAL OWNERSHIP:\n"
            "  * The framing, selection of principles, and application to iNHCES context reflect "
            "decisions made by the research team. The AI tool provided draft language that the team "
            "reviewed, approved, and adopted as their stated policy. The research team bears full "
            "responsibility for the content of this document."
        )
    )

    # =========================================================================
    # SECTION 1: INTRODUCTION
    # =========================================================================
    pdf.add_page()
    pdf.section_title("1.  Introduction")
    pdf.body(
        "The Intelligent National Housing Cost Estimating System (iNHCES) is a funded research "
        "initiative under the TETFund National Research Fund (NRF) 2025 cycle, anchored at the "
        "Department of Quantity Surveying, Ahmadu Bello University (ABU) Zaria, Nigeria. The "
        "project aims to develop a web-based, machine-learning-driven system that produces reliable, "
        "real-time construction cost estimates for housing projects across Nigeria -- integrating "
        "macroeconomic indicators, regional material prices, and historical project data into a "
        "unified predictive model."
    )
    pdf.body(
        "The development of iNHCES spans six research objectives (O1 through O6), encompassing a "
        "systematic literature review, macroeconomic data analysis, requirements engineering, "
        "conceptual database modelling, machine learning model development, and full-stack software "
        "implementation. Each objective generates multiple research artefacts: PDFs, datasets, "
        "trained models, and deployed services."
    )
    pdf.body(
        "This preamble document serves a singular and important purpose: to formally document, "
        "at the outset of the research pipeline, that the development work described across all "
        "six objectives is conducted as a RESEARCH SIMULATION assisted by artificial intelligence "
        "tools -- specifically, Claude (Anthropic) accessed via GitHub Copilot within Microsoft "
        "VS Code. This document explains what that means, what it does not mean, and how the "
        "research team will uphold the highest standards of academic integrity throughout."
    )

    pdf.sub_heading("1.1  Purpose of This Document")
    pdf.body(
        "This document serves five purposes:"
    )
    pdf.bullet([
        "To provide a transparent, written declaration of the AI-simulation methodology "
        "before any research outputs are generated or submitted.",
        "To clearly distinguish between outputs that are AI-generated simulations (placeholders "
        "to be replaced by real data) and outputs that constitute genuine research contributions.",
        "To establish the ethical framework and data-source declaration system (GREEN / AMBER / "
        "RED banners) that applies to every PDF, dataset, and model produced by iNHCES.",
        "To articulate the obligations of the research team in validating, replacing, and "
        "ultimately taking intellectual ownership of every simulated output.",
        "To serve as a reference document for ethics board reviews, grant reporting, and "
        "publication disclosures related to AI use in this research programme.",
    ])

    pdf.sub_heading("1.2  How to Read This Document")
    pdf.body(
        "This document should be read in full by every member of the iNHCES research team before "
        "engaging with any other artefact in the pipeline. It establishes the ground rules for "
        "the entire project. Section 2 defines iNHCES and the six objectives. Section 3 explains "
        "the simulation framework. Sections 4 and 5 distinguish what the AI is and is not doing. "
        "Section 6 provides the ethics and academic integrity framework. Section 7 describes the "
        "pipeline from simulation to real research. Section 8 states the obligations of the team. "
        "Section 9 provides guidelines for citing AI assistance."
    )

    # =========================================================================
    # SECTION 2: WHAT IS iNHCES
    # =========================================================================
    pdf.add_page()
    pdf.section_title("2.  What is iNHCES?")
    pdf.body(
        "The Intelligent National Housing Cost Estimating System is a proposed software platform "
        "designed to address a critical gap in Nigeria's construction and housing sector: the "
        "absence of a data-driven, real-time, nationally calibrated cost estimation tool that "
        "accounts for Nigeria's unique macroeconomic volatility, regional material price "
        "disparities, and rapidly changing labour market conditions."
    )

    pdf.sub_heading("2.1  Research Objectives")
    pdf.body("The iNHCES programme is structured around six core research objectives:")

    for num, obj, desc in [
        ("O1", "Systematic Literature Review",
         "A PRISMA 2020 compliant review of AI and ML applications in construction cost "
         "estimation, identifying methodological gaps and establishing the theoretical "
         "foundations for the iNHCES model family."),
        ("O2", "Macroeconomic Variable Analysis",
         "Collection, stationarity testing, VAR/VECM cointegration analysis, and SHAP-based "
         "feature selection of seven macro variables: GDP growth, CPI inflation, lending rate, "
         "Brent crude oil price, NGN/USD, NGN/EUR, and NGN/GBP exchange rates."),
        ("O3", "Requirements Engineering",
         "Delphi survey of QS professionals and software requirements specification (SRS) "
         "defining the functional and non-functional requirements of the iNHCES platform."),
        ("O4", "Conceptual Data Modelling",
         "Entity-relationship and schema design for the Supabase PostgreSQL database, "
         "including row-level security policies, seed data, and system architecture diagrams."),
        ("O5", "Machine Learning Model Development",
         "Feature engineering, multi-algorithm benchmarking (Ridge, RF, XGBoost, LightGBM, "
         "MLP, SVR, Stacking Ensemble), SHAP explainability, MLflow model registry, and "
         "automated retraining pipeline via Apache Airflow."),
        ("O6", "System Implementation and Deployment",
         "Full-stack implementation: FastAPI backend (Railway), vanilla HTML/CSS/JS frontend "
         "(Vercel), Supabase PostgreSQL, Cloudflare R2 storage, and CI/CD pipeline."),
    ]:
        pdf.numbered_item(num, obj, desc)

    pdf.sub_heading("2.2  Target Outputs")
    pdf.body(
        "Each objective produces peer-reviewed publications targeting Q1/Q2 international "
        "journals, conference papers, and practical artefacts (the iNHCES platform itself, "
        "trained models, and open datasets). The ultimate goal is a deployed, functional "
        "system available to Nigerian quantity surveyors, developers, and government agencies -- "
        "and a body of publications that advance the academic field of AI-assisted construction "
        "cost estimation in developing economies."
    )

    # =========================================================================
    # SECTION 3: THE SIMULATION FRAMEWORK
    # =========================================================================
    pdf.add_page()
    pdf.section_title("3.  The AI-Assisted Research Simulation Framework")

    pdf.body(
        "The development of a research project of the scale and complexity of iNHCES -- six "
        "interlinked objectives, multiple data collection pipelines, machine learning model "
        "development, and full-stack software engineering -- represents an enormous undertaking "
        "for a university research group. Prior to committing substantial fieldwork resources, "
        "survey time, and computational infrastructure, the research team has adopted a "
        "structured SIMULATION PHASE using AI assistance."
    )

    pdf.sub_heading("3.1  What 'Simulation' Means in This Context")
    pdf.body(
        "In this project, 'simulation' refers to the use of an AI language model (Claude, "
        "accessed via GitHub Copilot) to generate first-pass, structured drafts of every "
        "research artefact that will eventually need to be produced in full by the research "
        "team. The simulation phase produces:"
    )
    pdf.bullet([
        "Structured PDF documents (protocols, analysis plans, survey instruments, literature "
        "review drafts) that represent what the finished document SHOULD look like -- but "
        "populated with AI-authored content and, where necessary, synthetic/hypothetical data.",
        "Python scripts that implement the statistical analyses and ML pipelines -- complete, "
        "runnable code that the team can inspect, validate, and refine.",
        "Database schemas, API route definitions, and system architecture diagrams.",
        "Macroeconomic data collection scripts that, where live API keys are available, "
        "return REAL data; and where they are not, return clearly labelled synthetic fallbacks.",
    ])

    pdf.sub_heading("3.2  Why Simulate First?")
    pdf.highlight_box(
        "Simulation allows the research team to see the complete picture of what they are "
        "building BEFORE investing in data collection, fieldwork, and infrastructure. It "
        "reveals methodological gaps, sequence dependencies, and technical challenges early -- "
        "when they are cheap to fix. Every simulated artefact is a hypothesis to be tested "
        "against real-world data and expert validation."
    )
    pdf.body(
        "Specific benefits of the simulation-first approach for iNHCES include:"
    )
    pdf.bullet([
        "METHODOLOGY VALIDATION: The PRISMA protocol, SPSS analysis plan, and ML benchmarking "
        "framework can be reviewed and refined by the team's supervisors before any fieldwork "
        "begins, ensuring no costly methodological errors are discovered after data collection.",
        "CODE INFRASTRUCTURE: The Python data collection scripts, ML pipeline, and API backend "
        "can be tested and debugged against synthetic data, so that when real data arrives the "
        "pipeline is already verified and ready.",
        "GRANT REPORTING: The simulation outputs allow the research team to demonstrate to "
        "TETFund that the project is progressing systematically, with structured artefacts at "
        "each stage, even while field data collection is underway.",
        "TEAM CAPACITY BUILDING: Junior researchers and postgraduate students can study, "
        "critique, and learn from the simulated outputs -- understanding what each artefact "
        "should contain before being responsible for producing the real version.",
        "RISK REDUCTION: Potential failure points (API availability, data quality, model "
        "convergence) are identified in the simulation phase and mitigation plans put in place.",
    ])

    pdf.sub_heading("3.3  The DATA SOURCE Declaration System")
    pdf.body(
        "Every PDF document generated by the iNHCES pipeline includes a dedicated DATA SOURCE "
        "DECLARATION page immediately after the cover. This page uses a colour-coded banner "
        "system to make the nature of the content unmistakably clear to any reader:"
    )

    iw = [25, 40, PAGE_W - 65]
    pdf.thead(["Colour", "Category", "Meaning"], iw)
    rows = [
        ("GREEN", "LIVE / REAL",
         "Data was retrieved from a real, live API or official database at the time the script "
         "ran. No AI substitution. Cite the original source."),
        ("AMBER", "AI-GENERATED",
         "Content is AI-authored template, framework, or illustrative material. No field data "
         "collected yet. Researcher must validate, populate, and own before publication."),
        ("RED",   "SYNTHETIC / SIMULATED",
         "All numeric values are generated by a seeded NumPy random process or hardcoded "
         "estimates. MUST be replaced with real collected data before any publication."),
    ]
    fills = [False, True, False]
    for (col, cat, meaning), fill in zip(rows, fills):
        if col == "GREEN":
            pdf.colored_row([col, cat, meaning], iw,
                            bg_color=(210, 240, 215), text_color=DARK_GREY, bold_col=0)
        elif col == "AMBER":
            pdf.colored_row([col, cat, meaning], iw,
                            bg_color=(255, 235, 185), text_color=DARK_GREY, bold_col=0)
        else:
            pdf.colored_row([col, cat, meaning], iw,
                            bg_color=(248, 210, 210), text_color=DARK_GREY, bold_col=0)

    pdf.ln(3)
    pdf.body(
        "At time of writing, the following documents carry LIVE (GREEN) data: all three O2 "
        "Step 1 macroeconomic data reports (World Bank, EIA/FRED Brent crude, CBN/FRED "
        "exchange rates -- subject to API key availability). All O1 documents carry GREEN "
        "(real methodology instruments) or AMBER (AI-authored frameworks). Hypothetical "
        "survey analysis documents (O1, PDFs 11-15) carry RED banners."
    )

    # =========================================================================
    # SECTION 3.4: S2RF -- FORMAL COMPONENT DOCUMENTATION
    # =========================================================================
    pdf.add_page()
    pdf.sub_heading("3.4  The Simulation to Research Framework (S2RF): Formal Component Documentation")
    pdf.body(
        "Through the execution of the iNHCES project, a replicable, platform-independent research "
        "methodology has emerged and been formalised as the Simulation to Research Framework (S2RF) "
        "(S2RF). The S2RF was originated and developed under the intellectual leadership of "
        "Dr. Bello Abdullahi (S2P Architect and Research Investigator, BAE Consulting Engineers, "
        "Abuja) in collaboration with the iNHCES research team at ABU Zaria. The framework "
        "consists of five core, sequentially applied components:"
    )

    for num, title, desc in [
        (1, "THE GOVERNING PREAMBLE",
         "A formal declaration document (this document) that establishes the simulation methodology, "
         "ethical framework, data-source obligations, and researcher responsibilities before any "
         "AI-assisted research output is generated. The Governing Preamble is the founding "
         "instrument of every S2RF-governed project and must be read by all team members before "
         "any pipeline artefact is used."),
        (2, "THE DATA SOURCE DECLARATION SYSTEM",
         "A colour-coded banner page included at the beginning of every document generated in the "
         "pipeline. GREEN = live or real data from verified APIs or fieldwork. AMBER = AI-authored "
         "framework or methodology content that has been reviewed and validated by a researcher. "
         "RED = synthetic or simulated data that MUST be replaced before any publication use. "
         "This system makes the epistemological status of every output immediately visible."),
        (3, "THE REPLACEMENT OBLIGATION",
         "A mandatory protocol requiring that all RED-banner (synthetic) data be replaced with "
         "real collected data before any publication, grant report, policy brief, or public "
         "presentation. RED is not a failure state -- it is a defined, temporary, and explicitly "
         "managed condition on the path from simulation to verified research. The obligation is "
         "documented in this Preamble and in each affected document."),
        (4, "THE HUMAN VALIDATION GATE",
         "A defined review checkpoint at which a qualified human researcher -- not the AI -- must "
         "approve the transition of any artefact from simulation to research instrument. No "
         "AI output advances to the next pipeline stage without sign-off by a named member of "
         "the research team. This gate preserves human intellectual authority over every "
         "research decision and is the primary safeguard against AI-generated error propagating "
         "into published findings."),
        (5, "PLATFORM INDEPENDENCE",
         "The S2RF is designed to operate across all major AI platforms: Claude.ai Projects, "
         "ChatGPT Projects with Code Interpreter, Google Gemini Gems, and DeepSeek R1/V3 "
         "(via a manually pasted Context Block). The framework's core components are "
         "platform-agnostic and can be implemented in any AI-native environment -- enabling "
         "non-system-development research that does not require a VS Code environment. This "
         "component extends the S2RF to survey research, policy analysis, literature reviews, "
         "and other qualitative or quantitative academic inquiry."),
    ]:
        pdf.numbered_item(str(num), title, desc)

    pdf.highlight_box(
        "S2RF FRAMEWORK RULE:  No AI-generated output, regardless of which platform produced it, "
        "may advance to any form of publication, formal reporting, or policy advice without "
        "passing through all five S2RF components: (1) Preamble declaration, (2) DATA SOURCE "
        "labelling, (3) Replacement Obligation compliance, (4) Human Validation Gate sign-off, "
        "and (5) Platform Independence verification."
    )
    pdf.body(
        "The S2RF has been formally documented in a companion research paper: 'Research Simulation "
        "Using AI Tools for the Development of iNHCES: A Simulation to Research Framework (S2RF) "
        "(S2RF)' (P9 of the iNHCES publication portfolio, authored by Dr. Bello Abdullahi et al.). "
        "That paper provides the full academic treatment of the framework, application across the "
        "O1-O6 pipeline, extension to non-VS Code environments, and a developmental chronicle "
        "(Appendix E) documenting the human-AI interactions that gave rise to the framework."
    )

    # =========================================================================
    # SECTION 4: WHAT THE SIMULATION IS NOT
    # =========================================================================
    pdf.add_page()
    pdf.section_title("4.  What This Simulation Is NOT")

    pdf.warn_box(
        "IMPORTANT DECLARATION:  The iNHCES research team explicitly rejects and condemns "
        "the practice of submitting AI-generated content as original human research without "
        "disclosure.  This simulation is not, and will never be used as, a substitute for "
        "genuine research conduct."
    )

    pdf.body(
        "To remove all ambiguity, the following practices are explicitly excluded from the "
        "iNHCES research programme:"
    )

    for num, title, desc in [
        (1, "NOT: Submitting AI outputs as original research",
         "No PDF, analysis, or document generated by the AI simulation will be submitted to "
         "any journal, conference, or grant body without full disclosure of AI involvement, "
         "replacement of all synthetic data with real collected data, and review and validation "
         "by qualified human researchers. The simulation outputs are WORKING DOCUMENTS, not "
         "final research products."),
        (2, "NOT: Fabricating research data",
         "The RED-banner (synthetic) outputs in this pipeline are clearly labelled as "
         "computer-generated hypothetical data for pipeline testing purposes only. No synthetic "
         "data value will ever appear in a published table, figure, or statistical result unless "
         "it is explicitly identified as a simulation scenario (e.g., for software testing). "
         "All published statistics will derive from real field surveys, real API data, or "
         "real project records."),
        (3, "NOT: Bypassing peer review or quality assurance",
         "The AI simulation generates first drafts that must pass through multiple layers of "
         "human validation: supervisor review, statistical verification by a qualified "
         "statistician, peer review at target journals, and ethics board approval for all "
         "human-subjects components (Delphi surveys, practitioner questionnaires)."),
        (4, "NOT: Removing human intellectual contribution",
         "The AI tool generates structured content based on instructions from the research "
         "team. Every instruction, every structural decision, every validation judgment, and "
         "every acceptance or rejection of AI output is a human intellectual act performed "
         "by a member of the research team. The AI does not direct the research -- the "
         "researchers direct the AI."),
        (5, "NOT: Misrepresenting authorship",
         "AI tools (including Claude and GitHub Copilot) do not qualify as authors under "
         "the ICMJE criteria (International Committee of Medical Journal Editors, 2024) or "
         "under COPE guidelines. The human researchers who designed the study, validated "
         "the outputs, collected the field data, and bear accountability for the results "
         "are the authors. AI will be disclosed as a tool in the acknowledgements and "
         "methods section of every publication."),
        (6, "NOT: A shortcut that degrades research quality",
         "The simulation phase is intended to IMPROVE research quality by ensuring the "
         "methodology is sound before fieldwork begins. A simulation that reveals a flaw in "
         "the design at the prototype stage has added value -- not reduced it. The final "
         "iNHCES outputs will meet or exceed the methodological rigour expected for Q1 "
         "publication in construction management and AI journals."),
    ]:
        pdf.numbered_item(str(num), title, desc)

    # =========================================================================
    # SECTION 5: WHAT THE SIMULATION IS
    # =========================================================================
    pdf.add_page()
    pdf.section_title("5.  What This Simulation IS")

    pdf.body(
        "Having established what the simulation is not, this section articulates precisely "
        "what role the AI tool plays in the iNHCES research programme."
    )

    for num, title, desc in [
        (1, "A METHODOLOGY SCAFFOLD",
         "The AI generates structured first drafts of research instruments: PRISMA protocols, "
         "SPSS analysis plans, Delphi survey questionnaires, and ML benchmarking frameworks. "
         "These drafts are informed by the AI's training on thousands of published research "
         "papers and methodological texts. The research team then reviews, critiques, and "
         "refines each draft to fit the specific iNHCES context. The AI provides the initial "
         "structure; the team provides the intellectual judgement about what is right for "
         "this study."),
        (2, "A CODE INFRASTRUCTURE BUILDER",
         "The AI generates Python scripts for data collection, statistical analysis, and ML "
         "model training. These scripts are inspected, tested, and validated by the team. "
         "The team understands what each script does and can modify it. The scripts are "
         "not black-box magic -- they are readable, documented, and reproducible by any "
         "competent Python developer. Using AI to accelerate coding does not differ in "
         "principle from using statistical software like SPSS or R to accelerate analysis."),
        (3, "A KNOWLEDGE SYNTHESISER FOR LITERATURE FRAMING",
         "The AI provides broad summaries of relevant literature, identifies key authors and "
         "methodological themes, and helps structure the theoretical framework. However, all "
         "specific citations in published papers will be independently verified by the team "
         "using Scopus, Web of Science, and Zotero. No AI-hallucinated citation will appear "
         "in any publication."),
        (4, "A WRITING AID (DRAFT LANGUAGE, NOT FINAL TEXT)",
         "The AI produces draft language for sections of the research papers and documents. "
         "This draft language is the starting point for human writing -- not the final "
         "output. The research team rewrites, restructures, and adds specialist knowledge "
         "that only domain experts (quantity surveyors, construction economists, Nigerian "
         "policy specialists) can contribute. This is comparable to using a research "
         "assistant to produce a first draft for the supervisor to review."),
        (5, "A SYNTHETIC DATA GENERATOR FOR PIPELINE TESTING",
         "Where live data is not yet available (e.g., before the Delphi survey has been "
         "conducted), the AI simulation uses seeded NumPy random generators to produce "
         "realistic-looking hypothetical datasets. These datasets allow the statistical "
         "pipelines and ML training loops to be tested end-to-end BEFORE real data arrives. "
         "This is standard software engineering practice ('test-driven development') applied "
         "to research. Every synthetic dataset is clearly labelled RED and will be replaced."),
        (6, "A RESEARCH PLANNING AND ORGANISATION TOOL",
         "The AI helps the research team maintain a structured development context: tracking "
         "which objectives are complete, which are in progress, what data sources are needed, "
         "and what the next steps are. This project management function improves research "
         "efficiency without affecting the intellectual content of the research."),
    ]:
        pdf.numbered_item(str(num), title, desc)

    # =========================================================================
    # SECTION 6: RESEARCH ETHICS AND ACADEMIC INTEGRITY
    # =========================================================================
    pdf.add_page()
    pdf.section_title("6.  Research Ethics and Academic Integrity")

    pdf.body(
        "The use of AI tools in academic research has generated significant discussion across "
        "the global research community since 2022. This section sets out the ethical framework "
        "that governs the iNHCES project, with specific reference to authoritative policy "
        "statements and the practical measures adopted by this team."
    )

    pdf.sub_heading("6.1  Foundational Principles of Research Integrity")
    pdf.body("The following principles from the Singapore Statement on Research Integrity (2010) "
             "and the European Code of Conduct for Research Integrity (ALLEA, 2023) apply in full:")

    for label, detail, fill in [
        ("Honesty",
         "Report research findings honestly and transparently. Never fabricate, falsify, or "
         "selectively report data. All DATA SOURCE declarations in iNHCES documents are a "
         "direct implementation of this principle.", False),
        ("Rigour",
         "Apply statistical and methodological best practices throughout. Conduct peer "
         "review of methods before data collection. The simulation phase is a rigour "
         "mechanism -- it tests the methodology before real resources are committed.", True),
        ("Transparency",
         "Disclose all methods, including AI assistance, in every publication. Report "
         "limitations. Ensure that published results can be independently reproduced "
         "by other researchers using the provided data and code.", False),
        ("Independence",
         "Conduct research free from undue influence. The AI tool provides suggestions; "
         "the researchers make all intellectual decisions. The team's domain expertise "
         "in quantity surveying and Nigerian construction economics is the intellectual "
         "foundation of the research.", True),
        ("Responsibility",
         "Accept full personal and institutional responsibility for all research outputs. "
         "The human researchers are accountable for every result, even those where AI "
         "assistance was used. The AI bears no moral or legal accountability.", False),
        ("Care for Others",
         "Ensure surveys and data collection treat participants (QS professionals, "
         "contractors) with dignity and respect. Obtain informed consent. Comply with "
         "ABU Zaria and TETFund ethics board requirements for human-subjects research.", True),
    ]:
        pdf.principle_row(label, detail, fill)
    pdf.ln(3)

    pdf.sub_heading("6.2  AI Use and Academic Integrity -- The Current Global Landscape")
    pdf.body(
        "Major publishers and research councils have updated their policies on AI use in "
        "research since 2023. The following positions are relevant to iNHCES:"
    )
    pdf.bullet([
        "COPE (Committee on Publication Ethics, 2023): 'AI tools cannot be listed as an author. "
        "Authors are responsible for the accuracy and integrity of work assisted by AI tools. "
        "Use of AI must be disclosed in the methods section.'",
        "ICMJE (International Committee of Medical Journal Editors, 2023): 'AI and AI-assisted "
        "technologies do not meet the criteria for authorship... Corresponding authors are "
        "responsible for ensuring the work was conducted appropriately.'",
        "Elsevier AI Policy (2024): 'Authors must disclose the use of generative AI in the "
        "writing process... AI and AI-assisted technologies cannot be listed as an author.'",
        "Springer Nature AI Policy (2024): 'Use of AI tools must be documented in a dedicated "
        "statement in the methods or acknowledgements section of the paper.'",
        "Taylor & Francis (2023): Explicitly prohibits listing AI as author; requires "
        "disclosure in the manuscript.",
        "TETFund / NRF (Nigeria): While a formal AI policy for grant-funded research was "
        "not yet published at project inception, the team applies the above international "
        "standards as a minimum, in addition to ABU Zaria's institutional academic integrity "
        "policy.",
        "UNESCO Recommendation on the Ethics of AI (2021): Calls for transparency, human "
        "oversight, and accountability in all AI applications -- including research tools.",
    ])

    pdf.sub_heading("6.3  The Critical Distinction: AI as AUTHOR vs AI as TOOL")
    pdf.highlight_box(
        "There is a fundamental ethical difference between (A) using AI to do research and "
        "presenting the AI's output as your own original work, and (B) using AI as a "
        "sophisticated research tool -- just as researchers use SPSS, R, Python, Zotero, "
        "or Excel -- to assist in conducting research that the human researchers design, "
        "execute, validate, and take responsibility for.\n\n"
        "iNHCES is firmly and irrevocably in category (B)."
    )
    pdf.body(
        "The analogy is precise: a quantity surveyor who uses BCIS (Building Cost Information "
        "Service) software to generate a cost plan has not fabricated the estimate -- the "
        "software is a tool. A researcher who uses SPSS to run a factor analysis has not "
        "fabricated the statistics -- the software is a tool. A researcher who uses Claude "
        "to generate a structured first draft of a PRISMA protocol has not fabricated the "
        "methodology -- the AI is a tool. In every case, the professional judgement, "
        "validation, and accountability reside with the human expert."
    )

    pdf.add_page()
    pdf.sub_heading("6.4  Specific AI Integrity Measures in iNHCES")
    pdf.body("The following concrete measures are implemented throughout the iNHCES pipeline:")

    for num, title, desc in [
        (1, "Full Transparency of AI Involvement",
         "This preamble document exists. Every PDF in the pipeline has a DATA SOURCE "
         "DECLARATION page. The CLAUDE.md file in the project root documents the AI "
         "interaction context for every development session. No AI involvement is hidden."),
        (2, "No AI-Generated Citations",
         "AI language models are known to hallucinate citations. No reference to a "
         "specific paper, author, or finding will appear in any iNHCES publication unless "
         "it has been independently located and verified in Scopus, Web of Science, or "
         "the primary source. All citations in simulation documents are labelled as "
         "'representative examples to be verified.'"),
        (3, "Synthetic Data Replacement Obligation",
         "Every RED-banner document contains a mandatory note: the synthetic data MUST "
         "be replaced with real collected data before any use in publication, grant "
         "reporting, or policy advice. This obligation is documented in this preamble "
         "and in each affected document."),
        (4, "Human Validation at Every Stage",
         "No AI output advances to the next stage of the pipeline without review and "
         "approval by a named human researcher on the team. The principal investigator "
         "and co-investigators hold sign-off responsibility for each objective."),
        (5, "Disclosure in All Publications",
         "Every paper submitted from this project will include a standard AI Disclosure "
         "Statement in the Acknowledgements (see Section 9 of this document for the "
         "recommended wording). This disclosure will specify the tool used, the purpose "
         "for which it was used, and how the outputs were validated."),
        (6, "Ethics Board Compliance",
         "All human-subjects components (Delphi surveys for O3, practitioner "
         "questionnaires for O1 Phase 2) will obtain Institutional Review Board (IRB) / "
         "ethics committee approval from ABU Zaria before data collection begins. "
         "Informed consent forms will be provided to all participants. Data will be "
         "anonymised before analysis."),
        (7, "Open Science Commitment",
         "In line with TETFund's expectation of knowledge dissemination, the iNHCES "
         "team will publish all non-sensitive datasets, trained models, and code to "
         "open repositories (GitHub, Zenodo, or Figshare) upon publication -- enabling "
         "independent replication by other researchers."),
    ]:
        pdf.numbered_item(str(num), title, desc)

    pdf.sub_heading("6.5  AI Use in the Nigerian Academic Context")
    pdf.body(
        "Nigerian higher education institutions and research funding bodies are actively "
        "developing AI use policies. ABU Zaria, as a leading federal university, is expected "
        "to adopt policies aligned with international best practice. The iNHCES team commits "
        "to the following, regardless of the specific policy that is eventually formalised:"
    )
    pdf.bullet([
        "Engage proactively with ABU Zaria's senate and research office on AI disclosure "
        "norms as they develop.",
        "Consult the Nigerian Universities Commission (NUC) guidelines on AI in research "
        "as they become available.",
        "Ensure that postgraduate students involved in iNHCES receive training on "
        "responsible AI use as part of their research methodology instruction.",
        "Not use AI tools in ways that would provide an unfair advantage in competitive "
        "grant applications without disclosure.",
        "Advocate within the Department of Quantity Surveying for the adoption of an "
        "explicit AI-in-research policy, using iNHCES as a model case study.",
    ])

    # =========================================================================
    # SECTION 7: SIMULATION TO REAL RESEARCH PIPELINE
    # =========================================================================
    pdf.add_page()
    pdf.section_title("7.  The Simulation-to-Research Pipeline")

    pdf.body(
        "The iNHCES development pipeline moves through distinct phases for each objective. "
        "Understanding this progression is essential for every team member."
    )

    stages = [
        ("PHASE 1: Simulation (AI-Assisted Draft)",
         "AI generates structured first-pass artefacts for each objective: protocol documents, "
         "analysis plan PDFs, code scripts, schema designs. All synthetic data is labelled RED. "
         "All AI-authored methodology content is labelled AMBER. Real API data is labelled GREEN. "
         "Status: This is the phase currently underway for iNHCES."),
        ("PHASE 2: Team Review and Critique",
         "The principal investigator, co-investigators, and relevant postgraduate students "
         "review every simulation output. They identify errors, methodological weaknesses, "
         "and gaps. They revise protocols, questionnaires, and code. This phase converts "
         "AMBER documents to reviewed, approved research instruments."),
        ("PHASE 3: Ethics Approval and Registration",
         "Human-subjects components are submitted to ABU Zaria IRB / ethics committee. "
         "PRISMA protocol is registered with PROSPERO before database searching begins. "
         "All required institutional approvals are obtained before fieldwork commences."),
        ("PHASE 4: Real Data Collection",
         "Delphi surveys and practitioner questionnaires are conducted. Live API keys are "
         "obtained and macroeconomic data is fetched in real time. Project cost records are "
         "collected from contractors, MDAs, and NIQS cost databases. All RED synthetic data "
         "is replaced with real measurements."),
        ("PHASE 5: Analysis and Model Training",
         "The validated Python pipelines (tested in Phase 1 on synthetic data) are run "
         "against the real datasets. ML models are trained, tuned, and evaluated against "
         "real iNHCES targets. SHAP analysis identifies the most important features. "
         "MLflow tracks all experiments for full reproducibility."),
        ("PHASE 6: Publication and Deployment",
         "Validated findings are written up for target journals with full AI disclosure. "
         "The iNHCES web platform is deployed. Datasets and models are published to open "
         "repositories. The research team takes full intellectual and professional "
         "responsibility for every published claim."),
    ]

    for title, desc in stages:
        pdf.ln(2)
        pdf.set_x(LEFT)
        pdf.set_fill_color(*DARK_NAVY)
        pdf.set_text_color(*WHITE)
        pdf.set_font("Helvetica", "B", 8.5)
        pdf.multi_cell(PAGE_W, 6.5, sanitize(f"  {title}"), fill=True, border=0)
        pdf.set_text_color(*DARK_GREY)
        pdf.set_x(LEFT + 4)
        pdf.set_font("Helvetica", "", 9)
        pdf.multi_cell(PAGE_W - 4, 5.2, sanitize(desc))
        pdf.ln(1)

    pdf.highlight_box(
        "KEY PRINCIPLE: No simulated output advances to publication without passing "
        "through Phases 2 through 6. The simulation produces the skeleton; real research "
        "provides the flesh, blood, and soul."
    )

    # =========================================================================
    # SECTION 8: OBLIGATIONS OF THE RESEARCH TEAM
    # =========================================================================
    pdf.add_page()
    pdf.section_title("8.  Obligations of the Research Team")

    pdf.body(
        "The following obligations apply to all members of the iNHCES research team "
        "(principal investigator, co-investigators, postdoctoral researchers, and "
        "postgraduate students):"
    )

    for num, title, desc in [
        (1, "Read This Document",
         "Every team member must read this preamble document before engaging with any "
         "iNHCES simulation output. Ignorance of the AI-simulation nature of the current "
         "documents is not an acceptable defence for misuse."),
        (2, "Check the DATA SOURCE Banner",
         "Before using any figure, table, or finding from any iNHCES PDF, check its DATA "
         "SOURCE DECLARATION page. GREEN = cite the original source. AMBER = validate and "
         "own the content. RED = REPLACE with real data before any use."),
        (3, "Never Submit RED-Banner Data",
         "Synthetic data marked RED must NEVER appear in any submitted publication, grant "
         "report, policy brief, or public presentation without explicit disclosure that it "
         "is a simulation scenario. Any such use without disclosure constitutes research "
         "misconduct."),
        (4, "Verify All Citations Independently",
         "No citation generated or suggested by an AI tool should be used in any "
         "publication without independent verification via Scopus, Web of Science, "
         "Google Scholar, or the primary source. Maintain a Zotero library of all "
         "verified references."),
        (5, "Disclose AI Assistance in All Publications",
         "Include the AI disclosure statement (Section 9) in every publication, grant "
         "report, thesis chapter, and conference paper that draws on iNHCES outputs. "
         "The specific tools used, the tasks they performed, and the validation process "
         "must be documented."),
        (6, "Maintain Human Intellectual Leadership",
         "The research questions, theoretical framework, domain expertise, validation "
         "judgements, and accountability must remain with the human researchers at all "
         "times. If the team cannot explain and defend an AI-generated output in their "
         "own words, they should not use it."),
        (7, "Report Concerns",
         "Any team member who observes potential misuse of AI outputs -- including "
         "attempts to use synthetic data as real, fabricate citations, or misrepresent "
         "AI contributions -- must report this to the principal investigator and, if "
         "necessary, to the ABU Zaria research integrity officer."),
    ]:
        pdf.numbered_item(str(num), title, desc)

    # =========================================================================
    # SECTION 9: CITING AI ASSISTANCE
    # =========================================================================
    pdf.add_page()
    pdf.section_title("9.  Guidelines for Citing AI Assistance in Publications")

    pdf.body(
        "The following guidance is adapted from recommendations by COPE (2023), Elsevier "
        "(2024), and Springer Nature (2024) for disclosing AI tool use in academic publications."
    )

    pdf.sub_heading("9.1  In the Methods Section")
    pdf.body(
        "Include a subsection titled 'AI Tools and Software' or similar. Describe:"
    )
    pdf.bullet([
        "The AI tool(s) used (name, version/date, provider).",
        "The specific tasks for which the tool was used "
        "(e.g., drafting protocol documents, generating code, synthesising literature themes).",
        "How AI outputs were validated before use "
        "(e.g., reviewed by two co-authors, verified against primary sources, tested against "
        "real data, approved by a domain expert statistician).",
        "That the AI tool was not used for final data analysis or statistical inference "
        "(if applicable).",
    ])

    pdf.sub_heading("9.2  Recommended Disclosure Statement for iNHCES Publications")
    pdf.body(
        "The following standard disclosure statement is approved for use in all iNHCES-related "
        "publications. It should be adapted as appropriate to the specific paper:"
    )
    pdf.code_box(
        "AI ASSISTANCE DISCLOSURE\n\n"
        "During the development of this research, the authors used Claude (Anthropic), "
        "accessed via GitHub Copilot (Microsoft), to assist with: (i) drafting the initial "
        "structure of the [PRISMA protocol / survey instrument / analysis plan / software "
        "pipeline -- specify], (ii) generating Python code for [data collection / statistical "
        "analysis / ML pipeline -- specify], and (iii) producing first-draft text for "
        "[specified sections].\n\n"
        "All AI-generated content was reviewed, validated, and revised by the research team. "
        "All statistical analyses were verified by [name, qualification]. All citations were "
        "independently verified in Scopus and Web of Science. All field data was collected by "
        "the research team and not generated by AI. The AI tool was used as a productivity "
        "and scaffolding aid; all intellectual decisions, research design choices, and "
        "conclusions are the sole responsibility of the named human authors.\n\n"
        "No AI tool is listed as an author of this work. This disclosure is made in "
        "accordance with COPE (2023) and [journal name] AI disclosure policy."
    )

    pdf.sub_heading("9.3  In the Acknowledgements Section")
    pdf.body(
        "Include a brief acknowledgement note such as:"
    )
    pdf.code_box(
        "The authors acknowledge the use of Claude (Anthropic) via GitHub Copilot (Microsoft) "
        "as an AI-assisted drafting and coding tool during the preparation of this research. "
        "All content was reviewed, validated, and approved by the human research team."
    )

    pdf.sub_heading("9.4  For Thesis Chapters (Postgraduate Students)")
    pdf.body(
        "Postgraduate students using iNHCES outputs in their theses must include a dedicated "
        "'AI Tool Use Declaration' section in their General Introduction chapter, specifying:"
    )
    pdf.bullet([
        "Every chapter or section where AI-assisted drafts were used as a starting point.",
        "A clear statement that the final submitted thesis text is the student's own work, "
        "substantially revised from any AI-generated draft.",
        "Confirmation that no AI-generated text was submitted as the student's own writing "
        "without significant revision and intellectual transformation.",
        "Acknowledgement that the supervisor reviewed and approved the AI disclosure.",
    ])
    pdf.warn_box(
        "ABU ZARIA THESIS SUBMISSION NOTE: Students must verify the current ABU Zaria "
        "postgraduate thesis regulations regarding AI use at the time of submission. "
        "If institutional policy requires more restrictive disclosure or prohibits certain "
        "AI uses, the institutional policy takes precedence over this document."
    )

    # =========================================================================
    # SECTION 10: CONCLUSION
    # =========================================================================
    pdf.add_page()
    pdf.section_title("10.  Conclusion")

    pdf.body(
        "The iNHCES project is a rigorous, ethically conducted academic research programme. "
        "The use of AI assistance in its development is not a compromise of research integrity "
        "-- it is a transparent, disclosed, and carefully managed application of a powerful "
        "modern tool in the service of a genuine research mission."
    )
    pdf.body(
        "The housing construction cost crisis in Nigeria is real. The gap it creates in "
        "housing affordability, public infrastructure planning, and private investment "
        "decision-making is real. The research community's need for better cost estimation "
        "tools is real. The iNHCES project addresses a real problem with real methods, real "
        "data, and real technical rigour. AI assistance in the scaffold phase of its "
        "development does not diminish any of this -- it accelerates the team's ability to "
        "build the best possible research programme."
    )
    pdf.body(
        "What the AI cannot provide -- and what the research team must provide -- is the "
        "domain expertise of Nigerian quantity surveying professionals, the field knowledge "
        "of Nigeria's construction market dynamics, the professional judgement to validate "
        "model outputs against practical experience, and the intellectual accountability "
        "to stand behind published findings. These things belong to the human researchers, "
        "and they cannot be simulated."
    )
    pdf.highlight_box(
        "FINAL STATEMENT:  The iNHCES research team is using AI as a tool -- the same way "
        "a previous generation of researchers used statistical software, and the generation "
        "before them used calculators. The tool does not make the research. The researchers "
        "make the research. This document is our commitment to that principle."
    )

    pdf.ln(4)
    pdf.set_x(LEFT)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*DARK_NAVY)
    pdf.cell(PAGE_W, 6, sanitize("Research Team -- Department of Quantity Surveying, ABU Zaria"), ln=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*DARK_GREY)
    pdf.cell(PAGE_W, 6, sanitize(f"TETFund NRF 2025  |  iNHCES Project  |  {date.today().strftime('%d %B %Y')}"), ln=True)

    # =========================================================================
    # SECTION 11: KEY REFERENCES AND GUIDELINES
    # =========================================================================
    pdf.add_page()
    pdf.section_title("11.  Key References and Policy Documents")

    pdf.body(
        "The following authoritative documents underpin the ethics framework set out in this "
        "preamble. The research team should consult these directly and verify currency at time "
        "of publication:"
    )

    refs = [
        ("ALLEA (2023)",
         "The European Code of Conduct for Research Integrity (Revised Edition 2023). "
         "All European Academies (ALLEA). allea.org/code-of-conduct"),
        ("COPE (2023)",
         "Authorship and AI tools: COPE Position Statement. Committee on Publication Ethics. "
         "publicationethics.org/cope-position-statements/ai-author"),
        ("Elsevier (2024)",
         "AI and Authorship Policy. Elsevier. "
         "elsevier.com/about/policies/publishing-ethics/use-of-ai-and-ai-assisted-technologies-in-scientific-writing"),
        ("ICMJE (2024)",
         "Recommendations for the Conduct, Reporting, Editing, and Publication of Scholarly "
         "Work in Medical Journals. International Committee of Medical Journal Editors. "
         "icmje.org/recommendations"),
        ("Page et al. (2021)",
         "The PRISMA 2020 statement: An updated guideline for reporting systematic reviews. "
         "BMJ 2021;372:n71. doi: 10.1136/bmj.n71"),
        ("Singapore Statement (2010)",
         "Singapore Statement on Research Integrity. 2nd World Conference on Research "
         "Integrity, Singapore 2010. singaporestatement.org"),
        ("Springer Nature (2024)",
         "Artificial Intelligence (AI) Policy. Springer Nature. "
         "springernature.com/gp/policies/editorial-policies"),
        ("Taylor & Francis (2023)",
         "Authorship criteria and responsibilities. Taylor & Francis Author Services. "
         "authorservices.taylorandfrancis.com/publishing-your-research/authorship"),
        ("TETFund (2025)",
         "National Research Fund (NRF) 2025 Research Grant Guidelines. "
         "Tertiary Education Trust Fund, Abuja, Nigeria. tetfund.gov.ng"),
        ("UNESCO (2021)",
         "Recommendation on the Ethics of Artificial Intelligence. "
         "United Nations Educational, Scientific and Cultural Organisation. "
         "doi:10.54677/MNMH8546"),
        ("World Conferences on Research Integrity Foundation (WCRIF)",
         "Hong Kong Principles for Assessing Researchers (2020). "
         "doi:10.1371/journal.pone.0239123"),
    ]

    for i, (author, detail) in enumerate(refs):
        fill = (i % 2 == 0)
        pdf.set_fill_color(*(LIGHT_BLUE if fill else WHITE))
        y0 = pdf.get_y()
        pdf.set_x(LEFT)
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_text_color(*DARK_NAVY)
        pdf.multi_cell(50, LINE_H, sanitize(f" {author}"), border=1, fill=fill)
        y1 = pdf.get_y()
        pdf.set_xy(LEFT + 50, y0)
        pdf.set_font("Helvetica", "", 8)
        pdf.set_text_color(*DARK_GREY)
        pdf.multi_cell(PAGE_W - 50, LINE_H, sanitize(f" {detail}"), border=1, fill=fill)
        y2 = pdf.get_y()
        pdf.set_y(max(y1, y2))

    pdf.ln(6)
    pdf.set_x(LEFT)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GREY)
    pdf.multi_cell(PAGE_W, 5, sanitize(
        "NOTE: All policy documents should be verified for currency at time of use. "
        "AI ethics policies from publishers and funding bodies are evolving rapidly. "
        "Always check the current version on the issuing body's website. "
        "This document was last updated " + date.today().strftime("%d %B %Y") + "."
    ))

    # =========================================================================
    # APPENDIX A: S2RF DISCOVERY CHRONICLE
    # =========================================================================
    pdf.add_page()
    pdf.section_title("Appendix A: From Research Challenge to Framework Discovery")
    pdf.sub_heading(
        "A Developmental Chronicle of the Human-AI Interactions That Gave Rise "
        "to the Simulation to Research Framework (S2RF)"
    )
    pdf.body(
        "This appendix documents, in chronological order, the key milestones in the "
        "human-AI interaction sequence that produced the S2RF. It is included as part "
        "of this Governing Preamble so that every member of the research team "
        "understands not only what the framework rules are, but where they came from "
        "and why each rule was established. The S2RF emerged from practice -- from "
        "specific decisions made during the iNHCES project in April 2026 -- not from "
        "prior theoretical design. The full academic treatment appears in companion "
        "Paper P9 (Dr. Bello Abdullahi et al.)."
    )
    pdf.body(
        "All interactions took place in April 2026 using GitHub Copilot (Claude "
        "Sonnet 4.6, via VS Code) under the direction of Dr. Bello Abdullahi, "
        "S2R Architect and Principal Investigator, TETFund NRF 2025."
    )

    discovery_items = [
        ("E.1  The Starting Point: A Research Programme Without a Framework",
         "The iNHCES project began with a clear ambition -- an AI-powered housing cost "
         "estimating system for Nigeria -- and a significant practical challenge: the "
         "full six-objective, nine-paper programme would normally require 3-5 years of "
         "fieldwork. The initial AI interactions focused on scaffolding the project: "
         "folder structure, CLAUDE.md, PROJECT_CONTEXT.md, and the first deliverables "
         "(PRISMA protocol, search strings, data extraction template). At this stage, "
         "there was no explicit framework. The AI was a productivity tool; integrity "
         "safeguards were informal researcher judgements rather than codified rules."),
        ("E.2  The First Critical Decision: What Is Real?",
         "The pivotal moment came during O1 Step 2 when the AI generated a methodology "
         "taxonomy table. The PI asked: what data source label should this carry? The "
         "AI's response introduced the three-level DATA SOURCE system -- GREEN (live "
         "API or real instrument), AMBER (AI-authored template), RED (synthetic data) -- "
         "and recommended AMBER on the grounds that the table was drawn from AI training "
         "knowledge, not from a real PRISMA database search. This interaction was the "
         "conceptual origin of the S2RF: the PI directed that this system be applied to "
         "every PDF produced in the project, without exception. That directive became "
         "S2RF Rule 2 -- the DATA SOURCE Declaration System."),
        ("E.3  The RED Banner: When Synthetic Data Became a Risk",
         "O1 Step 5 produced the first RED-banner document: a complete hypothetical "
         "survey analysis (n=60, NumPy seed=2025) with Cronbach alpha values, EFA "
         "factor loadings, and TAM path coefficients -- all from synthetic data. The "
         "document looked like a finished research paper. The PI immediately identified "
         "the risk and the Replacement Obligation was formalised: RED-banner content "
         "MUST be replaced with real data before any publication. The interaction also "
         "established a key principle: the more convincing a simulated output looks, "
         "the more important it is to label it clearly -- plausibility is itself a "
         "risk when the data is synthetic."),
        ("E.4  The Live Data Discovery: Designing for Upgrade",
         "O2 Step 1 produced a pattern that became one of the S2RF's most significant "
         "design features. The World Bank script fetched real GDP data via a live API "
         "(GREEN). The EIA and CBN scripts, lacking API keys, fell back to synthetic "
         "data (RED). But the scripts were designed so that setting the relevant "
         "environment variables would automatically upgrade from RED to GREEN without "
         "any code changes. This established a key design principle: AI simulation "
         "outputs should be designed for upgrade. RED is not a permanent failure state "
         "-- it is a defined position in a progression toward GREEN."),
        ("E.5  The IRB Boundary: Where AI Simulation Cannot Go",
         "O3 Delphi work produced the clearest articulation of the boundary between "
         "simulation and genuine research. Delphi instruments were AMBER (AI can design "
         "them from domain knowledge). Delphi analysis (n=20, seed=42 synthetic experts) "
         "was RED. But the PI articulated the pedagogical purpose of RED outputs: they "
         "show the research team what a finished Delphi looks like before the team "
         "undertakes the real one with real Nigerian experts. Simulation is rehearsal, "
         "not substitute. That distinction became the conceptual core of the Human "
         "Validation Gate. Crucially: the real Delphi requires IRB approval from ABU "
         "Zaria -- no AI tool can obtain IRB approval or substitute for expert "
         "knowledge of Nigerian construction practitioners."),
        ("E.6  Architecture Decision: Embedding Quality in the Database",
         "O4 Step 2 extended the S2RF beyond documents into the live system. The PI "
         "directed that the GREEN/AMBER/RED signal be embedded as a data_source_level "
         "column in the Supabase database, propagated through FastAPI responses, and "
         "rendered as a DataSourceBadge in the Next.js frontend. A quantity surveyor "
         "using the live iNHCES system sees, on every macro variable displayed, whether "
         "that variable came from a live API (GREEN) or a synthetic fallback (RED). "
         "This decision transformed the S2RF from a document-level audit tool into a "
         "system-level transparency mechanism."),
        ("E.7  The Honest Failure: Reporting What Should Not Be Hidden",
         "O5 Step 3 SHAP analysis returned near-zero values for all features because "
         "with n=22 training rows the model had converged to near-constant prediction. "
         "On direction from the PI, the near-zero result was reported honestly with a "
         "full explanation -- not replaced with a fabricated importance chart. This "
         "produced an important S2RF meta-rule: the framework requires honest reporting "
         "of simulation limitations, especially when those limitations make the output "
         "look unconvincing. A simulation that only produces impressive-looking results "
         "is a source of false confidence, not a useful research scaffold."),
        ("E.8  The System Goes Live: Automated Validation Gate",
         "The completion of O6 -- FastAPI backend (17 routes), Next.js frontend "
         "(8 pages), 7 Airflow DAGs, 73/73 passing tests, and a 4-job CI/CD pipeline "
         "-- marked the point at which the S2RF became demonstrably end-to-end. The "
         "CI/CD pipeline added a further dimension to the Human Validation Gate: "
         "GitHub Actions enforces that no code reaches Railway or Vercel unless all "
         "73 tests pass and the Next.js build succeeds. This is the first instance of "
         "the Human Validation Gate being enforced by code rather than by researcher "
         "discipline alone -- a significant maturation from principle to mechanism."),
        ("E.9  The Framework Recognised: From Practice to Publication",
         "Paper P9 was not planned at the outset of the project. It emerged when the "
         "PI observed that the interactions producing the S2RF were themselves a "
         "significant research contribution not being captured in Papers P1-P8. The "
         "decision to document the S2RF as a standalone paper was itself an exercise "
         "in human validation: the PI recognised a contribution the AI had not "
         "identified as publishable. The framework was subsequently extended to "
         "non-VS Code platforms (Claude.ai, ChatGPT, Gemini, DeepSeek), making it "
         "accessible to researchers without system development backgrounds."),
    ]
    for title, body in discovery_items:
        pdf.sub_heading(title)
        pdf.body(body)

    pdf.highlight_box(
        "S2RF FOUNDING PRINCIPLE (distilled from the discovery chronicle above): "
        "Every rule in this framework exists because a specific human decision was "
        "needed that the AI could not make. The DATA SOURCE system exists because a "
        "PI asked 'what label should this carry?' The Replacement Obligation exists "
        "because a PI recognised that synthetic data looked too convincing. The Human "
        "Validation Gate exists because a PI identified that IRB approval and expert "
        "recruitment are irreplaceable human obligations. The S2RF is not a constraint "
        "on AI capability -- it is a map of the boundary between AI productivity and "
        "human research accountability."
    )

    # =========================================================================
    # SAVE
    # =========================================================================
    pdf.output(out_path)
    print(f"[OK] 00_S2RF_Governing_Preamble_iNHCES.pdf  saved -> {out_path}")


# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    generate_intro()
