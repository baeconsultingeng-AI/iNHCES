"""
iNHCES Claude AI Assistance Guide — PDF Generator
TETFund National Research Fund (NRF) 2025
Department of Quantity Surveying, ABU Zaria

Generates: NHCES_Claude_Assistance_Guide.pdf
Replaces the original pre-existing PDF with a version that includes
"Why This Step Is Required" rationale boxes for every step.

Run with:  .venv\Scripts\python.exe Research_Documents\generate_claude_assistance_guide.py
"""

import os
from fpdf import FPDF
from datetime import date

OUTPUT_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "01_S2RF_Claude_AI_Workflow_Guide_iNHCES.pdf"
)

# ── Colour palette ─────────────────────────────────────────────────────────────
DARK_NAVY    = (15,  40,  80)
GOLD         = (180, 140,  30)
LIGHT_BLUE   = (220, 230, 245)
LABEL_BLUE   = (195, 210, 235)
WHITE        = (255, 255, 255)
DARK_GREY    = (60,  60,  60)
MID_GREY     = (120, 120, 120)
GREEN_BG     = (220, 240, 225)
GREEN_BORDER = (60,  140,  80)
AMBER_BG     = (255, 248, 220)
AMBER_BORDER = (180, 130,  20)
CODE_BG      = (245, 245, 245)


def sanitize(text):
    return (str(text)
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
            .replace('\u20a6', 'NGN')
            .encode('latin-1', errors='replace').decode('latin-1'))


class GuidePDF(FPDF):

    def __init__(self, title):
        super().__init__('P', 'mm', 'A4')
        self.title_str = title
        self.set_margins(12, 18, 12)
        self.set_auto_page_break(True, margin=20)

    def header(self):
        self.set_fill_color(*DARK_NAVY)
        self.rect(0, 0, 210, 14, 'F')
        self.set_font("Helvetica", "B", 7.5)
        self.set_text_color(*WHITE)
        self.set_xy(5, 4)
        self.cell(0, 6, sanitize("Implementing the S2RF: A Claude AI Workflow Guide for iNHCES Researchers  |  ABU Zaria / TETFund"), ln=0)
        self.set_text_color(*DARK_GREY)
        self.ln(16)

    def footer(self):
        self.set_y(-13)
        self.set_draw_color(*GOLD)
        self.set_line_width(0.5)
        self.line(12, self.get_y(), 198, self.get_y())
        self.set_font("Helvetica", "", 7.5)
        self.set_text_color(*MID_GREY)
        self.cell(0, 6,
                  sanitize(f"Implementing the S2RF: A Claude AI Workflow Guide for iNHCES Researchers | ABU Zaria Research Team | "
                            f"TETFund Grant | April 2026 | Model: claude-sonnet-4-6"),
                  align='C')

    # ── Layout helpers ─────────────────────────────────────────────────────────

    def cover(self):
        self.add_page()
        # Hero block
        self.set_fill_color(*DARK_NAVY)
        self.rect(0, 14, 210, 70, 'F')
        self.set_font("Helvetica", "B", 22)
        self.set_text_color(*WHITE)
        self.set_xy(12, 26)
        self.multi_cell(186, 10, sanitize("IMPLEMENTING THE SIMULATION TO RESEARCH FRAMEWORK (S2RF)"), align='C')
        self.set_font("Helvetica", "", 12)
        self.set_xy(12, 52)
        self.multi_cell(186, 7,
                        sanitize("A Claude AI Workflow Guide for iNHCES Researchers"),
                        align='C')
        self.set_font("Helvetica", "I", 9)
        self.set_xy(12, 62)
        self.multi_cell(186, 5,
                        sanitize("ABU Zaria Research Team  |  TETFund Grant  |  April 2026"),
                        align='C')
        self.set_font("Helvetica", "", 8.5)
        self.set_xy(12, 72)
        self.multi_cell(186, 5,
                        sanitize("Optimised for: VS Code + Claude Sonnet 4.6 (claude-sonnet-4-6)"),
                        align='C')

        self.set_text_color(*DARK_GREY)
        self.set_xy(12, 90)
        self.set_font("Helvetica", "", 9)
        self.set_fill_color(*LIGHT_BLUE)
        self.multi_cell(186, 6,
                        sanitize(
                            "VS Code + Claude Sonnet 4.6 Setup: Install the Claude Code extension "
                            "from the VS Code Marketplace. Configure your Anthropic API key "
                            "(claude-sonnet-4-6). Open your NHCES project folder. Use "
                            "Ctrl+Shift+P -> 'Claude: Open Chat' to start a session. Every prompt "
                            "in this guide can be typed directly into the Claude chat panel within "
                            "VS Code -- Claude sees your open files and folder structure "
                            "automatically."),
                        border=1, fill=True)

        # Stats row
        self.ln(5)
        stats = [("6", "Objectives"), ("30+", "Steps"),
                 ("80+", "Deliverables"), ("100+", "Example Prompts")]
        x0 = 12
        for val, lbl in stats:
            self.set_xy(x0, self.get_y())
            self.set_fill_color(*DARK_NAVY)
            self.set_font("Helvetica", "B", 18)
            self.set_text_color(*WHITE)
            self.cell(42, 14, val, border=0, align='C', fill=True)
            self.set_xy(x0, self.get_y() + 14)
            self.set_fill_color(*LIGHT_BLUE)
            self.set_font("Helvetica", "", 8)
            self.set_text_color(*DARK_GREY)
            self.cell(42, 7, lbl, border=0, align='C', fill=True)
            x0 += 45

        self.set_text_color(*DARK_GREY)
        self.ln(12)

        # TOC
        self.section_title("Contents at a Glance")
        toc = [
            ("O1", "Evaluate Cost Estimation Methodologies & Associated Parameters",
             "4 steps", "Very High"),
            ("O2", "Appraise Impact of Macroeconomic Variables on Housing Cost Estimates",
             "4 steps", "High"),
            ("O3", "Establish Requirement Models for the NHCES",
             "4 steps", "Very High"),
            ("O4", "Develop Conceptual Models for the Estimating System",
             "4 steps", "Very High"),
            ("O5", "Develop Appropriate Machine Learning Models for Housing Cost Estimation",
             "5 steps", "High"),
            ("O6", "Develop Prototype Web-based NHCES with Inbuilt ML Capabilities",
             "6 steps", "Very High"),
        ]
        for obj, desc, steps, impact in toc:
            self.set_font("Helvetica", "B", 9)
            self.set_text_color(*DARK_NAVY)
            self.cell(12, 6, sanitize(obj), ln=0)
            self.set_font("Helvetica", "", 9)
            self.set_text_color(*DARK_GREY)
            self.cell(130, 6, sanitize(desc), ln=0)
            self.set_font("Helvetica", "I", 8.5)
            self.set_text_color(*MID_GREY)
            self.cell(30, 6, sanitize(steps), ln=0)
            self.set_font("Helvetica", "B", 8.5)
            self.set_text_color(*GREEN_BORDER)
            self.cell(24, 6, sanitize(f"Impact: {impact}"), ln=1)

    def section_title(self, text):
        self.set_fill_color(*DARK_NAVY)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*WHITE)
        self.cell(0, 8, sanitize("  " + text), border=0, ln=1, fill=True)
        self.ln(2)
        self.set_text_color(*DARK_GREY)

    def obj_header(self, code, title, level):
        self.add_page()
        # Impact badge
        colour = DARK_NAVY if level == "Very High" else (60, 100, 60)
        self.set_fill_color(*colour)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*WHITE)
        self.cell(30, 8, sanitize(level), align='C', fill=True, ln=0)
        self.set_font("Helvetica", "B", 16)
        self.set_fill_color(*LIGHT_BLUE)
        self.set_text_color(*DARK_NAVY)
        self.cell(0, 8, sanitize(f"  {code}   {title}"), fill=True, ln=1)
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(*MID_GREY)
        self.cell(0, 5,
                  sanitize(f"Claude Contribution Level: {level}"), ln=1)
        self.ln(2)
        self.set_text_color(*DARK_GREY)

    def step_header(self, num, title):
        self.set_fill_color(*LABEL_BLUE)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*DARK_NAVY)
        self.cell(0, 7, sanitize(f"  Step {num} -- {title}"), fill=True, ln=1)
        self.ln(1)
        self.set_text_color(*DARK_GREY)

    def body(self, text):
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*DARK_GREY)
        self.multi_cell(0, 5, sanitize(text))
        self.ln(1)

    def bullet_list(self, items):
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*DARK_GREY)
        for item in items:
            self.set_x(self.l_margin + 4)
            self.multi_cell(0, 5, sanitize(f"* {item}"))

    def prompt_box(self, prompt_text):
        self.set_fill_color(*CODE_BG)
        self.set_draw_color(*MID_GREY)
        self.set_line_width(0.3)
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*DARK_NAVY)
        self.cell(0, 6, sanitize("  Example Prompt for Claude Sonnet 4.6:"), fill=True,
                  border='LTR', ln=1)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*DARK_GREY)
        self.set_x(self.l_margin)
        self.multi_cell(0, 4.5, sanitize(prompt_text), border='LBR', fill=True)
        self.ln(2)

    def outputs_line(self, files):
        self.set_font("Helvetica", "B", 8.5)
        self.set_text_color(*DARK_NAVY)
        self.cell(40, 5, "Outputs / Files Claude produces:", ln=0)
        self.set_font("Helvetica", "", 8.5)
        self.set_text_color(*MID_GREY)
        self.multi_cell(0, 5, sanitize(files))
        self.ln(1)

    def why_box(self, text):
        """Green 'Why This Step Is Required' rationale block."""
        self.set_fill_color(*GREEN_BG)
        self.set_draw_color(*GREEN_BORDER)
        self.set_line_width(0.5)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*GREEN_BORDER)
        self.cell(0, 7, sanitize("  WHY THIS STEP IS REQUIRED"), fill=True,
                  border='LTR', ln=1)
        self.set_font("Helvetica", "", 8.5)
        self.set_text_color(*DARK_GREY)
        self.set_x(self.l_margin)
        self.multi_cell(0, 5, sanitize(text), border='LBR', fill=True)
        self.ln(3)

    def method_box(self, method, rationale):
        """Steel-blue 'Research Method' block shown once per objective."""
        self.set_fill_color(210, 228, 252)
        self.set_draw_color(25, 75, 155)
        self.set_line_width(0.5)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(25, 75, 155)
        self.cell(0, 7, sanitize("  RESEARCH METHOD FOR THIS OBJECTIVE"),
                  fill=True, border='LTR', ln=1)
        self.set_font("Helvetica", "B", 8.5)
        self.set_text_color(*DARK_NAVY)
        self.set_x(self.l_margin)
        self.multi_cell(0, 5, sanitize(method), border='LR', fill=True)
        self.set_font("Helvetica", "", 8.5)
        self.set_text_color(*DARK_GREY)
        self.set_x(self.l_margin)
        self.multi_cell(0, 5, sanitize(rationale), border='LBR', fill=True)
        self.ln(3)

    def info_box(self, text):
        self.set_fill_color(*AMBER_BG)
        self.set_draw_color(*AMBER_BORDER)
        self.set_line_width(0.4)
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*AMBER_BORDER)
        self.cell(0, 6, sanitize("  NOTE"), fill=True, border='LTR', ln=1)
        self.set_font("Helvetica", "", 8.5)
        self.set_text_color(*DARK_GREY)
        self.multi_cell(0, 5, sanitize(text), border='LBR', fill=True)
        self.ln(3)

    def boundary_box(self, text):
        self.set_fill_color(*LIGHT_BLUE)
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*DARK_NAVY)
        self.multi_cell(0, 5,
                        sanitize(f"BOUNDARY: {text}"),
                        border=1, fill=True)
        self.ln(2)

    def tip_box(self, text):
        self.set_fill_color(*LIGHT_BLUE)
        self.set_font("Helvetica", "I", 8.5)
        self.set_text_color(*DARK_NAVY)
        self.multi_cell(0, 5, sanitize(f"VS Code Workflow Tip -- {text}"),
                        border=1, fill=True)
        self.ln(2)


# ═══════════════════════════════════════════════════════════════════════════════
# BUILD FUNCTION
# ═══════════════════════════════════════════════════════════════════════════════

def build_guide():
    pdf = GuidePDF("Implementing the S2RF: A Claude AI Workflow Guide for iNHCES Researchers")
    pdf.set_author("ABU Zaria Research Team")
    pdf.set_title("Implementing the Simulation to Research Framework (S2RF): A Claude AI Workflow Guide for iNHCES Researchers")

    # ─────────────────────────────────────────────────────────────────────────
    # COVER
    # ─────────────────────────────────────────────────────────────────────────
    pdf.cover()

    # =========================================================================
    # OVERARCHING RESEARCH METHODOLOGY
    # =========================================================================
    pdf.add_page()
    pdf.section_title("Overarching Research Methodology")

    pdf.body(
        "Before working through each objective, every member of the research team -- and "
        "Claude -- must understand the single methodological framework that governs the entire "
        "iNHCES study. All six objectives, all eight publications, and every deliverable in "
        "this guide sit inside this framework. It is not a label chosen for convenience; it "
        "is the architecture that determines what data is collected, in what order, using what "
        "methods, and for what purpose."
    )

    # ── Framework name ────────────────────────────────────────────────────────
    pdf.set_fill_color(*DARK_NAVY)
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(*WHITE)
    pdf.cell(0, 10,
             sanitize("  Sequential Explanatory Mixed Methods Design  (Creswell, 2014)"),
             fill=True, ln=1)
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(2)

    pdf.body(
        "Sequential Explanatory Mixed Methods (SEMM) is a two-phase research design in which "
        "quantitative evidence is collected and analysed FIRST, and its results are then used "
        "to design and interpret a second phase of primary data collection that EXPLAINS what "
        "the numbers mean. The arrow is one-directional and non-negotiable:\n\n"
        "   Phase 1: QUANTITATIVE  -->  Phase 2: QUALITATIVE / Mixed (to explain Phase 1)\n\n"
        "The defining rule is that Phase 2 is always shaped by Phase 1 findings. You do not "
        "design the survey instrument before the literature review is complete. You do not "
        "begin the Delphi before the SLR gap analysis is finished. The sequence is the method."
    )

    # ── Phase mapping table ───────────────────────────────────────────────────
    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 9.5)
    pdf.set_text_color(*DARK_NAVY)
    pdf.cell(0, 6, sanitize("How SEMM Maps Across the Six Objectives"), ln=1)
    pdf.ln(1)

    col_w = [38, 60, 88]
    headers = ["Phase", "Objectives", "What Happens"]
    pdf.set_fill_color(*DARK_NAVY)
    pdf.set_font("Helvetica", "B", 8.5)
    pdf.set_text_color(*WHITE)
    for h, w in zip(headers, col_w):
        pdf.cell(w, 7, sanitize("  " + h), fill=True, border=1)
    pdf.ln()

    rows = [
        ("QUAN Phase 1\n(Secondary evidence)",
         "O1 Steps 1-3\nO2 Steps 1-4",
         "PRISMA SLR of 87 global papers measures the research gaps "
         "quantitatively (4/87 Nigerian; 0/87 with macro features; 0/87 with "
         "SHAP explainability). Time-series econometrics quantifies the "
         "relationship between macroeconomic variables and Nigerian housing cost."),
        ("QUAL / Mixed Phase 2\n(Primary evidence\nexplains Phase 1)",
         "O1 Step 4\nO3 Steps 1-4",
         "Expert survey (Likert / RII) and 3-round Delphi answer why Nigerian "
         "practice diverges from the global literature, what parameters "
         "practitioners actually collect, and what they need from the system. "
         "These questions arise BECAUSE of Phase 1 -- they could not have been "
         "designed without knowing which gaps existed."),
        ("Artefact phase\n(Integrated response\nto both phases)",
         "O4, O5, O6",
         "System architecture, ML models, and the prototype web system are "
         "designed and evaluated using evidence from BOTH phases. The O3 SRS "
         "requirements feed O6 development; the O1 RII rankings are compared "
         "against O5 SHAP rankings -- a cross-phase validation unique to iNHCES."),
    ]

    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(*DARK_GREY)
    for i, (phase, objs, desc) in enumerate(rows):
        fill = (i % 2 == 0)
        pdf.set_fill_color(*(LIGHT_BLUE if fill else WHITE))
        # measure the tallest cell
        y_start = pdf.get_y()
        x_start = pdf.get_x()
        # col 1
        pdf.set_xy(x_start, y_start)
        pdf.set_font("Helvetica", "B", 8)
        pdf.multi_cell(col_w[0], 5, sanitize(phase), border=1, fill=fill)
        h1 = pdf.get_y() - y_start
        # col 2
        pdf.set_xy(x_start + col_w[0], y_start)
        pdf.set_font("Helvetica", "I", 8)
        pdf.multi_cell(col_w[1], 5, sanitize(objs), border=1, fill=fill)
        h2 = pdf.get_y() - y_start
        # col 3
        pdf.set_xy(x_start + col_w[0] + col_w[1], y_start)
        pdf.set_font("Helvetica", "", 8)
        pdf.multi_cell(col_w[2], 5, sanitize(desc), border=1, fill=fill)
        h3 = pdf.get_y() - y_start
        pdf.set_xy(x_start, y_start + max(h1, h2, h3))

    pdf.set_text_color(*DARK_GREY)
    pdf.ln(4)

    # ── Why SEMM was selected ─────────────────────────────────────────────────
    pdf.set_font("Helvetica", "B", 9.5)
    pdf.set_text_color(*DARK_NAVY)
    pdf.cell(0, 6, sanitize("Why SEMM Was Selected Over Alternative Designs"), ln=1)
    pdf.ln(1)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*DARK_GREY)

    reasons = [
        ("1. Pure quantitative design was insufficient",
         "The SLR and macro analysis produce statistical evidence, but they cannot answer "
         "context-specific questions about Nigerian professional practice. Only 4 of 87 PRISMA "
         "studies are Nigerian -- the global literature does not represent Nigerian cost "
         "parameters, data availability constraints, or practitioner willingness to adopt AI "
         "tools. SEMM fills this gap with a primary-data Phase 2."),
        ("2. Pure qualitative design was insufficient",
         "A purely Delphi-based study would produce practitioner opinions but no objective "
         "performance benchmark. The ML benchmarking in O5 (MAPE comparisons across 9 model "
         "families) and the econometric causality tests in O2 require quantitative methods that "
         "cannot be replaced by expert opinion alone."),
        ("3. Concurrent mixed methods was not viable",
         "A concurrent design (running the survey simultaneously with the SLR) would mean the "
         "survey instrument is designed without knowing what the SLR found -- i.e., without "
         "knowing the key gaps are G1 (no ML in Nigeria) and G2 (no macro features). The "
         "survey questions MUST be informed by SLR results to be meaningful. SEMM's sequential "
         "structure enforces this dependency."),
        ("4. It matches the research question structure",
         "O1-O2 answer: 'What does the global evidence show about construction cost estimation "
         "methods and macroeconomic drivers?' O3 answers: 'What do Nigerian practitioners need, "
         "and why does practice diverge from the literature?' The second question is the "
         "QUAL explanation of the first -- the definitional structure of SEMM."),
        ("5. It maximises the publication portfolio",
         "SEMM produces two separately publishable phases: P1 (PRISMA SLR -- quantitative "
         "Phase 1) and P2 (Delphi Requirements -- qualitative Phase 2). A mono-method design "
         "would collapse these into one paper, reducing the 8-paper portfolio to fewer outputs "
         "and weakening the TETFund deliverable case."),
    ]

    for title, body in reasons:
        pdf.set_font("Helvetica", "B", 8.5)
        pdf.set_text_color(*DARK_NAVY)
        pdf.cell(0, 5, sanitize(title), ln=1)
        pdf.set_font("Helvetica", "", 8.5)
        pdf.set_text_color(*DARK_GREY)
        pdf.set_x(pdf.l_margin + 4)
        pdf.multi_cell(0, 5, sanitize(body))
        pdf.ln(1)

    # ── The critical SEMM linkage ─────────────────────────────────────────────
    pdf.ln(2)
    pdf.set_fill_color(*GREEN_BG)
    pdf.set_draw_color(*GREEN_BORDER)
    pdf.set_line_width(0.5)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*GREEN_BORDER)
    pdf.cell(0, 7,
             sanitize("  THE CRITICAL SEMM LINKAGE -- RII vs. SHAP Cross-Phase Validation"),
             fill=True, border='LTR', ln=1)
    pdf.set_font("Helvetica", "", 8.5)
    pdf.set_text_color(*DARK_GREY)
    pdf.multi_cell(0, 5,
        sanitize(
            "The clearest evidence that iNHCES is a genuine SEMM study -- not two "
            "independent mono-method studies -- is the cross-phase validation loop:\n\n"
            "  Step 1: O1 Step 4 produces an RII ranking of cost parameters from Nigerian "
            "practitioners (QUAL Phase 2 primary data)\n\n"
            "  Step 2: O5 Step 3 produces a SHAP ranking of the same parameters from the "
            "ML model (quantitative re-analysis using the Phase 2-informed feature set)\n\n"
            "  Step 3: The comparison -- 'Did the ML model agree with expert practitioners "
            "about which parameters matter most?' -- is the novel cross-method validation "
            "contribution that no prior Nigerian construction cost study has produced.\n\n"
            "This comparison is only possible because SEMM ran Phase 1 (SLR to identify the "
            "parameter universe) before Phase 2 (survey to rank them by practitioner "
            "importance) before the ML modelling (SHAP to rank by predictive power). Changing "
            "the sequence destroys the contribution. This is published as part of P5 "
            "(Automation in Construction) and is the core novelty argument for Gap G3."
        ),
        border='LBR', fill=True)
    pdf.ln(3)

    # ── Claude's role within SEMM ─────────────────────────────────────────────
    pdf.set_fill_color(*LIGHT_BLUE)
    pdf.set_draw_color(*DARK_NAVY)
    pdf.set_line_width(0.3)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*DARK_NAVY)
    pdf.cell(0, 7,
             sanitize("  CLAUDE'S ROLE WITHIN THE SEMM FRAMEWORK"),
             fill=True, border='LTR', ln=1)
    pdf.set_font("Helvetica", "", 8.5)
    pdf.set_text_color(*DARK_GREY)
    pdf.multi_cell(0, 5,
        sanitize(
            "Claude operates inside the SEMM framework -- it does not change the design or "
            "violate its sequence. Claude's contributions by phase are:\n\n"
            "QUANTITATIVE PHASE 1 (O1 Steps 1-3, O2): Claude drafts PRISMA protocol and "
            "search strings; synthesises literature into taxonomy tables, gap analyses, and "
            "chapter drafts; writes Python scripts for all econometric analyses; interprets "
            "ADF, Granger, VAR/VECM results in academic language. You collect the papers and "
            "run the scripts on your Nigerian data.\n\n"
            "QUALITATIVE / MIXED PHASE 2 (O1 Step 4, O3): Claude designs Delphi instruments "
            "and survey questionnaires -- but ONLY AFTER the SLR gaps are established. Claude "
            "analyses the response data you paste back and writes RII tables, consensus "
            "findings, and the SRS. You administer the instruments to real practitioners.\n\n"
            "ARTEFACT PHASE (O4, O5, O6): Claude writes all system design documents, ML "
            "training and benchmarking scripts, SHAP analysis, Airflow DAGs, FastAPI backend, "
            "and frontend -- using both phases' evidence as the specification. You make "
            "infrastructure decisions, run experiments on your dataset, and conduct UAT."
        ),
        border='LBR', fill=True)
    pdf.ln(4)

    # =========================================================================
    # O1
    # =========================================================================
    pdf.obj_header("O1",
                   "Evaluate Cost Estimation Methodologies & Associated Parameters",
                   "Very High")
    pdf.body(
        "Claude acts as your primary research engine for Objective 1 -- generating, "
        "structuring, and synthesising literature at publication speed. Every deliverable "
        "from PRISMA protocol to taxonomy tables can be produced or substantially drafted "
        "in Claude, then refined by your team."
    )
    pdf.method_box(
        "Systematic Literature Review (PRISMA 2020)  +  Structured Expert Survey (Likert / RII)",
        "WHY PRISMA 2020: PRISMA (Preferred Reporting Items for Systematic Reviews and "
        "Meta-Analyses) is the internationally recognised standard for conducting and reporting "
        "systematic reviews in construction and engineering research. Its 27-item checklist "
        "and flow diagram ensure that paper selection is reproducible, transparent, and free "
        "from confirmation bias. Without PRISMA compliance, the literature review cannot be "
        "submitted to Construction Management and Economics or Automation in Construction -- "
        "both require PRISMA reporting as a condition of peer review.\n\n"
        "WHY EXPERT SURVEY (Steps 1.4): The global SLR reveals that only 4 of 87 included "
        "studies are Nigerian -- all using Multiple Linear Regression only. The SLR therefore "
        "cannot answer the objective's requirement to evaluate 'associated parameters' in the "
        "Nigerian context. A structured questionnaire administered to NIQS-registered quantity "
        "surveyors fills this gap: it produces a Relative Importance Index (RII) ranking of "
        "cost parameters from active Nigerian practitioners, provides TAM willingness-to-adopt "
        "scores before O6 development begins, and generates the primary empirical dataset "
        "required by the Sequential Explanatory Mixed Methods design (Creswell, 2014)."
    )

    # -- O1 Step 1 ------------------------------------------------------------
    pdf.step_header(1, "Set Up the PRISMA Systematic Literature Review Protocol")
    pdf.body("What Claude does: Claude drafts the full PRISMA-2020 protocol document including "
             "research questions, PICO framework, eligibility criteria, search string "
             "construction, and data extraction template.")
    pdf.body("How to work with Claude in VS Code:")
    pdf.bullet_list([
        "Open VS Code with the NHCES project folder",
        "Activate Claude Sonnet 4.6 via the Claude Code extension or Ctrl+Shift+P -> 'Claude: Start Chat'",
        "Paste your research title and objectives, then use the prompt below",
        "Claude returns a complete PRISMA protocol -- save as 01_PRISMA_Protocol.pdf",
    ])
    pdf.prompt_box(
        "Draft a full PRISMA 2020 systematic literature review protocol for this study: "
        "'Development of a Web-based AI National Housing Cost Estimating System (NHCES) for "
        "Nigeria'. Include: research questions, PICO framework, inclusion/exclusion criteria, "
        "search strings for Scopus/Web of Science/Google Scholar, data extraction table "
        "template, and quality appraisal checklist using the CASP tool. Format as a structured "
        "document."
    )
    pdf.outputs_line(
        "01_PRISMA_Protocol.pdf | 02_Search_Strings.pdf | 03_Data_Extraction_Template.pdf"
    )
    pdf.why_box(
        "Without a formal, pre-registered PRISMA protocol, the systematic literature review "
        "is not replicable and will be rejected by top-tier journals. PRISMA 2020 compliance "
        "is the minimum standard for any published systematic review. More fundamentally, the "
        "protocol defines your eligibility criteria upfront -- without it, paper selection "
        "becomes biased toward results that support a conclusion you have already reached "
        "(confirmation bias). The protocol also establishes the six research gaps (G1-G6) "
        "that justify the entire iNHCES study. Without documented gaps, the research has no "
        "academic novelty claim."
    )

    # -- O1 Step 2 ------------------------------------------------------------
    pdf.step_header(2, "Build the Methodology Taxonomy Table")
    pdf.body("What Claude does: Claude generates a comprehensive comparative taxonomy of all "
             "cost estimation methodologies -- traditional, statistical, and AI/ML -- with "
             "pros, cons, accuracy benchmarks, and key citations.")
    pdf.body("How to work with Claude in VS Code:")
    pdf.bullet_list([
        "Feed Claude any papers you have already collected (paste abstracts or upload PDFs)",
        "Request a structured taxonomy covering all three methodology generations",
        "Claude returns a structured table you can paste directly into your Chapter 2",
        "Iterate: ask Claude to add rows as you find more papers",
    ])
    pdf.prompt_box(
        "Create a comprehensive taxonomy table of construction cost estimation methodologies "
        "for a systematic literature review. Organise into three categories: (1) Traditional "
        "Methods -- parametric, analogous, elemental/bottom-up, expert judgement; "
        "(2) Statistical Methods -- MLR, Hedonic Pricing, ARIMA/ARIMAX, Box-Jenkins; "
        "(3) AI/ML Methods -- ANN, SVR, Random Forest, XGBoost, LightGBM, DNN, Stacking "
        "Ensemble. For each method: accuracy range (MAPE%), dataset size requirements, "
        "interpretability (High/Med/Low), computational cost, best application context, "
        "and 2 key citations. Format as a structured table."
    )
    pdf.outputs_line(
        "04_Methodology_Taxonomy_Table.pdf | 05_ML_Method_Comparison.pdf"
    )
    pdf.why_box(
        "The taxonomy is the evidence base for your model family selection in O5. Without it, "
        "choosing XGBoost over ANN in O5 is an arbitrary engineering decision -- not a "
        "research-justified choice. Any journal reviewer will ask: 'Why this model family?' "
        "The answer must reference the taxonomy. The taxonomy also directly populates Chapter "
        "2 of your research report, and demonstrates that you have surveyed Gen-1, Gen-2, and "
        "Gen-3 estimation methods -- a requirement of the objective 'evaluate VARIOUS "
        "methodologies'. Without this step, your evaluation is incomplete."
    )

    # -- O1 Step 3 ------------------------------------------------------------
    pdf.step_header(3, "Conduct Gap Analysis and Write the Literature Review Chapter")
    pdf.body("What Claude does: Claude identifies research gaps, articulates the novelty of "
             "NHCES, and writes full chapter sections to journal-submission standard.")
    pdf.body("How to work with Claude in VS Code:")
    pdf.bullet_list([
        "Provide Claude with your collected paper summaries (paste key findings)",
        "Ask Claude to identify gaps specifically for Nigeria and developing economies",
        "Request a structured Chapter 2 draft with all sub-sections",
        "Refine iteratively -- Claude can rewrite any paragraph to a specific tone or word count",
    ])
    pdf.prompt_box(
        "Based on the following summaries of papers I have reviewed [PASTE YOUR SUMMARIES "
        "HERE], identify: (1) research gaps in AI-based construction cost estimation for "
        "developing economies; (2) specific gaps for Nigeria (data scarcity, macroeconomic "
        "volatility, informal labour markets); (3) how the NHCES addresses each gap. Then "
        "draft a 1,500-word Literature Review section titled 'Gaps in Existing Research and "
        "the NHCES Contribution' suitable for submission to Automation in Construction journal."
    )
    pdf.outputs_line(
        "06_Literature_Review_Draft.pdf | 07_Gap_Analysis_Table.pdf | "
        "08_Included_Studies_Bibliography.pdf"
    )
    pdf.why_box(
        "The gap analysis is the core academic contribution of O1. It is the answer to the "
        "question every examiner and reviewer asks first: 'What is new about this study?' "
        "Without a formally documented gap analysis (G1: no AI/ML in Nigerian studies; "
        "G2: no macroeconomic features; G3: no SHAP explainability; G4: single-region; "
        "G5: no continuous retraining; G6: no web deployment), the research has no novelty "
        "claim and cannot be submitted for publication. Steps 1 and 2 provide the raw "
        "material; Step 3 is where that material is synthesised into an academic argument. "
        "The 08_Included_Studies_Bibliography.pdf additionally satisfies PRISMA 2020 "
        "transparency requirements -- all 87 included studies must be publicly documented."
    )

    # -- O1 Step 4 ------------------------------------------------------------
    pdf.step_header(4, "Design and Analyse Expert Survey Instruments")
    pdf.body("What Claude does: Claude designs the questionnaire instruments for expert "
             "validation studies (Delphi or structured survey) and later analyses returned data.")
    pdf.body("How to work with Claude in VS Code:")
    pdf.bullet_list([
        "Ask Claude to design a structured questionnaire for QS experts on cost estimation methods",
        "Export to Google Forms or use the NIQS membership contact list",
        "When data returns, paste frequency tables into Claude for statistical analysis",
        "Claude writes the findings narrative with Relative Importance Index (RII) calculations",
    ])
    pdf.prompt_box(
        "Design a structured questionnaire to survey Nigerian Quantity Surveyors (NIQS "
        "members) on current cost estimation practice. Include: Likert-scale questions (1-5) "
        "on frequency of use of each estimation method, satisfaction with current accuracy, "
        "willingness to use an AI-based system, and perceived barriers. Include 5 open-ended "
        "questions. Format for Google Forms export. Also provide the SPSS analysis plan "
        "including RII formula."
    )
    pdf.outputs_line(
        "09_QS_Survey_Instrument.pdf | 10_SPSS_Analysis_Plan.pdf"
    )
    pdf.why_box(
        "This is the most critical question to answer: why is Step 4 needed when Steps 1-3 "
        "have already covered the global literature?\n\n"
        "The core answer is that Steps 1-3 answer a LITERATURE question: 'What have "
        "researchers globally done?' Step 4 answers a PRACTICE question: 'What do Nigerian QS "
        "practitioners actually do -- and will they use what you build?'\n\n"
        "Four specific reasons make Step 4 non-optional:\n\n"
        "1. THE NIGERIA GAP IN THE LITERATURE. Of the 87 PRISMA-included studies, only 4 are "
        "Nigerian -- and all four use MLR only. The remaining 83 studies are from UK, China, "
        "Korea, Turkey: contexts with reliable data, formal markets, and computerised QS "
        "records. What the global literature says about 'associated parameters' (the objective "
        "wording) does not represent what Nigerian QS practitioners collect or trust at the "
        "pre-tender stage.\n\n"
        "2. PRIMARY DATA FOR PARAMETER RANKING. The objective requires evaluating 'associated "
        "PARAMETERS' -- not just methods. Step 4 produces an RII (Relative Importance Index) "
        "ranking of cost parameters from Nigerian practitioners. This ranking: (a) provides "
        "the a-priori feature importance baseline against which SHAP results in O5 are "
        "compared; (b) validates which parameters are feasible to collect at tender stage in "
        "Nigerian practice; (c) identifies parameters that exist in literature but are "
        "unavailable in Nigeria (e.g., BIM-derived quantities).\n\n"
        "3. SEQUENTIAL EXPLANATORY MIXED METHODS OBLIGATION. Your declared research design "
        "(Creswell, 2014) requires that documentary/quantitative evidence (Steps 1-3) is "
        "explained and validated by primary survey evidence (Step 4). Omitting Step 4 means O1 "
        "is only half a phase of your stated design -- an examinable methodological flaw.\n\n"
        "4. DOWNSTREAM DEPENDENCIES. Step 4 feeds: O3 (practitioner-validated system "
        "features); O5 (RII baseline vs SHAP comparison as a novel contribution); P1 "
        "publication (Nigerian empirical dimension without which CME reviewers would reject "
        "the paper); and user adoption evidence (TAM willingness scores establish viability "
        "before a line of code is written in O6)."
    )
    pdf.tip_box(
        "Create a folder /01_literature_review/ in your VS Code project. Store all Claude "
        "outputs as .pdf files generated by Python fpdf2 scripts. Use Claude to maintain a "
        "running 08_Included_Studies_Bibliography.pdf as you collect papers."
    )
    pdf.boundary_box(
        "Claude cannot access Scopus or Web of Science directly. You download the papers; "
        "Claude synthesises and writes. You administer the QS survey to real NIQS members; "
        "Claude designs the instrument and analyses data you paste back."
    )

    # =========================================================================
    # O2
    # =========================================================================
    pdf.obj_header("O2",
                   "Appraise Impact of Macroeconomic Variables on Housing Cost Estimates",
                   "High")
    pdf.body(
        "Claude handles the analytical framework, code for data collection, econometric "
        "guidance, and full results interpretation. You supply the Nigerian dataset; Claude "
        "does the heavy analytical lifting."
    )
    pdf.method_box(
        "Quantitative Secondary Data Analysis -- Time-Series Econometrics "
        "(VAR / VECM / ADF)  +  SHAP Feature Importance",
        "WHY TIME-SERIES ECONOMETRICS: The macroeconomic variables central to this objective "
        "(NGN/USD exchange rate, CPI, Brent crude oil price) are time-indexed and exhibit "
        "temporal dependence -- they are NOT cross-sectional observations. Standard OLS "
        "regression applied to non-stationary time series produces spurious correlations that "
        "appear statistically significant but have no causal meaning (Granger and Newbold, "
        "1974). The Augmented Dickey-Fuller (ADF) test first determines each variable's "
        "integration order. If variables are cointegrated (I(1) with a common long-run "
        "relationship), the Vector Error Correction Model (VECM) is used; otherwise a Vector "
        "Autoregression (VAR) in first differences is appropriate. This is the same "
        "methodological pathway used by Ashuri and Lu (2010) for US construction cost indices "
        "and is the academically accepted approach for multi-variable macroeconomic "
        "construction cost research.\n\n"
        "WHY SHAP (Step 2.4): Econometric methods (Granger causality) establish temporal "
        "precedence but not predictive importance within a non-linear ML model. SHAP "
        "(SHapley Additive exPlanations) quantifies each variable's marginal contribution to "
        "the ML prediction -- bridging the econometric and machine learning phases. Comparing "
        "Granger-causal rankings against SHAP importance rankings is a novel contribution of "
        "iNHCES that no prior Nigerian construction cost study has produced."
    )

    # -- O2 Step 1 ------------------------------------------------------------
    pdf.step_header(1, "Build the Variable Framework and Data Collection Scripts")
    pdf.body("What Claude does: Claude produces a justified list of all macroeconomic "
             "variables, maps each to its Nigerian data source, and writes Python scripts to "
             "pull data from CBN, World Bank API, and EIA.")
    pdf.body("How to work with Claude in VS Code:")
    pdf.bullet_list([
        "Open /02_macro_analysis/ folder in VS Code",
        "Ask Claude to write the data collection script for all Tier 1 API sources",
        "Run scripts to build your macroeconomic time-series dataset",
        "Claude validates the output and writes the variable justification for Chapter 3",
    ])
    pdf.prompt_box(
        "Write a Python script to collect macroeconomic data for Nigeria for use in a "
        "construction cost estimation study. Use these sources: (1) World Bank API via wbdata "
        "package -- indicators: FP.CPI.TOTL.ZG (inflation), NY.GDP.MKTP.KD.ZG (GDP growth), "
        "FR.INR.LEND (lending rate); (2) EIA API for Brent crude oil daily prices; (3) CBN "
        "exchange rates page scraper for NGN/USD daily rates. For each source: fetch data from "
        "2000 to present, handle missing values with forward-fill, save to a Pandas DataFrame, "
        "and export to CSV. Include error handling and logging. Target folder: "
        "/02_macro_analysis/data/raw/"
    )
    pdf.outputs_line(
        "fetch_worldbank.py | fetch_eia_oil.py | fetch_cbn_fx.py | macro_dataset.csv"
    )
    pdf.why_box(
        "Without this step, your ML models in O5 would have no macroeconomic features -- "
        "reducing them to project-parameter-only models. The global literature (Akintoye et "
        "al., 2003; Ma et al., 2020) shows that macro features reduce MAPE by 4-8 percentage "
        "points. Omitting them would leave iNHCES with MAPE above 20%, failing the target. "
        "This step also directly validates Research Gap G2 ('no study has used macroeconomic "
        "features in a Nigerian construction cost model') -- you cannot close a gap you have "
        "not formally operationalised. The automated data collection pipeline is additionally "
        "the operational foundation for the continuous retraining system in O5/O6."
    )

    # -- O2 Step 2 ------------------------------------------------------------
    pdf.step_header(2, "Conduct Correlation and Stationarity Analysis")
    pdf.body("What Claude does: Claude writes the full statistical analysis scripts "
             "(ADF tests, correlation matrix, VIF) and interprets results in academic language.")
    pdf.body("How to work with Claude in VS Code:")
    pdf.bullet_list([
        "Paste your macro_dataset.csv into the VS Code project",
        "Ask Claude to write the stationarity and correlation analysis script",
        "Run the script; paste the output tables back to Claude",
        "Claude writes the statistical findings section for your paper",
    ])
    pdf.prompt_box(
        "Write a Python script using statsmodels and pandas to perform: (1) Augmented "
        "Dickey-Fuller (ADF) unit root tests on each macroeconomic variable in "
        "macro_dataset.csv to check stationarity; (2) Pearson and Spearman correlation matrix "
        "between all variables and housing construction cost; (3) Variance Inflation Factor "
        "(VIF) analysis to detect multicollinearity; (4) Granger causality tests at 1, 3, and "
        "6 lags. Produce publication-quality charts using matplotlib/seaborn. Save all outputs "
        "to /02_macro_analysis/results/. Then provide interpretation text for each test result "
        "that I can include in my research paper."
    )
    pdf.outputs_line(
        "stationarity_analysis.py | correlation_matrix.py | vif_analysis.py | "
        "granger_tests.py"
    )
    pdf.why_box(
        "Macroeconomic variables (NGN/USD exchange rate, CPI, oil price) are almost always "
        "non-stationary -- they have a unit root (I(1) process). Running MLR or ML regression "
        "on non-stationary features without this check produces SPURIOUS REGRESSION: the model "
        "finds correlations that are artifacts of shared trends, not real causal relationships. "
        "This is not a technicality -- it invalidates the entire O2 analysis and would cause "
        "peer reviewers to reject the paper. The stationarity test determines whether you use "
        "levels, first differences, or a VECM model in Step 3. You cannot proceed to Step 3 "
        "without Step 2 results."
    )

    # -- O2 Step 3 ------------------------------------------------------------
    pdf.step_header(3, "Build and Interpret the Econometric Models")
    pdf.body("What Claude does: Claude implements VAR and VECM models and writes the full "
             "econometric results discussion section.")
    pdf.body("How to work with Claude in VS Code:")
    pdf.bullet_list([
        "Share your clean, stationary dataset with Claude",
        "Claude writes the VAR/VECM model scripts",
        "Run models; paste results back to Claude for interpretation",
        "Claude generates the discussion section and policy implications",
    ])
    pdf.prompt_box(
        "Using the macroeconomic dataset for Nigeria in "
        "/02_macro_analysis/data/processed/macro_stationary.csv, write Python code to: "
        "(1) estimate a Vector Autoregression (VAR) model with lag selection using AIC/BIC "
        "criteria; (2) test for cointegration using Johansen test; (3) if cointegrated, "
        "estimate a Vector Error Correction Model (VECM); (4) generate Impulse Response "
        "Functions (IRFs) for a 12-period horizon; (5) produce Forecast Error Variance "
        "Decomposition (FEVD). Export all charts and tables. Then write an academic discussion "
        "of the results (approximately 800 words) explaining the short-run and long-run "
        "relationships between macroeconomic variables and Nigerian housing construction costs."
    )
    pdf.outputs_line(
        "var_vecm_model.py | impulse_response.py | 02_Macro_Results_Discussion.pdf"
    )
    pdf.why_box(
        "Granger causality from the VAR/VECM model is what converts correlation (Step 2) into "
        "predictive justification. The global literature (Ashuri & Lu, 2010) documents that "
        "oil price Granger-causes construction cost indices. Step 3 tests whether this "
        "relationship holds specifically for Nigeria -- a non-trivial question given Nigeria's "
        "fuel subsidy history. The Impulse Response Functions and FEVD also quantify HOW MUCH "
        "of construction cost variance each macro variable explains, directly informing the "
        "O5 feature importance discussion. This analysis is required for Publication P3 "
        "(Journal of Construction Engineering and Management)."
    )

    # -- O2 Step 4 ------------------------------------------------------------
    pdf.step_header(4, "SHAP Feature Importance for Variable Selection")
    pdf.body("What Claude does: Claude writes SHAP analysis to identify which macroeconomic "
             "variables to include in the ML models, bridging Objectives 2 and 5.")
    pdf.body("How to work with Claude in VS Code:")
    pdf.bullet_list([
        "Use your initial dataset with a simple XGBoost model",
        "Claude writes SHAP analysis code",
        "Results directly inform which variables enter the final ML pipeline",
        "Claude writes the variable selection justification for your methodology chapter",
    ])
    pdf.prompt_box(
        "Write a Python script that trains an XGBoost model on the Nigerian housing cost "
        "dataset to predict construction cost per sqm, using macroeconomic variables as "
        "features. Then compute SHAP (SHapley Additive exPlanations) values to rank feature "
        "importance. Produce: (1) SHAP summary beeswarm plot; (2) SHAP bar chart of mean "
        "absolute values; (3) SHAP waterfall plot for the median prediction; (4) a ranked "
        "table of variables with their mean |SHAP| values. Save all outputs to "
        "/02_macro_analysis/shap_results/. Provide academic text explaining the SHAP results "
        "for inclusion in the variable selection section of a research paper."
    )
    pdf.outputs_line(
        "shap_variable_selection.py | shap_summary_plot.png | "
        "02_Variable_Selection_Justification.pdf"
    )
    pdf.why_box(
        "SHAP is the bridge between O2 (econometrics) and O5 (ML modelling). Steps 2 and 3 "
        "use econometric methods (ADF, Granger) to establish which variables are statistically "
        "significant. But statistical significance is not the same as predictive importance in "
        "a non-linear ML model. A variable can be Granger-causal yet contribute negligibly to "
        "ML prediction accuracy, or vice versa. SHAP variable selection ensures that ONLY "
        "variables with genuine predictive power enter the O5 feature matrix -- preventing "
        "overfitting from irrelevant macro features. Without Step 4, the O5 feature set is "
        "either arbitrary (chosen by intuition) or too large (all 12 macro variables included "
        "regardless of contribution). This step is also the source of the novel cross-method "
        "contribution in P3: comparing Granger causality rankings vs. SHAP importance rankings."
    )
    pdf.tip_box(
        "Create /02_macro_analysis/data/raw/, /processed/, /results/, and /shap_results/ "
        "subfolders. Claude maintains the analysis scripts; you manage the data files."
    )
    pdf.boundary_box(
        "You run the actual econometric models on your Nigerian dataset. Claude writes the "
        "code, interprets outputs you paste back, and drafts the findings text."
    )

    # =========================================================================
    # O3
    # =========================================================================
    pdf.obj_header("O3",
                   "Establish Requirement Models for the NHCES",
                   "Very High")
    pdf.body(
        "Requirements engineering is fundamentally a writing and structured thinking task -- "
        "exactly where Claude excels. Claude can produce every artefact: Delphi instruments, "
        "stakeholder matrices, SRS documents, use cases, and user stories."
    )
    pdf.method_box(
        "Delphi Technique (3-Round Expert Consensus Survey)  +  "
        "Requirements Engineering (IEEE 830 SRS)",
        "WHY DELPHI: The Delphi technique is the most rigorous method for eliciting structured "
        "expert consensus when objective data is unavailable and face-to-face group dynamics "
        "(such as dominance by senior members) would bias results. The three-round structure "
        "is not optional: Round 1 (open-ended) avoids researcher-imposed item lists and "
        "ensures the requirements emerge from practitioners, not from the research team's "
        "assumptions. Round 2 (Likert rating) quantifies importance on a 1-5 scale, enabling "
        "Relative Importance Index (RII) calculation. Round 3 (re-rating with group feedback) "
        "achieves measurable consensus, quantified by Kendall's Coefficient of Concordance "
        "(W). A Kendall's W >= 0.7 is the threshold accepted by Automation in Construction "
        "and ECAM for claiming expert consensus. Without three rounds, this threshold cannot "
        "be demonstrated.\n\n"
        "WHY IEEE 830 SRS: The IEEE 830 standard converts the Delphi consensus outputs into a "
        "formally structured requirements document with completeness, consistency, and "
        "verifiability guarantees. Each requirement in an IEEE 830 SRS is uniquely numbered "
        "and testable -- meaning every O6 development deliverable can be traced to a specific "
        "requirement. This traceability is required for TETFund milestone reporting and is "
        "the foundation for the User Acceptance Testing (UAT) protocol in O6."
    )

    # -- O3 Step 1 ------------------------------------------------------------
    pdf.step_header(1, "Stakeholder Analysis and Power/Interest Matrix")
    pdf.body("What Claude does: Claude produces a complete stakeholder register and "
             "power/interest matrix for NHCES -- identifying all parties, their interests, "
             "and engagement strategy.")
    pdf.body("How to work with Claude in VS Code:")
    pdf.bullet_list([
        "Provide Claude with the Nigerian housing sector context",
        "Claude generates the full stakeholder register with engagement strategies",
        "Use output to identify your Delphi survey panellist targets",
    ])
    pdf.prompt_box(
        "Produce a comprehensive stakeholder analysis for the National Housing Cost Estimating "
        "System (NHCES) in Nigeria. Identify all stakeholder groups: Federal Housing Authority "
        "(FHA), National Institute of Quantity Surveyors (NIQS), Real Estate Developers "
        "Association of Nigeria (REDAN), state housing corporations, Federal Mortgage Bank of "
        "Nigeria (FMBN), commercial banks, NBS, the research team at ABU Zaria, and end-users "
        "(builders, contractors). For each stakeholder: role in housing sector, interest in "
        "NHCES, influence level (High/Medium/Low), engagement strategy, and data they can "
        "provide. Present as a structured table and a 2x2 Power-Interest Matrix description. "
        "Also identify 20 ideal Delphi survey panellists by professional category."
    )
    pdf.outputs_line(
        "03_Stakeholder_Register.pdf | 03_Delphi_Panellist_Targets.pdf"
    )
    pdf.why_box(
        "Requirements without stakeholder analysis are speculative. The power/interest matrix "
        "identifies three critical things: (1) which stakeholders can BLOCK implementation "
        "(FHA, NIQS -- high power, must be managed); (2) which stakeholders can provide DATA "
        "(NBS, CBN, NIQS schedule of rates); (3) who the primary USERS are (practising QS "
        "professionals, not academics). Without this step, the Delphi panellist selection in "
        "Step 2 is undirected -- you may survey the wrong population. The stakeholder "
        "register also demonstrates research rigour to TETFund reviewers who expect "
        "institutional engagement evidence."
    )

    # -- O3 Step 2 ------------------------------------------------------------
    pdf.step_header(2, "Design All Three Delphi Survey Rounds")
    pdf.body("What Claude does: Claude designs the complete 3-round Delphi instrument -- "
             "open-ended elicitation (Round 1), rating scales (Round 2), and "
             "ranking/consensus (Round 3).")
    pdf.body("How to work with Claude in VS Code:")
    pdf.bullet_list([
        "Specify your panellist profile to Claude (senior QS, housing developers, academics)",
        "Claude generates all three rounds with instructions",
        "Format Round 1 for email/Google Forms; Rounds 2 and 3 as Excel feedback sheets",
        "After each round, paste responses into Claude for consensus analysis",
    ])
    pdf.prompt_box(
        "Design a 3-round Delphi survey instrument for the NHCES requirements study. Round 1 "
        "(open-ended): 10 open-ended questions to elicit system features, data requirements, "
        "user interface preferences, and concerns about AI-based estimation from expert "
        "quantity surveyors and housing developers. Round 2 (rating): Convert Round 1 "
        "responses into Likert-scale items (1 = Not important, 5 = Critically important) "
        "covering functional requirements, non-functional requirements, data inputs, and "
        "output formats. Include 30 items. Round 3 (ranking): Present top 20 requirements "
        "identified from Round 2 for final ranking and consensus scoring. Include Kendall's W "
        "formula for consensus measurement."
    )
    pdf.outputs_line(
        "03_Delphi_Round1.pdf | 03_Delphi_Round2.pdf | 03_Delphi_Round3.pdf"
    )
    pdf.why_box(
        "A single-round survey produces requirements that reflect what practitioners THINK they "
        "need before reflection. A 3-round Delphi is the gold standard for expert consensus in "
        "construction informatics because it allows panellists to revise their positions in "
        "light of the aggregated group view (anonymously, without social pressure). "
        "Specifically: Round 1 prevents the researcher from pre-loading the item list (avoiding "
        "researcher bias); Round 2 quantifies importance using validated Likert scaling; "
        "Round 3 achieves measurable consensus (Kendall's W >= 0.7 is the publication "
        "threshold). Without three rounds, the SRS in Step 4 is based on low-consensus "
        "opinions and cannot be validated as practitioner-endorsed requirements."
    )

    # -- O3 Step 3 ------------------------------------------------------------
    pdf.step_header(3, "Analyse Delphi Results and Compute Consensus")
    pdf.body("What Claude does: Claude calculates consensus indices and writes the "
             "requirements findings section when you paste your collected Delphi data.")
    pdf.body("How to work with Claude in VS Code:")
    pdf.bullet_list([
        "Collect panellist responses (Excel/Google Sheets)",
        "Paste the response matrix into Claude",
        "Claude computes means, standard deviations, Kendall's W, and RII",
        "Claude writes the requirements analysis chapter section",
    ])
    pdf.prompt_box(
        "Analyse the following Delphi survey Round 2 response matrix [PASTE YOUR DATA TABLE "
        "HERE]. For each item: compute mean score, standard deviation, coefficient of "
        "variation, and Relative Importance Index (RII = sum of scores / (5 x N)). Rank items "
        "by RII. Identify items with consensus (CV < 0.5 and mean >= 3.5). Then write an "
        "academic findings section (approximately 600 words) presenting the top 15 agreed "
        "requirements for the NHCES, suitable for a TETFund research report and journal "
        "publication."
    )
    pdf.outputs_line(
        "03_Delphi_Analysis.py | 03_Requirements_Findings.pdf | 03_Consensus_Table.pdf"
    )
    pdf.why_box(
        "Raw survey data is not publishable and not actionable. Step 3 transforms collected "
        "responses into RII-ranked, statistically validated requirements -- the format required "
        "by Automation in Construction and ECAM journals. The RII ranking also directly feeds "
        "O5: the top-ranked practitioner parameters (from O1 Step 4 and O3 Step 3) become the "
        "a-priori feature importance order against which SHAP values are compared. This "
        "comparison -- 'did the ML model agree with expert practitioners about which parameters "
        "matter most?' -- is a novel contribution unique to iNHCES. Without Step 3, this "
        "analysis cannot be done."
    )

    # -- O3 Step 4 ------------------------------------------------------------
    pdf.step_header(4, "Write the Full System Requirements Specification (SRS)")
    pdf.body("What Claude does: Claude writes the complete SRS document to IEEE 830 standard, "
             "covering all functional and non-functional requirements including the data "
             "pipeline admin requirements.")
    pdf.body("How to work with Claude in VS Code:")
    pdf.bullet_list([
        "Feed Claude the Delphi consensus results",
        "Claude generates the full SRS document",
        "Review and have your team validate",
        "SRS becomes the contract document between research and development phases",
    ])
    pdf.prompt_box(
        "Write a complete System Requirements Specification (SRS) for the National Housing "
        "Cost Estimating System (NHCES) following IEEE 830 standard. Include: (1) Introduction "
        "-- purpose, scope, definitions; (2) Overall Description -- product perspective, user "
        "classes (QS professional, housing developer, government planner, system "
        "administrator); (3) Functional Requirements -- project input module, macroeconomic "
        "context module, ML estimation engine, SHAP sensitivity analysis, PDF report "
        "generation, data pipeline dashboard, admin data feed; (4) Non-Functional Requirements "
        "-- performance (response < 3 seconds), availability (99.5% uptime), security (RLS), "
        "scalability (multi-state sub-models), maintainability (weekly auto-retrain); "
        "(5) External Interface Requirements -- CBN API, World Bank API, EIA API, Supabase, "
        "FastAPI. Format as a professional technical document."
    )
    pdf.outputs_line(
        "03_SRS_NHCES_IEEE830.pdf | 03_UML_Use_Cases.pdf | 03_User_Stories.pdf"
    )
    pdf.why_box(
        "The SRS is the contract document between research phases. Without it, O6 development "
        "has no formal requirements baseline -- any feature can be added or removed ad hoc, "
        "making post-development evaluation against stated objectives impossible. "
        "Specifically: (1) TETFund milestone reporting requires evidence that the system was "
        "built to a documented specification; (2) the MAPE <=15% and API response <3 seconds "
        "targets must be formally specified here before O5/O6 begin -- you cannot evaluate "
        "against a target not previously documented; (3) the IEEE 830 standard ensures the SRS "
        "is complete (all use cases covered), consistent (no contradictions), and verifiable "
        "(each requirement is testable in O6)."
    )
    pdf.tip_box(
        "Create /03_requirements/ with subfolders /delphi/, /srs/, /use_cases/. Claude "
        "generates all documents as PDFs via Python fpdf2 scripts for archive-quality "
        "deliverables."
    )
    pdf.boundary_box(
        "You administer the Delphi survey to real experts. Claude designs the instrument, "
        "analyses returned data, and writes findings -- but data collection is yours."
    )

    # =========================================================================
    # O4
    # =========================================================================
    pdf.obj_header("O4",
                   "Develop Conceptual Models for the Estimating System",
                   "Very High")
    pdf.body(
        "Claude designs the full NHCES architecture -- from database schema to system layer "
        "diagrams to data flow models -- before your team writes a single line of production "
        "code. This is the blueprint phase."
    )
    pdf.method_box(
        "Structured Systems Analysis and Design (SSAD)  +  "
        "Design Science Research (Hevner et al., 2004)",
        "WHY SSAD: Structured Systems Analysis and Design provides the standardised notation "
        "(Data Flow Diagrams, Entity-Relationship models, Architecture Layer Diagrams) that "
        "makes design decisions AUDITABLE and COMPLETE before implementation begins. In the "
        "Nigerian construction informatics context, where system development is often ad hoc, "
        "SSAD discipline ensures that: (a) all SRS functional requirements from O3 map to a "
        "specific system component; (b) the database schema is designed once, consistently, "
        "before any of the O5 feature engineering scripts or O6 API routers reference it; "
        "(c) Row Level Security policies are embedded in the schema design -- not retrofitted "
        "after deployment. The DFDs also provide the diagrams required for Chapter 4 of the "
        "research report and for the P4 publication (Scientific Data journal).\n\n"
        "WHY DESIGN SCIENCE RESEARCH (DSR): DSR (Hevner, March, Park and Ram, 2004) is the "
        "dominant epistemological framework for Information Systems research that produces an "
        "artefact as its primary contribution. DSR distinguishes iNHCES from a pure software "
        "engineering project: the NHCES system architecture, database schema, and ML pipeline "
        "design are themselves RESEARCH CONTRIBUTIONS that advance knowledge about how to "
        "build AI-based construction cost systems for developing-economy contexts -- not merely "
        "a tool built to serve a client. This framing is required for TETFund publication "
        "targets P4, P5, and P7."
    )

    # -- O4 Step 1 ------------------------------------------------------------
    pdf.step_header(1, "Design the Full System Architecture")
    pdf.body("What Claude does: Claude produces the complete 6-layer NHCES architecture "
             "document with technology choices justified and mapped to your existing "
             "SSAD infrastructure.")
    pdf.body("How to work with Claude in VS Code:")
    pdf.bullet_list([
        "Provide Claude with your existing stack (Vercel, Railway, Supabase, FastAPI)",
        "Claude produces the architecture document with layer descriptions",
        "Also generates a Mermaid.js diagram you can render in VS Code",
        "Architecture document becomes Chapter 4 of your research report",
    ])
    pdf.prompt_box(
        "Design the complete system architecture for the National Housing Cost Estimating "
        "System (NHCES). The system uses: Vercel (frontend), Railway (FastAPI backend + "
        "Airflow), Supabase PostgreSQL (database), MLflow (model registry), Cloudflare R2 "
        "(file storage). Define six architecture layers: (1) Data Acquisition Layer -- live "
        "APIs and scrapers; (2) Data Processing and Feature Engineering Layer -- ETL, "
        "validation; (3) ML Model Layer -- XGBoost ensemble + SHAP; (4) MLOps Layer -- "
        "Airflow DAGs, MLflow registry, drift detection; (5) API/Service Layer -- FastAPI "
        "endpoints; (6) Web Presentation Layer -- responsive HTML/JS frontend. For each "
        "layer: components, technologies, data flows, and justification. Also produce a "
        "Mermaid.js architecture diagram."
    )
    pdf.outputs_line(
        "04_System_Architecture.pdf | 04_Architecture_Diagram.mmd"
    )
    pdf.why_box(
        "A system built without an architecture document is not a research artefact -- it is "
        "ad hoc development with no documented design rationale. The architecture document "
        "serves three purposes: (1) it becomes Chapter 4 of your research report, satisfying "
        "the 'conceptual model' requirement of O4; (2) it makes technology choices "
        "academically defensible -- 'Why FastAPI?' must be answered in the architecture "
        "justification, not as a post-hoc explanation; (3) the 6-layer framework directly "
        "maps to AACE Parametric Estimation Theory and Adaptive Learning Theory, providing "
        "the theoretical grounding required for TETFund publication."
    )

    # -- O4 Step 2 ------------------------------------------------------------
    pdf.step_header(2, "Design the PostgreSQL Database Schema")
    pdf.body("What Claude does: Claude designs the complete Supabase PostgreSQL schema -- "
             "all tables, columns, data types, relationships, indexes, and Row Level "
             "Security policies.")
    pdf.body("How to work with Claude in VS Code:")
    pdf.bullet_list([
        "Tell Claude your data requirements from the Delphi SRS",
        "Claude generates full SQL DDL statements",
        "Copy SQL directly into Supabase SQL editor to create schema",
        "Claude also writes the migration scripts for future schema updates",
    ])
    pdf.prompt_box(
        "Design the complete PostgreSQL database schema for the NHCES Supabase instance. "
        "Create SQL DDL statements for these tables: (1) projects -- housing project records; "
        "(2) macro_fx -- daily exchange rates; (3) macro_cpi -- monthly CPI and inflation; "
        "(4) macro_interest -- monthly interest and MPR rates; (5) macro_oil -- daily Brent "
        "crude prices; (6) macro_gdp -- quarterly GDP data; (7) material_cement -- weekly "
        "cement prices; (8) material_steel -- weekly iron rod prices; (9) material_pms -- "
        "monthly petrol prices by state; (10) unit_rates -- NIQS quarterly schedule of rates; "
        "(11) market_prices -- weekly property listing prices; (12) model_versions -- MLflow "
        "model registry mirror; (13) pipeline_runs -- Airflow DAG run logs. Include Supabase "
        "Row Level Security (RLS) policies for each table."
    )
    pdf.outputs_line(
        "04_schema.sql | 04_rls_policies.sql | 04_seed_data.sql"
    )
    pdf.why_box(
        "The database schema is the data contract for the entire system. Without it: the O2 "
        "data collection scripts have no target tables to write to; the O5 feature engineering "
        "pipeline has no consistent source schema; and the O6 FastAPI backend has no data "
        "model. Designing the schema at O4 (before coding begins) ensures all three phases "
        "are consistent. The RLS (Row Level Security) policies are not optional -- they are "
        "the primary OWASP A01 (Broken Access Control) defence and are required for any "
        "system handling institutional housing cost data. Leaving RLS to O6 is a security "
        "architecture mistake that is difficult to retrofit."
    )

    # -- O4 Step 3 ------------------------------------------------------------
    pdf.step_header(3, "Create Data Flow Diagrams and Process Models")
    pdf.body("What Claude does: Claude produces Level 0 and Level 1 DFDs and BPMN process "
             "models for every system workflow.")
    pdf.body("How to work with Claude in VS Code:")
    pdf.bullet_list([
        "Describe each system workflow to Claude",
        "Claude returns Mermaid.js flowchart syntax (renders in VS Code with Mermaid plugin)",
        "Export as PNG for inclusion in research report figures",
    ])
    pdf.prompt_box(
        "Create Mermaid.js flowchart diagrams for these NHCES processes: (1) Level 0 Context "
        "DFD -- showing NHCES as a single process with all external entities and data flows; "
        "(2) Level 1 DFD -- exploding NHCES into its six main processes with internal data "
        "stores; (3) User journey flowchart -- from project parameter input to PDF cost "
        "estimate report; (4) Data pipeline flowchart -- from API fetch through validation, "
        "transformation, feature store storage, and ML retraining; (5) ML inference flowchart "
        "-- from feature extraction through model ensemble to SHAP explanation and confidence "
        "interval output."
    )
    pdf.outputs_line(
        "04_DFD_Level0.mmd | 04_DFD_Level1.mmd | 04_User_Journey.mmd | "
        "04_Pipeline_Flow.mmd"
    )
    pdf.why_box(
        "DFDs are required for Systems Analysis and Design (SAD) methodology -- a core "
        "component of O4 'Develop Conceptual Models'. They make the system's data flows "
        "AUDITABLE: an examiner can trace exactly what data enters from CBN, how it is "
        "transformed in the feature engineering layer, and what outputs the API produces. "
        "Without DFDs, your conceptual model is purely textual and cannot be evaluated for "
        "completeness. The user journey diagram is also essential for the UAT (User Acceptance "
        "Testing) protocol in O6 -- testers follow the journey diagram to verify each step "
        "works as specified."
    )

    # -- O4 Step 4 ------------------------------------------------------------
    pdf.step_header(4, "Write Chapter 4 -- Conceptual Models")
    pdf.body("What Claude does: Claude writes the complete Chapter 4 of your research report, "
             "incorporating all architecture decisions and models.")
    pdf.body("How to work with Claude in VS Code:")
    pdf.bullet_list([
        "Feed Claude the architecture document, schema, and DFDs",
        "Claude drafts the full chapter with narrative justification",
        "Chapter is ready for supervisor review with all figures referenced",
    ])
    pdf.prompt_box(
        "Write Chapter 4 'Conceptual Models for the National Housing Cost Estimating System' "
        "for a TETFund research report. The chapter should be approximately 3,000 words and "
        "cover: (1) Theoretical foundation -- AACE Parametric Estimation Theory (Class 1-5 "
        "framework) and Adaptive Learning Theory; (2) System conceptual model -- the 6-layer "
        "architecture with justification of each technology choice; (3) Database conceptual "
        "model -- ER diagram description and schema design rationale; (4) Data flow models -- "
        "Level 0 and Level 1 DFD explanations; (5) MLOps conceptual model -- the "
        "champion-challenger retraining loop and drift detection framework; (6) Summary. "
        "Write to the standard of Automation in Construction journal."
    )
    pdf.outputs_line(
        "04_Chapter4_Conceptual_Models.pdf"
    )
    pdf.why_box(
        "Architecture decisions and diagrams are not valuable unless documented with "
        "academic justification. Chapter 4 converts the technical design artefacts from Steps "
        "1-3 into publishable academic prose -- the format required for P4 (Engineering, "
        "Construction and Architectural Management journal). Without this step, O4 produces "
        "technical files (SQL, Mermaid diagrams) but no research output. The chapter "
        "also links the conceptual models explicitly to the theoretical foundations (AACE, "
        "Adaptive Learning Theory) -- connecting practice to theory as required by all "
        "TETFund deliverables."
    )
    pdf.tip_box(
        "Install the 'Mermaid Preview' VS Code extension to render all .mmd files inline. "
        "Claude's architecture diagrams become live interactive documents in your editor."
    )
    pdf.boundary_box(
        "Architecture decisions should be validated by your team against actual Nigerian "
        "infrastructure constraints before implementation begins."
    )

    # =========================================================================
    # O5
    # =========================================================================
    pdf.obj_header("O5",
                   "Develop Appropriate Machine Learning Models for Housing Cost Estimation",
                   "High")
    pdf.body(
        "Claude writes the complete ML pipeline -- from data preparation scripts to model "
        "training, SHAP explainability, benchmarking framework, and automated retraining DAGs. "
        "You run the code on your Nigerian dataset and paste results back for interpretation "
        "and academic write-up."
    )
    pdf.method_box(
        "Computational Experimental Research -- ML Model Benchmarking  +  "
        "SHAP Explainability Analysis  +  MLOps (Champion-Challenger Retraining)",
        "WHY COMPUTATIONAL EXPERIMENTATION: Computational experiments treat each ML model "
        "configuration as an experimental condition, with the Nigerian project dataset as the "
        "controlled experimental environment. 10-fold stratified cross-validation provides "
        "unbiased performance estimates by ensuring every record serves as both training and "
        "test data. Optuna Bayesian hyperparameter optimisation (50 trials per model) ensures "
        "each model family is evaluated at or near its optimal configuration -- preventing the "
        "common methodological flaw of comparing a tuned XGBoost against a default Random "
        "Forest. The comparison table produced in Step 2 is the core evidence for the research "
        "claim that the stacking ensemble achieves superior accuracy -- without it, model "
        "selection is an arbitrary engineering decision, not a research finding.\n\n"
        "WHY SHAP (Step 3): Post-hoc explainability is a METHODOLOGICAL REQUIREMENT for "
        "applied ML research published after 2020. Journals such as Automation in Construction "
        "now require evidence that results are interpretable, not merely accurate. SHAP "
        "satisfies both the academic requirement (Ribeiro et al., 2016; Lundberg and Lee, "
        "2017) and the professional practice requirement: QS practitioners need to understand "
        "WHICH cost drivers are pushing an estimate up or down before they will trust it.\n\n"
        "WHY MLOPS CHAMPION-CHALLENGER (Step 4): A static model is not an intelligent system. "
        "The champion-challenger retraining loop ensures iNHCES adapts as Nigerian macro "
        "conditions change -- an essential property given Nigeria's history of abrupt exchange "
        "rate devaluations (2015, 2020, 2023) that would render a fixed-weight model obsolete "
        "within months. The automated safety gate (challenger must beat champion by more than "
        "1pp MAPE to be promoted) protects practitioners from model degradation."
    )

    # -- O5 Step 1 ------------------------------------------------------------
    pdf.step_header(1, "Build the Data Preparation and Feature Engineering Pipeline")
    pdf.body("What Claude does: Claude writes the ETL scripts that merge historical project "
             "data with macroeconomic features, handle missing values, and engineer all "
             "derived features.")
    pdf.body("How to work with Claude in VS Code:")
    pdf.bullet_list([
        "Provide Claude with your raw project dataset schema and macro_dataset.csv",
        "Claude writes the full feature engineering pipeline",
        "Run to produce the clean ML-ready feature matrix",
    ])
    pdf.prompt_box(
        "Write a Python feature engineering pipeline for the NHCES ML models. Input: "
        "(1) projects.csv -- historical Nigerian housing project records; "
        "(2) macro_dataset.csv -- monthly macroeconomic indicators. Tasks: (1) Merge projects "
        "with macroeconomic snapshot at project completion date; (2) Engineer features: "
        "cost_per_sqm (target variable), location_cost_index, material_cost_index_at_tender, "
        "exchange_rate_at_tender, inflation_at_tender, oil_price_at_tender, 3-month and "
        "6-month lagged values of all macro variables; (3) One-hot encode categorical "
        "variables; (4) Apply MinMaxScaler to continuous features; (5) Split into 80/10/10 "
        "train/val/test stratified by geopolitical_zone and year. Save feature_matrix.csv "
        "and scaler.pkl."
    )
    pdf.outputs_line(
        "05_feature_engineering.py | feature_matrix.csv | scaler.pkl | feature_names.json"
    )
    pdf.why_box(
        "Feature engineering is where domain knowledge is encoded into the model. Raw project "
        "data (floor area, location, structural type) without macro feature engineering "
        "produces models with MAPE 25-35% -- well above the 15% target. The lagged macro "
        "variables (3-month, 6-month lags) are particularly important: cement and steel prices "
        "are purchased 2-4 months before construction -- the lag captures the actual price the "
        "contractor paid, not the current market price. Without proper lag engineering, the "
        "model uses the wrong temporal feature value. This step is the difference between "
        "research-grade and production-grade ML for construction cost."
    )

    # -- O5 Step 2 ------------------------------------------------------------
    pdf.step_header(2, "Train and Benchmark the Full Model Family")
    pdf.body("What Claude does: Claude writes the complete benchmarking script that trains "
             "all model families, tunes hyperparameters with Optuna, and produces a "
             "publication-quality comparison table.")
    pdf.body("How to work with Claude in VS Code:")
    pdf.bullet_list([
        "Claude writes the benchmarking script against feature_matrix.csv",
        "Run overnight -- models train sequentially with cross-validation",
        "Paste the results table back to Claude for interpretation",
        "Claude selects the champion model and justifies the choice",
    ])
    pdf.prompt_box(
        "Write a comprehensive ML model benchmarking script for NHCES housing cost estimation "
        "using feature_matrix.csv. Train these model families: (1) Baseline -- Ridge "
        "Regression, Lasso, ElasticNet; (2) Tree-based -- Random Forest, Gradient Boosting, "
        "XGBoost, LightGBM; (3) Neural -- MLP (3 layers: 256, 128, 64 neurons); (4) SVR; "
        "(5) Stacking Ensemble -- XGBoost + LightGBM + RF as base learners, Ridge as "
        "meta-learner. For each model: 10-fold cross-validation, Optuna hyperparameter tuning "
        "(50 trials), evaluation reporting MAE, RMSE, MAPE, and R2. Produce comparison table "
        "and charts. Save best model as best_model.pkl."
    )
    pdf.outputs_line(
        "05_model_benchmarking.py | results_comparison_table.csv | best_model.pkl | "
        "05_Model_Selection_Report.pdf"
    )
    pdf.why_box(
        "You cannot claim XGBoost is the best model for iNHCES without benchmarking all "
        "credible alternatives. The benchmark table is the CORE CONTRIBUTION of P5 (Automation "
        "in Construction). A reviewer at that journal will not accept 'we used XGBoost because "
        "it is popular' -- they require a full comparison table showing that XGBoost/stacking "
        "outperforms Ridge, RF, SVR, and DNN on your specific Nigerian dataset. The champion "
        "model identity may surprise you: on small datasets (n < 200), SVR or RF sometimes "
        "outperform XGBoost. You must benchmark to find out. The stacking ensemble, which "
        "consistently achieves the lowest MAPE in the literature (Gao et al., 2021: 4.9%), "
        "can only be justified through this head-to-head comparison."
    )

    # -- O5 Step 3 ------------------------------------------------------------
    pdf.step_header(3, "Implement SHAP Explainability Analysis")
    pdf.body("What Claude does: Claude writes the full SHAP analysis suite -- summary plots, "
             "waterfall charts, dependence plots -- and the explainability narrative for "
             "the paper.")
    pdf.body("How to work with Claude in VS Code:")
    pdf.bullet_list([
        "Claude writes SHAP scripts using best_model.pkl",
        "Run scripts to produce all SHAP visualisations",
        "Paste SHAP value tables into Claude for narrative interpretation",
        "SHAP plots become key figures in your journal paper",
    ])
    pdf.prompt_box(
        "Write a SHAP analysis script for the NHCES best model (best_model.pkl). Produce: "
        "(1) SHAP TreeExplainer for the XGBoost/LightGBM champion model; "
        "(2) Summary beeswarm plot -- all features, all test samples; "
        "(3) Bar chart of mean |SHAP| values ranked -- top 20 features; "
        "(4) SHAP waterfall plot for the median-cost prediction; "
        "(5) SHAP dependence plot for the top 5 most important features; "
        "(6) SHAP interaction plot for exchange_rate vs cement_price; "
        "(7) Force plot for 3 case study predictions (low/medium/high cost). "
        "Save all plots as PNG at 300dpi. Also write 600 words of academic interpretation."
    )
    pdf.outputs_line(
        "05_shap_analysis.py | shap_summary.png | shap_waterfall.png | "
        "05_SHAP_Interpretation.pdf"
    )
    pdf.why_box(
        "SHAP is not optional for an ML paper published after 2020. Automation in Construction, "
        "ECAM, and JCEM reviewers now require explainability analysis as a condition of "
        "acceptance -- a black-box model that achieves good MAPE but cannot explain its "
        "predictions will be rejected as 'not suitable for professional practice'. "
        "For iNHCES specifically, SHAP serves a second purpose: it provides the USER-FACING "
        "cost driver explanation in the web interface. A QS professional presenting an "
        "estimate to a client cannot simply say 'the AI says NGN 85,000/sqm' -- they need "
        "to explain that exchange rate volatility accounts for 23% of the estimate. SHAP "
        "makes this possible. This dual role (academic + practical) addresses Gap G3."
    )

    # -- O5 Step 4 ------------------------------------------------------------
    pdf.step_header(4, "Build the Automated MLflow Retraining Pipeline")
    pdf.body("What Claude does: Claude writes the complete Airflow DAG for weekly automated "
             "retraining with MLflow experiment tracking, champion-challenger comparison, "
             "and automatic model promotion.")
    pdf.body("How to work with Claude in VS Code:")
    pdf.bullet_list([
        "Claude writes the Airflow DAG file for the retraining pipeline",
        "Deploy to your Railway Airflow instance",
        "DAG runs every Sunday -- retrains, evaluates, promotes if improved",
        "MLflow UI tracks all experiments at mlflow.yourdomain.com",
    ])
    pdf.prompt_box(
        "Write a complete Apache Airflow DAG (using TaskFlow API, Python 3.10+) for automated "
        "weekly NHCES model retraining with MLflow integration. The DAG nhces_retrain_weekly "
        "should: (1) Pull latest feature snapshot from Supabase; (2) Retrain XGBoost, "
        "LightGBM, and Stacking Ensemble with Optuna tuning (30 trials each); "
        "(3) Log all runs to MLflow: hyperparameters, MAE, RMSE, MAPE, R2; "
        "(4) Compare best challenger MAPE against current Production model; "
        "(5) If challenger MAPE <= production MAPE + 1.0pp: promote to Production; "
        "(6) Send email summary report; (7) Handle exceptions with retry logic. "
        "Schedule: Sundays at 02:00 WAT."
    )
    pdf.outputs_line(
        "05_dags/nhces_retrain_weekly.py | 05_mlflow_config.py | 05_model_promotion.py"
    )
    pdf.why_box(
        "A model that cannot retrain is not an INTELLIGENT system -- it is a static lookup "
        "table. This is what the 'i' in iNHCES stands for. Without automated retraining: "
        "(1) the model becomes stale as Nigerian inflation, FX rates, and material prices "
        "change -- a model trained in 2025 will have unacceptable MAPE by 2027 without "
        "retraining; (2) the research cannot claim 'continuous learning' as a contribution; "
        "(3) the TETFund deliverable 'operational web system' requires ongoing model "
        "maintenance, which is only feasible if automated. The champion-challenger framework "
        "also provides SAFETY: the current production model is only replaced if the new model "
        "is demonstrably better -- protecting practitioner users from model degradation."
    )

    # -- O5 Step 5 ------------------------------------------------------------
    pdf.step_header(5, "Write the ML Chapter and Results Section")
    pdf.body("What Claude does: Claude writes Chapter 5 (ML methodology) and the Results "
             "section using your actual model outputs, SHAP charts, and benchmarking tables.")
    pdf.body("How to work with Claude in VS Code:")
    pdf.bullet_list([
        "Paste your results_comparison_table.csv into Claude",
        "Paste SHAP mean |SHAP| value table",
        "Claude writes the full results chapter with all figures referenced",
        "Output is journal-ready text for Automation in Construction",
    ])
    pdf.prompt_box(
        "Write Chapter 5 'Machine Learning Model Development and Results' for the NHCES "
        "TETFund research report. Use the following actual results [PASTE YOUR "
        "results_comparison_table.csv HERE]. The chapter should cover: (1) Data preparation "
        "and feature engineering methodology; (2) Model selection rationale; (3) Training "
        "procedure -- cross-validation, Optuna tuning, champion-challenger framework; "
        "(4) Results -- model comparison table, champion model identification with "
        "justification; (5) Explainability analysis -- SHAP feature importance interpretation "
        "for Nigerian housing context; (6) Limitations. Target: 3,500 words, Automation in "
        "Construction style."
    )
    pdf.outputs_line(
        "05_Chapter5_ML_Models_Results.pdf"
    )
    pdf.why_box(
        "Steps 1-4 of O5 produce code and data files -- not a research output. Step 5 is "
        "where the technical results become academic knowledge. Without this step, O5 has no "
        "publishable artefact and cannot contribute to P5 (Automation in Construction). The "
        "write-up also requires explicit interpretation of results in the Nigerian context: "
        "explaining WHY exchange rate is the top SHAP feature for a Nigerian audience requires "
        "domain knowledge that connects the ML result to NGN/USD devaluation history. This "
        "contextualisation is the value that transforms a generic ML result into a "
        "Nigeria-specific research contribution."
    )
    pdf.tip_box(
        "Install the Python and Jupyter extensions in VS Code. Run Claude's scripts in "
        "Jupyter notebooks first for interactive debugging, then convert to .py files for "
        "production."
    )
    pdf.boundary_box(
        "You run the code on your actual Nigerian project dataset. Claude cannot access raw "
        "data directly -- but will debug every error you encounter when you paste it."
    )

    # =========================================================================
    # O6
    # =========================================================================
    pdf.obj_header("O6",
                   "Develop Prototype Web-based NHCES with Inbuilt ML Capabilities",
                   "Very High")
    pdf.body(
        "This is where Claude contributes most directly -- writing production-quality "
        "full-stack code for the entire NHCES system. Building on your proven SSAD "
        "architecture (Vercel + Railway + Supabase), Claude can produce every component "
        "of the system from FastAPI endpoints to the frontend UI to the pipeline dashboard."
    )
    pdf.method_box(
        "Software Prototyping (Iterative / Agile Development)  +  "
        "User Acceptance Testing (UAT)  +  Technology Acceptance Model (TAM)",
        "WHY PROTOTYPING: A working prototype is the research artefact of O6 -- it is the "
        "evidence that the conceptual models from O4 and the ML models from O5 can be "
        "integrated into a functional system. Iterative prototyping (build -> test -> refine) "
        "is preferred over a waterfall approach because NHCES is a first-of-kind system: "
        "requirements that were not fully anticipated in O3 will emerge during O6 development. "
        "TETFund expects a DEMONSTRABLE PROTOTYPE as a project deliverable -- a document "
        "describing a system is not sufficient. Prototyping produces this deliverable "
        "incrementally, with each sprint validated against the O3 SRS requirements.\n\n"
        "WHY UAT WITH NIQS PRACTITIONERS: User Acceptance Testing is the bridge between "
        "technical correctness (the system works as coded) and professional fitness for "
        "purpose (QS practitioners can use it for real work). UAT with real NIQS quantity "
        "surveyors produces the usability evidence required for P7 (Journal of Information "
        "Technology in Construction). Without UAT, the research cannot claim practical "
        "contribution -- only technical contribution.\n\n"
        "WHY TAM (Technology Acceptance Model): TAM (Davis, 1989) measures Perceived "
        "Usefulness and Perceived Ease of Use -- the two constructs that predict whether "
        "practitioners will actually adopt the system. The TAM willingness-to-adopt scores "
        "established in O1 Step 4 become the pre-development baseline; post-UAT TAM scores "
        "in O6 measure adoption intent change after hands-on exposure. This before/after "
        "comparison is the adoption evidence required for P7 and for TETFund's "
        "socioeconomic impact reporting."
    )

    # -- O6 Step 1 ------------------------------------------------------------
    pdf.step_header(1, "Set Up the Project Structure and FastAPI Backend Skeleton")
    pdf.body("What Claude does: Claude creates the complete project folder structure and "
             "FastAPI application skeleton with all route definitions, dependency injection, "
             "and database connection.")
    pdf.body("How to work with Claude in VS Code:")
    pdf.bullet_list([
        "Create a new /nhces-backend/ folder in VS Code",
        "Ask Claude to generate the complete project structure",
        "Claude produces all boilerplate files ready to fill in",
        "Run locally with uvicorn -- the API skeleton is immediately testable",
    ])
    pdf.prompt_box(
        "Create a complete FastAPI project structure for the NHCES backend. Generate: "
        "(1) Full folder structure with /app/routers/, /app/models/, /app/schemas/, "
        "/app/services/, /app/ml/, /app/pipeline/; (2) main.py with CORS, lifespan events "
        "(load ML model on startup), Swagger docs config; (3) database.py -- Supabase "
        "SQLAlchemy async connection with connection pooling; (4) All router files with "
        "endpoint stubs; (5) Pydantic schemas for all request and response models; "
        "(6) requirements.txt with all dependencies; (7) .env.example file; "
        "(8) Dockerfile for Railway deployment. Add type hints and docstrings."
    )
    pdf.outputs_line(
        "main.py | database.py | requirements.txt | Dockerfile | routers/estimate.py | "
        "routers/reports.py | routers/pipeline.py"
    )
    pdf.why_box(
        "Structure before code is a software engineering principle that is especially "
        "critical for a research system that must be reproducible by other researchers. "
        "A skeleton defines all API endpoints before any business logic is written, "
        "ensuring: (1) all SRS functional requirements have a corresponding endpoint; "
        "(2) the ML inference engine (Step 2) and report generator (Step 4) have a defined "
        "integration point from day one; (3) the Dockerfile ensures deployment is "
        "reproducible on Railway without manual configuration. Starting with Step 2 without "
        "a skeleton would produce a monolithic script that cannot be extended to production."
    )

    # -- O6 Step 2 ------------------------------------------------------------
    pdf.step_header(2, "Build the ML Inference Engine")
    pdf.body("What Claude does: Claude writes the ML serving layer -- model loading from "
             "MLflow, feature preparation, ensemble inference, SHAP explanation, and "
             "confidence interval calculation.")
    pdf.body("How to work with Claude in VS Code:")
    pdf.bullet_list([
        "Claude writes app/ml/inference.py and app/ml/explainer.py",
        "Integrate with the /api/estimate endpoint",
        "Test with a sample project input -- Claude helps debug any issues",
        "The inference engine is the technical heart of the system",
    ])
    pdf.prompt_box(
        "Write the ML inference engine for the NHCES FastAPI backend. Create "
        "app/ml/inference.py with: (1) ModelManager class -- loads champion model from MLflow "
        "registry on startup, caches in memory, reloads automatically when a new Production "
        "model is registered; (2) FeaturePreparator class -- takes ProjectInput Pydantic "
        "schema, fetches latest macroeconomic snapshot from Supabase, engineers all derived "
        "features, applies saved scaler.pkl, returns feature vector; (3) predict() function "
        "-- runs ensemble inference, returns point estimate and 90% confidence interval using "
        "bootstrap method (200 iterations); (4) explain() function -- runs SHAP TreeExplainer, "
        "returns top 10 feature contributions. Include async/await patterns throughout."
    )
    pdf.outputs_line(
        "app/ml/inference.py | app/ml/explainer.py | app/ml/feature_prep.py"
    )
    pdf.why_box(
        "The inference engine is the technical deliverable that makes iNHCES an INTELLIGENT "
        "system rather than a form with a database lookup. Without it, the web interface "
        "(Step 3) cannot serve ML predictions -- the entire O6 objective collapses. The "
        "confidence interval (90% bootstrap CI) specifically addresses practitioner trust: "
        "a QS professional will not use a point estimate alone -- they need to know the "
        "uncertainty range to set contingency. The ModelManager auto-reload mechanism "
        "is also critical: it ensures that when O5's nhces_retrain_weekly DAG promotes a "
        "new champion model, the live API immediately serves the new model without downtime."
    )

    # -- O6 Step 3 ------------------------------------------------------------
    pdf.step_header(3, "Build the Frontend -- Project Input and Results UI")
    pdf.body("What Claude does: Claude writes the complete responsive frontend -- the project "
             "input form, macroeconomic context display, cost estimate results panel, and "
             "SHAP sensitivity visualisation.")
    pdf.body("How to work with Claude in VS Code:")
    pdf.bullet_list([
        "Create /nhces-frontend/ in VS Code (or use your existing HTML/JS SSAD structure)",
        "Claude writes index.html, styles.css, and app.js",
        "Deploy to Vercel -- Claude writes the vercel.json config",
        "Claude iterates on UI based on your feedback",
    ])
    pdf.prompt_box(
        "Build a complete mobile-first responsive web frontend for NHCES in vanilla HTML, "
        "CSS, and JavaScript (no framework). Create: (1) index.html -- multi-step form: "
        "Project Location (state + LGA dropdown, geopolitical zone auto-fill), Building "
        "Details (type, storeys, floor area, structural system, procurement method), Economic "
        "Context (live auto-fetched macro snapshot with last-updated timestamp), Estimate "
        "Results (cost estimate + CI displayed as a gauge chart + number cards), SHAP "
        "Explanation (horizontal bar chart of top 10 cost drivers); (2) styles.css -- "
        "professional Nigerian government-appropriate colour scheme, fully responsive, "
        "dark mode support; (3) app.js -- fetch() calls to FastAPI, form validation, "
        "Chart.js for gauge and SHAP bar charts, PDF download trigger."
    )
    pdf.outputs_line(
        "index.html | styles.css | app.js | vercel.json"
    )
    pdf.why_box(
        "iNHCES is defined as a WEB-BASED system in its title -- a backend with no frontend "
        "does not satisfy the O6 objective. The frontend is what QS practitioners interact "
        "with; all the ML sophistication in O5 is worthless if it is not accessible through "
        "a usable interface. Three design choices are specifically required: (1) the SHAP "
        "bar chart in the results panel directly satisfies Gap G3 (explainability for "
        "practitioners); (2) the live macro context display shows practitioners the economic "
        "conditions embedded in their estimate -- building trust through transparency; "
        "(3) mobile-first design is essential because Nigerian site-based QS professionals "
        "predominantly access web systems via mobile devices."
    )

    # -- O6 Step 4 ------------------------------------------------------------
    pdf.step_header(4, "Build the PDF Report Generator")
    pdf.body("What Claude does: Claude writes the WeasyPrint/ReportLab PDF generation module "
             "that produces professional QS-formatted cost estimate reports.")
    pdf.body("How to work with Claude in VS Code:")
    pdf.bullet_list([
        "Claude writes app/services/report_generator.py",
        "Test with a sample estimate -- Claude refines the layout",
        "Reports include: project details, macro snapshot, estimate + CI, SHAP chart, model version",
    ])
    pdf.prompt_box(
        "Write a PDF report generator for NHCES using ReportLab. Create "
        "app/services/report_generator.py with a generate_estimate_report() function that "
        "produces a professional cost estimate PDF including: (1) Header -- NHCES logo, "
        "report title, report ID, date, model version; (2) Project Details table; "
        "(3) Macroeconomic Context table -- exchange rate, inflation, oil price, cement "
        "price at time of estimate; (4) Cost Estimate section -- point estimate with "
        "confidence interval, cost per sqm, comparison to NIQS benchmark rate for that zone; "
        "(5) Top Cost Drivers -- SHAP bar chart; (6) Disclaimer section; "
        "(7) Footer -- ABU Zaria / TETFund attribution. Save to Cloudflare R2 and return "
        "signed URL."
    )
    pdf.outputs_line(
        "app/services/report_generator.py | app/services/r2_storage.py"
    )
    pdf.why_box(
        "A web page result is not an acceptable deliverable for QS professional practice -- "
        "the Nigerian construction industry operates on formal document trails. A QS "
        "professional presenting a preliminary estimate to a developer, bank, or government "
        "agency requires a signed, dated PDF document with a unique report ID. This is the "
        "professional output format. The comparison to the NIQS benchmark rate for that "
        "geopolitical zone is particularly important: it contextualises the AI estimate "
        "within the practitioner's existing reference frame, building trust and enabling "
        "professional endorsement. Without this step, the system produces numbers but not "
        "professional documents -- it cannot be adopted in practice."
    )

    # -- O6 Step 5 ------------------------------------------------------------
    pdf.step_header(5, "Build the Data Pipeline Dashboard")
    pdf.body("What Claude does: Claude writes the admin-facing pipeline health dashboard "
             "showing DAG status, model version, MAPE trend, and manual retrain trigger.")
    pdf.body("How to work with Claude in VS Code:")
    pdf.bullet_list([
        "Claude writes the dashboard HTML page and /api/pipeline/status endpoint",
        "Protected by Supabase auth -- only admin users can access",
        "Real-time polling updates DAG status every 60 seconds",
    ])
    pdf.prompt_box(
        "Build the NHCES data pipeline admin dashboard. Create: (1) FastAPI endpoint GET "
        "/api/pipeline/status -- queries Supabase pipeline_runs table and MLflow API to "
        "return: last run time and status for each of 9 DAGs, current production model "
        "version, current MAPE on holdout set, training data size, data freshness per source; "
        "(2) dashboard.html -- a single-page admin dashboard showing: 9 DAG status cards "
        "(green/amber/red by last run status), current model metrics panel, MAPE trend line "
        "chart (last 12 weeks), data source freshness table, manual retrain trigger button. "
        "Protected by Supabase auth token check. Auto-refreshes every 60 seconds."
    )
    pdf.outputs_line(
        "dashboard.html | routers/pipeline.py (complete) | "
        "app/services/pipeline_monitor.py"
    )
    pdf.why_box(
        "Without the pipeline dashboard, the system's 'intelligent' retraining capability "
        "is invisible and unmanageable. An administrator has no way to know whether the "
        "CBN FX data pipeline failed last Tuesday, whether the model retrained successfully "
        "last Sunday, or whether the current MAPE has drifted above 15%. The dashboard "
        "makes these operational facts visible and actionable. It is also a RESEARCH "
        "CONTRIBUTION: it demonstrates that the system is not merely a static ML model but "
        "a monitored, maintained, continuously learning system -- the full MLOps cycle. "
        "This is the technical evidence for the 'intelligent' and 'national' claims in the "
        "system name."
    )

    # -- O6 Step 6 ------------------------------------------------------------
    pdf.step_header(6, "Write Tests and Deploy")
    pdf.body("What Claude does: Claude writes the complete test suite (unit + integration) "
             "and GitHub Actions CI/CD pipeline for automated deployment to Vercel and Railway.")
    pdf.body("How to work with Claude in VS Code:")
    pdf.bullet_list([
        "Claude writes pytest test files for every endpoint and service",
        "Claude writes .github/workflows/deploy.yml",
        "Push to GitHub -- CI runs tests, then deploys on success",
        "Claude writes the deployment documentation",
    ])
    pdf.prompt_box(
        "Write the complete test suite and CI/CD pipeline for NHCES. Create: "
        "(1) tests/test_estimate.py -- pytest unit tests for the ML inference engine: "
        "test prediction within reasonable range, test SHAP values sum to prediction, "
        "test feature preparation with missing macro data, test confidence interval width; "
        "(2) tests/test_api.py -- FastAPI TestClient integration tests for all endpoints; "
        "(3) tests/test_pipeline.py -- unit tests for each Airflow DAG task function; "
        "(4) .github/workflows/deploy.yml -- GitHub Actions workflow: on push to main, "
        "run pytest, if tests pass deploy backend to Railway, deploy frontend to Vercel; "
        "(5) README.md -- complete deployment guide. Use pytest fixtures and mock "
        "Supabase/MLflow calls appropriately."
    )
    pdf.outputs_line(
        "tests/test_estimate.py | tests/test_api.py | .github/workflows/deploy.yml | "
        "README.md"
    )
    pdf.why_box(
        "Untested code is not a research artefact -- it is an untested prototype. TETFund "
        "deliverable validation requires that the system works as specified. The test suite "
        "provides formal evidence of correctness: that SHAP values sum to the prediction "
        "(a mathematical property that must hold), that the API response is within the "
        "<3 second SRS requirement, and that pipeline tasks execute without error. CI/CD "
        "ensures the deployed system remains in a validated state as the code evolves -- "
        "preventing the common research project failure where a 'working' system breaks "
        "after a dependency update and the researcher cannot identify when or why."
    )
    pdf.tip_box(
        "Install the REST Client VS Code extension. Claude generates .http files for every "
        "API endpoint -- test directly in VS Code without leaving the editor."
    )
    pdf.boundary_box(
        "You handle deployment credentials, domain configuration, and Nigerian-context "
        "User Acceptance Testing (UAT) with real NIQS quantity surveyors. Claude debugs "
        "any errors you encounter."
    )

    # =========================================================================
    # FOLDER STRUCTURE
    # =========================================================================
    pdf.add_page()
    pdf.section_title("NHCES Master Project Folder Structure in VS Code")
    pdf.body(
        "Below is the complete VS Code project structure that emerges from Claude's outputs "
        "across all six objectives. Create this structure at the start of your project and "
        "use it as the single source of truth for all research artefacts."
    )
    structure = [
        "NHCES/",
        "  01_literature_review/",
        "      01_PRISMA_Protocol.pdf",
        "      02_Search_Strings.pdf",
        "      03_Data_Extraction_Template.pdf",
        "      04_Methodology_Taxonomy_Table.pdf",
        "      05_ML_Method_Comparison.pdf",
        "      06_Literature_Review_Draft.pdf",
        "      07_Gap_Analysis_Table.pdf",
        "      08_Included_Studies_Bibliography.pdf",
        "      09_QS_Survey_Instrument.pdf",
        "      10_SPSS_Analysis_Plan.pdf",
        "  02_macro_analysis/",
        "      data/raw/   <- CBN, WB, EIA CSVs",
        "      data/processed/   <- clean datasets",
        "      fetch_worldbank.py",
        "      fetch_eia_oil.py",
        "      fetch_cbn_fx.py",
        "      stationarity_analysis.py",
        "      var_vecm_model.py",
        "      shap_variable_selection.py",
        "  03_requirements/",
        "      delphi/   <- Round 1, 2, 3 instruments",
        "      03_SRS_NHCES_IEEE830.pdf",
        "      03_UML_Use_Cases.pdf",
        "      03_User_Stories.pdf",
        "  04_conceptual_models/",
        "      04_System_Architecture.pdf",
        "      04_Architecture_Diagram.mmd",
        "      04_schema.sql",
        "      04_rls_policies.sql",
        "      04_DFD_Level0.mmd",
        "      04_Chapter4_Conceptual_Models.pdf",
        "  05_ml_models/",
        "      05_feature_engineering.py",
        "      05_model_benchmarking.py",
        "      05_shap_analysis.py",
        "      05_dags/nhces_retrain_weekly.py",
        "      best_model.pkl",
        "      05_Chapter5_ML_Models_Results.pdf",
        "  nhces-backend/   <- FastAPI application",
        "      app/routers/",
        "      app/ml/inference.py",
        "      app/ml/explainer.py",
        "      app/services/report_generator.py",
        "      tests/",
        "      Dockerfile",
        "      requirements.txt",
        "  nhces-frontend/   <- Vercel web app",
        "      index.html",
        "      dashboard.html",
        "      styles.css",
        "      app.js",
        "      vercel.json",
        "  .github/workflows/deploy.yml",
        "  README.md",
    ]
    pdf.set_fill_color(*CODE_BG)
    pdf.set_draw_color(*MID_GREY)
    pdf.set_line_width(0.3)
    pdf.set_font("Courier", "", 7.5)
    pdf.set_text_color(*DARK_GREY)
    start_y = pdf.get_y()
    for line in structure:
        pdf.set_x(pdf.l_margin)
        pdf.cell(0, 4.5, sanitize(line), ln=1, fill=True)
    pdf.set_text_color(*DARK_GREY)
    pdf.set_font("Helvetica", "", 9)

    # =========================================================================
    # MODEL REFERENCE
    # =========================================================================
    pdf.add_page()
    pdf.section_title("Claude Sonnet 4.6 -- Model Reference for VS Code")
    rows = [
        ("Model ID",            "claude-sonnet-4-6",
         "Use this exact string in API calls and extension config"),
        ("Interface",           "Claude Code CLI + VS Code Extension",
         "Install: code --install-extension anthropic.claude-code"),
        ("Context window",      "200,000 tokens",
         "Can process entire codebases and long research documents"),
        ("Best for",            "Code generation, academic writing, data analysis, system design",
         "All NHCES objectives well within capability"),
        ("Prompt style",        "Be specific and detailed",
         "Include file paths, column names, output format, word count"),
        ("Iterative workflow",  "Paste -> Review -> Refine",
         "Claude improves on explicit feedback -- never accept first draft as final"),
        ("File access",         "Claude sees open VS Code files",
         "Share context by keeping relevant files open in editor tabs"),
        ("Cost management",     "Use Claude.ai Pro or API",
         "API: pay-per-token; Pro: unlimited for interactive research sessions"),
    ]
    heads = ["Parameter", "Value", "Notes"]
    widths = [38, 58, 90]
    pdf.set_fill_color(*DARK_NAVY)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*WHITE)
    for h, w in zip(heads, widths):
        pdf.cell(w, 7, sanitize("  " + h), fill=True, border=1)
    pdf.ln()
    pdf.set_font("Helvetica", "", 8.5)
    pdf.set_text_color(*DARK_GREY)
    for i, (p, v, n) in enumerate(rows):
        fill = (i % 2 == 0)
        pdf.set_fill_color(*(LIGHT_BLUE if fill else WHITE))
        pdf.cell(widths[0], 6, sanitize("  " + p), fill=fill, border=1)
        pdf.cell(widths[1], 6, sanitize(v), fill=fill, border=1)
        pdf.cell(widths[2], 6, sanitize(n), fill=fill, border=1, ln=1)

    pdf.output(OUTPUT_PATH)
    print(f"  [OK] {OUTPUT_PATH}")


if __name__ == "__main__":
    print("Generating NHCES_Claude_Assistance_Guide.pdf ...")
    build_guide()
    print("Done.")
