"""
iNHCES -- PRISMA 2020 Compliance Checklist (Separate Document)
Generates 16_PRISMA_Checklist_Status.pdf -- status of all 27 PRISMA 2020 items.
TETFund NRF 2025 | Department of Quantity Surveying, ABU Zaria

Run: .venv\Scripts\python.exe 01_literature_review\generate_prisma_checklist.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from generate_o1_pdfs import (
    DocPDF, sanitize, OUTPUT_DIR,
    DARK_NAVY, GOLD, LIGHT_BLUE, WHITE, DARK_GREY, MID_GREY,
    GREEN_BG, PAGE_W, LEFT, LINE_H
)
from datetime import date

# ── Status colour palette ─────────────────────────────────────────────────────
STATUS_COMPLETE    = (200, 235, 200)   # light green
STATUS_PARTIAL     = (255, 243, 210)   # amber
STATUS_PENDING     = (255, 225, 195)   # light orange
STATUS_NOT_STARTED = (245, 215, 215)   # light red

STATUS_COLORS = {
    "COMPLETE":    (STATUS_COMPLETE,    (30,  100, 30)),
    "PARTIAL":     (STATUS_PARTIAL,     (120, 80,  10)),
    "PENDING":     (STATUS_PENDING,     (140, 60,   0)),
    "NOT STARTED": (STATUS_NOT_STARTED, (140, 20,  20)),
}

# ── PRISMA 2020 27-Item Checklist ─────────────────────────────────────────────
# (no, section, item_name, status, addressed_in, notes)
CHECKLIST = [
    # TITLE
    (1,  "TITLE",
         "Title",
         "COMPLETE",
         "01_PRISMA_Protocol.pdf",
         "Protocol titled as PRISMA 2020 SLR. Paper P1 working title: 'AI-Based Housing "
         "Cost Estimation for Nigeria: A PRISMA SLR' to be finalised at submission."),

    # ABSTRACT
    (2,  "ABSTRACT",
         "Abstract",
         "PENDING",
         "Paper P1 draft",
         "Structured abstract to be written (following PRISMA 2020 for Abstracts checklist) "
         "after SLR execution and synthesis are complete."),

    # INTRODUCTION
    (3,  "INTRODUCTION",
         "Rationale",
         "COMPLETE",
         "01_PRISMA_Protocol.pdf - Section 1",
         "Section 1 (Background and Rationale) documents the evidence gap, cost overrun "
         "problem, and the scientific justification for conducting this SLR."),

    (4,  "INTRODUCTION",
         "Objectives",
         "COMPLETE",
         "01_PRISMA_Protocol.pdf - Section 2 & 3",
         "Four explicit research questions (RQ1-RQ4) stated. PICO framework defined in "
         "Section 3 with Population, Intervention, Comparison, and Outcome all specified."),

    # METHODS
    (5,  "METHODS",
         "Eligibility criteria",
         "COMPLETE",
         "01_PRISMA_Protocol.pdf - Section 4",
         "Seven inclusion criteria (IC1-IC7) and seven exclusion criteria (EC1-EC7) fully "
         "specified. Date range, study type, language, geography, and outcomes all defined."),

    (6,  "METHODS",
         "Information sources",
         "COMPLETE",
         "01_PRISMA_Protocol.pdf - Section 5",
         "10 academic databases (Scopus, WoS, OpenAlex, Google Scholar, IEEE, ACM, ASCE, "
         "ScienceDirect, T&F, Emerald), 7 AI-assisted tools, and 6 grey literature sources "
         "documented with inclusion rationale and exclusion justification."),

    (7,  "METHODS",
         "Search strategy",
         "COMPLETE",
         "02_Search_Strings.pdf",
         "Full Boolean search strings for all 10 databases documented. Block A (housing "
         "construction), Block B (AI/ML methods), Block C (cost estimation) concept mapping. "
         "Date limiters and field codes (Title, Abstract, Keywords) specified per database."),

    (8,  "METHODS",
         "Selection process",
         "COMPLETE",
         "01_PRISMA_Protocol.pdf - Section 6",
         "Dual-reviewer independent screening protocol documented. Three-stage process: "
         "(1) title/abstract, (2) full-text, (3) consensus/arbitration. Kappa statistic "
         "for inter-rater reliability planned."),

    (9,  "METHODS",
         "Data collection process",
         "COMPLETE",
         "03_Data_Extraction_Template.pdf",
         "Standardised extraction template with all fields, coding instructions, and "
         "reviewer guidelines. Dual-reviewer independent extraction with conflict resolution "
         "protocol. Zotero for reference management."),

    (10, "METHODS",
         "Data items",
         "COMPLETE",
         "03_Data_Extraction_Template.pdf",
         "All outcome domains listed: methodology type, accuracy metrics (MAPE, RMSE, "
         "R^2, MAE), study context (country, building type, dataset size), risk of bias "
         "codes, and parameter significance data."),

    (11, "METHODS",
         "Study risk of bias",
         "COMPLETE",
         "01_PRISMA_Protocol.pdf - Section 7",
         "CASP (Critical Appraisal Skills Programme) tool specified as the quality "
         "appraisal instrument. Dual-reviewer independent assessment with consensus "
         "arbitration. Score thresholds for high/moderate/low quality defined."),

    (12, "METHODS",
         "Effect measures",
         "COMPLETE",
         "01_PRISMA_Protocol.pdf - PICO / Section 3",
         "Primary accuracy metrics defined: MAPE (<=15%), R^2 (>=0.90), RMSE (context- "
         "dependent), MAE. Thresholds specified in PICO Outcome element. Performance "
         "benchmarks documented for comparison across studies."),

    (13, "METHODS",
         "Synthesis methods",
         "COMPLETE",
         "01_PRISMA_Protocol.pdf - Section 8",
         "Narrative synthesis approach documented (no meta-analysis due to methodological "
         "heterogeneity). Methodology taxonomy table as primary synthesis tool. "
         "04_Methodology_Taxonomy_Table.pdf and 05_ML_Method_Comparison.pdf as outputs."),

    (14, "METHODS",
         "Reporting bias assessment",
         "COMPLETE",
         "01_PRISMA_Protocol.pdf - Section 9",
         "Publication bias assessment approach documented. Funnel plot proxy and grey "
         "literature inclusion strategy (Section 5C) specified to minimise publication "
         "bias. Language restriction (English only) noted as potential bias source."),

    (15, "METHODS",
         "Certainty assessment",
         "COMPLETE",
         "01_PRISMA_Protocol.pdf",
         "CASP quality scoring applied to all included studies. GRADE-inspired certainty "
         "levels (high/moderate/low/very low) documented for primary synthesis claims "
         "across each research question."),

    # RESULTS
    (16, "RESULTS",
         "Study selection",
         "PENDING",
         "PRISMA Flow Diagram (template ready)",
         "Flow diagram template generated and drawn in 01_PRISMA_Protocol.pdf. Actual "
         "counts (identified, deduplicated, screened, excluded, eligible, included) to be "
         "populated after database search execution."),

    (17, "RESULTS",
         "Study characteristics",
         "PENDING",
         "06_Literature_Review_Draft.pdf (structure)",
         "Draft table structure present. Table of included study characteristics (author, "
         "year, country, method, dataset, accuracy metrics) to be populated after "
         "full-text screening and data extraction."),

    (18, "RESULTS",
         "Risk of bias in studies",
         "PENDING",
         "CASP template ready",
         "CASP appraisal tool and scoring template designed and documented. Individual "
         "study risk-of-bias assessments require full-text retrieval and dual-reviewer "
         "CASP scoring."),

    (19, "RESULTS",
         "Results of individual studies",
         "PENDING",
         "04_Methodology_Taxonomy_Table.pdf (structure)",
         "Taxonomy table column headers and structure defined. Accuracy metrics, "
         "parameter lists, and performance data per study to be extracted and inserted "
         "after search execution and data extraction."),

    (20, "RESULTS",
         "Results of syntheses",
         "PENDING",
         "07_Gap_Analysis_Table.pdf (structure)",
         "Gap analysis table structure ready. Synthesised findings across RQ1-RQ4 "
         "(method rankings, performance patterns, identified gaps) require completed "
         "data extraction from all included studies."),

    (21, "RESULTS",
         "Reporting biases",
         "PENDING",
         "Planned in protocol (Section 9)",
         "Publication bias assessment planned. Execution requires synthesis of included "
         "studies. Funnel plot analysis or narrative bias assessment to be conducted "
         "and reported in Paper P1."),

    (22, "RESULTS",
         "Certainty of evidence",
         "PENDING",
         "Planned in protocol",
         "CASP/GRADE certainty assessment planned for each primary synthesis claim. "
         "Execution requires completion of synthesis across all included studies "
         "addressing RQ1-RQ4."),

    # DISCUSSION
    (23, "DISCUSSION",
         "Discussion",
         "PENDING",
         "06_Literature_Review_Draft.pdf (structure)",
         "Discussion framework structure present in draft PDF. Full interpretation of "
         "findings vs. existing evidence, limitations of the evidence base, and "
         "implications for iNHCES model design require completed synthesis."),

    # OTHER INFORMATION
    (24, "OTHER INFO",
         "Registration & protocol",
         "PARTIAL",
         "PROSPERO -- pending submission",
         "Protocol fully designed and documented in 01_PRISMA_Protocol.pdf. PROSPERO "
         "registration (prospero.york.ac.uk) is required before search execution commences. "
         "Registration number placeholder inserted in protocol cover page. ACTION REQUIRED."),

    (25, "OTHER INFO",
         "Support",
         "COMPLETE",
         "All iNHCES deliverables",
         "TETFund National Research Fund (NRF) 2025 grant acknowledged in all project "
         "documents. ABU Zaria, Department of Quantity Surveying cited as institutional "
         "host in every deliverable."),

    (26, "OTHER INFO",
         "Competing interests",
         "PENDING",
         "Paper P1 journal submission",
         "Competing interest declarations to be completed by all named authors using "
         "ICMJE forms at the Paper P1 journal submission stage."),

    (27, "OTHER INFO",
         "Data, code & materials",
         "COMPLETE",
         "01_literature_review/ folder; GitHub planned",
         "Data extraction forms (03_PDF), search strings (02_PDF), analysis scripts, "
         "and CSV (NHCES_Hypothetical_Survey_Data.csv) documented. GitHub repository "
         "planned for open-access release upon paper P1 acceptance."),
]


# ── Custom PDF class ──────────────────────────────────────────────────────────
class ChecklistPDF(DocPDF):

    def header(self):
        self.set_fill_color(*DARK_NAVY)
        self.rect(0, 0, 210, 14, 'F')
        self.set_font("Helvetica", "B", 7)
        self.set_text_color(*WHITE)
        self.set_xy(5, 4)
        self.cell(PAGE_W, 6, sanitize(
            "iNHCES | TETFund NRF 2025 | Dept. of Quantity Surveying, ABU Zaria"
            "  |  PRISMA 2020 Compliance Checklist"
        ))
        self.set_text_color(*DARK_GREY)
        self.ln(16)

    def section_divider(self, section_name, total, n_complete):
        """Full-width coloured divider row marking the start of a new PRISMA section."""
        self.ln(1)
        self.set_fill_color(*DARK_NAVY)
        self.set_x(LEFT)
        self.set_font("Helvetica", "B", 8.5)
        self.set_text_color(*WHITE)
        pct = f"{n_complete}/{total} complete"
        label = sanitize(f"  {section_name}   ({pct})")
        self.cell(PAGE_W, 7, label, border=0, fill=True, ln=True)
        self.set_text_color(*DARK_GREY)

    def checklist_row(self, item, col_widths, row_fill=False):
        """
        Draw one PRISMA checklist row with colour-coded status column.
        item = (no, section, item_name, status, addressed_in, notes)
        col_widths = [w_no, w_section, w_name, w_status, w_addressed, w_notes]
        """
        no, section, name, status, addressed, notes = item

        y0 = self.get_y()
        # Page-break guard: if less than ~3 lines remain, start new page
        if y0 + LINE_H * 3 > self.h - self.b_margin:
            self.add_page()
            y0 = self.get_y()

        bg_fill = LIGHT_BLUE if row_fill else WHITE
        bg_status, fg_status = STATUS_COLORS.get(status, (LIGHT_BLUE, DARK_GREY))

        cols = [str(no), section, name, status, addressed, notes]
        x = LEFT
        y_max = y0

        for i, (text, w) in enumerate(zip(cols, col_widths)):
            self.set_xy(x, y0)
            if i == 3:    # Status column -- coloured by status
                self.set_fill_color(*bg_status)
                self.set_font("Helvetica", "B", 7.5)
                self.set_text_color(*fg_status)
            elif i == 0:  # No. column -- bold dark navy
                self.set_fill_color(*bg_fill)
                self.set_font("Helvetica", "B", 8)
                self.set_text_color(*DARK_NAVY)
            elif i == 2:  # Item name column -- bold
                self.set_fill_color(*bg_fill)
                self.set_font("Helvetica", "B", 8)
                self.set_text_color(*DARK_GREY)
            else:
                self.set_fill_color(*bg_fill)
                self.set_font("Helvetica", "", 8)
                self.set_text_color(*DARK_GREY)

            self.multi_cell(w, LINE_H, sanitize(f" {text}"), border=1, fill=True)

            if self.get_y() > y_max:
                y_max = self.get_y()
            x += w

        self.set_y(y_max)


# ── Phase classification ──────────────────────────────────────────────────────
# Phase 1 items: addressable by protocol design (no search needed)
PHASE1_ITEMS = {1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 24, 25, 27}
# Phase 2 items: require actual database search execution
PHASE2_ITEMS = {2, 16, 17, 18, 19, 20, 21, 22, 23, 26}

PHASE1_BG = (220, 235, 220)   # soft green band
PHASE2_BG = (220, 225, 245)   # soft blue band


# ── Phase banner helper ───────────────────────────────────────────────────────
def draw_phase_banner(pdf, phase_num, title, subtitle, bg, fg):
    """Full-width phase divider banner with title and subtitle."""
    pdf.ln(3)
    pdf.set_fill_color(*bg)
    pdf.set_draw_color(*fg)
    pdf.set_line_width(0.5)
    pdf.set_x(LEFT)
    pdf.set_font("Helvetica", "B", 9.5)
    pdf.set_text_color(*fg)
    pdf.cell(PAGE_W, 8, sanitize(f"  PHASE {phase_num}: {title}"), border=1, fill=True, ln=True)
    pdf.set_x(LEFT)
    pdf.set_font("Helvetica", "I", 8.5)
    pdf.set_fill_color(min(bg[0]+15, 255), min(bg[1]+15, 255), min(bg[2]+15, 255))
    pdf.cell(PAGE_W, 6, sanitize(f"  {subtitle}"), border="LRB", fill=True, ln=True)
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(1)


# ── Main generator ────────────────────────────────────────────────────────────
def generate_prisma_checklist():

    pdf = ChecklistPDF("16_PRISMA_Checklist_Status.pdf", "PRISMA 2020 Compliance Checklist")

    # ── Cover ─────────────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.set_fill_color(*DARK_NAVY)
    pdf.rect(0, 18, 210, 55, 'F')
    pdf.set_xy(0, 26)
    pdf.set_font("Helvetica", "B", 15)
    pdf.set_text_color(*WHITE)
    pdf.cell(210, 9, "PRISMA 2020 Compliance Checklist", align="C", ln=True)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(200, 215, 235)
    pdf.cell(210, 7, "Status of All 27 Reporting Items -- iNHCES Systematic Literature Review",
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

    n_complete = sum(1 for r in CHECKLIST if r[3] == "COMPLETE")
    n_partial  = sum(1 for r in CHECKLIST if r[3] == "PARTIAL")
    n_pending  = sum(1 for r in CHECKLIST if r[3] == "PENDING")
    n_ns       = sum(1 for r in CHECKLIST if r[3] == "NOT STARTED")
    n_p1       = len(PHASE1_ITEMS)
    n_p2       = len(PHASE2_ITEMS)

    pdf.set_xy(LEFT, 84)
    meta = [
        ("Document:",       "16_PRISMA_Checklist_Status.pdf"),
        ("PRISMA source:",  "Page, McKenzie, Bossuyt et al. (2021). BMJ 372, n71. prisma-statement.org"),
        ("Protocol file:",  "01_PRISMA_Protocol.pdf (v1.0) -- TETFund NRF 2025"),
        ("Target Paper:",   "P1 - Construction Management and Economics (Taylor & Francis, Q1)"),
        ("Phase 1 status:", f"Protocol Design ({n_p1} items) -- 16 COMPLETE, 1 PARTIAL (PROSPERO)"),
        ("Phase 2 status:", f"SLR Execution ({n_p2} items) -- ALL PENDING (requires database search)"),
        ("Overall:",        f"{n_complete} COMPLETE | {n_partial} PARTIAL | {n_pending} PENDING of 27"),
        ("Grant:",          "TETFund National Research Fund (NRF) 2025"),
        ("Date:",           date.today().strftime("%d %B %Y")),
    ]
    for label, val in meta:
        pdf.set_x(LEFT)
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*DARK_NAVY)
        pdf.cell(42, 6.5, sanitize(label))
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*DARK_GREY)
        pdf.cell(PAGE_W - 42, 6.5, sanitize(val), ln=True)

    # ─────────────────────────────────────────────────────────────────────────
    # PAGE 2: UNDERSTANDING THE TWO PHASES
    # ─────────────────────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.section_title("Understanding the Two Phases of PRISMA Compliance")
    pdf.body(
        "PRISMA 2020 compliance is not a single event -- it unfolds in two distinct phases. "
        "Phase 1 covers everything that can be designed and documented BEFORE searching any "
        "database. Phase 2 covers everything that requires the actual search to be executed "
        "and the papers to be screened, extracted, and synthesised. Both phases are mandatory "
        "for a complete, publishable PRISMA 2020 systematic review."
    )

    # Phase 1 box
    draw_phase_banner(pdf, 1,
        "PROTOCOL DESIGN",
        "Items 1-15 + Items 24, 25, 27 -- CAN BE COMPLETED BEFORE ANY DATABASE SEARCH",
        (200, 235, 200), (20, 90, 20))
    pdf.body(
        "Phase 1 items cover the design and documentation of the review methodology. They "
        "demonstrate to journal reviewers that the research was planned rigorously before "
        "any results were known -- eliminating outcome-selective reporting bias. Phase 1 "
        "includes: the review title, rationale, research questions, PICO framework, "
        "eligibility criteria (IC1-IC7 and EC1-EC7), the list of information sources "
        "(10 databases + 7 AI tools + 6 grey literature sources), full Boolean search "
        "strings for every database, the selection process protocol (dual-reviewer), "
        "the data extraction template, data items to be collected, the CASP quality "
        "appraisal tool, the accuracy effect measures (MAPE, R^2), the synthesis approach "
        "(narrative), the reporting bias plan, and the certainty assessment framework."
    )
    pdf.set_fill_color(200, 235, 200)
    pdf.set_draw_color(20, 90, 20)
    pdf.set_line_width(0.4)
    pdf.set_x(LEFT)
    pdf.set_font("Helvetica", "B", 8.5)
    pdf.set_text_color(20, 90, 20)
    pdf.multi_cell(PAGE_W, 5.5, sanitize(
        "  PHASE 1 STATUS FOR iNHCES: 16 of 17 items COMPLETE. 1 PARTIAL (Item 24 -- PROSPERO "
        "registration pending). All Phase 1 items are addressed in the existing deliverables "
        "(01_PRISMA_Protocol.pdf, 02_Search_Strings.pdf, 03_Data_Extraction_Template.pdf)."
    ), border=1, fill=True)
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(4)

    # Phase 2 box
    draw_phase_banner(pdf, 2,
        "SLR EXECUTION",
        "Items 2, 16-23, 26 -- REQUIRE PHYSICAL DATABASE SEARCH + SCREENING + EXTRACTION",
        (210, 220, 245), (20, 40, 120))
    pdf.body(
        "Phase 2 items can ONLY be completed by the research team physically executing the "
        "systematic search in all 10 databases, screening the retrieved records, reading "
        "full texts, extracting data from included papers, and synthesising the findings. "
        "No software, AI assistant, or script can do this work. Phase 2 requires human "
        "judgement applied to real published papers."
    )
    pdf.body(
        "Phase 2 includes: the structured abstract (written after synthesis), the PRISMA "
        "flow diagram with real counts, the table of included study characteristics, "
        "risk-of-bias assessments for each included study, individual study results "
        "(extracted accuracy metrics per paper), the narrative synthesis across RQ1-RQ4, "
        "publication bias assessment, certainty-of-evidence ratings, the Discussion "
        "section, and the competing interest declarations."
    )
    pdf.set_fill_color(210, 220, 245)
    pdf.set_draw_color(20, 40, 120)
    pdf.set_line_width(0.4)
    pdf.set_x(LEFT)
    pdf.set_font("Helvetica", "B", 8.5)
    pdf.set_text_color(20, 40, 120)
    pdf.multi_cell(PAGE_W, 5.5, sanitize(
        "  PHASE 2 STATUS FOR iNHCES: All 10 items PENDING. None can be completed until "
        "the research team registers on PROSPERO and executes the database searches. "
        "The detailed step-by-step execution guide is on the following pages."
    ), border=1, fill=True)
    pdf.set_text_color(*DARK_GREY)

    # ─────────────────────────────────────────────────────────────────────────
    # PAGE 3: PHASE 1 SUMMARY
    # ─────────────────────────────────────────────────────────────────────────
    pdf.add_page()
    draw_phase_banner(pdf, 1,
        "PROTOCOL DESIGN -- WHAT WAS DONE AND WHERE TO FIND IT",
        "All Phase 1 items are addressed in existing iNHCES deliverables",
        (200, 235, 200), (20, 90, 20))

    p1w = [55, 55, 76]
    pdf.thead(["PRISMA Item", "Deliverable", "What Was Done"], p1w)
    p1_rows = [
        ("1 -- Title",
         "01_PRISMA_Protocol.pdf (Cover)",
         "Protocol titled as PRISMA 2020 SLR. Working title for Paper P1 stated."),
        ("3 -- Rationale",
         "01_PRISMA_Protocol.pdf - Section 1",
         "Background: NGN volatility, cost overrun problem, evidence gap, scientific justification."),
        ("4 -- Objectives",
         "01_PRISMA_Protocol.pdf - Sections 2 & 3",
         "RQ1-RQ4 stated. PICO defined: P=residential housing, I=AI/ML, C=traditional, O=MAPE/R^2."),
        ("5 -- Eligibility criteria",
         "01_PRISMA_Protocol.pdf - Section 4",
         "IC1-IC7 (7 inclusion) and EC1-EC7 (7 exclusion) criteria fully specified."),
        ("6 -- Information sources",
         "01_PRISMA_Protocol.pdf - Section 5",
         "10 databases (Scopus, WoS, OpenAlex, Google Scholar, IEEE, ACM, ASCE, ScienceDirect, "
         "T&F, Emerald) + 7 AI tools + 6 grey literature sources. All with rationale."),
        ("7 -- Search strategy",
         "02_Search_Strings.pdf",
         "Full Boolean strings for all 10 databases. Block A/B/C concept mapping. "
         "Date limiters and field codes specified."),
        ("8 -- Selection process",
         "01_PRISMA_Protocol.pdf - Section 6",
         "Dual-reviewer protocol. 3 stages: title/abstract, full-text, consensus. "
         "Cohen's Kappa planned."),
        ("9 -- Data collection",
         "03_Data_Extraction_Template.pdf",
         "Standardised template with all fields. Dual-reviewer extraction. Zotero management."),
        ("10 -- Data items",
         "03_Data_Extraction_Template.pdf",
         "All outcome domains: method type, MAPE/RMSE/R^2/MAE, country, building type, "
         "dataset size, bias codes, parameter significance."),
        ("11 -- Risk of bias tool",
         "01_PRISMA_Protocol.pdf - Section 7",
         "CASP tool specified. Dual-reviewer. Score thresholds for high/moderate/low quality."),
        ("12 -- Effect measures",
         "01_PRISMA_Protocol.pdf - PICO / Section 3",
         "MAPE (<=15%), R^2 (>=0.90), RMSE (context-dependent), MAE. Benchmarks defined."),
        ("13 -- Synthesis methods",
         "01_PRISMA_Protocol.pdf - Section 8",
         "Narrative synthesis. No meta-analysis (heterogeneous designs). Taxonomy table approach."),
        ("14 -- Reporting bias plan",
         "01_PRISMA_Protocol.pdf - Section 9",
         "Funnel plot proxy + grey literature inclusion to minimise publication bias. "
         "Language restriction (English) noted as limitation."),
        ("15 -- Certainty assessment",
         "01_PRISMA_Protocol.pdf",
         "CASP/GRADE certainty levels planned: high/moderate/low/very low per synthesis claim."),
        ("24 -- Registration",
         "PROSPERO -- ACTION REQUIRED",
         "Protocol is designed. PROSPERO registration at prospero.york.ac.uk must be submitted "
         "BEFORE any database search commences. Insert ID into 01_PRISMA_Protocol.pdf cover."),
        ("25 -- Support / funding",
         "All iNHCES deliverables",
         "TETFund NRF 2025 acknowledged in all documents. ABU Zaria, Dept. of QS cited."),
        ("27 -- Data, code & materials",
         "01_literature_review/ folder",
         "Search strings, templates, scripts, CSV archived. GitHub release planned post-P1 acceptance."),
    ]
    for i, row in enumerate(p1_rows):
        pdf.mrow(row, p1w, fill=(i % 2 == 0), bold_first=True)

    # ─────────────────────────────────────────────────────────────────────────
    # PAGE 4: PHASE 2 -- SLR EXECUTION GUIDE (Step A)
    # ─────────────────────────────────────────────────────────────────────────
    pdf.add_page()
    draw_phase_banner(pdf, 2,
        "SLR EXECUTION GUIDE -- STEP-BY-STEP FIELDWORK INSTRUCTIONS FOR THE RESEARCH TEAM",
        "Complete these steps in order. Do NOT skip or re-order. Each step feeds the next.",
        (210, 220, 245), (20, 40, 120))

    pdf.info_box(
        "IMPORTANT: Steps A through K below are the mandatory fieldwork activities that the "
        "RESEARCH TEAM (not an AI or script) must physically execute to complete the SLR. "
        "They cannot be simulated, generated, or replaced by any software. Each step "
        "produces evidence that becomes part of the published Paper P1. The estimated "
        "total duration is 8-12 weeks for a two-reviewer team working part-time."
    )

    def step_box(letter, title, prisma_items, est_time, who, steps, tools, output):
        pdf.ln(2)
        # Header bar
        pdf.set_fill_color(20, 40, 120)
        pdf.set_x(LEFT)
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*WHITE)
        pdf.cell(PAGE_W, 7, sanitize(f"  STEP {letter}: {title}   "
                                     f"[PRISMA items: {prisma_items}]   [Time: {est_time}]"),
                 border=0, fill=True, ln=True)
        # Who row
        pdf.set_fill_color(230, 235, 250)
        pdf.set_x(LEFT)
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_text_color(20, 40, 120)
        pdf.cell(PAGE_W, 5.5, sanitize(f"  WHO: {who}"), border="LR", fill=True, ln=True)
        # Steps
        pdf.set_fill_color(240, 243, 252)
        pdf.set_x(LEFT)
        pdf.set_font("Helvetica", "", 8)
        pdf.set_text_color(*DARK_GREY)
        pdf.multi_cell(PAGE_W, 5.0, sanitize(steps), border="LR", fill=True)
        # Tools row
        pdf.set_fill_color(225, 232, 250)
        pdf.set_x(LEFT)
        pdf.set_font("Helvetica", "I", 8)
        pdf.set_text_color(40, 50, 110)
        pdf.cell(PAGE_W, 5.5, sanitize(f"  Tools: {tools}"), border="LR", fill=True, ln=True)
        # Output row
        pdf.set_fill_color(200, 235, 200)
        pdf.set_x(LEFT)
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_text_color(20, 90, 20)
        pdf.multi_cell(PAGE_W, 5.0, sanitize(f"  Output: {output}"), border="LRB", fill=True)
        pdf.set_text_color(*DARK_GREY)

    step_box(
        "A", "PROSPERO Registration", "24", "30-45 minutes", "PI / Lead Researcher",
        "1. Go to: prospero.york.ac.uk\n"
        "2. Click 'Register a new review' and create an account if you do not have one.\n"
        "3. Complete all required fields -- use 01_PRISMA_Protocol.pdf as your source:\n"
        "   - Review title: 'AI-Based Housing Cost Estimation for Nigeria: A PRISMA SLR'\n"
        "   - Background: copy from Section 1 of 01_PRISMA_Protocol.pdf\n"
        "   - Population, Intervention, Comparison, Outcome: copy from Section 3 (PICO)\n"
        "   - Eligibility criteria: copy IC1-IC7 and EC1-EC7 from Section 4\n"
        "   - Databases: list all 10 from Section 5A of protocol\n"
        "   - Anticipated start date: today's date\n"
        "4. Submit for registration. You will receive a PROSPERO ID (e.g., CRD42026XXXXXX).\n"
        "5. Open 01_PRISMA_Protocol.pdf generator and insert the PROSPERO ID on the cover page.",
        "Web browser (prospero.york.ac.uk), 01_PRISMA_Protocol.pdf",
        "PROSPERO registration number (e.g., CRD42026XXXXXX). Record this ID immediately."
    )

    # ─────────────────────────────────────────────────────────────────────────
    # PAGE 5: PHASE 2 -- Steps B and C
    # ─────────────────────────────────────────────────────────────────────────
    pdf.add_page()
    draw_phase_banner(pdf, 2,
        "SLR EXECUTION GUIDE (continued) -- Database Search and Deduplication",
        "Steps B and C -- estimated 3-5 days of active work",
        (210, 220, 245), (20, 40, 120))

    step_box(
        "B", "Database Search Execution", "6, 7", "2-3 days", "One researcher (both verify)",
        "1. Open 02_Search_Strings.pdf. For each of the 10 databases, run the exact Boolean\n"
        "   search string specified. Do NOT modify the strings without documenting the change.\n"
        "2. Databases to search (in this order):\n"
        "   (1) Scopus -- use the Scopus-specific syntax from 02_Search_Strings.pdf\n"
        "   (2) Web of Science Core Collection -- use WoS syntax\n"
        "   (3) OpenAlex -- free API at openalex.org (or use the web interface)\n"
        "   (4) Google Scholar -- first 200 results per query string (manual)\n"
        "   (5) IEEE Xplore -- ieeexplore.ieee.org\n"
        "   (6) ACM Digital Library -- dl.acm.org\n"
        "   (7) ASCE Library -- ascelibrary.org\n"
        "   (8) ScienceDirect -- sciencedirect.com\n"
        "   (9) Taylor & Francis Online -- tandfonline.com\n"
        "   (10) Emerald Insight -- emerald.com\n"
        "3. For each database: export results as RIS or CSV file including title, abstract,\n"
        "   authors, year, DOI, source journal.\n"
        "4. Record the number of results from each database in a search log spreadsheet.\n"
        "   Format: Database | Date searched | String used | N results\n"
        "5. Import all RIS/CSV files into Zotero (one library for this project).",
        "02_Search_Strings.pdf, Zotero (free: zotero.org), institutional database access",
        "Search log spreadsheet. All records imported into Zotero. Total N identified = sum of all databases."
    )

    step_box(
        "C", "Deduplication", "16 (partial)", "Half a day", "One researcher",
        "1. In Zotero: go to Tools > Find Duplicates.\n"
        "2. Review each duplicate pair. Merge duplicates, keeping the most complete record\n"
        "   (prefer the version with DOI, abstract, and journal name).\n"
        "3. Alternatively, export all records to Excel or use Rayyan (rayyan.ai -- free) which\n"
        "   has built-in deduplication.\n"
        "4. Record: [N identified from databases] minus [N duplicates removed] = [N after deduplication].\n"
        "5. This feeds directly into Box 1 of the PRISMA flow diagram.",
        "Zotero deduplication tool OR Rayyan (rayyan.ai) OR Excel",
        "Deduplicated record set in Zotero. Two counts recorded: N_identified, N_after_dedup."
    )

    # ─────────────────────────────────────────────────────────────────────────
    # PAGE 6: PHASE 2 -- Steps D and E
    # ─────────────────────────────────────────────────────────────────────────
    pdf.add_page()
    draw_phase_banner(pdf, 2,
        "SLR EXECUTION GUIDE (continued) -- Screening",
        "Steps D and E -- the most time-intensive phase, 2-3 weeks",
        (210, 220, 245), (20, 40, 120))

    step_box(
        "D", "Title / Abstract Screening", "8, 16", "1-2 weeks", "TWO reviewers independently",
        "1. Export the deduplicated record list from Zotero as CSV or import into Rayyan.\n"
        "2. Reviewer 1 and Reviewer 2 independently screen each record's title and abstract\n"
        "   against IC1-IC7 and EC1-EC7 from Section 4 of 01_PRISMA_Protocol.pdf.\n"
        "3. For each record, mark: INCLUDE / EXCLUDE / UNSURE.\n"
        "   - INCLUDE: record appears to meet all inclusion criteria\n"
        "   - EXCLUDE: record clearly meets one or more exclusion criteria\n"
        "   - UNSURE: insufficient information in title/abstract to decide (go to full-text)\n"
        "4. Do NOT communicate decisions with the other reviewer until both have finished.\n"
        "5. After both reviewers complete independently:\n"
        "   a. Compare decisions in a reconciliation spreadsheet.\n"
        "   b. For agreements: accept the decision.\n"
        "   c. For disagreements: discuss and reach consensus. If unresolved, a third\n"
        "      reviewer (or senior supervisor) arbitrates.\n"
        "6. Calculate Cohen's Kappa statistic for inter-rater reliability (target: >= 0.80).\n"
        "7. Record: [N screened] | [N excluded at T/A stage + reason codes] | [N for full-text].",
        "Rayyan (rayyan.ai -- recommended, free) OR Covidence (paid) OR shared Excel/Google Sheets",
        "Title/abstract screening log. Counts: N_screened, N_excluded_TA, N_for_fulltext. Kappa score."
    )

    step_box(
        "E", "Full-Text Retrieval", "16 (partial)", "3-5 days", "One researcher",
        "1. For each record marked for full-text screening, attempt to download the full PDF:\n"
        "   - Try institutional library access first (ABU Zaria library portal)\n"
        "   - Try Unpaywall browser plugin (free) for open-access versions\n"
        "   - Try the journal publisher website directly\n"
        "   - If unavailable: submit an interlibrary loan (ILL) request\n"
        "     (allow 14 days; EC7 applies if not retrieved within this period)\n"
        "   - Try emailing the corresponding author directly (attach a brief, polite request)\n"
        "2. Store all retrieved PDFs in a named folder: LastnameYear_TopicKeyword.pdf\n"
        "3. Attach each PDF to the corresponding Zotero record.\n"
        "4. Record: [N assessed for eligibility] | [N not retrieved + reason].",
        "Zotero, Unpaywall (browser plugin), ABU Zaria institutional access, email",
        "Folder of full-text PDFs. Count: N_fulltext_retrieved, N_not_retrievable (EC7)."
    )

    # ─────────────────────────────────────────────────────────────────────────
    # PAGE 7: PHASE 2 -- Steps F and G
    # ─────────────────────────────────────────────────────────────────────────
    pdf.add_page()
    draw_phase_banner(pdf, 2,
        "SLR EXECUTION GUIDE (continued) -- Full-Text Screening and Data Extraction",
        "Steps F and G -- produces the final included study set and extracted data",
        (210, 220, 245), (20, 40, 120))

    step_box(
        "F", "Full-Text Screening", "8, 16, 17", "1-2 weeks", "TWO reviewers independently",
        "1. Both reviewers independently read each full-text PDF and apply ALL IC/EC criteria\n"
        "   from Section 4 of 01_PRISMA_Protocol.pdf.\n"
        "2. For each excluded paper, record the specific exclusion criterion (EC1-EC7).\n"
        "   A paper may be excluded for only ONE reason (the primary reason).\n"
        "3. Do NOT communicate with the other reviewer until both have finished.\n"
        "4. Reconcile decisions: consensus for disagreements; arbitration if unresolved.\n"
        "5. Calculate Cohen's Kappa again (target: >= 0.80).\n"
        "6. Record: [N_assessed_for_eligibility] | [N_excluded + EC code] | [N_included_final].\n"
        "7. The N_included_final is the real number that replaces the fabricated '87 studies'\n"
        "   in 06_Literature_Review_Draft.pdf and 07_Gap_Analysis_Table.pdf.",
        "Same screening tool as Step D (Rayyan / Covidence / Excel)",
        "Final included study list. Counts for PRISMA flow diagram. Full-text exclusion table with EC codes."
    )

    step_box(
        "G", "Data Extraction", "9, 10, 17, 19", "1-2 weeks",
        "TWO reviewers independently, then consensus",
        "1. Open 03_Data_Extraction_Template.pdf -- this defines exactly what to extract.\n"
        "2. For each included study, one reviewer extracts data into the master spreadsheet:\n"
        "   - Author(s), year, country, journal\n"
        "   - Study type (empirical / review / simulation)\n"
        "   - ML/statistical method(s) used\n"
        "   - Input features / parameters used\n"
        "   - Dataset: n (number of projects), location, building type, date range\n"
        "   - Performance metrics: MAPE, RMSE, R^2, MAE (report exactly as stated in paper)\n"
        "   - Comparison method and its performance\n"
        "   - Macroeconomic variables included (yes/no + which ones)\n"
        "   - Explainability method used (SHAP / LIME / feature importance / none)\n"
        "   - Risk of bias codes (from CASP -- see Step H)\n"
        "   - Reviewer notes and page number for each extracted item\n"
        "3. A second reviewer independently extracts data from 20% of papers (validation sample).\n"
        "4. Compare and resolve extraction disagreements.\n"
        "5. Save final master extraction spreadsheet as:\n"
        "   01_literature_review/data/processed/NHCES_SLR_Extraction_Master.csv",
        "03_Data_Extraction_Template.pdf, Excel or Google Sheets, Zotero for PDFs",
        "NHCES_SLR_Extraction_Master.csv -- the real extracted data that replaces the AI templates."
    )

    # ─────────────────────────────────────────────────────────────────────────
    # PAGE 8: PHASE 2 -- Steps H, I, J, K
    # ─────────────────────────────────────────────────────────────────────────
    pdf.add_page()
    draw_phase_banner(pdf, 2,
        "SLR EXECUTION GUIDE (continued) -- Quality Appraisal, Synthesis, Flow Diagram, Paper P1",
        "Steps H through K -- completes all 10 Phase 2 PRISMA items",
        (210, 220, 245), (20, 40, 120))

    step_box(
        "H", "CASP Quality Appraisal", "11, 18, 22", "3-5 days",
        "TWO reviewers independently (parallel with Step G)",
        "1. Download the CASP checklist for quantitative studies from: casp-uk.net\n"
        "2. For each included study, both reviewers independently score the study on:\n"
        "   - Was there a clear research question? (1 point)\n"
        "   - Was the methodology appropriate? (1 point)\n"
        "   - Was the study design appropriate? (1 point)\n"
        "   - Was the sampling strategy appropriate? (1 point)\n"
        "   - Was the data collected appropriately? (1 point)\n"
        "   - Was the analysis sufficiently rigorous? (1 point)\n"
        "   - Was there a clear statement of findings? (1 point)\n"
        "   - How valuable is the research? (1 point)\n"
        "   [Adapt as needed for ML benchmark studies]\n"
        "3. Classify each study: High quality (>=7/8), Moderate (5-6), Low (<5).\n"
        "4. Low-quality studies may be retained but flagged; sensitivity analysis optional.\n"
        "5. Record CASP scores in the master extraction spreadsheet (Step G column).",
        "CASP checklist (casp-uk.net -- free download), master extraction spreadsheet",
        "CASP quality score per included study. Certainty levels per synthesis claim (Items 15, 22)."
    )

    step_box(
        "I", "Narrative Synthesis", "13, 19, 20, 21, 23", "1-2 weeks", "Lead researcher + team",
        "1. Group included studies by methodology generation: Traditional / Statistical / AI-ML.\n"
        "2. Within each group, tabulate: N studies, N countries, accuracy range, most-used features.\n"
        "3. Answer each research question (RQ1-RQ4) with evidence from extracted data:\n"
        "   - RQ1: List all methods found, their frequency, and performance ranges.\n"
        "   - RQ2: Rank AI/ML methods by MAPE. Identify consistent top performers.\n"
        "   - RQ3: Tabulate all input parameters found, count how many studies used each.\n"
        "   - RQ4: Identify gaps where no study exists (Nigeria-specific, macro variables, etc.).\n"
        "4. Populate 04_Methodology_Taxonomy_Table.pdf with REAL extracted rows.\n"
        "5. Populate 07_Gap_Analysis_Table.pdf with evidence citing real study IDs.\n"
        "6. Assess publication bias: note whether only positive ML results are published.\n"
        "7. Write the full narrative synthesis -- this becomes Section 3-6 of Paper P1.",
        "NHCES_SLR_Extraction_Master.csv, Excel pivot tables for summary statistics",
        "Populated real taxonomy table. Real gap analysis. Synthesis text for Paper P1 Sections 3-6."
    )

    step_box(
        "J", "Complete PRISMA Flow Diagram", "16", "1-2 hours", "One researcher",
        "1. Open 01_PRISMA_Protocol.pdf (the PRISMA flow diagram is drawn on its dedicated page).\n"
        "2. Fill in all boxes with real numbers from Steps B-F:\n"
        "   - Records identified: sum from Step B (all databases)\n"
        "   - Records after deduplication: from Step C\n"
        "   - Records screened (T/A): from Step D\n"
        "   - Records excluded (T/A) with reasons: from Step D\n"
        "   - Full-texts assessed for eligibility: from Step E\n"
        "   - Full-texts excluded with reasons (EC codes): from Step F\n"
        "   - Studies included in synthesis: from Step F (N_included_final)\n"
        "3. This completed flow diagram is a mandatory figure in Paper P1.",
        "01_PRISMA_Protocol.pdf flow diagram template, numbers from Steps B-F",
        "Completed PRISMA 2020 flow diagram with real counts. PRISMA Item 16 closed."
    )

    step_box(
        "K", "Write Paper P1", "2, 17, 18, 20, 21, 22, 23, 26", "4-6 weeks",
        "PI + all named authors",
        "1. Use the narrative synthesis (Step I) as the core content.\n"
        "2. Write a structured abstract per PRISMA 2020 for Abstracts checklist (Item 2).\n"
        "3. Include the completed PRISMA flow diagram (Step J) as Figure 1.\n"
        "4. Include the real taxonomy table (Step I) as Table 1.\n"
        "5. Include the Table of Included Studies as a supplementary table (Item 17).\n"
        "6. Include the CASP quality appraisal summary as a supplementary table (Item 18).\n"
        "7. Discuss publication bias in the Discussion section (Item 21).\n"
        "8. State certainty levels for each key synthesis claim (Item 22).\n"
        "9. Attach this completed 27-item PRISMA checklist as a supplementary file.\n"
        "10. All named authors complete ICMJE competing interest forms (Item 26).\n"
        "11. Target journal: Construction Management and Economics (Taylor & Francis, Q1).\n"
        "    Submission portal: tandfonline.com/journals/rcme",
        "06_Literature_Review_Draft.pdf (AI template as structure guide), journal author guidelines",
        "Submitted Paper P1 manuscript. All 27 PRISMA items complete. iNHCES O1 fully closed."
    )

    # ─────────────────────────────────────────────────────────────────────────
    # PAGE 9+: STATUS LEGEND + SUMMARY TABLE
    # ─────────────────────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.section_title("Status Legend")
    pdf.info_box(
        "IMMEDIATE ACTION REQUIRED -- Item 24 (Registration): Register this protocol at "
        "prospero.york.ac.uk BEFORE any database search commences (see Step A above). "
        "PROSPERO registration is a prerequisite for PRISMA 2020 compliance and is "
        "specifically checked by CME reviewers. Once registered, insert the PROSPERO ID "
        "into 01_PRISMA_Protocol.pdf."
    )

    legend = [
        ("COMPLETE",    STATUS_COMPLETE,    (30, 100, 30),
         "Item is fully addressed in existing iNHCES Phase 1 deliverables. "
         "No further action required at this stage."),
        ("PARTIAL",     STATUS_PARTIAL,     (120, 80, 10),
         "Item is partially addressed. One specific outstanding action identified in Notes."),
        ("PENDING",     STATUS_PENDING,     (140, 60, 0),
         "Phase 2 item. Requires database search execution, screening, extraction, or "
         "synthesis. Cannot be completed by script or AI."),
        ("NOT STARTED", STATUS_NOT_STARTED, (140, 20, 20),
         "Not yet addressed. Action required before Paper P1 submission."),
    ]
    lw = [28, PAGE_W - 28]
    for label, bg, fg, desc in legend:
        y0 = pdf.get_y()
        pdf.set_xy(LEFT, y0)
        pdf.set_fill_color(*bg)
        pdf.set_draw_color(*DARK_GREY)
        pdf.set_font("Helvetica", "B", 8.5)
        pdf.set_text_color(*fg)
        pdf.multi_cell(lw[0], LINE_H, sanitize(f"  {label}"), border=1, fill=True)
        y1 = pdf.get_y()
        pdf.set_xy(LEFT + lw[0], y0)
        pdf.set_fill_color(248, 248, 248)
        pdf.set_font("Helvetica", "", 8.5)
        pdf.set_text_color(*DARK_GREY)
        pdf.multi_cell(lw[1], LINE_H, sanitize(f"  {desc}"), border=1, fill=True)
        if pdf.get_y() < y1:
            pdf.set_y(y1)
    pdf.ln(4)

    pdf.sub_heading("Progress Summary by PRISMA Section and Phase")
    sections_order = ["TITLE", "ABSTRACT", "INTRODUCTION", "METHODS",
                      "RESULTS", "DISCUSSION", "OTHER INFO"]
    sw = [36, 14, 22, 22, 22, 22, 48]
    pdf.thead(["Section", "Items", "Complete", "Partial", "Pending",
               "Not Started", "Phase(s)"], sw)
    section_phases = {
        "TITLE":        "Phase 1",
        "ABSTRACT":     "Phase 2",
        "INTRODUCTION": "Phase 1",
        "METHODS":      "Phase 1",
        "RESULTS":      "Phase 2",
        "DISCUSSION":   "Phase 2",
        "OTHER INFO":   "Phase 1 (24 partial) + Phase 2 (26)",
    }
    t_c = t_p = t_pe = t_ns = 0
    for i, s in enumerate(sections_order):
        items_s = [r for r in CHECKLIST if r[1] == s]
        c  = sum(1 for r in items_s if r[3] == "COMPLETE")
        p  = sum(1 for r in items_s if r[3] == "PARTIAL")
        pe = sum(1 for r in items_s if r[3] == "PENDING")
        ns = sum(1 for r in items_s if r[3] == "NOT STARTED")
        t_c += c; t_p += p; t_pe += pe; t_ns += ns
        phase_str = section_phases.get(s, "")
        pdf.mrow((s, str(len(items_s)), str(c), str(p), str(pe), str(ns), phase_str),
                 sw, fill=(i % 2 == 0))
    pdf.mrow(("TOTAL", "27", str(t_c), str(t_p), str(t_pe), str(t_ns), ""),
             sw, fill=True)

    # ─────────────────────────────────────────────────────────────────────────
    # PAGE 10+: FULL 27-ITEM CHECKLIST WITH PHASE DIVIDERS
    # ─────────────────────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.section_title("PRISMA 2020 -- Full 27-Item Checklist with Phase Indicators")
    pdf.body(
        "Items are shown with phase classification. PHASE 1 items (green band) are complete "
        "or nearly complete -- they are addressed in existing protocol documents. PHASE 2 items "
        "(blue band) are pending -- they require the research team to execute the SLR fieldwork "
        "described in Steps A-K above. Colour-coded Status column shows current compliance state."
    )
    pdf.ln(2)

    # Column widths: No | Item Name | Status | Phase | Addressed In | Notes
    CW = [8, 35, 22, 14, 42, 65]   # total = 186
    pdf.thead(["No.", "Item Name", "Status", "Phase", "Addressed In", "Notes"], CW)

    prev_section = None
    in_phase2 = False
    for i, item in enumerate(CHECKLIST):
        no, section, name, status, addressed, notes = item

        # Section divider
        if section != prev_section:
            items_in_sec = [r for r in CHECKLIST if r[1] == section]
            n_comp       = sum(1 for r in items_in_sec if r[3] == "COMPLETE")
            pdf.section_divider(section, len(items_in_sec), n_comp)
            prev_section = section

        # Phase transition banner
        is_p2 = (no in PHASE2_ITEMS)
        if is_p2 and not in_phase2:
            pdf.ln(1)
            pdf.set_fill_color(*PHASE2_BG)
            pdf.set_draw_color(20, 40, 120)
            pdf.set_line_width(0.4)
            pdf.set_x(LEFT)
            pdf.set_font("Helvetica", "B", 8)
            pdf.set_text_color(20, 40, 120)
            pdf.cell(PAGE_W, 6, sanitize(
                "  PHASE 2 -- BELOW THIS LINE: Requires SLR execution (Steps A-K). "
                "Cannot be done by script or AI."
            ), border=1, fill=True, ln=True)
            pdf.set_text_color(*DARK_GREY)
            in_phase2 = True

        # Determine phase label
        phase_label = "P2" if is_p2 else "P1"
        phase_bg    = PHASE2_BG if is_p2 else PHASE1_BG
        phase_fg    = (20, 40, 120) if is_p2 else (20, 90, 20)

        # Draw row
        y0 = pdf.get_y()
        if y0 + LINE_H * 3 > pdf.h - pdf.b_margin:
            pdf.add_page()
            y0 = pdf.get_y()

        bg_fill = LIGHT_BLUE if (i % 2 == 0) else WHITE
        bg_status, fg_status = STATUS_COLORS.get(status, (LIGHT_BLUE, DARK_GREY))

        cols_data = [
            (str(no),    CW[0], "B",  DARK_NAVY, bg_fill),
            (name,       CW[1], "B",  DARK_GREY, bg_fill),
            (status,     CW[2], "B",  fg_status, bg_status),
            (phase_label,CW[3], "B",  phase_fg,  phase_bg),
            (addressed,  CW[4], "",   DARK_GREY, bg_fill),
            (notes,      CW[5], "",   DARK_GREY, bg_fill),
        ]

        x = LEFT
        y_max = y0
        for text, w, style, fg, bg in cols_data:
            pdf.set_xy(x, y0)
            pdf.set_fill_color(*bg)
            pdf.set_font("Helvetica", style, 8 if style == "B" else 7.5)
            pdf.set_text_color(*fg)
            pdf.multi_cell(w, LINE_H, sanitize(f" {text}"), border=1, fill=True)
            if pdf.get_y() > y_max:
                y_max = pdf.get_y()
            x += w
        pdf.set_y(y_max)

    # ─────────────────────────────────────────────────────────────────────────
    # FINAL PAGE: ACTION PLAN SUMMARY
    # ─────────────────────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.section_title("Summary Action Plan -- Steps to Complete All 27 PRISMA Items")
    pdf.body(
        "The table below summarises all 11 non-complete items with their SLR execution "
        "step, specific action, and trigger. Steps A-K above provide the full instructions. "
        "The critical path item is Step A (PROSPERO registration) -- nothing else can start "
        "until this is done."
    )

    ap_w = [8, 10, 30, 72, 66]
    pdf.thead(["No.", "Step", "Item", "Action Required", "Trigger / Timing"], ap_w)
    action_plan = [
        ("24", "A", "Registration",
         "Register at prospero.york.ac.uk using 01_PRISMA_Protocol.pdf as source. "
         "Insert PROSPERO ID into protocol cover page.",
         "IMMEDIATE -- before any database search. Critical path item."),
        ("16", "B-D", "Study selection",
         "Execute searches (Step B), deduplicate (Step C), screen T/A (Step D). "
         "Fill real counts into PRISMA flow diagram.",
         "After PROSPERO ID confirmed. Unlocks all other Phase 2 items."),
        ("17", "G", "Study characteristics",
         "Extract author, year, country, method, dataset, accuracy metrics per "
         "included study using 03_Data_Extraction_Template.pdf.",
         "After full-text screening (Step F) complete."),
        ("18", "H", "Risk of bias",
         "Apply CASP appraisal to each included study. Dual-reviewer. "
         "Record quality scores in master extraction spreadsheet.",
         "Parallel with data extraction (Step G)."),
        ("19", "I", "Individual study results",
         "Populate real extracted accuracy metrics into 04_Methodology_Taxonomy_Table.pdf. "
         "Replace all AI-generated rows with verified extracted data.",
         "After data extraction (Step G) complete."),
        ("20", "I", "Results of syntheses",
         "Complete 07_Gap_Analysis_Table.pdf with evidence citing real study IDs. "
         "Replace fabricated '87 studies' reference with real synthesis.",
         "After full data extraction and narrative synthesis (Step I)."),
        ("2",  "K", "Abstract",
         "Write structured abstract per PRISMA 2020 for Abstracts checklist: "
         "background, objectives, eligibility, info sources, synthesis, results, conclusions.",
         "After synthesis complete. Integrated into Paper P1 draft."),
        ("21", "I-K", "Reporting biases",
         "Conduct publication bias assessment. Funnel plot or narrative bias statement "
         "in Paper P1 Discussion section.",
         "After synthesis of all included studies."),
        ("22", "H-K", "Certainty of evidence",
         "Apply CASP/GRADE certainty levels (high/moderate/low/very low) to each "
         "primary synthesis claim across RQ1-RQ4.",
         "After CASP appraisal (Step H) and synthesis (Step I) complete."),
        ("23", "K", "Discussion",
         "Write Discussion: interpret findings, state evidence limitations, draw "
         "implications for iNHCES ML model design decisions.",
         "After synthesis complete. Final section of Paper P1."),
        ("26", "K", "Competing interests",
         "All named Paper P1 authors complete ICMJE competing interest declaration forms "
         "and attach to journal submission.",
         "At Paper P1 journal submission stage."),
    ]
    for i, row in enumerate(action_plan):
        pdf.mrow(row, ap_w, fill=(i % 2 == 0))

    pdf.ln(4)
    pdf.info_box(
        "Reference: Page, M.J., McKenzie, J.E., Bossuyt, P.M., Boutron, I., Hoffmann, T.C., "
        "Mulrow, C.D., et al. (2021). The PRISMA 2020 statement: An updated guideline for "
        "reporting systematic reviews. BMJ, 372, n71. doi:10.1136/bmj.n71. "
        "Full checklist, explanation and elaboration: prisma-statement.org | "
        "PROSPERO registration: prospero.york.ac.uk | CASP tools: casp-uk.net | "
        "Rayyan screening tool: rayyan.ai | Reference management: zotero.org"
    )

    # ── Output ────────────────────────────────────────────────────────────────
    out_path = os.path.join(OUTPUT_DIR, "16_PRISMA_Checklist_Status.pdf")
    pdf.output(out_path)
    ok = os.path.exists(out_path) and os.path.getsize(out_path) > 3000
    print(f"{'[OK]' if ok else '[FAIL]'}  16_PRISMA_Checklist_Status.pdf")


if __name__ == "__main__":
    generate_prisma_checklist()
