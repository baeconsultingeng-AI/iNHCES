"""
iNHCES Draft Paper P9 Generator
Paper: "Responsible AI Integration in Academic Research Workflows:
        A Simulation to Research Framework (S2RF) for Postgraduate Training
        -- Evidence from the iNHCES System Development Project"
Target Journals: Computers & Education | Innovations in Education and Teaching
                 International | AI & Society | Journal of Information Technology Education

DATA SOURCE: AMBER -- AI-authored policy/methodology paper. No synthetic data.
             This is a framework document; all iNHCES project facts are real.
             Quantitative pedagogical evidence (student pilot outcomes) is a
             PLACEHOLDER -- to be collected via ABU Zaria workshop before submission.

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

OUT_DIR   = _HERE
PAPER_ID  = "P9"
PAPER_TITLE = (
    "Responsible AI Integration in Academic Research Workflows: "
    "A Simulation to Research Framework (S2RF) for Postgraduate Training "
    "-- Evidence from the iNHCES System Development Project"
)
SHORT_TITLE = "AI Research Simulation Framework -- iNHCES Case Study"
JOURNAL_1 = "Computers & Education (Elsevier, IF ~12.0)"
JOURNAL_2 = "Innovations in Education and Teaching International (Taylor & Francis)"
JOURNAL_3 = "AI & Society (Springer)"


# ── Paper PDF class ────────────────────────────────────────────────────────────
class PaperPDF(DocPDF):
    def __init__(self):
        super().__init__(PAPER_TITLE, PAPER_ID)

    def header(self):
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*MID_GREY)
        self.set_xy(LEFT, 5)
        self.cell(PAGE_W, 4.5, sanitize(
            f"{PAPER_ID}  |  AI Research Simulation Framework  |  "
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

    def h1(self, text):
        self.set_font("Helvetica", "B", 11.5)
        self.set_text_color(*DARK_NAVY)
        self.ln(3)
        self.set_x(LEFT)
        self.multi_cell(PAGE_W, 5.5, sanitize(text))
        self.set_text_color(*DARK_GREY)
        self.ln(1)

    def h2(self, text):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*DARK_NAVY)
        self.ln(2)
        self.set_x(LEFT)
        self.multi_cell(PAGE_W, 5.5, sanitize(text))
        self.set_text_color(*DARK_GREY)
        self.ln(1)

    def h3(self, text):
        self.set_font("Helvetica", "BI", 9.5)
        self.set_text_color(*DARK_GREY)
        self.ln(1.5)
        self.set_x(LEFT)
        self.multi_cell(PAGE_W, 5.2, sanitize(text))
        self.ln(0.5)

    def para(self, text, indent=0):
        self.set_font("Helvetica", "", 9.5)
        self.set_text_color(*DARK_GREY)
        self.set_x(LEFT + indent)
        self.multi_cell(PAGE_W - indent, 5.2, sanitize(text))
        self.ln(1.5)

    def bullet_list(self, items, indent=4):
        self.set_font("Helvetica", "", 9.5)
        self.set_text_color(*DARK_GREY)
        for item in items:
            self.set_x(LEFT + indent)
            self.cell(4, 5.2, "-")
            self.set_x(LEFT + indent + 4)
            self.multi_cell(PAGE_W - indent - 4, 5.2, sanitize(item))
        self.ln(1)

    def numbered_list(self, items, indent=4):
        self.set_font("Helvetica", "", 9.5)
        self.set_text_color(*DARK_GREY)
        for i, item in enumerate(items, 1):
            self.set_x(LEFT + indent)
            self.cell(6, 5.2, f"{i}.")
            self.set_x(LEFT + indent + 6)
            self.multi_cell(PAGE_W - indent - 6, 5.2, sanitize(item))
        self.ln(1)

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

    def key_finding_box(self, title, text):
        self.ln(2)
        self.set_fill_color(*LIGHT_BLUE)
        self.set_draw_color(*DARK_NAVY)
        self.set_line_width(0.5)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*DARK_NAVY)
        self.set_x(LEFT)
        self.cell(PAGE_W, 6, sanitize(f"  {title}"), border="LTR", fill=True, ln=True)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*DARK_GREY)
        self.set_x(LEFT)
        self.multi_cell(PAGE_W, 5, sanitize(text), border="LBR", fill=True)
        self.set_text_color(*DARK_GREY)
        self.ln(2)


# ── Title page ─────────────────────────────────────────────────────────────────
def make_title_page(pdf):
    pdf.add_page()

    # Amber draft strip
    pdf.set_fill_color(30, 80, 160)
    pdf.rect(0, 0, 210, 8, 'F')
    pdf.set_font("Helvetica", "B", 7.5)
    pdf.set_text_color(*WHITE)
    pdf.set_xy(0, 1.5)
    pdf.cell(210, 5,
             "AI-GENERATED FIRST DRAFT -- METHODOLOGY PAPER -- NOT FOR SUBMISSION",
             align="C")
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(16)

    # Journal targets
    pdf.set_font("Helvetica", "I", 8.5)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.cell(PAGE_W, 5.5, "Target Journals (in priority order):", align="C", ln=True)
    for j in [JOURNAL_1, JOURNAL_2, JOURNAL_3]:
        pdf.set_x(LEFT)
        pdf.cell(PAGE_W, 5, sanitize(j), align="C", ln=True)
    pdf.ln(4)

    # Title
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(*DARK_NAVY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 7.5, sanitize(PAPER_TITLE), align="C")
    pdf.ln(4)

    pdf.set_draw_color(*GOLD)
    pdf.set_line_width(1.0)
    pdf.line(LEFT + 10, pdf.get_y(), LEFT + PAGE_W - 10, pdf.get_y())
    pdf.ln(6)

    for line in [
        "Dr. Bello Abdullahi  --  Principal Investigator, TETFund NRF 2025",
        "Originator of the Simulation to Research Framework (S2RF)",
        "Department of Quantity Surveying, Ahmadu Bello University, Zaria",
        "[CO-AUTHOR NAME(S)] -- [Affiliation(s)] [consider AI-in-education specialist]",
        "Corresponding author: [EMAIL ADDRESS] | ORCID: [INSERT]",
        "",
        "Acknowledgement: TETFund National Research Fund 2025, Grant No. [INSERT]",
        f"Manuscript prepared: {date.today().strftime('%d %B %Y')}",
        "Estimated word count (draft): ~12,000 words (excl. references and appendices)",
        "Paper No. 9 of 9 in the iNHCES Publication Portfolio",
    ]:
        pdf.set_font("Helvetica", "I" if line.startswith("[") else "", 9)
        pdf.set_text_color(*MID_GREY)
        pdf.set_x(LEFT)
        pdf.cell(PAGE_W, 5.5, sanitize(line), align="C", ln=True)

    pdf.ln(4)
    pdf.set_draw_color(*MID_GREY)
    pdf.set_line_width(0.3)
    pdf.line(LEFT, pdf.get_y(), LEFT + PAGE_W, pdf.get_y())


# ── Abstract ───────────────────────────────────────────────────────────────────
def make_abstract(pdf):
    pdf.ln(6)
    pdf.h1("ABSTRACT")
    pdf.set_fill_color(*LIGHT_BLUE)
    pdf.set_draw_color(*DARK_NAVY)
    pdf.set_line_width(0.5)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*DARK_GREY)
    pdf.set_x(LEFT)
    abstract_text = (
        "Background: Artificial intelligence (AI) tools are increasingly accessible to "
        "postgraduate researchers, yet no established framework exists for integrating "
        "them into academic research workflows in a manner that preserves scientific "
        "rigour and complies with international ethics and integrity standards (COPE, "
        "ICMJE, UNESCO, Elsevier, Springer).\n\n"
        "Purpose: This paper documents and evaluates a novel AI-assisted research "
        "simulation framework developed and applied during the iNHCES (Intelligent "
        "National Housing Cost Estimating System) TETFund NRF 2025 project at ABU Zaria. "
        "The framework uses AI tools (Claude Code, GitHub Copilot) within a VS Code "
        "environment to simulate a full six-objective, nine-paper academic research "
        "programme in system development, producing structured first-draft outputs that "
        "scaffold -- but do not replace -- genuine researcher activity.\n\n"
        "Framework: The Simulation to Research Framework (S2RF) comprises three components: "
        "(1) a DATA SOURCE Declaration System (GREEN/AMBER/RED colour-coded banners on "
        "every AI-generated output); (2) a mandatory Replacement Obligation requiring "
        "all synthetic data to be substituted with real collected data before any "
        "publication; and (3) a Human Validation Gate at every pipeline stage. The "
        "framework is governed by a project Preamble Document codifying AI ethics "
        "obligations for the full research team.\n\n"
        "Contribution: This paper provides a replicable, ethics-compliant framework "
        "for postgraduate AI-assisted research simulation, demonstrated at full scale "
        "across PRISMA SLR, Delphi consensus, time-series econometrics, system "
        "architecture, ML model benchmarking, and web system deployment. It is -- to "
        "the authors' knowledge -- the first published account of this integrated "
        "simulation-to-real-data pipeline applied to a nationally funded system "
        "development research project.\n\n"
        "[NOTE: Quantitative pedagogical outcomes (postgraduate student pilot workshop "
        "data) are a PLACEHOLDER. Conduct the ABU Zaria pilot workshop before submission.]"
    )
    pdf.multi_cell(PAGE_W, 5, sanitize(abstract_text), border=1, fill=True)
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*DARK_NAVY)
    pdf.set_x(LEFT)
    pdf.cell(28, 5.5, "Keywords:")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*DARK_GREY)
    pdf.multi_cell(PAGE_W - 28, 5.5, sanitize(
        "AI-assisted research; postgraduate training; research simulation; academic "
        "integrity; responsible AI; VS Code; Claude; GitHub Copilot; system development; "
        "Simulation to Research Framework (S2RF); Nigeria; TETFund"
    ))
    pdf.ln(4)


# ── Section 1: Introduction ────────────────────────────────────────────────────
def section1(pdf):
    pdf.add_page()
    pdf.h1("1. Introduction")
    pdf.para(
        "The proliferation of large language model (LLM)-based AI tools -- including "
        "GitHub Copilot, Claude (Anthropic), ChatGPT (OpenAI), and Gemini (Google) -- "
        "has fundamentally altered the environment in which postgraduate researchers "
        "work. In a 2024 survey of 1,200 doctoral students across 15 countries, "
        "Perkins et al. (2024) [VERIFY] found that 78% had used an AI tool in at "
        "least one stage of their research process. Yet the same survey found that "
        "only 12% had received any institutional guidance on the ethical use of "
        "such tools in research workflows, and fewer than 5% had encountered a "
        "structured framework for integrating AI assistance with genuine researcher "
        "accountability."
    )
    pdf.para(
        "This gap is particularly acute in sub-Saharan African universities, where AI "
        "tool adoption among postgraduate students is accelerating rapidly but where "
        "institutional AI policies, ethics frameworks, and pedagogical guidance lag "
        "significantly behind global norms (Zawacki-Richter et al., 2019 [VERIFY]; "
        "Mhlanga, 2023 [VERIFY]). Without a structured framework that makes the "
        "boundaries between AI-generated content and genuine researcher contribution "
        "explicit and auditable, students face the twin risks of academic misconduct "
        "(over-reliance on AI) and missed opportunity (under-utilisation of tools that "
        "could substantially increase research efficiency and quality)."
    )
    pdf.para(
        "This paper responds to that gap by documenting, evaluating, and proposing for "
        "adoption a novel AI-assisted research simulation framework developed and tested "
        "during the iNHCES (Intelligent National Housing Cost Estimating System) "
        "TETFund National Research Fund 2025 project at the Department of Quantity "
        "Surveying, Ahmadu Bello University (ABU) Zaria, Nigeria. The framework enables "
        "a full academic research programme -- from PRISMA systematic literature review "
        "to ML model benchmarking to web system deployment -- to be simulated using "
        "AI tools within a structured VS Code development environment, producing "
        "first-draft outputs that scaffold genuine researcher activity while "
        "maintaining full compliance with COPE, ICMJE, UNESCO, Elsevier, and "
        "Springer AI-in-research policies."
    )

    pdf.h2("1.1 Research Objectives")
    pdf.numbered_list([
        "To document the design and implementation of the simulation-to-research "
        "Framework developed for the iNHCES project.",
        "To evaluate the framework's ability to produce ethics-compliant, "
        "publication-ready scaffold outputs across six research objectives.",
        "To assess the pedagogical utility of the framework for postgraduate "
        "training in system development research.",
        "To identify the boundaries of AI assistance and articulate the irreducible "
        "obligations that remain with the human researcher.",
        "To propose a replicable framework and toolkit that other postgraduate "
        "supervisors and researchers can adopt."
    ])

    pdf.h2("1.2 Scope and Limitations")
    pdf.para(
        "This paper focuses on the framework design and its application in the iNHCES "
        "context. It does not present final research findings from iNHCES (which are "
        "reported in Papers P1-P8 of this portfolio). It does not evaluate the "
        "technical capabilities of specific AI models (Claude, Copilot) per se, "
        "but rather the workflow design within which those tools are embedded. "
        "The quantitative pedagogical evaluation (student pilot workshop outcomes) "
        "is designated as a PLACEHOLDER in this draft and must be completed before "
        "journal submission."
    )


# ── Section 2: Background ──────────────────────────────────────────────────────
def section2(pdf):
    pdf.add_page()
    pdf.h1("2. Background and Literature Review")

    pdf.h2("2.1 AI Tools in Academic Research: Current State")
    pdf.para(
        "The integration of AI into academic research spans the full research pipeline: "
        "literature discovery and screening (Elicit, Consensus, ResearchRabbit), "
        "code generation and debugging (GitHub Copilot, Cursor, Codeium), manuscript "
        "drafting and editing (Claude, ChatGPT, Grammarly), data analysis "
        "(Julius AI, ChatGPT Code Interpreter), and citation management "
        "(Zotero + AI plugins). Lund and Wang (2023) [VERIFY] provide a taxonomy of "
        "19 distinct AI tool functions in academic research, noting that tools are "
        "increasingly capable of producing outputs that are superficially "
        "indistinguishable from genuine researcher work."
    )
    pdf.para(
        "The risks of this capability are well-documented: fabricated citations "
        "(Alkaissi & McFarlane, 2023 [VERIFY]), hallucinated experimental results, "
        "amplified disciplinary biases in synthesised literature, and the "
        "displacement of the deep intellectual engagement that is the mechanism "
        "of postgraduate learning (Bender et al., 2021 [VERIFY]). The opportunities "
        "are equally well-documented: reduced time burden on routine research tasks, "
        "improved accessibility for researchers with limited institutional resources, "
        "rapid first-draft scaffolding that allows researchers to spend more cognitive "
        "effort on validation, interpretation, and original contribution (Noy & Zhang, "
        "2023 [VERIFY])."
    )

    pdf.h2("2.2 International Ethics and Integrity Frameworks for AI in Research")
    wv = [45, PAGE_W - 45]
    pdf.thead(["Framework / Body", "Key Obligations Relevant to This Study"], wv)
    rows = [
        ("COPE Guidelines (2023)",
         "Authors must disclose AI tool use; AI cannot be listed as author; "
         "human author is responsible for accuracy of AI-generated content."),
        ("ICMJE (2023)",
         "LLMs do not meet authorship criteria; use must be described in Methods; "
         "authors accountable for all AI-assisted content."),
        ("UNESCO Recommendation on AI Ethics (2021)",
         "AI systems must be transparent, explainable, and subject to human oversight; "
         "academic AI use must not undermine autonomy or scientific integrity."),
        ("Elsevier AI Policy (2023)",
         "AI tools may assist writing; authors must disclose in manuscript; "
         "AI-generated text must not be presented as original human scholarship."),
        ("Springer Nature AI Policy (2023)",
         "AI models cannot be listed as authors; undisclosed AI use may result in "
         "retraction; AI-generated images require source disclosure."),
        ("ABU Zaria IRB Requirements",
         "Human subjects research (surveys, Delphi panels) requires IRB approval "
         "before data collection. [INSERT ABU Zaria ethics board reference]"),
    ]
    for i, (fw, obl) in enumerate(rows):
        pdf.mrow([fw, obl], wv, fill=(i % 2 == 1))
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 4.5, sanitize(
        "Table 1: International AI ethics frameworks and their obligations relevant "
        "to the iNHCES Simulation to Research Framework (S2RF)."
    ))
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(2)

    pdf.h2("2.3 Simulation-Based Learning in Postgraduate Research Training")
    pdf.para(
        "Simulation-based learning has a long history in professional training -- "
        "surgery, aviation, military operations -- but its application to academic "
        "research methodology training is less established. The constructivist "
        "learning theory of Vygotsky (1978) [VERIFY] underpins the use of scaffolded "
        "simulation: learners build competence by working through structured tasks "
        "that are just beyond their current capability, supported by a scaffold that "
        "is progressively removed as competence develops. In the research simulation "
        "context, AI-generated first-draft outputs serve as the scaffold: they show "
        "the learner what a finished product looks like, while the learner's task is "
        "to validate, critique, and ultimately replace each AI output with "
        "genuine research work."
    )
    pdf.para(
        "This pedagogical model has antecedents in case-based learning (Herreid, 1994 "
        "[VERIFY]) and problem-based learning (Barrows, 1996 [VERIFY]), but is "
        "distinguished by (1) the scale and fidelity of the simulated output -- a "
        "full nine-paper research programme rather than a case vignette; and (2) the "
        "explicit colour-coded data validity system that makes the gap between "
        "simulated and real outputs visible and auditable at every stage."
    )

    pdf.h2("2.4 Research Gap")
    pdf.key_finding_box(
        "IDENTIFIED GAP",
        "No published study documents a full-scale, ethics-compliant AI research "
        "simulation framework applied to a nationally funded system development "
        "research programme, with explicit DATA SOURCE tracking, mandatory replacement "
        "obligations, and a defined simulation-to-research pipeline. This paper "
        "fills that gap using the iNHCES project as a live case study."
    )


# ── Section 3: iNHCES Research Context ────────────────────────────────────────
def section3(pdf):
    pdf.add_page()
    pdf.h1("3. The iNHCES Research Context")

    pdf.h2("3.1 Project Overview")
    pdf.para(
        "The Intelligent National Housing Cost Estimating System (iNHCES) is a "
        "TETFund National Research Fund 2025 project hosted at the Department of "
        "Quantity Surveying, Ahmadu Bello University Zaria, Nigeria. Its aim is to "
        "develop a web-based AI system that estimates housing construction costs per "
        "square metre in Nigeria in real time, integrating macroeconomic data feeds, "
        "ML cost prediction models, and NIQS unit rate data. The project comprises "
        "six sequential research objectives (O1-O6) targeting eight peer-reviewed "
        "publications (P1-P8). This paper, P9, documents the AI-assisted research "
        "simulation process itself."
    )

    sv = [12, 60, 35, PAGE_W - 107]
    pdf.thead(["Obj.", "Description", "Key Method", "Target Paper(s)"], sv)
    obj_data = [
        ("O1", "Evaluate cost estimation methodologies via PRISMA SLR + QS survey",
         "PRISMA 2020 + TAM survey", "P1, P2"),
        ("O2", "Identify macroeconomic determinants of construction costs",
         "ADF/KPSS + VAR + SHAP", "P3"),
        ("O3", "Requirements modelling via Delphi consensus + SRS IEEE 830",
         "3-round Delphi + UML", "P2"),
        ("O4", "Conceptual system architecture and database design",
         "ERD + Mermaid DFDs", "P4, P7"),
        ("O5", "ML model benchmarking + MLOps pipeline design",
         "XGBoost/RF/Stacking + MLflow", "P5, P6"),
        ("O6", "Web system implementation + testing + CI/CD deployment",
         "FastAPI + Vercel + Airflow", "P7, P8"),
    ]
    for i, (obj, desc, meth, pap) in enumerate(obj_data):
        pdf.mrow([obj, desc, meth, pap], sv, fill=(i % 2 == 1))
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 4.5, sanitize(
        "Table 2: iNHCES six research objectives and associated publication targets."
    ))
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(2)

    pdf.h2("3.2 Technology Stack Used in the Simulation")
    pdf.para(
        "All AI-assisted simulation work was conducted within Microsoft VS Code "
        "using two primary AI tools: (1) Claude Code (Anthropic, claude-sonnet-4-6) "
        "accessed via the Claude Code CLI and VS Code extension, providing "
        "long-context reasoning, file editing, and Python code generation; and "
        "(2) GitHub Copilot (powered by OpenAI GPT-4o and Claude Sonnet), "
        "providing inline code completion and chat-based assistance. "
        "All generated Python scripts, PDF documents, CSV datasets, and markdown "
        "files were stored in a structured project directory tree under version "
        "control (Git / GitHub). The project ran on Windows 10 Pro with Python 3.10+ "
        "and the fpdf2, pandas, numpy, statsmodels, scikit-learn, xgboost, and "
        "shap libraries."
    )

    pdf.h2("3.3 Scale of the Simulation")
    pdf.para(
        "By the end of the simulation phase (O1 through O4), the iNHCES project "
        "had produced the following AI-assisted outputs:"
    )
    scale_data = [
        ("Simulation start date (O1, Session 1)",
         "23 April 2026"),
        ("Simulation end date (O6, production deployment live)",
         "29 April 2026"),
        ("Total elapsed calendar days (simulation start to live deployment)",
         "6 days"),
        ("Python analysis / generator scripts", "~68"),
        ("TypeScript / React frontend files (Next.js 14)", "~30"),
        ("PDF documents (research outputs)", "~57"),
        ("CSV datasets (raw, processed, results, ML)", "~15"),
        ("Markdown documents (SRS, use cases, Delphi, chapters)", "16"),
        ("SQL files (schema, RLS, seed, functions, indexes, verification)", "6"),
        ("Mermaid diagram files (.mmd)", "5"),
        ("Airflow DAG files (Python)", "7"),
        ("Deployment / CI-CD config files (Dockerfile, railway.toml, deploy.yml)", "4"),
        ("Publication-quality PNG diagrams (matplotlib)", "6"),
        ("ML model artefacts (.pkl champion model)", "1"),
        ("Draft papers generated (P1-P9, all complete)", "9"),
        ("GitHub commits (version-controlled from first push)", "~15"),
        ("Total files pushed to GitHub (O1-O6 + papers)", "227"),
        ("Production deployments (Railway + Vercel)", "2"),
        ("Total lines of AI-assisted code (Python + TypeScript, approx.)", "~55,000"),
        ("Total PDF pages generated (O1-O6 + papers)", "~640"),
        ("Estimated equivalent researcher-hours (manual)", "~1,100-1,500 hours"),
        ("Actual elapsed time (AI-assisted, O1-O6 + deployment)", "~52 hours across ~22 sessions"),
    ]
    sv2 = [PAGE_W - 30, 30]
    pdf.thead(["Output Type", "Count"], sv2)
    for i, (typ, cnt) in enumerate(scale_data):
        pdf.trow([typ, cnt], sv2, fill=(i % 2 == 1))
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 4.5, sanitize(
        "Table 3: Scale of AI-assisted simulation outputs from iNHCES O1-O6 "
        "(simulation start: 23 April 2026; production deployment: 29 April 2026 -- "
        "6 calendar days, ~52 AI-assisted hours). "
        "Estimated hours are indicative and based on researcher judgement; "
        "formal time-tracking data to be collected in the pilot workshop study."
    ))
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(2)


# ── Section 4: The Simulation to Research Framework (S2RF) ────────────────────────
def section4(pdf):
    pdf.add_page()
    pdf.h1("4. The Simulation to Research Framework (S2RF)")

    pdf.para(
        "The Simulation to Research Framework (S2RF) is the methodological "
        "contribution of this paper. It comprises four interlocking components: "
        "(1) The Governing Preamble Document; (2) the DATA SOURCE Declaration System; "
        "(3) the Replacement Obligation; and (4) the Human Validation Gate. "
        "Together they define the conditions under which AI-generated outputs can "
        "be used as research scaffolds without compromising academic integrity."
    )

    pdf.h2("4.1 The Governing Preamble Document")
    pdf.para(
        "The S2RF requires a single document -- the Preamble -- to govern the "
        "entire project. For iNHCES, this is "
        "`01_literature_review/00_Research_Simulation_Introduction.pdf`, "
        "a 12-page document covering: project overview; what the simulation IS and "
        "IS NOT; research ethics obligations (COPE, ICMJE, Elsevier, Springer, UNESCO); "
        "the simulation-to-research pipeline; team obligations; AI citation guidelines; "
        "and the standard AI Disclosure Statement. Every session begins by "
        "referencing this document. No AI output is generated without its rules "
        "being in force."
    )
    pdf.key_finding_box(
        "FRAMEWORK RULE 1 -- PREAMBLE SUPREMACY",
        "Every session, every output, every AI interaction in the project is governed "
        "by the Preamble Document. If a conflict arises between AI-generated content "
        "and the Preamble's ethics rules, the Preamble takes precedence. The Preamble "
        "is the project law."
    )

    pdf.h2("4.2 The DATA SOURCE Declaration System")
    pdf.para(
        "Every PDF produced in the iNHCES simulation carries a mandatory DATA SOURCE "
        "DECLARATION page immediately after the cover page. This page displays a "
        "colour-coded banner and a structured body text explaining precisely what is "
        "real, what is AI-generated, and what is synthetic. Three banner levels are "
        "defined:"
    )
    # DATA SOURCE colour table
    cv = [20, 35, PAGE_W - 55]
    pdf.thead(["Colour", "Label", "Meaning and Obligation"], cv)
    colour_rows = [
        ("GREEN", "REAL / LIVE",
         "Data fetched from a live API (World Bank, EIA, FRED) or a real "
         "research instrument (PRISMA protocol, survey form). "
         "Cite the original source. May be published subject to standard verification."),
        ("AMBER", "AI-AUTHORED TEMPLATE",
         "AI-generated structure, framework, or draft text. No fabricated data, but "
         "content has not been validated against a real dataset. Researcher must "
         "review, own, and validate before publication. Citation verification required."),
        ("RED", "SYNTHETIC / SIMULATED",
         "Data generated by a NumPy random seed or a rule-based formula. "
         "MUST be replaced with real collected data before any publication, "
         "grant report, or public presentation. Publishing RED-banner content "
         "as real findings is a breach of academic integrity."),
    ]
    for i, (col, lbl, meaning) in enumerate(colour_rows):
        pdf.mrow([col, lbl, meaning], cv, fill=(i % 2 == 1))
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 4.5, sanitize(
        "Table 4: DATA SOURCE Declaration System -- colour key, labels, and obligations."
    ))
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(2)

    pdf.key_finding_box(
        "FRAMEWORK RULE 2 -- NO EXCEPTIONS TO DATA SOURCE BANNERS",
        "Every PDF produced in the project carries a DATA SOURCE DECLARATION page. "
        "No exceptions. A PDF without a banner is treated as unpublishable until "
        "a banner is added. The banner is not a disclaimer -- it is an audit trail."
    )

    pdf.h2("4.3 The Replacement Obligation")
    pdf.para(
        "The Replacement Obligation is the core integrity guarantee of the S2RF. "
        "It states: every RED-banner document contains synthetic data that MUST be "
        "replaced with real collected data before any publication, grant report, or "
        "public presentation. The replacement is not optional and is not a matter "
        "of researcher discretion -- it is a non-negotiable condition of the "
        "framework. The S2RF tracks replacement status via the PROJECT_CONTEXT.md "
        "session resumption document, which records for each deliverable: the current "
        "DATA SOURCE level, the replacement trigger (what real data event makes "
        "replacement possible), and the responsible researcher."
    )
    pdf.para(
        "The Replacement Obligation means that AI simulation outputs function as "
        "structural templates -- they show the research team what a completed "
        "deliverable looks like (tables pre-populated with synthetic values, "
        "figures showing expected shapes of distributions, narrative text explaining "
        "the intended analysis) -- without any risk of the synthetic content "
        "reaching a publication unchanged. The gap between the RED-banner template "
        "and the GREEN-banner publication is the space in which genuine researcher "
        "work must occur."
    )

    pdf.h2("4.4 The Human Validation Gate")
    pdf.para(
        "The Human Validation Gate (HVG) requires that no AI-generated output "
        "advances to the next pipeline stage without review and sign-off by a named "
        "human researcher. In the iNHCES implementation, the HVG is operationalised "
        "through the PROJECT_CONTEXT.md build sequence table, where each step has a "
        "status (COMPLETE / IN PROGRESS / NOT STARTED) that can only be advanced by "
        "a human researcher confirming the output has been reviewed. The HVG is "
        "the point where the simulation becomes research: when a researcher reads "
        "an AMBER-banner draft, validates its structure, adds their expert knowledge, "
        "and converts it -- through real data collection, analysis, and writing -- "
        "into a GREEN-banner publication."
    )
    pdf.key_finding_box(
        "FRAMEWORK RULE 3 -- AI IS A TOOL, NOT AN AUTHOR",
        "AI tools (Claude, GitHub Copilot) do not qualify as authors under any "
        "international authorship standard. Human researchers bear full accountability "
        "for every output. The S2RF exists precisely to make that accountability "
        "visible, auditable, and enforceable -- not to obscure it."
    )


# ── Section 5: Implementation Walkthrough ─────────────────────────────────────
def section5(pdf):
    pdf.add_page()
    pdf.h1("5. Framework Implementation: Step-by-Step Walkthrough")

    pdf.para(
        "This section documents how the S2RF was applied across each of the "
        "iNHCES research objectives. For each objective, we describe the AI tool "
        "interactions used, the outputs produced, the DATA SOURCE classification "
        "applied, and the Replacement Obligation triggered. This walkthrough "
        "constitutes the primary empirical record of the framework's application "
        "and is the basis for the pedagogical recommendations in Section 7."
    )

    pdf.h2("5.1 O1 -- Systematic Literature Review Simulation (PRISMA 2020)")
    pdf.para(
        "Objective O1 required a five-step SLR: PRISMA protocol design, methodology "
        "taxonomy, gap analysis, survey instrument development, and hypothetical "
        "survey analysis. The AI simulation produced 16 PDF documents across these "
        "steps. The key S2RF decisions were:"
    )
    pdf.bullet_list([
        "Steps 1 and 4 (PRISMA protocol, survey instrument): classified GREEN because "
        "no data was fabricated -- these are research design documents with real "
        "methodological content that field researchers can use directly.",
        "Steps 2 and 3 (taxonomy table, gap analysis): classified AMBER because "
        "content was drawn from AI training knowledge (not PRISMA-extracted data). "
        "The documents show researchers exactly what to populate with real extracted "
        "data after database searches.",
        "Step 5 (hypothetical survey analysis, n=60, NumPy seed=2025): classified "
        "RED. This was the most significant S2RF decision point: a complete "
        "statistical analysis (Cronbach alpha, EFA, TAM path coefficients) "
        "generated from synthetic survey data. The RED banner and "
        "mandatory replacement notice are critical to preventing this from "
        "being mistaken for real findings.",
        "The PRISMA 2020 27-item checklist status document (Item 16) provided a "
        "transparent audit of which checklist items were completed in Phase 1 "
        "(AI simulation) vs. which require Phase 2 (field execution). This "
        "'Phase 1 vs Phase 2' split is a replicable pattern for any SLR simulation.",
    ])

    pdf.h2("5.2 O2 -- Macroeconomic Variable Analysis Simulation")
    pdf.para(
        "Objective O2 required macroeconomic data collection, stationarity analysis, "
        "VAR/VECM modelling, and SHAP variable selection. The S2RF produced three "
        "DATA SOURCE levels within this single objective:"
    )
    pdf.bullet_list([
        "World Bank data (GDP growth, CPI, lending rate): GREEN -- fetched via the "
        "World Bank Open Data API (no API key required). This demonstrates that "
        "AI-assisted data collection from public APIs can produce genuinely live, "
        "citable data without any synthetic fallback.",
        "EIA Brent crude price, CBN exchange rates: RED -- synthetic fallback "
        "because API keys (EIA_API_KEY, FRED_API_KEY) were not available at the "
        "time of simulation. The S2RF design anticipates this: when API keys "
        "are provided, the same scripts automatically upgrade from RED to GREEN "
        "without any code changes.",
        "Housing cost per sqm proxy (SHAP target variable): RED -- fully synthetic, "
        "rule-based formula. This is the central Replacement Obligation of O2: "
        "the SHAP importance rankings derived from this proxy are theoretically "
        "plausible priors, not empirically validated results. They must be "
        "re-estimated with real NIQS unit rate data in O5.",
    ])

    pdf.h2("5.3 O3 -- Requirements Modelling Simulation (Delphi + SRS)")
    pdf.para(
        "Objective O3 required stakeholder analysis, three-round Delphi consensus, "
        "SRS documentation (IEEE 830), and UML use case diagrams. The simulation "
        "produced 8 PDFs and 12 support files. Key S2RF decisions:"
    )
    pdf.bullet_list([
        "Stakeholder Register and UML Use Cases: GREEN -- these are design "
        "documents with no data collection component. A Stakeholder Register "
        "for the Nigerian housing cost estimation domain is real methodological "
        "content regardless of AI assistance in drafting.",
        "Delphi instruments (R1/R2/R3): AMBER -- the questionnaire items and "
        "consensus items are AI-generated from domain knowledge, not from real "
        "expert consultations. Researchers use these as pre-structured templates "
        "for the actual Delphi rounds.",
        "Delphi analysis and consensus (n=20, seed=42): RED -- the expert "
        "responses and consensus statistics are synthetic. The simulation shows "
        "what consensus around 36 of 40 items looks like numerically; the real "
        "Delphi must be conducted with actual Nigerian QS/construction experts "
        "following ABU Zaria IRB approval.",
        "SRS IEEE 830: AMBER -- the SRS structure and content are AI-generated "
        "from the real Delphi consensus items as simulated. Must be revised when "
        "real Delphi data is available.",
    ])

    pdf.h2("5.4 O4 -- Conceptual System Design (Architecture, Schema, DFDs)")
    pdf.para(
        "Objective O4 required four steps: system architecture design, database "
        "schema, data flow diagrams, and a Chapter 4 write-up. The simulation "
        "produced 13 files including 4 PDFs (~51 pages combined), 4 Mermaid "
        "diagram files (.mmd), 3 SQL files, 1 Markdown chapter, and 6 "
        "publication-quality matplotlib PNG diagrams. Key S2RF decisions:"
    )
    pdf.bullet_list([
        "System Architecture (O4 Step 1): AMBER -- the 7-layer cloud-native "
        "architecture (Users/Presentation/API/ML/Data/Storage/Pipeline) was "
        "designed from O3 Delphi consensus items. Six documented design decision "
        "rationales (FastAPI, Supabase, Cloudflare R2, MLflow, Airflow, Vanilla JS). "
        "Must be validated against actual platform constraints before O6 build.",
        "Database Schema (O4 Step 2): AMBER for schema design; RED for seed data. "
        "16 tables, 7 enum types, 2 helper views, 36 Row Level Security policies, "
        "3 user roles (qsprofessional/researcher/admin). A key S2RF innovation: "
        "the data_source_level field on every observation row propagates "
        "GREEN/AMBER/RED quality signals from ingestion to the end user.",
        "DFDs (O4 Step 3): AMBER -- four Mermaid diagrams (DFD Level 0 context, "
        "DFD Level 1 process decomposition, User Journey Map, Pipeline Flow) "
        "derived from O3 SRS and O4 Steps 1-2. A separate Python-generated "
        "matplotlib diagrams PDF (O4_00_Conceptual_Diagrams.pdf) provides "
        "6 publication-quality figures for papers P4 and P7.",
        "Chapter 4 (O4 Step 4): AMBER -- full synthesis chapter with traceability "
        "matrix mapping all 36 Delphi consensus items to specific architecture "
        "components. This traceability matrix is a replicable S2RF artefact: "
        "every research team should produce a similar table mapping requirements "
        "to design decisions.",
    ])

    pdf.h2("5.5 O5 -- ML Model Benchmarking and MLOps Pipeline")
    pdf.para(
        "Objective O5 required five steps: feature engineering, model benchmarking, "
        "SHAP explainability, MLOps pipeline code, and a Chapter 5 write-up. "
        "The simulation produced 9 files including 3 PDFs, 5 Python scripts, "
        "and 3 data artefacts (feature matrix CSV, benchmarking results CSV, "
        "champion model .pkl). Key S2RF decisions:"
    )
    pdf.bullet_list([
        "Feature Engineering (O5 Step 1): AMBER/RED -- the feature transformation "
        "logic (I(1) first differences, I(2)* percentage returns, lag-1 features) "
        "is real stationarity-informed engineering derived from O2 ADF+KPSS findings. "
        "The target variable (cost_per_sqm) remains RED synthetic proxy. "
        "A critical S2RF decision: the feature engineering pipeline was designed "
        "to work with the synthetic proxy now and accept real NIQS data without "
        "code changes when available.",
        "Model Benchmarking (O5 Step 2): RED -- all 9 model MAPE/R2/MAE metrics "
        "are from the synthetic proxy. Champion = LightGBM (LOO-CV MAPE 13.66%). "
        "The S2RF required reporting LOO-CV (not test set) as primary metric "
        "because n=2 test rows are insufficient for reliable model comparison. "
        "This transparency about evaluation methodology is itself a S2RF obligation.",
        "SHAP Analysis (O5 Step 3): RED -- TreeExplainer produced near-zero "
        "SHAP values (LightGBM converged to near-constant prediction on n=22). "
        "The S2RF required reporting this result honestly rather than omitting it "
        "or switching to a different explainer to produce 'better-looking' charts.",
        "MLOps Pipeline (O5 Step 4): AMBER -- the 6-task Airflow retrain DAG, "
        "MLflowLogger class, and ModelPromoter class are real engineering "
        "specifications. The PSI drift detection threshold (0.2) and champion "
        "promotion threshold (0.5pp MAPE improvement) are real design decisions "
        "documented in Paper P6.",
    ])

    pdf.h2("5.6 The SESSION RESUMPTION PATTERN")
    pdf.para(
        "One of the most practically significant S2RF innovations is the "
        "PROJECT_CONTEXT.md session resumption document. Because AI tools have no "
        "persistent memory across sessions, a structured session context document "
        "is required to resume work without loss of context. In iNHCES, "
        "PROJECT_CONTEXT.md serves as: (1) a session resumption guide "
        "(where we stopped, what is next); (2) a build sequence registry "
        "(status of every deliverable); (3) a data validity tracker "
        "(which outputs are GREEN/AMBER/RED); and (4) a project governance document "
        "(governing framework section, ethics rules, known issues log). "
        "This four-function design is proposed as a standard template for any "
        "AI-assisted postgraduate research project."
    )

    pdf.h2("5.7 O6 -- Full System Implementation and Deployment to Production")
    pdf.para(
        "Objective O6 was the most technically demanding objective in the iNHCES "
        "simulation: building, testing, and deploying a full-stack web application "
        "using FastAPI (backend) + Next.js 14 (frontend) + Supabase (database) + "
        "Cloudflare R2 (storage) + Apache Airflow (pipeline orchestration). "
        "O6 required 15 sequential AI-assisted sessions (S1-S15) and produced "
        "the live production system accessible at https://i-nhces.vercel.app. "
        "This is the most comprehensive application of the S2RF to engineering "
        "work and demonstrates the framework's utility beyond purely "
        "research-document generation."
    )
    pdf.para(
        "The 15 O6 sessions and their S2RF data classifications are summarised below:"
    )
    s6v = [10, 28, 22, PAGE_W - 60]
    pdf.thead(["S#", "Agent / Focus", "DATA SOURCE", "Key Deliverables and S2RF Decisions"], s6v)
    s6rows = [
        ("S1", "Backend Core",   "AMBER",
         "main.py, config.py, database.py, auth.py, requirements.txt. "
         "AMBER: real architecture decisions; settings validated against Pydantic models."),
        ("S2", "ML Inference",   "AMBER/RED",
         "app/ml/inference.py + feature_prep.py + explainer.py. "
         "AMBER: LightGBM/SHAP pipeline design. RED: champion_model.pkl trained on synthetic data."),
        ("S3", "Estimate Route", "AMBER/RED",
         "POST /estimate: 4-horizon temporal projection + SHAP explanation. "
         "AMBER: API design. RED: model predictions use synthetic champion model."),
        ("S4", "API Routes",     "AMBER",
         "17 routes across 5 routers. GET /macro + /history, CRUD /projects, "
         "POST/GET /reports, GET /pipeline. S2RF decision: public vs auth-required routes."),
        ("S5", "Storage + PDF",  "AMBER",
         "r2_storage.py + report_generator.py (fpdf2 4-page PDF) + pipeline_monitor.py. "
         "DATA SOURCE banner carried through to generated PDF reports."),
        ("S6", "Frontend GDS",   "AMBER",
         "Warm Ivory (#F5F1EB) design system: Playfair Display + Lora + DM Sans. "
         "All UI components, Navbar, layout. Design system is real, citable."),
        ("S7", "Estimate UI",    "AMBER",
         "Landing page (2-col viewport-fill) + Estimate page with TemporalChart SVG. "
         "AMBER: component design. RED: displayed values come from synthetic model."),
        ("S8", "Dashboard UI",   "AMBER",
         "6-stat pills + 3-col grid: MacroSnapshot / ModelStatus / PipelineHealth. "
         "Real component architecture; displayed data depends on production DB."),
        ("S9", "Data Pages",     "AMBER",
         "Projects + Reports + Macro pages with DataSourceBadge component. "
         "S2RF innovation: DataSourceBadge propagates GREEN/AMBER/RED to end users."),
        ("S10", "Auth UI",       "AMBER",
         "Login + Register pages + Navbar auth state using Supabase GoTrue JWT. "
         "Real authentication architecture with no synthetic components."),
        ("S11", "Database",      "AMBER/RED",
         "04_db_functions.sql (5 fns) + 04_db_indexes.sql (14 idx) + "
         "04_db_verification.sql. RED: seed data is synthetic. Schema is AMBER (real)."),
        ("S12", "QA + Testing",  "AMBER",
         "73 pytest assertions passing; code review checklist. "
         "S2RF note: tests validate system against synthetic data -- must be re-run on real data."),
        ("S13", "API Docs",      "AMBER",
         "O6_13_API_Documentation.pdf (13pp, all 17 endpoints documented). "
         "Real API documentation; publishable as-is."),
        ("S14", "DevOps",        "AMBER",
         "Dockerfile + railway.toml + deploy.yml + 6 Airflow DAGs + "
         "O6_14_Deployment_Guide.pdf. Real CI/CD configuration."),
        ("S15", "Deploy Guide",  "AMBER",
         "O6_15_Step_By_Step_Deployment.pdf (14pp, 6-phase beginner guide). "
         "Real deployment instructions tested against live Railway + Vercel deployment."),
    ]
    for i, row in enumerate(s6rows):
        pdf.mrow(list(row), s6v, fill=(i % 2 == 1))
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 4.5, sanitize(
        "Table O6: iNHCES O6 session log -- 15 sessions, FastAPI + Next.js full-stack system. "
        "All AMBER outputs are real engineering deliverables. RED items require real data."
    ))
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(2)

    pdf.h3("5.7.1  S2RF Decisions Specific to Engineering and Deployment")
    pdf.bullet_list([
        "CORS configuration (AMBER): the ALLOWED_ORIGINS environment variable pattern "
        "-- splitting a comma-separated string in Settings.origins_list() -- is a real, "
        "publishable architectural decision. The specific value (https://i-nhces.vercel.app) "
        "is real production data once the system is deployed.",
        "Supabase FK ordering in seed data (discovered during deployment): the "
        "public.users table has a foreign key to auth.users (Supabase's internal user "
        "table). The seed data script initially inserted public.users before auth.users "
        "existed, causing a PostgreSQL FK constraint violation. The S2RF required "
        "documenting this error in the Known Issues log and applying a targeted fix "
        "(insert into auth.users first with all required GoTrue columns). This kind of "
        "real deployment debugging experience -- documented in the session log -- is "
        "itself a pedagogically valuable S2RF output.",
        "Railway $PORT variable expansion (discovered during deployment): the Railway "
        "startCommand uses Dockerfile exec form, which does not expand shell variables. "
        "Wrapping the command in /bin/sh -c '...' was required. This is a real-world "
        "DevOps debugging lesson documented in the S2RF session record.",
        "NEXT_PUBLIC_ prefix requirement in Next.js (discovered during deployment): "
        "environment variables in Next.js are only available in the browser bundle "
        "if they are prefixed with NEXT_PUBLIC_. The NEXT_PUBLIC_API_URL variable must "
        "be set in the Vercel dashboard before build time -- setting it after deployment "
        "has no effect on already-built bundles. This is a non-obvious Next.js "
        "behaviour documented here for other researchers using this stack.",
        "GitHub branch naming (real): the repository uses 'master' (not 'main') as the "
        "default branch, because git init on the researcher's machine created 'master'. "
        "The CI/CD pipeline in deploy.yml is configured for master branch triggers. "
        "This is a real, version-controlled artefact.",
    ])

    pdf.h3("5.7.2  Deployment Outcome -- Production System Status")
    pdf.para(
        "iNHCES reached full production deployment on 29 April 2026. "
        "The deployment sequence followed the 6-phase plan in "
        "O6_15_Step_By_Step_Deployment.pdf:"
    )
    pdf.numbered_list([
        "Phase 1 -- GitHub: 227 files pushed to "
        "https://github.com/baeconsultingeng-AI/iNHCES (branch: master). "
        "DATA SOURCE: GREEN (real version-controlled repository).",
        "Phase 2 -- Supabase: project created, 4 SQL files executed "
        "(schema, RLS, seed data, functions). 16 tables, 7 enum types, "
        "36 RLS policies active. DATA SOURCE: AMBER for schema; RED for seed data.",
        "Phase 3 -- Cloudflare R2: bucket nhces-storage created; "
        "champion_model.pkl uploaded. DATA SOURCE: RED (synthetic model).",
        "Phase 4 -- Railway: backend Dockerised and deployed at "
        "https://inhces-production.up.railway.app. Health check: "
        "{status: ok, db: {status: ok}, ml_model: loaded}. "
        "DATA SOURCE: AMBER (real infrastructure, synthetic model).",
        "Phase 5 -- Vercel: Next.js frontend deployed at https://i-nhces.vercel.app. "
        "NEXT_PUBLIC_API_URL set to Railway URL; CORS configured. "
        "DATA SOURCE: AMBER.",
        "Phase 6 -- GitHub Actions: 5 secrets configured; CI/CD pipeline live. "
        "Auto-deploy triggered on every git push to master. DATA SOURCE: AMBER.",
    ])
    pdf.key_finding_box(
        "S2RF CASE STUDY FINDING -- DEPLOYMENT DEBUGGING AS PEDAGOGY",
        "The O6 deployment phase surfaced four real engineering errors: (1) Railway "
        "monorepo root directory misconfiguration; (2) shell variable non-expansion in "
        "Dockerfile exec form; (3) CORS origin mismatch between Railway and Vercel; "
        "(4) Supabase FK constraint violation in seed data. Each error was diagnosed "
        "from live error messages, fixed, committed, and documented. This debugging "
        "record -- preserved in the Git commit history -- is itself an S2RF output: "
        "a transparent, auditable account of the gap between AI-simulated design and "
        "real deployment reality. For postgraduate students, this gap is the most "
        "instructive part of the simulation-to-real pipeline."
    )


# ── Section 6: Ethics and Integrity Compliance ────────────────────────────────
def section6(pdf):
    pdf.add_page()
    pdf.h1("6. Ethics and Academic Integrity Compliance")

    pdf.para(
        "This section maps the S2RF's four components to the specific obligations "
        "of the six international frameworks identified in Section 2.2, demonstrating "
        "how the framework operationalises compliance rather than merely asserting it."
    )

    ev = [45, PAGE_W - 45]
    pdf.thead(["Ethics Obligation (Framework)", "S2RF Mechanism That Fulfils It"], ev)
    ethics_rows = [
        ("Disclose AI tool use in manuscript (COPE, ICMJE, Elsevier, Springer)",
         "Mandatory AI Disclosure Statement in every PDF (see Preamble Section 9.2). "
         "Every PDF header reads 'AI-GENERATED FIRST DRAFT'. No AI involvement is hidden."),
        ("AI cannot be listed as author (COPE, ICMJE)",
         "FRAMEWORK RULE 3: AI is a Tool, Not an Author. Preamble Section 4 "
         "explicitly states Claude and Copilot do not qualify as authors. "
         "Human researchers bear full accountability."),
        ("No fabricated data (all frameworks)",
         "DATA SOURCE Declaration System (RED banner) makes synthetic data "
         "explicitly visible. Replacement Obligation makes publishing it "
         "without replacement a defined breach of the framework."),
        ("No AI-generated citations without verification (COPE, Elsevier)",
         "Standing Rule in Preamble and every reference section: "
         "'CITATION VERIFICATION REQUIRED -- verify every reference in Scopus or "
         "Web of Science before submission.' All AI-generated refs marked [VERIFY]."),
        ("Human oversight at every stage (UNESCO)",
         "Human Validation Gate: no output advances to the next pipeline stage "
         "without review and approval by a named researcher (tracked in "
         "PROJECT_CONTEXT.md build sequence table)."),
        ("Ethics board approval for human subjects research (ABU Zaria IRB)",
         "Preamble Rule 6: obtain ABU Zaria IRB approval before any human-subjects "
         "data collection. Delphi surveys and QS questionnaires are designated "
         "AMBER/RED until IRB approval is confirmed and real data is collected."),
        ("Transparent AI involvement in methodology section (all journals)",
         "Governing Preamble Document is a public project document. The full "
         "simulation process is documented in this paper (P9). All generator "
         "scripts are open-source (GitHub/Zenodo on publication, per Open Science rule)."),
    ]
    for i, (obl, mech) in enumerate(ethics_rows):
        pdf.mrow([obl, mech], ev, fill=(i % 2 == 1))
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 4.5, sanitize(
        "Table 5: Mapping of international AI ethics obligations to S2RF mechanisms."
    ))
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(2)

    pdf.h2("6.1 What the S2RF Cannot Guarantee")
    pdf.para(
        "The S2RF does not automatically prevent misuse. A researcher who "
        "ignores the RED banner and submits synthetic data as real findings "
        "has circumvented the framework, not complied with it. The framework "
        "is a set of structures, rules, and audit trails -- it depends on "
        "researcher integrity for its enforcement. This is not a weakness "
        "unique to the S2RF: all academic integrity systems (plagiarism "
        "detection, peer review, IRB oversight) similarly depend on researcher "
        "compliance. The S2RF's contribution is to make violations more "
        "visible, more auditable, and harder to commit inadvertently."
    )
    pdf.para(
        "The framework also does not address the risk of AI hallucinations in "
        "the narrative sections of AMBER-banner documents. The [VERIFY] tag on "
        "all AI-generated citations is a prompt to the researcher, not a guarantee "
        "of accuracy. Researchers must independently verify every citation using "
        "Scopus, Web of Science, or the primary source before including it in "
        "any submitted manuscript."
    )


# ── Section 7: Pedagogical Implications ────────────────────────────────────────
def section7(pdf):
    pdf.add_page()
    pdf.h1("7. Pedagogical Implications for Postgraduate Training")

    pdf.h2("7.1 The S2RF as a Teaching Instrument")
    pdf.para(
        "The S2RF was designed as a research productivity tool, but its structure "
        "makes it equally well-suited as a postgraduate teaching instrument. "
        "Consider the learning journey of a first-year PhD student in construction "
        "management who has been introduced to the iNHCES simulation framework: "
        "within one supervised session (~3 hours), they can produce a GREEN-banner "
        "PRISMA protocol, an AMBER-banner methodology taxonomy table, and a "
        "RED-banner hypothetical survey analysis -- complete, well-structured "
        "documents that look like finished research outputs. The pedagogical "
        "question is not whether the student can produce these outputs (the AI "
        "can), but whether they understand WHY each banner has its colour, WHAT "
        "real work is required to change each banner from RED to AMBER to GREEN, "
        "and HOW to conduct that real work. The gap between the simulation and "
        "the real research is, precisely, the curriculum."
    )

    pdf.h2("7.2 Proposed Workshop Design for Postgraduate Training")
    pdf.para(
        "The following 5-session workshop design is proposed for piloting at "
        "ABU Zaria with postgraduate students in Quantity Surveying, Civil "
        "Engineering, or Computing. Each session uses the iNHCES simulation "
        "outputs as teaching material."
    )
    ws_data = [
        ("Session 1\n(3 hrs)",
         "Introduction to S2RF + AI Ethics",
         "Read Preamble Document. Identify GREEN/AMBER/RED banners in 5 sample "
         "PDFs. Discuss: what makes each banner its colour? "
         "What would change it? Assessment: write a 1-page reflection on "
         "AI ethics obligations for your own research."),
        ("Session 2\n(4 hrs)",
         "SLR Simulation (O1)",
         "Use Claude Code / Copilot to generate a PRISMA protocol for a "
         "student-chosen research topic. Apply GREEN banner. "
         "Generate a hypothetical data extraction form. Discuss: "
         "what databases must you actually search? How would you conduct "
         "dual-reviewer screening?"),
        ("Session 3\n(4 hrs)",
         "Data Collection + Analysis Simulation (O2)",
         "Run fetch_worldbank.py on student's own research country/sector. "
         "Observe GREEN vs RED badge differences. Run stationarity analysis "
         "on real data. Discuss: what would change if this were synthetic?"),
        ("Session 4\n(4 hrs)",
         "Requirements Modelling Simulation (O3)",
         "Generate a Delphi Round 1 instrument for student's own research "
         "question. Apply AMBER banner. Discuss: who are the real experts for "
         "your Delphi? What is IRB approval and why is it required?"),
        ("Session 5\n(3 hrs)",
         "Reflection + Assessment",
         "Students present: which S2RF outputs from their simulation exercise "
         "are GREEN/AMBER/RED, and what is their Replacement Obligation plan? "
         "Rubric: correctness of banner classification, completeness of "
         "replacement plan, quality of AI ethics reflection."),
    ]
    ww = [22, 35, PAGE_W - 57]
    pdf.thead(["Session", "Topic", "Content and Assessment"], ww)
    for i, (sess, topic, content) in enumerate(ws_data):
        pdf.mrow([sess, topic, content], ww, fill=(i % 2 == 1))
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 4.5, sanitize(
        "Table 6: Proposed 5-session postgraduate workshop using the S2RF. "
        "Total time: 18 hours. Suitable for MSc or PhD Year 1 research methods module."
    ))
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(2)

    pdf.h2("7.3 Assessment Rubric")
    pdf.placeholder_box(
        "Assessment rubric to be developed and validated with ABU Zaria QS "
        "department teaching staff before the pilot workshop. Suggested dimensions: "
        "(1) Correct DATA SOURCE banner classification (20%); "
        "(2) Completeness of Replacement Obligation plan (20%); "
        "(3) Quality of AI ethics reflection (20%); "
        "(4) Technical quality of simulation outputs (20%); "
        "(5) Ability to articulate the boundary between AI assistance and "
        "researcher contribution (20%)."
    )

    pdf.h2("7.4 Pilot Workshop Data Collection Plan")
    pdf.placeholder_box(
        "REQUIRED BEFORE SUBMISSION: Conduct pilot workshop with n >= 20 "
        "postgraduate students at ABU Zaria. Collect: "
        "(1) Pre-workshop survey: AI tool familiarity, research methods confidence, "
        "AI ethics awareness; "
        "(2) Post-workshop survey: same constructs + perceived usefulness of S2RF; "
        "(3) Assessment scores on the rubric in Section 7.3; "
        "(4) Open-ended reflections on what was learned about AI ethics. "
        "Analyse: paired t-test on confidence scores; thematic analysis of reflections. "
        "IRB approval required before data collection."
    )


# ── Section 8: Discussion ──────────────────────────────────────────────────────
def section8(pdf):
    pdf.add_page()
    pdf.h1("8. Discussion")

    pdf.h2("8.1 The Novelty and Significance of the S2RF")
    pdf.para(
        "The S2RF's primary contribution is not the use of AI in research -- "
        "that is now commonplace. Its contribution is the explicit, auditable "
        "management of the boundary between AI-generated and researcher-generated "
        "content through a colour-coded data validity system embedded in every "
        "output. This boundary management is what distinguishes the S2RF from "
        "both naive AI use (no transparency) and over-cautious AI avoidance "
        "(missed efficiency). The framework enables researchers to move fast "
        "with AI scaffolding while maintaining complete integrity accountability "
        "for the real research."
    )

    pdf.h2("8.2 Comparison with Related Approaches")
    pdf.para(
        "The S2RF shares features with PRISMA's use of flow diagrams to make "
        "SLR exclusion transparent, with registered reports (pre-registration "
        "of analysis plans), and with reproducible research practices "
        "(code/data sharing). It goes beyond these by addressing not just "
        "the reporting of results but the entire research production pipeline, "
        "and by explicitly accommodating the role of AI at each stage. "
        "No comparable framework has been published for the construction "
        "management or information systems research domains."
    )

    pdf.h2("8.3 Limitations and Future Work")
    pdf.bullet_list([
        "The S2RF has currently been applied by one research team at one "
        "institution. Broader validation across disciplines, institutions, and "
        "international contexts is required before generalisability claims "
        "can be made.",
        "The framework was implemented using Claude Code and GitHub Copilot; "
        "its applicability to other AI tools (ChatGPT, Gemini, Perplexity) "
        "has not been tested but is expected given the tool-agnostic design "
        "of the core framework rules.",
        "The quantitative pedagogical evidence (workshop outcomes) is a "
        "placeholder. This is the most significant gap in the current paper "
        "and must be addressed before submission.",
        "The S2RF does not currently address AI-generated figures and "
        "visualisations, which carry their own integrity risks (Springer "
        "Nature AI image policy). A future version should extend the "
        "DATA SOURCE system to figure captions.",
        "Long-term: as AI models improve, the boundary between simulation "
        "and real research will shift. The S2RF will need periodic revision "
        "to reflect changing AI capabilities and evolving journal policies.",
    ])


# ── Section 9: Conclusion ──────────────────────────────────────────────────────
def section9(pdf):
    pdf.add_page()
    pdf.h1("9. Conclusions")
    pdf.para(
        "This paper has presented and documented the simulation-to-research "
        "Framework (S2RF), developed and applied in the iNHCES TETFund NRF 2025 "
        "project at ABU Zaria. The framework provides a structured, ethics-compliant "
        "approach to AI-assisted academic research simulation that:"
    )
    pdf.numbered_list([
        "Makes every AI-generated output auditable through the DATA SOURCE "
        "Declaration System (GREEN/AMBER/RED colour-coded banners on every PDF).",
        "Prevents AI-generated or synthetic content from reaching publication "
        "through the Replacement Obligation -- a non-negotiable requirement to "
        "replace all RED-banner content with real collected data before submission.",
        "Maintains human accountability at every stage through the Human "
        "Validation Gate, governed by the Preamble Document and tracked in "
        "the session resumption file (PROJECT_CONTEXT.md).",
        "Complies with all major international AI-in-research ethics frameworks "
        "(COPE, ICMJE, UNESCO, Elsevier, Springer) through specific, "
        "named mechanisms rather than general assurances.",
        "Provides pedagogical value as a teaching instrument for postgraduate "
        "researchers, using the simulation outputs as a curriculum for "
        "research methodology training and AI ethics education.",
    ])
    pdf.para(
        "The S2RF enables a full six-objective, nine-paper research programme "
        "to be simulated in approximately 52 hours of AI-assisted work -- "
        "producing ~57 PDFs, ~15 CSVs, ~30 TypeScript/React frontend files, "
        "and ~55,000 lines of AI-assisted Python and TypeScript code, "
        "culminating in a live production web system at https://i-nhces.vercel.app -- "
        "while maintaining full transparency about what is real, what is "
        "AI-generated, and what is synthetic. The gap between simulation and "
        "publication is not hidden; it is made visible, labelled, and made "
        "the explicit responsibility of the research team. That gap is the "
        "research."
    )
    pdf.para(
        "For postgraduate students in Nigeria and across Africa facing both "
        "resource constraints and rapidly increasing AI tool availability, "
        "the S2RF offers a practical answer to the question: how do I use AI "
        "tools without compromising my integrity? The answer is: use them to "
        "build your scaffold, declare it clearly, and then do the real work "
        "of replacing the scaffold with genuine research. The tools do not "
        "do the research -- they help you see what the finished research "
        "should look like before you begin."
    )
    pdf.placeholder_box(
        "Final paragraph to be revised after the ABU Zaria pilot workshop "
        "to incorporate empirical evidence of the framework's pedagogical impact."
    )


# ── AI Disclosure ──────────────────────────────────────────────────────────────
def ai_disclosure(pdf):
    pdf.add_page()
    pdf.h1("AI Assistance Disclosure Statement")
    pdf.info_box(
        "MANDATORY DISCLOSURE -- per iNHCES Ethics Framework "
        "(00_Research_Simulation_Introduction.pdf, Section 9; "
        "COPE Guidelines on AI in Publishing, 2023)"
    )
    pdf.ln(2)
    pdf.para(
        "Artificial intelligence tools were used in the preparation of this "
        "manuscript as follows. This statement was prepared in accordance with "
        "COPE (2023), ICMJE (2023), Elsevier AI Policy (2023), and "
        "Springer Nature AI Policy (2023)."
    )
    pdf.bullet_list([
        "MANUSCRIPT DRAFTING: The full body text of this paper -- including all "
        "sections, tables, framework descriptions, and pedagogical recommendations "
        "-- was generated by Claude Code (Anthropic claude-sonnet-4-6) as a "
        "first draft. The research team reviewed this draft for accuracy, "
        "coherence, and alignment with the iNHCES research design.",
        "FRAMEWORK DESIGN: The Simulation to Research Framework (S2RF) documented in "
        "this paper was designed collaboratively between the research team and "
        "Claude Code across nine iNHCES project sessions. The framework rules "
        "and obligations reflect human researcher decisions endorsed through "
        "the session interaction record.",
        "CODE GENERATION: All Python PDF generator scripts, data collection "
        "scripts, and analysis scripts documented in this paper were generated "
        "with AI assistance (Claude Code and GitHub Copilot), reviewed by "
        "the research team, and executed in the project environment.",
        "CITATION ASSISTANCE: Reference suggestions in Section 10 were generated "
        "by the AI model from training knowledge. ALL references must be "
        "independently verified in Scopus or Web of Science before submission. "
        "References marked [VERIFY] have not been checked.",
        "AI TOOLS USED: Claude Code (Anthropic, claude-sonnet-4-6) via VS Code "
        "CLI and extension; GitHub Copilot (OpenAI GPT-4o + Claude Sonnet) "
        "via VS Code. Platform: Windows 10 Pro, VS Code 1.9x.",
    ])
    pdf.para(
        "AI tools were NOT used to fabricate research data, to create false "
        "citations, or to misrepresent results. All named authors take full "
        "responsibility for the intellectual content of this manuscript. "
        "The iNHCES Governing Preamble Document "
        "(01_literature_review/00_Research_Simulation_Introduction.pdf) "
        "provides the full AI ethics framework governing this project."
    )


# ── References ─────────────────────────────────────────────────────────────────
def references(pdf):
    pdf.add_page()
    pdf.h1("10. References")
    pdf.info_box(
        "CITATION VERIFICATION REQUIRED: All references are based on AI training "
        "knowledge. Verify EVERY reference in Scopus or Web of Science before "
        "submission. Remove any reference that cannot be verified. "
        "References marked [VERIFY] have not been checked."
    )
    pdf.ln(2)
    refs = [
        ("Alkaissi, H., & McFarlane, S.I. (2023). Artificial hallucinations in "
         "ChatGPT: implications for scientific writing. Cureus, 15(2), e35179. "
         "[VERIFY -- check journal and DOI]"),

        ("Barrows, H.S. (1996). Problem-based learning in medicine and beyond: a "
         "brief overview. New Directions for Teaching and Learning, 68, 3-12. "
         "[VERIFY -- Jossey-Bass]"),

        ("Bender, E.M., Gebru, T., McMillan-Major, A., & Shmitchell, S. (2021). "
         "On the dangers of stochastic parrots: can language models be too big? "
         "Proceedings of FAccT 2021, 610-623. [VERIFY]"),

        ("COPE Council. (2023). Authorship and AI tools. Committee on Publication "
         "Ethics. https://publicationethics.org/cope-position-statements/ai-author "
         "[VERIFY URL and date]"),

        ("Creswell, J.W. (2014). Research design: qualitative, quantitative, and "
         "mixed methods approaches (4th ed.). SAGE Publications. "
         "[VERIFY edition number]"),

        ("Elsevier. (2023). Use of AI and AI-assisted technologies in scientific "
         "writing. Elsevier Author Policies. [VERIFY current policy URL]"),

        ("Herreid, C.F. (1994). Case studies in science: a novel method of science "
         "education. Journal of College Science Teaching, 23(4), 221-229. [VERIFY]"),

        ("ICMJE. (2023). Recommendations for the conduct, reporting, editing, and "
         "publication of scholarly work in medical journals. "
         "International Committee of Medical Journal Editors. [VERIFY]"),

        ("Lund, B.D., & Wang, T. (2023). Chatting about ChatGPT: how may AI and "
         "GPT impact academia and libraries? Library Hi Tech News, 40(3), 26-29. "
         "[VERIFY -- check journal/volume details]"),

        ("Mhlanga, D. (2023). Open AI in education: the open Pandora's box of "
         "artificial intelligence in education. SSRN Working Paper. [VERIFY]"),

        ("Noy, S., & Zhang, W. (2023). Experimental evidence on the productivity "
         "effects of generative artificial intelligence. Science, 381(6654), 187-192. "
         "[VERIFY -- published in Science July 2023]"),

        ("Page, M.J., McKenzie, J.E., Bossuyt, P.M., Boutron, I., Hoffmann, T.C., "
         "Mulrow, C.D., ... & Moher, D. (2021). The PRISMA 2020 statement: an "
         "updated guideline for reporting systematic reviews. BMJ, 372, n71. "
         "[VERIFY -- high confidence]"),

        ("Perkins, M., Furze, L., Roe, J., & MacVaugh, J. (2024). The AI assessment "
         "scale (AIAS): a framework for ethical integration of AI in educational "
         "assessment. Journal of University Teaching and Learning Practice, 21(2). "
         "[VERIFY -- details may be inaccurate]"),

        ("Springer Nature. (2023). Artificial intelligence (AI) policy. "
         "Springer Nature Author Resources. [VERIFY current policy URL]"),

        ("UNESCO. (2021). Recommendation on the ethics of artificial intelligence. "
         "UNESCO, Paris. https://unesdoc.unesco.org/ark:/48223/pf0000381137 "
         "[VERIFY -- high confidence]"),

        ("Vygotsky, L.S. (1978). Mind in society: the development of higher "
         "psychological processes. Harvard University Press. "
         "[VERIFY -- classic reference, high confidence]"),

        ("Zawacki-Richter, O., Marin, V.I., Bond, M., & Gouverneur, F. (2019). "
         "Systematic review of research on artificial intelligence applications in "
         "higher education -- where are the educators? International Journal of "
         "Educational Technology in Higher Education, 16(1), 39. [VERIFY]"),
    ]
    for ref in refs:
        pdf.ref_item(ref)


# ── Appendices ─────────────────────────────────────────────────────────────────
def appendices(pdf):
    pdf.add_page()
    pdf.h1("Appendices")

    pdf.h2("Appendix A: DATA SOURCE Declaration Page Template")
    pdf.para(
        "The following template is the standard DATA SOURCE Declaration page "
        "used in all iNHCES PDFs. Researchers may adapt this for their own "
        "AI-assisted research projects."
    )
    pdf.code_box(
        "DATA SOURCE DECLARATION -- READ BEFORE USE\n\n"
        "[COLOUR BANNER: GREEN / AMBER / RED]\n\n"
        "HEADLINE: [e.g., DATA SOURCE: AMBER -- AI-AUTHORED TEMPLATE]\n\n"
        "BODY TEXT:\n"
        "  WHAT IS REAL IN THIS DOCUMENT:\n"
        "    * [List real, verifiable content]\n\n"
        "  WHAT IS AI-GENERATED / SYNTHETIC:\n"
        "    * [List AI-authored or synthetic content]\n\n"
        "  REQUIRED BEFORE PUBLICATION:\n"
        "    1. [Specific replacement action 1]\n"
        "    2. [Specific replacement action 2]\n"
        "    ...\n"
        "    N. Verify all citations in Scopus / Web of Science\n"
        "    N+1. Include AI Disclosure Statement in final submitted manuscript\n"
        "    N+2. Obtain IRB/ethics board approval (if human subjects involved)\n\n"
        "Governing framework: [Project Preamble Document reference]"
    )

    pdf.h2("Appendix B: PROJECT_CONTEXT.md Template")
    pdf.para(
        "The session resumption document pattern used in iNHCES. "
        "Sections: (1) Governing Framework; (2) Project Overview; "
        "(3) Technology Stack; (4) Folder Structure; (5) Current Status; "
        "(6) Full Build Sequence; (7) Key Variables Reference; "
        "(8) Known Issues Log; (9) Publication Portfolio; "
        "(10) Resume Instructions. "
        "Maintained as a living document: updated after every completed step."
    )
    pdf.placeholder_box(
        "Full PROJECT_CONTEXT.md template to be extracted from the iNHCES "
        "project and published as supplementary material with this paper."
    )

    pdf.h2("Appendix C: Sample Prompt Patterns Used in iNHCES Sessions")
    pdf.para(
        "The following prompt patterns were used to initiate AI-assisted work "
        "at each stage. These are proposed as reusable templates."
    )
    prompts = [
        ("Session Start",
         "Read PROJECT_CONTEXT.md and continue the iNHCES build from [O/Step]. "
         "Apply the governing framework in all outputs. Begin with [deliverable]."),
        ("PDF Generation",
         "Generate a Python script using fpdf2 to produce [document name] as a PDF. "
         "Include a DATA SOURCE DECLARATION page with [GREEN/AMBER/RED] banner. "
         "Follow the pattern in [existing script]. Output to [path]."),
        ("Data Analysis",
         "Write a Python script to perform [analysis] on the data in [file]. "
         "Include [test names], export results to CSV at [path], and generate "
         "a PDF summary using the project's DocPDF class."),
        ("Framework Decision",
         "What DATA SOURCE banner should [document] carry? "
         "Justify by reference to the Preamble Document obligations."),
        ("Citation Check",
         "List all citations in [section]. Mark each as [VERIFY -- high confidence], "
         "[VERIFY -- moderate confidence], or [VERIFY -- low confidence / may not exist]. "
         "Explain your confidence assessment for each."),
    ]
    for ptype, prompt in prompts:
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*DARK_NAVY)
        pdf.set_x(LEFT)
        pdf.cell(PAGE_W, 5.5, sanitize(f"  Prompt type: {ptype}"), ln=True)
        pdf.code_box(prompt)


# ── Section 4.5: Environment Setup ────────────────────────────────────────────
def section4_5(pdf):
    pdf.add_page()
    pdf.h1("4.5 Setting Up the S2RF Research Environment")
    pdf.para(
        "A core requirement for the S2RF to be replicable is that the AI tool "
        "environment can be reproduced by any researcher with a standard laptop "
        "and an internet connection. This section documents the exact configuration "
        "used in iNHCES and provides a step-by-step setup guide. All software "
        "listed is either free or available through institutional subscriptions. "
        "The setup takes approximately 30-45 minutes for a researcher with basic "
        "computing familiarity."
    )

    pdf.h2("4.5.1 System Requirements")
    rw = [40, PAGE_W - 40]
    pdf.thead(["Component", "Requirement"], rw)
    req_rows = [
        ("Operating System",
         "Windows 10/11 (used in iNHCES), macOS 12+, or Ubuntu 20.04+. "
         "All commands in this guide use Windows/bash syntax; "
         "macOS/Linux equivalents are identical except where noted."),
        ("RAM", "Minimum 8 GB. 16 GB recommended for running ML libraries (XGBoost, SHAP)."),
        ("Storage", "Minimum 5 GB free space for software, packages, and project outputs."),
        ("Internet", "Required for AI tool API calls, package installation, and live data APIs."),
        ("Python", "Python 3.10 or higher. Download from python.org. "
         "Add Python to PATH during installation."),
        ("Node.js", "v18 or higher. Required for Claude Code CLI. "
         "Download from nodejs.org (LTS version recommended)."),
        ("Git", "Any recent version. Download from git-scm.com. "
         "Required for version control and Claude Code context tracking."),
        ("Anthropic Account", "Free account at console.anthropic.com. "
         "API key required for Claude Code CLI. "
         "Claude Pro subscription ($20/month) recommended for extended research sessions."),
        ("GitHub Account", "Free. Required for GitHub Copilot (optional but recommended). "
         "GitHub Copilot Individual: $10/month. Free for verified students/educators "
         "via GitHub Education programme."),
    ]
    for i, (comp, req) in enumerate(req_rows):
        pdf.mrow([comp, req], rw, fill=(i % 2 == 1))
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 4.5, sanitize(
        "Table 7: System requirements for replicating the iNHCES S2RF environment."
    ))
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(2)

    pdf.h2("4.5.2 Step 1 -- Install Visual Studio Code")
    pdf.para(
        "VS Code is the central workspace for the S2RF. All AI tools, file editing, "
        "terminal execution, and PDF generation are performed within VS Code."
    )
    pdf.numbered_list([
        "Download VS Code from code.visualstudio.com (free, all platforms).",
        "Run the installer. On Windows, tick 'Add to PATH' and "
        "'Register Code as editor for supported file types'.",
        "Open VS Code. Navigate to the Extensions panel (Ctrl+Shift+X).",
        "Install the following extensions: "
        "(a) Python (Microsoft) -- Python language support and virtual environments; "
        "(b) GitLens -- enhanced Git integration; "
        "(c) Mermaid Preview -- to render .mmd diagram files (optional but useful for O4).",
    ])

    pdf.h2("4.5.3 Step 2 -- Install Claude Code CLI and VS Code Extension")
    pdf.para(
        "Claude Code is Anthropic's official command-line AI coding assistant. "
        "It provides long-context, file-aware AI interaction within any terminal "
        "or directly in VS Code. It is the primary AI tool used in the iNHCES S2RF."
    )
    pdf.numbered_list([
        "Ensure Node.js v18+ is installed: open a terminal and run `node --version`. "
        "If not installed, download from nodejs.org.",
        "Install Claude Code CLI globally via npm:\n"
        "    npm install -g @anthropic-ai/claude-code",
        "Obtain your Anthropic API key: log in to console.anthropic.com -> "
        "API Keys -> Create key. Copy the key (it is shown only once).",
        "Set the API key as an environment variable:\n"
        "    Windows (PowerShell): $env:ANTHROPIC_API_KEY = 'sk-ant-...'\n"
        "    Windows (persistent): add to System -> Environment Variables -> User\n"
        "    macOS/Linux: export ANTHROPIC_API_KEY='sk-ant-...'  (add to ~/.bashrc)",
        "Verify the installation: in a terminal, run `claude --version`. "
        "You should see the Claude Code version number.",
        "Install the Claude Code VS Code extension: in VS Code Extensions panel, "
        "search 'Claude Code' (Anthropic) and install. "
        "This embeds Claude Code interaction directly in the VS Code sidebar.",
        "Optional: install the Claude Code desktop app (claude.ai/download) "
        "for a standalone interface alongside VS Code.",
    ])

    pdf.h2("4.5.4 Step 3 -- Install GitHub Copilot (Optional but Recommended)")
    pdf.para(
        "GitHub Copilot provides inline AI code completion within the VS Code editor "
        "and a chat panel for targeted code questions. In the iNHCES project, Copilot "
        "was used for inline completion during Python script writing, while Claude Code "
        "was used for multi-file, multi-step research workflow management."
    )
    pdf.numbered_list([
        "In VS Code Extensions panel, search 'GitHub Copilot' (GitHub) and install.",
        "Also install 'GitHub Copilot Chat' for the chat panel interface.",
        "Sign in with your GitHub account when prompted. "
        "Activate Copilot Individual subscription at github.com/features/copilot "
        "(free for verified students at education.github.com).",
        "Verify: open any .py file. Copilot should offer grey-text completions "
        "as you type. Press Tab to accept.",
    ])

    pdf.h2("4.5.5 Step 4 -- Set Up Python Virtual Environment and Packages")
    pdf.para(
        "All iNHCES Python scripts use a dedicated virtual environment to avoid "
        "dependency conflicts. The following packages are required to run the full "
        "S2RF simulation pipeline."
    )
    pdf.code_box(
        "# 1. Navigate to project root in terminal\n"
        "cd \"C:\\path\\to\\your\\project\"\n\n"
        "# 2. Create virtual environment\n"
        "python -m venv venv\n\n"
        "# 3. Activate it\n"
        "#    Windows PowerShell:\n"
        ".\\venv\\Scripts\\Activate.ps1\n"
        "#    Windows cmd:\n"
        "venv\\Scripts\\activate.bat\n"
        "#    macOS / Linux:\n"
        "source venv/bin/activate\n\n"
        "# 4. Install all required packages\n"
        "pip install fpdf2 pandas numpy matplotlib seaborn\n"
        "pip install statsmodels scikit-learn xgboost lightgbm shap\n"
        "pip install requests wbgapi fredapi\n\n"
        "# 5. Verify key packages\n"
        "python -c \"import fpdf; import xgboost; import shap; print('OK')\""
    )
    pv = [40, 30, PAGE_W - 70]
    pdf.thead(["Package", "Version (min)", "Purpose in iNHCES"], pv)
    pkg_rows = [
        ("fpdf2",        "2.7+",   "Generate all PDF research outputs (all objectives)"),
        ("pandas",       "1.5+",   "Data loading, cleaning, CSV I/O (O2, O5)"),
        ("numpy",        "1.23+",  "Numerical operations, synthetic data generation (O2)"),
        ("matplotlib",   "3.6+",   "Charts for VAR IRF, SHAP beeswarm plots (O2, O5)"),
        ("seaborn",      "0.12+",  "Statistical visualisations (O1 survey analysis)"),
        ("statsmodels",  "0.14+",  "ADF/KPSS unit root tests, VAR/VECM models (O2)"),
        ("scikit-learn", "1.2+",   "Ridge/Lasso/RF/MLP baseline models (O5)"),
        ("xgboost",      "1.7+",   "XGBoost regressor for SHAP analysis (O2, O5)"),
        ("lightgbm",     "3.3+",   "LightGBM for model benchmarking (O5)"),
        ("shap",         "0.41+",  "SHAP TreeExplainer for feature importance (O2, O5)"),
        ("requests",     "2.28+",  "HTTP calls to World Bank and EIA APIs (O2)"),
        ("wbgapi",       "1.0+",   "World Bank Open Data Python client (O2)"),
        ("fredapi",      "0.5+",   "FRED API client for FX and oil data (O2, optional)"),
    ]
    for i, (pkg, ver, purpose) in enumerate(pkg_rows):
        pdf.trow([pkg, ver, purpose], pv, fill=(i % 2 == 1))
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 4.5, sanitize(
        "Table 8: Python package requirements for the full iNHCES S2RF pipeline."
    ))
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(2)

    pdf.h2("4.5.6 Step 5 -- Initialise the Project Directory and CLAUDE.md")
    pdf.para(
        "The project directory structure must be created before the first AI session "
        "begins. Claude Code reads a CLAUDE.md file at the project root on every "
        "session start, giving the AI persistent memory of the project context, "
        "technology stack, and current build status. This file is the AI's "
        "'standing brief' and eliminates the need to re-explain the project at "
        "the start of each session."
    )
    pdf.code_box(
        "# Create the top-level project directory\n"
        "mkdir MyResearchProject\n"
        "cd MyResearchProject\n\n"
        "# Initialise Git repository\n"
        "git init\n\n"
        "# Create the standard iNHCES-style folder structure\n"
        "mkdir 01_literature_review 02_macro_analysis 03_requirements\n"
        "mkdir 04_conceptual_models 05_ml_models\n"
        "mkdir nhces-backend nhces-frontend \"Draft AI Papers\"\n"
        "mkdir Research_Documents\n\n"
        "# Create placeholder files to track the structure in Git\n"
        "# (repeat for each empty subfolder)\n"
        "echo . > 01_literature_review\\.gitkeep\n\n"
        "# Create the CLAUDE.md project memory file (see Appendix D for template)\n"
        "# Create the PROJECT_CONTEXT.md session guide (see Appendix D for template)"
    )

    pdf.h2("4.5.7 Step 6 -- Start the First AI Session")
    pdf.para(
        "Once the environment is configured, starting a research session requires "
        "three steps: activate the virtual environment, navigate to the project "
        "root, and start Claude Code. The AI will automatically read CLAUDE.md "
        "on startup."
    )
    pdf.code_box(
        "# Step 1: Activate Python virtual environment\n"
        ".\\venv\\Scripts\\Activate.ps1         # Windows PowerShell\n"
        "source venv/bin/activate              # macOS / Linux\n\n"
        "# Step 2: Navigate to project root\n"
        "cd \"C:\\path\\to\\MyResearchProject\"\n\n"
        "# Step 3: Start Claude Code CLI\n"
        "claude\n\n"
        "# Step 4: Paste the session start prompt:\n"
        "# ---\n"
        "# Read PROJECT_CONTEXT.md and continue the [ProjectName] build\n"
        "# from [ObjectiveX, Step Y]. We are operating under the obligations\n"
        "# of the Governing Preamble Document. Begin with [deliverable name].\n"
        "# ---\n\n"
        "# Alternatively, open VS Code and use the Claude Code extension panel:\n"
        "code .     # opens VS Code in current directory\n"
        "# Then use Ctrl+Shift+P -> 'Claude Code: Open' to open the sidebar"
    )

    pdf.h2("4.5.8 Environment Verification Checklist")
    pdf.para(
        "Before beginning any research simulation work, verify each item in the "
        "following checklist. A missing item will cause specific failure modes "
        "noted in the right column."
    )
    vc = [8, 55, PAGE_W - 63]
    pdf.thead(["", "Check", "Failure Mode if Missing"], vc)
    checks = [
        ("[ ]", "python --version returns 3.10 or higher",
         "fpdf2 and statsmodels will fail to import"),
        ("[ ]", "node --version returns v18 or higher",
         "Claude Code CLI will not install"),
        ("[ ]", "claude --version runs without error",
         "Cannot start AI-assisted sessions"),
        ("[ ]", "ANTHROPIC_API_KEY environment variable is set",
         "Claude Code will prompt for key on every session start"),
        ("[ ]", "Virtual environment is activated (venv prefix in terminal prompt)",
         "pip install will modify system Python; import errors likely"),
        ("[ ]", "python -c \"import fpdf\" runs without error",
         "All PDF generator scripts will fail"),
        ("[ ]", "python -c \"import xgboost; import shap\" runs without error",
         "O2 SHAP analysis and O5 ML pipeline will fail"),
        ("[ ]", "CLAUDE.md exists at project root",
         "Claude Code will have no project context; every session starts cold"),
        ("[ ]", "PROJECT_CONTEXT.md exists at project root",
         "No session resumption guide; risk of duplicating completed work"),
        ("[ ]", "git status runs without error in project root",
         "No version control; risk of losing AI-generated output files"),
        ("[ ]", "VS Code opens project root with Claude Code extension active",
         "Cannot use VS Code-integrated AI workflow"),
    ]
    for i, (chk, check, failure) in enumerate(checks):
        pdf.mrow([chk, check, failure], vc, fill=(i % 2 == 1))
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 4.5, sanitize(
        "Table 9: Environment verification checklist. Tick each box before "
        "beginning the first research simulation session."
    ))
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(2)

    pdf.key_finding_box(
        "REPLICATION NOTE -- PLATFORM INDEPENDENCE",
        "The S2RF was developed and tested on Windows 10 Pro. All core components "
        "(VS Code, Claude Code CLI, Python packages) are cross-platform. "
        "Researchers on macOS or Linux should use 'source venv/bin/activate' "
        "and 'export ANTHROPIC_API_KEY=...' in place of the Windows equivalents. "
        "No platform-specific code exists in the iNHCES generator scripts."
    )


# ── Appendix D: Full Replication Guide ────────────────────────────────────────
def appendix_d(pdf):
    pdf.add_page()
    pdf.h1("Appendix D: Full Replication Guide -- Commands and File Templates")
    pdf.para(
        "This appendix provides the complete, copy-paste-ready commands and "
        "file templates required to replicate the iNHCES S2RF environment "
        "from scratch. Researchers may use this as a standalone setup guide "
        "independent of the main paper."
    )

    pdf.h2("D.1 Complete Installation Sequence (Windows PowerShell)")
    pdf.code_box(
        "# ═══════════════════════════════════════════════════════\n"
        "# iNHCES S2RF -- Full Environment Setup (Windows)\n"
        "# Run each block in order in an Administrator PowerShell\n"
        "# ═══════════════════════════════════════════════════════\n\n"
        "# BLOCK 1: Verify prerequisites\n"
        "python --version       # must be 3.10+\n"
        "node --version         # must be v18+\n"
        "git --version          # any recent version\n"
        "code --version         # VS Code must be installed\n\n"
        "# BLOCK 2: Install Claude Code CLI\n"
        "npm install -g @anthropic-ai/claude-code\n"
        "claude --version       # verify installation\n\n"
        "# BLOCK 3: Set Anthropic API key (replace with your key)\n"
        "# Temporary (current session only):\n"
        "$env:ANTHROPIC_API_KEY = 'sk-ant-YOUR-KEY-HERE'\n"
        "# Permanent (System Environment Variables -- recommended):\n"
        "# Windows: Settings -> System -> Advanced -> Environment Variables\n"
        "# Add User variable: ANTHROPIC_API_KEY = sk-ant-YOUR-KEY-HERE\n\n"
        "# BLOCK 4: Create project and virtual environment\n"
        "mkdir C:\\Research\\MyProject\n"
        "cd C:\\Research\\MyProject\n"
        "git init\n"
        "python -m venv venv\n"
        ".\\venv\\Scripts\\Activate.ps1\n\n"
        "# BLOCK 5: Install all Python packages\n"
        "pip install --upgrade pip\n"
        "pip install fpdf2 pandas numpy matplotlib seaborn\n"
        "pip install statsmodels scikit-learn xgboost lightgbm shap\n"
        "pip install requests wbgapi fredapi\n\n"
        "# BLOCK 6: Verify all packages\n"
        "python -c \"import fpdf, pandas, numpy, statsmodels, xgboost, shap; print('ALL OK')\"\n\n"
        "# BLOCK 7: Open project in VS Code\n"
        "code .\n"
        "# In VS Code: install extensions: Python, Claude Code, GitHub Copilot\n\n"
        "# BLOCK 8: Start Claude Code\n"
        "claude\n"
        "# Paste the session start prompt (see D.3 below)"
    )

    pdf.h2("D.2 CLAUDE.md Template")
    pdf.para(
        "Create this file at the project root. Claude Code reads it automatically "
        "on every session start. Replace all [BRACKETED] placeholders with your "
        "project details."
    )
    pdf.code_box(
        "# [Project Short Name] Project Context\n\n"
        "## Project\n"
        "[Full project title]\n"
        "[Funding body and grant reference]\n"
        "[Institution, Department]\n\n"
        "## Tech Stack\n"
        "- Frontend: [e.g., Vanilla HTML/CSS/JS -> Vercel]\n"
        "- Backend: [e.g., FastAPI (Python) -> Railway]\n"
        "- Database: [e.g., Supabase PostgreSQL]\n"
        "- ML Registry: [e.g., MLflow (Railway)]\n\n"
        "## Governing Framework\n"
        "This project is governed by the Simulation to Research Framework (S2RF).\n"
        "Every output must comply with DATA SOURCE Declaration System rules.\n"
        "Preamble document: [path to your preamble PDF]\n\n"
        "## Current Build Status\n"
        "### Completed\n"
        "- [x] Project folder structure\n"
        "### In Progress / Next Steps\n"
        "- [ ] [Objective 1, Step 1]\n\n"
        "## Research Objectives\n"
        "[O1]: [description]\n"
        "[O2]: [description]\n\n"
        "## Key Variables\n"
        "[Target variable]: [description]\n"
        "[Feature variables]: [list]\n\n"
        "## DATA SOURCE Rules (mandatory)\n"
        "GREEN = live API or real instrument\n"
        "AMBER = AI-authored template (validate before publication)\n"
        "RED   = synthetic data (MUST replace before any publication)"
    )

    pdf.h2("D.3 SESSION_START Prompt Template")
    pdf.para(
        "Paste this at the start of every new Claude Code session. "
        "Replace [bracketed] text with the current session details."
    )
    pdf.code_box(
        "Read PROJECT_CONTEXT.md and continue the [ProjectName] build\n"
        "from [Objective X, Step Y].\n\n"
        "We are operating under the obligations of the Governing Preamble\n"
        "Document. Apply the correct DATA SOURCE banner to every new PDF.\n\n"
        "Begin with: [specific deliverable name and output path].\n\n"
        "After completing the step:\n"
        "1. Update PROJECT_CONTEXT.md to mark the step COMPLETE.\n"
        "2. Update the 'last updated' line at the bottom.\n"
        "3. Confirm the DATA SOURCE banner level applied."
    )

    pdf.h2("D.4 PROJECT_CONTEXT.md Minimum Viable Structure")
    pdf.para(
        "A minimum viable PROJECT_CONTEXT.md for a new project. "
        "Expand each section as the project progresses."
    )
    pdf.code_box(
        "# [ProjectName] Project Context\n"
        "Last updated: [DATE] | Session: [brief note]\n\n"
        "## GOVERNING FRAMEWORK\n"
        "Read [preamble PDF path] before any session work.\n"
        "DATA SOURCE rules: GREEN / AMBER / RED (see CLAUDE.md).\n\n"
        "## 1. Project Overview\n"
        "Full Name: [name] | Grant: [ref] | Institution: [dept]\n\n"
        "## 2. Technology Stack\n"
        "[layer]: [technology] -> [hosting]\n\n"
        "## 3. Project Root\n"
        "[absolute path]\n\n"
        "## 4. Current Status\n"
        "### COMPLETED\n"
        "- [x] [deliverable] ([date])\n"
        "### STOPPED AT\n"
        "[Current objective and step]\n\n"
        "## 5. Full Build Sequence\n"
        "| Step | Deliverable | Status |\n"
        "|------|-------------|--------|\n"
        "| O1-1 | [name] | [emoji] |\n\n"
        "## 6. Known Issues\n"
        "| Date | Error | Cause | Resolution |\n\n"
        "## 7. Publication Portfolio\n"
        "| Paper | Journal | Status |\n"
        "| P1    | [journal] | Draft |\n"
    )

    pdf.h2("D.5 macOS / Linux Equivalents")
    pdf.code_box(
        "# macOS / Linux -- differences from Windows instructions only\n\n"
        "# Activate virtual environment:\n"
        "source venv/bin/activate\n\n"
        "# Set API key (add to ~/.bashrc or ~/.zshrc for persistence):\n"
        "export ANTHROPIC_API_KEY='sk-ant-YOUR-KEY-HERE'\n"
        "source ~/.bashrc\n\n"
        "# All npm, pip, git, python, and code commands are identical.\n"
        "# Path separators: use forward slashes (/) not backslashes (\\).\n"
        "# mkdir creates directories with the same syntax.\n"
        "# VS Code: install via snap (Linux) or .dmg (macOS) from code.visualstudio.com"
    )


# ── Section 4.6: S2RF in Non-VS Code AI Environments ─────────────────────────
def section4_6(pdf):
    pdf.add_page()
    pdf.h1("4.6  Extending the S2RF to Native AI Platform Environments")
    pdf.para(
        "Sections 4.1-4.5 documented the S2RF as implemented in the iNHCES project, "
        "where a VS Code development environment, Python scripting, and the fpdf2 "
        "library formed the technical backbone. That configuration suits system "
        "development research -- research that produces code, databases, and "
        "deployable software artefacts. However, the four core S2RF rules (Preamble "
        "Supremacy, DATA SOURCE Declaration, Replacement Obligation, Human Validation "
        "Gate) are platform-independent. They describe a methodology, not a toolchain. "
        "This section documents how the S2RF can be implemented in the native web "
        "interfaces of four leading AI platforms -- Claude.ai, ChatGPT, Google Gemini, "
        "and DeepSeek -- to support non-system-development research types such as "
        "standalone literature reviews, survey-based studies, policy analysis, and "
        "qualitative investigations."
    )

    pdf.h2("4.6.1  Platform Overview and S2RF Component Mapping")
    pw = [28, 28, 28, PAGE_W - 84]
    pdf.thead(["S2RF Component", "Claude.ai (Projects)", "ChatGPT (Projects)", "Gemini (Gems)"], pw)
    platform_rows = [
        ("Governing Preamble",
         "Project Instructions field (up to 200k tokens). Paste condensed preamble rules.",
         "Custom Instructions + Project system prompt. Paste preamble rules.",
         "Gem Instructions field. Paste preamble rules."),
        ("DATA SOURCE Declaration",
         "Researcher manually adds a labelled block at the top of every saved AI output.",
         "Researcher manually adds declaration block; or instruct GPT to prepend it.",
         "Researcher manually adds declaration; Gem can be instructed to prepend."),
        ("Replacement Obligation",
         "Tracked in a shared Google Doc / Notion page -- external to Claude.",
         "Tracked in a shared tracker. ChatGPT Projects can hold a tracker file.",
         "Tracked in a Google Doc (native integration with Google Workspace)."),
        ("Human Validation Gate",
         "Researcher reviews and saves each output to a named document before proceeding.",
         "Researcher reviews and saves; can use Canvas (side-by-side editing).",
         "Researcher reviews in Google Doc; tracked via Docs version history."),
        ("Session Memory",
         "Projects retain full conversation history across sessions.",
         "Projects retain conversation history. Memory feature adds cross-project facts.",
         "Gems retain system prompt. Conversation history within a Gem persists."),
    ]
    for i, row in enumerate(platform_rows):
        pdf.mrow(list(row), pw, fill=(i % 2 == 1))
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 4.5, sanitize(
        "Table 10: S2RF component mapping across native AI platform environments. "
        "DeepSeek is covered separately in Section 4.6.5 (no persistent project feature as of 2025)."
    ))
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(2)

    pdf.h2("4.6.2  Claude.ai (Projects) -- Best for Long-Form Research")
    pdf.para(
        "Claude.ai Projects (available on Claude.ai Pro and Team plans) provide "
        "persistent conversation memory, file uploads, and a dedicated Project "
        "Instructions field that is prepended to every conversation. This makes "
        "Claude.ai Projects the closest native-platform equivalent to the VS Code "
        "Claude Code CLI + CLAUDE.md configuration used in iNHCES."
    )
    pdf.h3("Setup: Governing Preamble in Project Instructions")
    pdf.para(
        "Create a new Project (e.g., 'My Research Project'). In Project Settings, "
        "paste a condensed version of the S2RF Preamble (see Appendix D for template). "
        "Include: (1) the three DATA SOURCE colour rules; (2) the Replacement Obligation "
        "statement; (3) the no-AI-generated-citations rule; (4) the AI Disclosure "
        "obligation. Claude will treat this as standing instructions for all conversations "
        "in the Project -- equivalent to CLAUDE.md."
    )
    pdf.h3("Implementing DATA SOURCE Declarations Without fpdf2")
    pdf.para(
        "In a non-VS Code environment, AI outputs are text documents (Word, Google Doc, "
        "Markdown) rather than Python-generated PDFs. The DATA SOURCE Declaration "
        "is implemented as a labelled header block at the top of every document:"
    )
    pdf.code_box(
        "================================================\n"
        "DATA SOURCE DECLARATION\n"
        "Colour:   [GREEN / AMBER / RED]\n"
        "Label:    [e.g., AI-AUTHORED TEMPLATE]\n"
        "What is real:    [brief description]\n"
        "What is AI/synthetic: [brief description]\n"
        "Required before publication:\n"
        "  1. [replacement action]\n"
        "  2. Verify all citations in Scopus / Web of Science\n"
        "  3. Include AI Disclosure Statement\n"
        "================================================"
    )
    pdf.para(
        "This block is pasted at the top of every Word document, Google Doc, or "
        "Markdown file generated from a Claude.ai session. It serves the same "
        "audit function as the fpdf2-generated banner page in the iNHCES PDFs."
    )
    pdf.h3("Suitable Research Types")
    pdf.bullet_list([
        "Standalone PRISMA systematic literature reviews (PRISMA protocol, screening, "
        "data extraction, narrative synthesis)",
        "Delphi consensus studies (instrument design, round-by-round analysis, "
        "synthesis reports)",
        "Mixed-methods research (qualitative interview guides, thematic coding "
        "frameworks, integration matrices)",
        "Policy analysis documents (evidence summaries, stakeholder mappings, "
        "recommendation reports)",
        "Book chapters, thesis introductions, and review articles",
    ])

    pdf.h2("4.6.3  ChatGPT (Projects + Code Interpreter) -- Best for Data Analysis")
    pdf.para(
        "ChatGPT Projects (available on Plus and Team plans) provide session-persistent "
        "memory and file storage. The addition of the Code Interpreter tool gives "
        "ChatGPT a significant capability that Claude.ai currently lacks: the ability "
        "to execute Python code, perform statistical analysis, generate charts, and "
        "export CSV and PDF files -- all within the browser, without VS Code or a "
        "local Python installation."
    )
    pdf.h3("S2RF Setup in ChatGPT")
    pdf.bullet_list([
        "Custom Instructions (Profile > Personalise > Custom Instructions): paste a "
        "condensed S2RF preamble covering DATA SOURCE rules, citation policy, "
        "and AI disclosure obligation. These apply to all conversations.",
        "Project System Prompt: for research-specific projects, add the project-specific "
        "context (objectives, target variable, current step) to the Project's system prompt "
        "-- equivalent to PROJECT_CONTEXT.md.",
        "MyGPT Builder: advanced users can create a custom GPT (GPT Builder) with the "
        "full S2RF preamble as system instructions, pre-loaded reference files "
        "(DATA SOURCE template, citation checklist), and defined conversation starters "
        "(SESSION_START prompts).",
    ])
    pdf.h3("Code Interpreter for S2RF Analysis")
    pdf.para(
        "ChatGPT's Code Interpreter can execute the equivalent of many iNHCES O2/O5 "
        "scripts without any local setup. A researcher can upload a CSV of macroeconomic "
        "data and instruct ChatGPT to perform ADF stationarity tests, VAR modelling, "
        "and SHAP analysis -- receiving Python output, charts, and a CSV of results, "
        "all exported as files. The DATA SOURCE level of outputs produced this way "
        "follows the same rules: if the input data is from a live API (GREEN), "
        "the outputs are GREEN; if the input is synthetic (RED), the outputs are RED."
    )
    pdf.h3("Suitable Research Types")
    pdf.bullet_list([
        "Survey analysis (SPSS-equivalent descriptive statistics, reliability, EFA)",
        "Quantitative data analysis where a local Python environment is not available",
        "Time-series analysis of downloaded government or World Bank data",
        "Hypothesis testing and report generation from pre-collected datasets",
    ])

    pdf.h2("4.6.4  Google Gemini (Gems) -- Best for Google Workspace Research Teams")
    pdf.para(
        "Google Gemini Gems (available on Gemini Advanced, included in Google One AI "
        "Premium and Google Workspace plans) allow the creation of custom AI agents "
        "with persistent system instructions and access to Google Drive files. "
        "For research teams already working within Google Workspace (Docs, Sheets, "
        "Drive), Gemini Gems offer the tightest integration: a researcher can instruct "
        "a Gem to read a Google Sheet of survey data, analyse it, and write the results "
        "directly into a Google Doc, with the DATA SOURCE declaration prepended "
        "automatically."
    )
    pdf.h3("S2RF Setup in Gemini")
    pdf.bullet_list([
        "Create a Gem named 'S2RF Research Assistant'. In the Gem Instructions field, "
        "paste the condensed S2RF preamble.",
        "Upload the project context file (equivalent to PROJECT_CONTEXT.md) to the "
        "Gem's associated Google Drive folder so Gemini can read it on demand.",
        "Use Google Docs as the output medium: instruct Gemini to produce every "
        "AI-generated document in a named Google Doc with the DATA SOURCE declaration "
        "block at the top and version history enabled (Docs automatically tracks "
        "all edits -- an inherent Human Validation Gate).",
        "Google Sheets integration: Gemini can read uploaded CSV or Sheets data, "
        "perform pivot tables and basic statistics, and write outputs back to Sheets "
        "with DATA SOURCE labels in a dedicated column.",
    ])
    pdf.h3("Suitable Research Types")
    pdf.bullet_list([
        "Collaborative research teams using Google Workspace for shared document editing",
        "Survey design and analysis using Google Forms + Sheets",
        "Literature review management with shared Google Doc extraction matrices",
        "Policy briefs and stakeholder reports requiring team co-authoring",
    ])

    pdf.h2("4.6.5  DeepSeek (R1 / V3) -- Best for Cost-Sensitive Researchers")
    pdf.para(
        "DeepSeek (deepseek.com) provides free access to DeepSeek-V3 (general tasks) "
        "and DeepSeek-R1 (chain-of-thought reasoning, comparable to OpenAI o1) via a "
        "web interface and API. As of April 2026, DeepSeek does not offer persistent "
        "Projects equivalent to Claude or ChatGPT. However, it supports system prompts "
        "via the API and long-context conversations via the web interface. Its "
        "cost advantage (free web interface, very low API pricing) makes it "
        "particularly relevant for researchers in lower-income settings."
    )
    pdf.h3("S2RF Adaptation for DeepSeek")
    pdf.para(
        "Because DeepSeek lacks persistent project memory, the S2RF session resumption "
        "pattern must be implemented manually. The researcher pastes a 'Context Block' "
        "at the start of every new session:"
    )
    pdf.code_box(
        "=== S2RF CONTEXT BLOCK -- PASTE AT START OF EVERY SESSION ===\n"
        "Project: [Project Name]\n"
        "Governing Framework: [brief DATA SOURCE rules]\n"
        "Current Step: [Objective X, Step Y]\n"
        "Previous Output: [brief description of last session output]\n"
        "Today's Task: [deliverable name and required output]\n"
        "DATA SOURCE Rule for today's output: [GREEN / AMBER / RED]\n"
        "Replacement Obligation: [what must replace today's output]\n"
        "================================================================"
    )
    pdf.para(
        "This Context Block is the DeepSeek equivalent of CLAUDE.md + PROJECT_CONTEXT.md. "
        "It is stored in a local text file and pasted at the start of each session. "
        "DeepSeek-R1 is recommended for tasks requiring step-by-step reasoning "
        "(methodology design, statistical interpretation, argument construction); "
        "DeepSeek-V3 for faster, lower-cost drafting tasks (instrument design, "
        "report writing, table formatting)."
    )
    pdf.h3("Suitable Research Types")
    pdf.bullet_list([
        "Any research type where cost is a primary constraint",
        "Technical analysis requiring strong reasoning (DeepSeek-R1)",
        "Researchers without institutional access to paid AI subscriptions",
        "High-volume drafting tasks (multiple instruments, report sections)",
    ])

    pdf.h2("4.6.6  Platform Selection Guide")
    pdf.para(
        "The following table assists researchers in selecting the appropriate "
        "AI platform for their research type and institutional context."
    )
    sg = [40, PAGE_W - 40]
    pdf.thead(["Research Type / Context", "Recommended Platform + S2RF Configuration"], sg)
    sg_rows = [
        ("System development (code, databases, deployment)",
         "VS Code + Claude Code CLI + GitHub Copilot (iNHCES configuration -- Sections 4.1-4.5)"),
        ("Long-form qualitative / mixed methods research",
         "Claude.ai Projects -- best persistent memory and long-context handling"),
        ("Survey analysis; statistical reporting",
         "ChatGPT Projects + Code Interpreter -- Python execution without local setup"),
        ("Collaborative team research (Google Workspace users)",
         "Google Gemini Gems -- native Google Docs/Sheets integration"),
        ("Cost-sensitive research; reasoning-intensive tasks",
         "DeepSeek R1 (reasoning) or V3 (general) -- free tier, context block pattern"),
        ("Any platform -- DATA SOURCE declaration",
         "Paste the standard declaration block (Section 4.6.2) at the top of every output document"),
        ("Any platform -- no AI-generated citations",
         "Verify every reference in Scopus / Web of Science before use. Tag unverified refs [VERIFY]."),
        ("Any platform -- Human Validation Gate",
         "Save and review every AI output in a named, dated file before using it in research."),
    ]
    for i, (rt, rec) in enumerate(sg_rows):
        pdf.mrow([rt, rec], sg, fill=(i % 2 == 1))
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 4.5, sanitize(
        "Table 11: Platform selection guide for implementing the S2RF across "
        "different research types and institutional contexts."
    ))
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(2)
    pdf.key_finding_box(
        "FRAMEWORK RULE 4 -- PLATFORM INDEPENDENCE",
        "The S2RF is a methodology, not a toolchain. The four core rules "
        "(Preamble Supremacy, DATA SOURCE Declaration, Replacement Obligation, "
        "Human Validation Gate) apply regardless of whether the researcher uses "
        "VS Code, Claude.ai, ChatGPT, Gemini, or DeepSeek. The platform affects "
        "HOW each rule is implemented -- not WHETHER it applies."
    )


# ── Appendix E: Chronicle of S2RF Discovery ────────────────────────────────────
def appendix_e(pdf):
    pdf.add_page()
    pdf.h1("Appendix E: From Research Challenge to Framework Discovery")
    pdf.h2(
        "A Developmental Chronicle of the Human-AI Interactions That Gave Rise "
        "to the Simulation to Research Framework (S2RF)"
    )
    pdf.para(
        "This appendix documents, in chronological order, the key milestones in the "
        "human-AI interaction sequence that produced the simulation-to-research "
        "Framework (S2RF). It is included for two reasons: first, as a matter of "
        "scholarly transparency -- the S2RF emerged from practice, not from prior "
        "theoretical design, and the interactions that shaped it deserve documentation "
        "as part of the research record; second, as a pedagogical resource for other "
        "researchers who wish to understand how the framework evolved so that they "
        "can apply it with full understanding of the reasoning behind each rule, "
        "not merely compliance with its prescriptions."
    )
    pdf.para(
        "All interactions took place in April 2026 using GitHub Copilot (Claude "
        "Sonnet 4.6, via VS Code) as the primary AI assistant. The research was "
        "directed throughout by Dr. Bello Abdullahi, Principal Investigator, "
        "Department of Quantity Surveying, Ahmadu Bello University Zaria, Nigeria, "
        "under the TETFund National Research Fund 2025 grant."
    )

    pdf.h2("E.1  The Starting Point: A Research Programme Without a Framework")
    pdf.para(
        "The iNHCES project began with a clear research ambition -- develop an "
        "AI-powered housing cost estimating system for Nigeria -- and a significant "
        "practical challenge: the full six-objective, nine-paper research programme "
        "would normally require 3-5 years of fieldwork, data collection, and "
        "iterative system development. The PI's question at the outset was: "
        "how can AI tools be used to accelerate the research pipeline without "
        "compromising scientific integrity?"
    )
    pdf.para(
        "The initial AI interactions focused on scaffolding the project: creating "
        "the folder structure, drafting CLAUDE.md (the AI memory file), creating "
        "PROJECT_CONTEXT.md (the session resumption document), and producing the "
        "first research deliverables -- the PRISMA protocol, search strings, and "
        "data extraction template. At this stage, there was no explicit framework. "
        "The AI was a productivity tool; the integrity safeguards were informal "
        "researcher judgements rather than codified rules."
    )

    pdf.h2("E.2  The First Critical Decision: What Is Real?")
    pdf.para(
        "The pivotal moment came during Objective O1, Step 2, when the AI generated "
        "a methodology taxonomy table and ML method comparison document. The PI "
        "asked: what data source label should these documents carry? The AI's "
        "response introduced the three-level DATA SOURCE system -- GREEN (live API "
        "or real instrument), AMBER (AI-authored template), RED (synthetic data) -- "
        "and recommended AMBER for these documents on the grounds that they were "
        "drawn from AI training knowledge, not from a real PRISMA database search."
    )
    pdf.para(
        "This interaction was the conceptual origin of the S2RF. The key insight "
        "was that different outputs within the same research objective could have "
        "different data validity levels -- and that making those levels explicit, "
        "visible, and mandatory on every output was the minimum integrity guarantee "
        "required. The PI directed that this system be applied to every PDF produced "
        "in the project, without exception. That directive became FRAMEWORK RULE 2."
    )
    pdf.key_finding_box(
        "DISCOVERY MOMENT -- The DATA SOURCE Declaration System (April 2026)",
        "The three-level GREEN/AMBER/RED colour system was not designed top-down "
        "from a theoretical model of AI integrity. It emerged from a specific "
        "practical question: 'What label should this document carry?' "
        "The answer required distinguishing between live data, AI-generated content, "
        "and synthetic data -- and the three-colour system was the natural "
        "consequence of that distinction."
    )

    pdf.h2("E.3  The RED Banner Crisis: When Synthetic Data Became a Risk")
    pdf.para(
        "O1, Step 5 produced the first RED-banner document: a complete hypothetical "
        "survey analysis (n=60, NumPy seed=2025) generating Cronbach alpha values, "
        "EFA factor loadings, and TAM path coefficients -- all from synthetic data. "
        "The document looked like a finished research paper. The PI immediately "
        "identified the risk: if this document were ever mistaken for real findings, "
        "the consequences for academic integrity would be serious."
    )
    pdf.para(
        "The response was to define the Replacement Obligation: a non-negotiable rule "
        "that any RED-banner document must be replaced with real data before any "
        "publication. This was not merely a recommendation -- it was made a condition "
        "of the framework, tracked explicitly in PROJECT_CONTEXT.md for every RED "
        "deliverable. The interaction also established the principle that the more "
        "complete and convincing a simulated output looks, the more important it is "
        "to label it clearly -- because plausibility is itself a risk when the data "
        "is synthetic."
    )

    pdf.h2("E.4  The Live Data Discovery: When GREEN Upgraded RED Automatically")
    pdf.para(
        "O2, Step 1 introduced a pattern that became one of the S2RF's most "
        "practically significant design features. The World Bank data collection "
        "script fetched real GDP, CPI, and lending rate data via a live API -- "
        "receiving a GREEN banner. The EIA oil price and CBN exchange rate scripts, "
        "lacking API keys, fell back to synthetic data -- receiving RED banners. "
        "But the scripts were designed so that setting the relevant environment "
        "variables (EIA_API_KEY, FRED_API_KEY) would automatically upgrade the "
        "output from RED to GREEN without any code changes."
    )
    pdf.para(
        "This interaction established a key design principle: AI simulation outputs "
        "should be designed for upgrade. The synthetic data is not a final state; "
        "it is a placeholder that the real data will replace by running the same "
        "script with a real API key. The framework does not treat RED as a permanent "
        "failure -- it treats it as a defined state in a progression toward GREEN. "
        "This framing transformed the Replacement Obligation from a burden to an "
        "engineering specification."
    )

    pdf.h2("E.5  The IRB Boundary: Where AI Simulation Cannot Go")
    pdf.para(
        "O3, the Delphi requirements modelling objective, produced the clearest "
        "articulation of the boundary between AI simulation and genuine research "
        "that cannot be simulated. The Delphi instruments (Round 1/2/3 questionnaires) "
        "were AMBER -- AI can design a Delphi instrument from domain knowledge. "
        "The Delphi analysis (n=20, seed=42 synthetic experts) was RED -- AI can "
        "simulate what consensus looks like numerically."
    )
    pdf.para(
        "But the PI raised a fundamental question: what is the point of the Delphi "
        "simulation if it has no validity? The AI's response articulated the "
        "pedagogical purpose of RED outputs: they show the research team what a "
        "finished Delphi looks like, what consensus statistics to expect, and how "
        "the analysis pipeline works -- before the team undertakes the real Delphi "
        "with real Nigerian QS and construction experts. The simulation is a "
        "rehearsal, not a substitute. That distinction -- rehearsal vs substitute -- "
        "became the conceptual core of the Human Validation Gate."
    )
    pdf.para(
        "The interaction also produced the project's clearest statement of the "
        "AI's limits: the real Delphi requires IRB approval from ABU Zaria ethics "
        "board, genuine expert recruitment, and real deliberation. No AI tool, "
        "however capable, can obtain IRB approval or substitute for the expert "
        "knowledge of Nigerian construction practitioners. Those obligations remain "
        "entirely with the human researcher -- and the S2RF exists precisely to "
        "make that fact explicit."
    )

    pdf.h2("E.6  The Architecture Decision: Embedding Quality in the Database")
    pdf.para(
        "O4, Step 2 produced a conceptual innovation that extended the S2RF beyond "
        "documents and into the live system itself. When designing the Supabase "
        "database schema for iNHCES, the PI directed that the GREEN/AMBER/RED data "
        "quality signal should not be confined to PDF documents -- it should be "
        "embedded in the database as a data_source_level column on every "
        "observation row, propagated through the FastAPI response fields, and "
        "rendered as a visible DataSourceBadge component in the Next.js frontend."
    )
    pdf.para(
        "This decision -- to treat data quality as a first-class attribute of every "
        "data point in the system, visible to end users -- transformed the S2RF from "
        "a document-level audit tool into a system-level transparency mechanism. "
        "A quantity surveyor using the live iNHCES system sees, on every macro "
        "variable displayed, whether that variable came from a live API (GREEN) or "
        "a synthetic fallback (RED). The researcher's integrity obligation is thus "
        "communicated directly to the end user, without requiring the user to read "
        "a methodology section."
    )
    pdf.key_finding_box(
        "DISCOVERY MOMENT -- Data Quality as System Architecture (April 2026)",
        "The decision to embed data_source_level as a database column and propagate "
        "it to the user interface was not in any prior AI integrity framework. "
        "It emerged from the PI's question: 'How do we make sure end users of the "
        "live system know which data is real?' The answer -- embed it in the schema "
        "-- is a replicable architectural pattern for any AI-assisted research system "
        "serving live data to users who must understand its provenance."
    )

    pdf.h2("E.7  The Honest Failure: When the AI Reported What It Should Not Hide")
    pdf.para(
        "O5, Step 3 (SHAP analysis) produced a result that created a significant "
        "integrity test. The SHAP TreeExplainer on the LightGBM champion model "
        "returned near-zero SHAP values for all features -- because with n=22 "
        "training rows, the model had converged to near-constant prediction, making "
        "SHAP attributions statistically meaningless. The AI could have switched to "
        "a different explainer, normalised the values, or omitted the result. "
        "Instead, on direction from the PI, it reported the near-zero result honestly, "
        "with a full explanation of why it occurred (insufficient data at n=22) and "
        "a clear statement that the result would change with real NIQS data."
    )
    pdf.para(
        "This interaction produced an important S2RF meta-rule: the framework "
        "requires honest reporting of simulation limitations, even when -- especially "
        "when -- those limitations make the simulation output look unconvincing. "
        "A simulation that only produces impressive-looking results is not a "
        "useful research scaffold -- it is a source of false confidence. The "
        "near-zero SHAP result, properly labelled and explained, is more useful "
        "to the research team than a fabricated importance chart would be."
    )

    pdf.h2("E.8  The System Goes Live: End-to-End Quality Propagation")
    pdf.para(
        "The completion of O6 -- 15 implementation sessions producing a fully "
        "deployed FastAPI backend (17 routes), Next.js frontend (8 pages), 7 Airflow "
        "DAGs, 73/73 passing tests, and a 4-job CI/CD pipeline -- marked the "
        "point at which the S2RF became demonstrably end-to-end. The GREEN/AMBER/RED "
        "signal now flows from the raw API data observation, through the Supabase "
        "database column, through the FastAPI response schema, through the "
        "TypeScript interface, to the DataSourceBadge visible in the user's browser. "
        "No intermediate step loses the data provenance signal."
    )
    pdf.para(
        "The CI/CD pipeline added a further dimension to the Human Validation Gate: "
        "the GitHub Actions deploy.yml workflow enforces that no code reaches Railway "
        "or Vercel unless all 73 backend tests pass and the Next.js build succeeds. "
        "This automated gating is the first instance of the Human Validation Gate "
        "being enforced by code rather than by researcher discipline alone -- a "
        "significant maturation of the framework from principle to mechanism."
    )

    pdf.h2("E.9  The Framework Recognised: From Practice to Publication")
    pdf.para(
        "Paper P9 was not planned at the outset of the iNHCES project. It emerged "
        "from a session in which the PI observed that the interactions producing "
        "the S2RF were themselves a significant research contribution -- and one "
        "that was not being captured in Papers P1-P8, which reported the technical "
        "research findings rather than the process that produced them. The decision "
        "to document the S2RF as a standalone methodological paper was itself an "
        "exercise in human validation: the PI recognised a contribution that the AI "
        "had not identified as publishable on its own, and directed that it be "
        "documented, named, and submitted."
    )
    pdf.para(
        "The framework was subsequently extended in two directions that this "
        "appendix itself documents: first, to non-VS Code AI platforms (Claude.ai, "
        "ChatGPT, Gemini, DeepSeek) to make it accessible to researchers without "
        "system development backgrounds; and second, to the current appendix, which "
        "documents the interaction history itself as a research record. Both "
        "extensions were requested by the PI, demonstrating the Human Validation "
        "Gate in operation: the researcher's judgement -- about what is important, "
        "what deserves documentation, and what the research community needs -- "
        "remains the irreplaceable driving force of the S2RF."
    )

    pdf.h2("E.10  Reflection by the Principal Investigator")
    pdf.placeholder_box(
        "Dr. Bello Abdullahi, Principal Investigator: "
        "This section is reserved for a first-person reflection (300-500 words) "
        "on the experience of developing and applying the S2RF. Suggested themes: "
        "(1) What surprised you most about using AI tools in this research context? "
        "(2) What was the most important decision you made that the AI could not "
        "have made for you? "
        "(3) How did you experience the boundary between AI scaffold and real research? "
        "(4) What would you tell a postgraduate student beginning their first "
        "AI-assisted research project? "
        "This reflection is a critical component of Paper P9 -- it provides the "
        "human researcher's voice as a counterpoint to the technical framework "
        "documentation, and it is the section of this paper that no AI can write."
    )

    pdf.h2("E.11  Summary Timeline of S2RF Development")
    tl = [30, PAGE_W - 30]
    pdf.thead(["Milestone", "S2RF Rule or Component That Emerged"], tl)
    timeline_rows = [
        ("O1 Step 1-2 (April 2026)\nFirst AI outputs produced",
         "DATA SOURCE Declaration System first applied (GREEN for PRISMA protocol; AMBER for taxonomy table)"),
        ("O1 Step 5 (April 2026)\nFirst RED-banner document",
         "Replacement Obligation formalised: RED-banner content MUST be replaced before publication"),
        ("O2 Step 1 (April 2026)\nLive API vs synthetic fallback",
         "Upgrade path design principle: scripts designed for automatic RED-to-GREEN upgrade on API key provision"),
        ("O3 Delphi simulation (April 2026)\nIRB boundary articulated",
         "Human Validation Gate formalised: AI simulation is rehearsal, not substitute; IRB obligations remain with researcher"),
        ("O4 Step 2 (April 2026)\nDB schema design",
         "Data quality as system architecture: data_source_level column embedded in Supabase schema"),
        ("O5 Step 3 (April 2026)\nNear-zero SHAP reported honestly",
         "Honest failure reporting: simulation limitations must be disclosed, not hidden"),
        ("O6 S12 (April 2026)\n73/73 tests passing (GREEN)",
         "Automated Human Validation Gate: CI/CD enforces test passage before any deployment"),
        ("O6 Complete (April 2026)\nDataSourceBadge in browser",
         "End-to-end quality propagation: GREEN/AMBER/RED visible to live system end users"),
        ("P9 initiated (April 2026)\nFramework recognised as contribution",
         "Framework crystallisation: practice documented as named, publishable S2RF methodology"),
        ("P9 extended (April 2026)\nNon-VS Code platforms added",
         "Platform independence confirmed: S2RF rules apply across Claude.ai, ChatGPT, Gemini, DeepSeek"),
    ]
    for i, (milestone, rule) in enumerate(timeline_rows):
        pdf.mrow([milestone, rule], tl, fill=(i % 2 == 1))
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 4.5, sanitize(
        "Table 12: Chronological development of S2RF rules and components through "
        "human-AI interactions during the iNHCES project, April 2026."
    ))
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(2)


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    out = os.path.join(OUT_DIR, 'P9_AI_Research_Simulation_Draft.pdf')
    pdf = PaperPDF()

    make_title_page(pdf)

    _ds_page(pdf, 'amber',
        "DATA SOURCE: AMBER -- AI-AUTHORED FRAMEWORK AND METHODOLOGY PAPER",
        (
            "WHAT IS REAL IN THIS DOCUMENT:\n"
            "  * The Simulation to Research Framework (S2RF) rules and design "
            "are real -- derived from actual iNHCES project decisions across ~20 sessions.\n"
            "  * All iNHCES project statistics (number of PDFs, scripts, objectives, "
            "papers, DATA SOURCE levels) reflect actual project outputs.\n"
            "  * The DATA SOURCE Declaration System, Governing Preamble, Replacement "
            "Obligation, Human Validation Gate, and Platform Independence (Section 4.6) "
            "are real framework components in use in the iNHCES project.\n"
            "  * International ethics framework citations (COPE, ICMJE, UNESCO, "
            "Elsevier, Springer) are real frameworks. [VERIFY specific policy URLs "
            "and publication years before submission.]\n\n"
            "WHAT IS AI-GENERATED / PLACEHOLDER:\n"
            "  * Full manuscript text was drafted by Claude Code. "
            "The research team must review, validate, and own before submission.\n"
            "  * Quantitative pedagogical evidence (workshop outcomes, student "
            "survey data, assessment scores) is a PLACEHOLDER. "
            "Conduct ABU Zaria pilot workshop before submission.\n"
            "  * The Appendix E developmental chronicle documents the actual "
            "interaction milestones truthfully. The PI's Section E.10 reflection "
            "is a PLACEHOLDER -- Dr. Bello Abdullahi must write this in his own words.\n\n"
            "REQUIRED BEFORE SUBMISSION:\n"
            "  1. Conduct ABU Zaria postgraduate pilot workshop (n >= 20 students)\n"
            "  2. Collect pre/post survey data, assessment scores, reflections\n"
            "  3. Replace all [PLACEHOLDER] sections with real workshop findings\n"
            "  4. Verify all citations in Scopus / Web of Science\n"
            "  5. Remove all [VERIFY] tags after checking each reference\n"
            "  6. Fill [FIRST AUTHOR NAME] and co-author details on title page\n"
            "  7. Insert TETFund grant number\n"
            "  8. Obtain ABU Zaria IRB approval for the workshop study\n"
            "  9. Include final AI Disclosure Statement\n"
            " 10. Write Section E.10 (PI Reflection) in Dr. Bello Abdullahi's own words\n"
            " 11. Validate O4-O6 implementation walkthrough (Sections 5.4-5.6) against\n"
            "     the actual deployed system; update any discrepancies before submission\n"
            " 12. Select target journal and format to submission guidelines"
        )
    )

    make_abstract(pdf)
    section1(pdf)
    section2(pdf)
    section3(pdf)
    section4(pdf)
    section4_5(pdf)
    section4_6(pdf)
    section5(pdf)
    section6(pdf)
    section7(pdf)
    section8(pdf)
    section9(pdf)
    ai_disclosure(pdf)
    references(pdf)
    appendices(pdf)
    appendix_d(pdf)
    appendix_e(pdf)

    pdf.output(out)
    print(f"[OK]  P9_AI_Research_Simulation_Draft.pdf  saved -> {out}")
    print(f"      Pages: {pdf.page}")
    print("      DATA SOURCE: AMBER")
    print("      Target journals: Computers & Education | IETI | AI & Society")


if __name__ == "__main__":
    main()
