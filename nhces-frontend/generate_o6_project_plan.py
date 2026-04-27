"""
iNHCES O6 -- Agent 01 Project Plan PDF Generator
Produces: O6_00_Agent01_Project_Plan.pdf
This document governs ALL O6 agents (03-10).
No agent may write a single line of code before this plan is reviewed.

DATA SOURCE: AMBER
TETFund NRF 2025 | Department of Quantity Surveying, ABU Zaria
"""

import sys, os
from datetime import date

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, os.path.join(_ROOT, '01_literature_review'))

from generate_o1_pdfs import (
    DocPDF, sanitize, _ds_page,
    DARK_NAVY, GOLD, LIGHT_BLUE, WHITE, DARK_GREY, MID_GREY,
    PAGE_W, LEFT, LINE_H,
)

OUT = os.path.join(_HERE, 'O6_00_Agent01_Project_Plan.pdf')

# ── iNHCES Warm Ivory accent colours ──────────────────────────────────────────
ACCENT   = (139, 100, 0)    # #8b6400
GREEN_C  = (0, 122, 94)     # #007a5e
AMBER_C  = (184, 98, 10)    # #b8620a
RED_C    = (192, 57, 43)    # #c0392b
IVORY    = (245, 241, 235)  # #f5f1eb


class PlanPDF(DocPDF):
    def __init__(self):
        super().__init__("O6 Agent 01 Project Plan", "O6-00")

    def header(self):
        self.set_fill_color(*DARK_NAVY)
        self.rect(0, 0, 210, 14, 'F')
        self.set_font("Helvetica", "B", 7)
        self.set_text_color(*WHITE)
        self.set_xy(5, 4)
        self.cell(PAGE_W, 6, sanitize(
            "iNHCES  |  TETFund NRF 2025  |  ABU Zaria  |  O6 Agent 01 -- Master Project Plan"
        ))
        self.set_text_color(*DARK_GREY)
        self.ln(16)

    def footer(self):
        self.set_y(-13)
        self.set_draw_color(*GOLD)
        self.set_line_width(0.4)
        self.line(LEFT, self.get_y(), 198, self.get_y())
        self.set_font("Helvetica", "I", 7.5)
        self.set_text_color(*MID_GREY)
        self.cell(0, 8, sanitize(
            f"O6 Agent 01 Project Plan  |  ABU Zaria / TETFund NRF 2025  |  Page {self.page_no()}"
        ), align="C")

    def h1(self, text):
        self.ln(3)
        self.set_fill_color(*DARK_NAVY)
        self.set_text_color(*WHITE)
        self.set_font("Helvetica", "B", 10)
        self.set_x(LEFT)
        self.cell(PAGE_W, 8, sanitize(f"  {text}"), fill=True, ln=True)
        self.set_text_color(*DARK_GREY)
        self.ln(2)

    def h2(self, text):
        self.ln(2)
        self.set_font("Helvetica", "B", 9.5)
        self.set_text_color(*DARK_NAVY)
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

    def bullet(self, items, indent=4):
        self.set_font("Helvetica", "", 9.5)
        self.set_text_color(*DARK_GREY)
        for item in items:
            self.set_x(LEFT + indent)
            self.cell(4, 5.2, "-")
            self.set_x(LEFT + indent + 4)
            self.multi_cell(PAGE_W - indent - 4, 5.2, sanitize(item))
        self.ln(1)

    def agent_box(self, number, role, phase, colour, items):
        self.ln(2)
        self.set_fill_color(*colour)
        self.set_draw_color(*GOLD)
        self.set_line_width(0.5)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*WHITE)
        self.set_x(LEFT)
        self.cell(PAGE_W, 7,
                  sanitize(f"  Agent {number:02d} -- {role}   |   Phase: {phase}"),
                  border=1, fill=True, ln=True)
        self.set_fill_color(248, 248, 252)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*DARK_GREY)
        for item in items:
            self.set_x(LEFT + 4)
            self.cell(4, 5.0, "-")
            self.set_x(LEFT + 8)
            self.multi_cell(PAGE_W - 8, 5.0, sanitize(item), border="LR", fill=True)
        self.set_x(LEFT)
        self.cell(PAGE_W, 0, "", border="B")
        self.ln(2)

    def colour_row(self, label, hex_val, role, wcag=''):
        self.set_fill_color(*IVORY)
        self.set_draw_color(*MID_GREY)
        cw = [12, 30, 50, PAGE_W - 92]
        # Colour swatch
        r = int(hex_val[1:3], 16)
        g = int(hex_val[3:5], 16)
        b = int(hex_val[5:7], 16)
        self.set_fill_color(r, g, b)
        self.set_x(LEFT)
        self.cell(cw[0], LINE_H, "", border=1, fill=True)
        self.set_fill_color(*IVORY)
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*DARK_GREY)
        self.cell(cw[1], LINE_H, sanitize(f" {hex_val}"), border=1, fill=True)
        self.set_font("Helvetica", "", 8)
        self.cell(cw[2], LINE_H, sanitize(f" {label}"), border=1, fill=True)
        self.cell(cw[3], LINE_H, sanitize(f" {role}  {wcag}"), border=1, fill=True)
        self.ln()

    def api_block(self, method, path, purpose, req_ex='', resp_ex=''):
        self.ln(2)
        # Method badge
        m_col = {'POST': (0,100,50), 'GET': (0,80,140), 'PUT': (140,80,0), 'DELETE': (160,40,40)}
        col = m_col.get(method, DARK_NAVY)
        self.set_fill_color(*col)
        self.set_font("Helvetica", "B", 8.5)
        self.set_text_color(*WHITE)
        self.set_x(LEFT)
        self.cell(16, 6, sanitize(f" {method}"), fill=True)
        self.set_fill_color(235, 240, 255)
        self.set_text_color(*DARK_NAVY)
        self.set_font("Courier", "B", 9)
        self.cell(PAGE_W - 16, 6, sanitize(f"  {path}"), fill=True, ln=True)
        self.set_font("Helvetica", "I", 8.5)
        self.set_text_color(*DARK_GREY)
        self.set_x(LEFT)
        self.multi_cell(PAGE_W, 5, sanitize(f"  {purpose}"))
        if req_ex:
            self.set_font("Courier", "", 7.5)
            self.set_fill_color(245, 245, 250)
            self.set_x(LEFT)
            self.multi_cell(PAGE_W, 4.5, sanitize(req_ex), border=1, fill=True)
        if resp_ex:
            self.set_fill_color(240, 248, 240)
            self.set_x(LEFT)
            self.multi_cell(PAGE_W, 4.5, sanitize(resp_ex), border=1, fill=True)
        self.ln(1)

    def check_row(self, text, agent):
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*DARK_GREY)
        self.set_x(LEFT + 2)
        self.cell(6, 5.2, "[ ]")
        self.set_x(LEFT + 8)
        aw = 30
        self.multi_cell(PAGE_W - aw - 8, 5.2, sanitize(text), border=0)
        # agent label -- print on same line if possible (approximate)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*MID_GREY)
        self.ln(0.5)


# ── Cover ──────────────────────────────────────────────────────────────────────
def make_cover(pdf):
    pdf.add_page()
    # Amber top strip
    pdf.set_fill_color(*ACCENT)
    pdf.rect(0, 0, 210, 8, 'F')
    pdf.set_font("Helvetica", "B", 7.5)
    pdf.set_text_color(*WHITE)
    pdf.set_xy(0, 1.5)
    pdf.cell(210, 5, sanitize("AGENT 01 OUTPUT -- GOVERNS ALL O6 AGENTS -- READ BEFORE CODING"), align="C")
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(18)

    # Navy hero block
    pdf.set_fill_color(*DARK_NAVY)
    pdf.rect(0, 20, 210, 60, 'F')
    pdf.set_xy(0, 28)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(200, 210, 235)
    pdf.cell(210, 7, "Intelligent National Housing Cost Estimating System (iNHCES)", align="C", ln=True)
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(*WHITE)
    pdf.cell(210, 11, "O6 MASTER PROJECT PLAN", align="C", ln=True)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(200, 210, 235)
    pdf.cell(210, 7, "Agent 01 -- Project Leader Output", align="C", ln=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*LIGHT_BLUE)
    pdf.cell(210, 6, "Next.js 14  |  FastAPI  |  Supabase  |  Railway  |  Vercel  |  Warm Ivory Design System", align="C", ln=True)
    pdf.set_draw_color(*GOLD)
    pdf.set_line_width(0.8)
    pdf.line(30, 82, 180, 82)
    pdf.set_xy(LEFT, 90)

    meta = [
        ("Document:",     "O6_00_Agent01_Project_Plan.pdf"),
        ("Date:",         date.today().strftime("%d %B %Y")),
        ("Objective:",    "O6 -- Build and Deploy the Full iNHCES Web System"),
        ("Agents:",       "01 (Plan) + 02 (ML-done) + 03/04/05 + 06/07/08 + 09/10"),
        ("Frontend:",     "Next.js 14 (App Router)  →  Vercel"),
        ("Backend:",      "FastAPI (Python 3.10+)  →  Railway"),
        ("Database:",     "Supabase PostgreSQL  (schema: 04_schema.sql)"),
        ("ML Champion:",  "LightGBM  LOO-CV MAPE 13.66%  (05_ml_models/models/champion_model.pkl)"),
        ("Design:",       "Warm Ivory Palette -- Playfair Display + Lora + DM Sans"),
        ("Grant:",        "TETFund National Research Fund (NRF) 2025"),
        ("RULE:",         "No agent writes code until this plan is signed off by the research team."),
    ]
    for label, val in meta:
        pdf.set_x(LEFT)
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*DARK_NAVY)
        pdf.cell(42, 6.2, sanitize(label))
        pdf.set_font("Helvetica", "" if "RULE" not in label else "B", 9)
        pdf.set_text_color(*DARK_GREY if "RULE" not in label else (192,57,43))
        pdf.cell(PAGE_W - 42, 6.2, sanitize(val), ln=True)


# ── Section 1: Stack and Agent Team ────────────────────────────────────────────
def section1(pdf):
    pdf.add_page()
    pdf.h1("1. Confirmed Technology Stack and Agent Team")

    # Stack table
    pdf.h2("1.1 Technology Stack")
    sw = [40, 55, PAGE_W - 95]
    pdf.thead(["Layer", "Technology", "Hosting / Notes"], sw)
    stack = [
        ("Frontend",      "Next.js 14 (App Router) + TypeScript",   "Vercel -- auto-deploy from GitHub main"),
        ("Styling",       "Inline styles via GS object (Warm Ivory)","Google Fonts: Playfair Display + Lora + DM Sans"),
        ("Backend API",   "FastAPI (Python 3.10+)",                   "Railway Starter ~USD 5/mo"),
        ("ML Inference",  "LightGBM champion (champion_model.pkl)",   "Loaded at startup, cached in memory"),
        ("Database",      "Supabase PostgreSQL 15",                   "Schema from 04_schema.sql -- ALREADY DEPLOYED"),
        ("File Storage",  "Cloudflare R2",                            "PDF reports + model artefacts"),
        ("Orchestration", "Apache Airflow (9 DAGs)",                  "Railway -- nhces_retrain_weekly + drift_monitor"),
        ("ML Registry",   "MLflow",                                    "Railway -- model versioning"),
        ("CI/CD",         "GitHub Actions",                           "test.yml + deploy.yml"),
        ("Auth",          "Supabase GoTrue (JWT)",                    "3 roles: qsprofessional / researcher / admin"),
    ]
    for i, row in enumerate(stack):
        pdf.trow(list(row), sw, fill=(i % 2 == 1))
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 4.5, sanitize("Table 1: Confirmed iNHCES technology stack for O6."))
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(3)

    # Agent team
    pdf.h2("1.2 Agent Team and Execution Order")
    pdf.agent_box(1,  "Project Leader",        "0 -- COMPLETE (this document)", DARK_NAVY,
        ["Produce master project plan governing all other agents.",
         "Define API contract, file structure, design system, acceptance criteria.",
         "Review and sign off before any agent writes code."])
    pdf.agent_box(2,  "Data Scientist",         "1 -- COMPLETE (O5)",           (0,90,60),
        ["ML model benchmarking and SHAP analysis done in O5.",
         "Champion model: LightGBM, LOO-CV MAPE 13.66%.",
         "Artefact: 05_ml_models/models/champion_model.pkl (ready for Agent 04)."])
    pdf.agent_box(3,  "Front-End Developer",    "2 -- Parallel with 04 & 05",   (0,80,150),
        ["Build Next.js 14 (App Router) frontend.",
         "Implement all UI components using Warm Ivory GS design system.",
         "Connect to FastAPI backend via typed API client (lib/api.ts)."])
    pdf.agent_box(4,  "Back-End Developer",     "2 -- Parallel with 03 & 05",   (100,50,0),
        ["Build FastAPI application (main.py, routers, schemas, services).",
         "Load LightGBM champion model and implement /estimate inference.",
         "Integrate Supabase, Cloudflare R2, Airflow, and MLflow."])
    pdf.agent_box(5,  "Database Developer",     "2 -- Parallel with 03 & 04",   (60,40,20),
        ["Verify all 16 Supabase tables from 04_schema.sql are deployed.",
         "Test all 36 RLS policies for correctness across 3 roles.",
         "Create DB functions and optimise indexes for predictions table."])

    pdf.add_page()
    pdf.agent_box(6,  "QA Engineer",            "3 -- After 03/04/05 complete", (40,80,120),
        ["Design and execute test cases for /estimate, auth, CRUD, and reports.",
         "Run frontend checks on all 7 pages for console errors and responsiveness.",
         "Document and track all defects until resolved."])
    pdf.agent_box(7,  "Code Review Engineer",   "3 -- After 03/04/05 complete", (60,60,100),
        ["Review all backend and frontend code for quality and security.",
         "Confirm no hardcoded credentials, no console.log in production.",
         "Verify CORS is locked to production domain."])
    pdf.agent_box(8,  "Document Engineer",      "3 -- After 03/04/05 complete", (80,60,80),
        ["Write README.md for nhces-backend/ and nhces-frontend/.",
         "Document all environment variables and local setup steps.",
         "FastAPI auto-generates /docs (OpenAPI) -- verify it is complete."])
    pdf.agent_box(9,  "DevOps Engineer",        "4 -- After ALL agents done",   (20,60,80),
        ["Write Dockerfile for nhces-backend/.",
         "Write railway.toml and vercel.json deployment configs.",
         "Write GitHub Actions test.yml and deploy.yml CI/CD workflows.",
         "Verify Railway health check and Vercel deployment succeed."])
    pdf.agent_box(10, "MLOps Engineer",         "4 -- After ALL agents done",   (40,20,80),
        ["Confirm champion_model.pkl loaded from Cloudflare R2 at startup.",
         "Verify nhces_retrain_weekly DAG runs and logs to MLflow.",
         "Verify nhces_drift_monitor DAG runs and PSI scores saved to audit_log.",
         "Confirm SHAP values returned by /estimate and displayed in frontend."])


# ── Section 2: File Structure ───────────────────────────────────────────────────
def section2(pdf):
    pdf.add_page()
    pdf.h1("2. Complete File Structure")

    pdf.h2("2.1 Backend (nhces-backend/)")
    pdf.code_box(
        "nhces-backend/\n"
        "├── app/\n"
        "│   ├── __init__.py\n"
        "│   ├── main.py               ← FastAPI entry, CORS, router includes\n"
        "│   ├── database.py           ← Supabase async client (service_role)\n"
        "│   ├── auth.py               ← JWT middleware (Supabase GoTrue)\n"
        "│   ├── config.py             ← Pydantic Settings (env vars)\n"
        "│   ├── ml/\n"
        "│   │   ├── inference.py      ← Load champion .pkl, predict(), memory cache\n"
        "│   │   ├── feature_prep.py   ← Assemble 14-feature vector from Supabase\n"
        "│   │   └── explainer.py      ← SHAP values for /estimate response\n"
        "│   ├── routers/\n"
        "│   │   ├── estimate.py       ← POST /estimate\n"
        "│   │   ├── macro.py          ← GET /macro, GET /macro/history\n"
        "│   │   ├── projects.py       ← GET/POST/PUT/DELETE /projects\n"
        "│   │   ├── reports.py        ← POST /reports, GET /reports\n"
        "│   │   └── pipeline.py       ← GET /pipeline\n"
        "│   ├── schemas/\n"
        "│   │   ├── estimate.py       ← EstimateRequest, EstimateResponse\n"
        "│   │   ├── project.py        ← ProjectCreate, ProjectRead, ProjectUpdate\n"
        "│   │   ├── report.py         ← ReportRequest, ReportRead\n"
        "│   │   └── macro.py          ← MacroSnapshot, MacroVariable\n"
        "│   └── services/\n"
        "│       ├── r2_storage.py     ← boto3 Cloudflare R2 upload/download\n"
        "│       ├── report_generator.py ← fpdf2 PDF generation\n"
        "│       └── pipeline_monitor.py ← Airflow REST API calls\n"
        "├── tests/\n"
        "│   ├── conftest.py           ← pytest fixtures\n"
        "│   ├── test_estimate.py\n"
        "│   ├── test_api.py\n"
        "│   └── test_pipeline.py\n"
        "├── requirements.txt\n"
        "├── Dockerfile\n"
        "├── .env.example\n"
        "├── railway.toml\n"
        "└── README.md"
    )

    pdf.h2("2.2 Frontend (nhces-frontend/)")
    pdf.code_box(
        "nhces-frontend/\n"
        "├── app/                       ← Next.js 14 App Router\n"
        "│   ├── layout.tsx             ← Root layout: fonts, global CSS, Navbar\n"
        "│   ├── page.tsx               ← Landing / Home page\n"
        "│   ├── estimate/page.tsx      ← Cost Estimation (core feature)\n"
        "│   ├── dashboard/page.tsx     ← Overview dashboard\n"
        "│   ├── projects/page.tsx      ← Project management (CRUD)\n"
        "│   ├── reports/page.tsx       ← Report history and downloads\n"
        "│   ├── macro/page.tsx         ← Macro data viewer + charts\n"
        "│   ├── login/page.tsx         ← Login\n"
        "│   └── register/page.tsx      ← Registration\n"
        "├── components/\n"
        "│   ├── ui/                    ← Primitive components (use GS tokens)\n"
        "│   │   ├── Button.tsx\n"
        "│   │   ├── Card.tsx\n"
        "│   │   ├── Input.tsx\n"
        "│   │   ├── Select.tsx\n"
        "│   │   ├── Badge.tsx\n"
        "│   │   ├── DataSourceBadge.tsx  ← GREEN/AMBER/RED (iNHCES-specific)\n"
        "│   │   ├── LoadingSpinner.tsx\n"
        "│   │   └── Modal.tsx\n"
        "│   ├── layout/\n"
        "│   │   ├── Navbar.tsx\n"
        "│   │   └── Footer.tsx\n"
        "│   ├── estimate/\n"
        "│   │   ├── EstimateForm.tsx\n"
        "│   │   ├── EstimateResult.tsx\n"
        "│   │   └── ShapChart.tsx\n"
        "│   └── dashboard/\n"
        "│       ├── MacroSnapshot.tsx\n"
        "│       ├── ModelStatus.tsx\n"
        "│       ├── PipelineHealth.tsx\n"
        "│       └── RecentPredictions.tsx\n"
        "├── lib/\n"
        "│   ├── styles.ts              ← GS object -- Warm Ivory (SINGLE SOURCE)\n"
        "│   ├── api.ts                 ← Typed fetch wrapper for FastAPI\n"
        "│   ├── auth.ts                ← Supabase Auth client\n"
        "│   └── formatters.ts          ← formatNGN(), formatDate(), formatMAPE()\n"
        "├── types/index.ts             ← TypeScript interfaces\n"
        "├── next.config.js\n"
        "├── tsconfig.json\n"
        "├── .env.local.example\n"
        "└── vercel.json"
    )


# ── Section 3: Design System ───────────────────────────────────────────────────
def section3(pdf):
    pdf.add_page()
    pdf.h1("3. Design System -- Warm Ivory Palette")
    pdf.para(
        "All O6 frontend files MUST use the GS object from lib/styles.ts. "
        "Never hardcode a colour hex or font family directly in a component. "
        "This is the single source of truth for the entire iNHCES UI."
    )

    pdf.h2("3.1 Colour Tokens")
    pdf.thead(["Colour", "Hex", "Role in iNHCES", ""], [12, 28, 80, PAGE_W - 120])
    colour_rows = [
        ("#f5f1eb", "Page background (warm ivory)"),
        ("#ffffff",  "Cards, panels, form inputs"),
        ("#f0ece4",  "Alternate table rows, secondary panels"),
        ("#ddd8cf",  "Default borders"),
        ("#c9c2b8",  "Input focus rings"),
        ("#1a1410",  "Primary text -- WCAG AAA (16.8:1)"),
        ("#5c4f42",  "Muted text, labels -- WCAG AA (7.2:1)"),
        ("#8a7d72",  "Dim text, placeholders -- WCAG AA"),
        ("#8b6400",  "Accent -- buttons, active nav, headings"),
        ("#007a5e",  "GREEN data level badge, success states"),
        ("#b8620a",  "AMBER data level badge, warnings"),
        ("#c0392b",  "RED data level badge, errors, danger"),
    ]
    for i, (hex_val, role) in enumerate(colour_rows):
        r = int(hex_val[1:3], 16)
        g = int(hex_val[3:5], 16)
        b = int(hex_val[5:7], 16)
        fill = (i % 2 == 1)
        sw = [12, 28, 80, PAGE_W - 120]
        pdf.set_fill_color(r, g, b)
        pdf.set_x(LEFT)
        pdf.cell(sw[0], LINE_H, "", border=1, fill=True)
        pdf.set_fill_color(245, 241, 235) if fill else pdf.set_fill_color(*WHITE)
        pdf.set_font("Courier", "", 8)
        pdf.set_text_color(*DARK_GREY)
        pdf.cell(sw[1], LINE_H, sanitize(f" {hex_val}"), border=1, fill=True)
        pdf.set_font("Helvetica", "", 8)
        pdf.cell(sw[2], LINE_H, sanitize(f" {role}"), border=1, fill=True)
        pdf.cell(sw[3], LINE_H, "", border=1, fill=True)
        pdf.ln()
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 4.5, sanitize(
        "Table 2: Warm Ivory colour tokens. GREEN/AMBER/RED map directly to "
        "the iNHCES DATA SOURCE Declaration System. Do not alter these values."
    ))
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(2)

    pdf.h2("3.2 Typography")
    tw = [35, 30, 28, PAGE_W - 93]
    pdf.thead(["Font Family", "Role", "CSS Variable", "Weights Used"], tw)
    fonts = [
        ("Playfair Display", "Page titles, section headings", "--font-display", "700, 900"),
        ("Lora",             "Body copy, card text",          "--font-body",    "400, 500, 600, 700"),
        ("DM Sans",          "Buttons, nav, labels, data",    "--font-ui",      "400, 500, 600"),
    ]
    for i, row in enumerate(fonts):
        pdf.trow(list(row), tw, fill=(i % 2 == 1))
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 4.5, sanitize(
        "Table 3: Typography. Load all three from Google Fonts in app/layout.tsx "
        "using next/font/google. Use CSS variables for font-family throughout."
    ))
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(2)

    pdf.h2("3.3 DataSourceBadge Component (iNHCES-specific)")
    pdf.para(
        "The DataSourceBadge is a mandatory UI element. It must appear on every "
        "page that displays ML predictions, macro data, or any content derived "
        "from the iNHCES data pipeline. This operationalises the DATA SOURCE "
        "Declaration System at the user interface level."
    )
    pdf.code_box(
        "// components/ui/DataSourceBadge.tsx\n"
        "type Level = 'GREEN' | 'AMBER' | 'RED';\n"
        "const STYLES = {\n"
        "  GREEN: { bg: '#007a5e', label: 'Live Data'   },\n"
        "  AMBER: { bg: '#b8620a', label: 'AI Template' },\n"
        "  RED:   { bg: '#c0392b', label: 'Synthetic -- Replace Before Publication' },\n"
        "};\n"
        "export function DataSourceBadge({ level }: { level: Level }) {\n"
        "  const s = STYLES[level];\n"
        "  return (\n"
        "    <span style={{\n"
        "      background: s.bg, color: '#fff',\n"
        "      fontFamily: 'var(--font-ui)', fontSize: 12,\n"
        "      padding: '2px 10px', borderRadius: 20,\n"
        "    }}>\n"
        "      {level}: {s.label}\n"
        "    </span>\n"
        "  );\n"
        "}"
    )

    pdf.h2("3.4 Minimum Font Sizes (Accessibility)")
    fz = [30, 25, PAGE_W - 55]
    pdf.thead(["Size Token", "px Range", "Used For"], fz)
    sizes = [
        ("xs",   "13-14px", "Tags, badges, small labels"),
        ("sm",   "15-16px", "Secondary body, card metadata"),
        ("base", "17px",    "Primary body text"),
        ("md",   "19-20px", "Card titles, sub-headings"),
        ("lg",   "24-28px", "Section headings"),
        ("xl",   "32-36px", "Page titles (Playfair Display)"),
        ("2xl",  "44-56px", "Hero headings (landing page)"),
    ]
    for i, row in enumerate(sizes):
        pdf.trow(list(row), fz, fill=(i % 2 == 1))
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 4.5, sanitize(
        "Table 4: Minimum font sizes. Never go below 13px in any UI element."
    ))
    pdf.set_text_color(*DARK_GREY)


# ── Section 4: API Contract ────────────────────────────────────────────────────
def section4(pdf):
    pdf.add_page()
    pdf.h1("4. API Contract -- FastAPI Endpoints")
    pdf.para(
        "This is the binding contract between Agent 04 (backend) and Agent 03 "
        "(frontend). The frontend lib/api.ts must match these exactly. "
        "Base URL: https://nhces-api.up.railway.app (production) | "
        "http://localhost:8000 (development). "
        "All protected endpoints require: Authorization: Bearer <supabase-jwt>"
    )

    pdf.api_block("POST", "/estimate",
        "ML cost prediction. Core product endpoint. Target response < 3 seconds.",
        'Request: { "building_type": "Residential", "construction_type": "New Build",\n'
        '  "floor_area_sqm": 120.0, "num_floors": 1,\n'
        '  "location_state": "Kaduna", "location_zone": "North West",\n'
        '  "project_id": "uuid (optional)" }',
        'Response: { "prediction_id": "uuid", "predicted_cost_per_sqm": 182500.00,\n'
        '  "total_predicted_cost_ngn": 21900000.00,\n'
        '  "confidence_lower": 152000.00, "confidence_upper": 213000.00,\n'
        '  "mape_at_prediction": 13.66, "model_version": "lgb-2026-04-26",\n'
        '  "shap_values": { "ret_ngn_usd": 28450.0, ... },\n'
        '  "data_freshness": "RED", "api_response_ms": 1240 }'
    )

    pdf.api_block("GET", "/macro",
        "Latest macro snapshot for dashboard. Shows current data levels.",
        '',
        'Response: { "variables": [\n'
        '  { "variable": "ngn_usd", "label": "NGN/USD Rate",\n'
        '    "value": 1480.0, "unit": "NGN per USD",\n'
        '    "as_of_date": "2024-01-01", "data_level": "RED" }\n'
        '], "overall_freshness": "RED" }'
    )

    pdf.api_block("GET", "/macro/history?variable=ngn_usd&years=5",
        "Historical series for charting on macro page.",
        '',
        'Response: { "variable": "ngn_usd",\n'
        '  "data": [{"year": 2020, "value": 381.0}, ...] }'
    )

    pdf.api_block("GET", "/projects",
        "List authenticated user's projects (paginated, RLS enforced).",
        '',
        'Response: { "items": [{...}], "total": 5, "page": 1 }'
    )

    pdf.api_block("POST", "/projects",
        "Create a new project.",
        'Request: { "title": "3-Bed Bungalow Kaduna",\n'
        '  "building_type": "Residential", "construction_type": "New Build",\n'
        '  "floor_area_sqm": 120.0, "num_floors": 1,\n'
        '  "location_state": "Kaduna", "location_zone": "North West" }',
        'Response: { "id": "uuid", "title": "...", "created_at": "..." }'
    )

    pdf.api_block("POST", "/reports",
        "Generate PDF cost report, upload to Cloudflare R2, return presigned URL.",
        'Request: { "project_id": "uuid", "prediction_id": "uuid" }',
        'Response: { "report_id": "uuid",\n'
        '  "download_url": "https://r2-presigned...",\n'
        '  "url_expires_at": "2026-04-27T10:00:00Z", "page_count": 4 }'
    )

    pdf.api_block("GET", "/pipeline",
        "Airflow DAG health status for pipeline monitor dashboard.",
        '',
        'Response: { "dags": [\n'
        '  { "dag_id": "nhces_daily_fx_oil", "schedule": "0 5 * * *",\n'
        '    "last_run_state": "success", "last_run_at": "2026-04-26T05:00:00Z",\n'
        '    "data_level": "RED" }\n'
        '], "overall_health": "DEGRADED" }'
    )

    pdf.h2("4.1 Authentication Pattern")
    pdf.para(
        "Supabase GoTrue handles auth. FastAPI validates the JWT on every protected "
        "endpoint via the auth.py middleware. The frontend uses the Supabase JS client "
        "for login/register and passes the session token in the Authorization header "
        "of every API call."
    )
    pdf.code_box(
        "# FastAPI JWT validation (app/auth.py)\n"
        "from jose import jwt, JWTError\n"
        "SUPABASE_JWT_SECRET = settings.supabase_jwt_secret\n\n"
        "async def get_current_user(authorization: str = Header(...)):\n"
        "    token = authorization.replace('Bearer ', '')\n"
        "    payload = jwt.decode(token, SUPABASE_JWT_SECRET, algorithms=['HS256'])\n"
        "    return {'user_id': payload['sub'], 'role': payload.get('role', 'qsprofessional')}"
    )


# ── Section 5: Frontend Pages ──────────────────────────────────────────────────
def section5(pdf):
    pdf.add_page()
    pdf.h1("5. Frontend Pages -- Specification")

    pages = [
        ("Landing / Home  (app/page.tsx)", [
            "Hero section: Playfair Display 44px headline 'Intelligent Housing Cost Estimation for Nigeria'. Lora body. Two CTA buttons: 'Get an Estimate' (accent filled) + 'View Dashboard' (ghost).",
            "Stats strip: '7 Macro Variables | 9 Data Pipelines | 13.66% LOO-CV MAPE'. DM Sans, amber accent.",
            "How it Works: 3 cards (Enter Project -> AI Predicts -> Download Report). Card component with ivory background.",
            "Data Quality section: Explain GREEN/AMBER/RED. One DataSourceBadge per level with explanation text.",
            "CTA: 'Start Estimating' button linking to /estimate.",
        ]),
        ("Estimate  (app/estimate/page.tsx)  -- CORE FEATURE", [
            "Two-column layout: EstimateForm left, EstimateResult right (stacked on mobile).",
            "EstimateForm: Title, Building Type (select), Construction Type (select), Location State (input), Zone (select), Floor area sqm (number), Num floors (number), Target cost NGN (optional), Notes (textarea). Submit: 'Calculate Cost' (accent, full width).",
            "Loading state: spinner + 'Consulting champion model...' text.",
            "EstimateResult: Predicted NGN/sqm (DM Sans 36px, accent), Total cost (Lora 24px), Confidence band (amber styling), DataSourceBadge, Model version + MAPE, ShapChart (top 5 features, horizontal bars), 'Generate PDF Report' button, 'Save to Project' button.",
        ]),
        ("Dashboard  (app/dashboard/page.tsx)", [
            "MacroSnapshot card: 5 macro variables with value, unit, DataSourceBadge per row.",
            "ModelStatus card: champion model name, LOO-CV MAPE, R2, training date, is_champion badge (green).",
            "PipelineHealth card: 9 DAGs listed with last_run_state (green tick / red cross) and timestamp.",
            "RecentPredictions table: last 5 predictions with project name, cost/sqm, date.",
        ]),
        ("Projects  (app/projects/page.tsx)", [
            "Project card list: title, location, floor area, building type, status badge, 'Estimate' button (links to /estimate with project pre-loaded).",
            "'New Project' button (accent, top right) opens ProjectForm modal.",
            "Delete with confirmation dialog. RLS ensures users see only their projects.",
        ]),
        ("Reports  (app/reports/page.tsx)", [
            "Table: project name, date created, file size, 'Download PDF' button.",
            "Download button calls GET /reports to refresh presigned R2 URL, then opens in new tab.",
        ]),
        ("Macro Data  (app/macro/page.tsx)", [
            "Variable selector dropdown: ngn_usd, cpi_annual_pct, gdp_growth_pct, lending_rate_pct, brent_usd_barrel.",
            "Line chart (recharts or similar): historical series, x=year, y=value, ivory background.",
            "DataSourceBadge per variable. Summary table of all latest values.",
        ]),
        ("Auth Pages  (app/login + app/register)", [
            "Centred card layout on ivory background. iNHCES logo/title in Playfair Display.",
            "Email + Password inputs (GS.input style). Submit button (GS.btn).",
            "Supabase Auth JS client handles signup/login. Redirect to /dashboard on success.",
        ]),
    ]

    for title, bullets in pages:
        pdf.h2(title)
        pdf.bullet(bullets)


# ── Section 6: Acceptance Criteria ────────────────────────────────────────────
def section6(pdf):
    pdf.add_page()
    pdf.h1("6. Acceptance Criteria -- All Agents")

    criteria = {
        "Agent 03 -- Frontend": [
            "All 7 pages render without errors on desktop (1280px) and mobile (375px)",
            "Warm Ivory palette applied -- no hardcoded hex colours in components",
            "Playfair Display + Lora + DM Sans loaded via next/font/google",
            "POST /estimate integration: form submits, result panel renders",
            "GET /macro: macro values displayed with correct DataSourceBadge",
            "Project CRUD: create, list, delete all working",
            "Auth: login, register, protected routes (/estimate, /dashboard require login)",
            "DataSourceBadge renders GREEN/AMBER/RED correctly on all relevant pages",
            "ShapChart renders correctly with real SHAP data from /estimate",
            "Report download button triggers presigned URL and opens PDF",
        ],
        "Agent 04 -- Backend": [
            "GET / health check returns 200 (Railway deployment verification)",
            "/estimate returns prediction in < 3 seconds on Railway",
            "/estimate logs prediction row to Supabase predictions table",
            "JWT middleware rejects invalid tokens with 401",
            "CORS accepts requests from nhces.vercel.app and localhost:3000 only",
            "PDF generated by report_generator.py, uploaded to R2, presigned URL returned",
            "/pipeline returns Airflow DAG status",
            "All Pydantic schemas enforce types -- no 422 on valid input",
        ],
        "Agent 05 -- Database": [
            "All 16 tables present in Supabase production SQL Editor",
            "v_latest_macro view returns 5 rows (one per macro variable)",
            "v_champion_model view returns exactly 1 row",
            "RLS: qsprofessional sees only own projects (test with test JWT)",
            "RLS: service_role can INSERT into all macro/material tables",
            "predictions table index on user_id and created_at DESC confirmed",
        ],
        "Agent 06 -- QA": [
            "pytest nhces-backend/tests/ -- all tests pass",
            "No console errors on any of the 7 frontend pages",
            "Mobile layout (375px) renders all pages without horizontal scroll",
            "/estimate returns valid JSON for all valid building_type values",
        ],
        "Agent 07 -- Code Review": [
            "No secrets or API keys in any committed file",
            "No console.log() in production frontend code",
            "CORS origin list does not contain wildcard '*' in production config",
            "All environment variables documented in .env.example files",
        ],
        "Agent 09 -- DevOps": [
            "Railway deployment: GET https://nhces-api.up.railway.app/ returns 200",
            "Vercel deployment: https://nhces.vercel.app loads in < 3 seconds",
            "GitHub Actions test.yml runs and passes on every PR",
            "GitHub Actions deploy.yml deploys backend and frontend on merge to main",
        ],
        "Agent 10 -- MLOps": [
            "champion_model.pkl loaded from Cloudflare R2 at FastAPI startup",
            "/estimate SHAP values non-null when real data is available",
            "nhces_retrain_weekly DAG scheduled and visible in Airflow UI",
            "nhces_drift_monitor DAG running daily and PSI scores in audit_log",
        ],
    }

    for agent, checks in criteria.items():
        pdf.h2(agent)
        for check in checks:
            pdf.set_font("Helvetica", "", 9)
            pdf.set_text_color(*DARK_GREY)
            pdf.set_x(LEFT + 2)
            pdf.cell(6, 5.2, "[ ]")
            pdf.set_x(LEFT + 8)
            pdf.multi_cell(PAGE_W - 8, 5.2, sanitize(check))
        pdf.ln(1)


# ── Section 7: Session Sequence ────────────────────────────────────────────────
def section7(pdf):
    pdf.add_page()
    pdf.h1("7. Development Session Sequence")
    pdf.para(
        "Each session is a single Claude Code interaction. Sessions for Agent 03 "
        "and Agent 04 run concurrently (separate sessions). Complete all backend "
        "sessions before QA/Review sessions begin."
    )
    sw = [12, 12, 40, PAGE_W - 64]
    pdf.thead(["Session", "Agent", "Focus", "Key Deliverables"], sw)
    sessions = [
        ("O6-S1",  "04", "Backend core",         "main.py, config.py, database.py, auth.py, requirements.txt"),
        ("O6-S2",  "04", "ML inference",          "app/ml/inference.py, feature_prep.py, explainer.py"),
        ("O6-S3",  "04", "/estimate endpoint",    "routers/estimate.py, schemas/estimate.py"),
        ("O6-S4",  "04", "Other endpoints",       "routers/macro.py, projects.py, reports.py, pipeline.py"),
        ("O6-S5",  "04", "Services",              "services/r2_storage.py, report_generator.py, pipeline_monitor.py"),
        ("O6-S6",  "03", "Design system + UI",    "lib/styles.ts, lib/api.ts, components/ui/*, layout.tsx"),
        ("O6-S7",  "03", "Core pages",            "app/page.tsx (landing), app/estimate/page.tsx"),
        ("O6-S8",  "03", "Dashboard",             "app/dashboard/page.tsx, components/dashboard/*"),
        ("O6-S9",  "03", "Projects + Reports",    "app/projects/page.tsx, app/reports/page.tsx, app/macro/page.tsx"),
        ("O6-S10", "03", "Auth pages",            "app/login/page.tsx, app/register/page.tsx"),
        ("O6-S11", "05", "DB verification",       "RLS testing, index verification, DB functions"),
        ("O6-S12", "06+07", "QA + Code Review",   "tests/*.py, code review checklist"),
        ("O6-S13", "08", "Documentation",         "README.md (backend + frontend), API docs verification"),
        ("O6-S14", "09+10", "DevOps + MLOps",     "Dockerfile, railway.toml, vercel.json, deploy.yml, DAG config"),
    ]
    for i, row in enumerate(sessions):
        pdf.trow(list(row), sw, fill=(i % 2 == 1))
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 4.5, sanitize(
        "Table 5: Development session sequence. "
        "Sessions O6-S1 to O6-S5 (backend) and O6-S6 to O6-S10 (frontend) "
        "may run in parallel as they work on separate directories."
    ))
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(2)

    pdf.info_box(
        "NEXT ACTION: The research team must review this plan and confirm:\n"
        "  1. File structure is correct and consistent with O4 design\n"
        "  2. API contract matches SRS requirements from O3\n"
        "  3. Design system (Warm Ivory) is approved for iNHCES\n"
        "  4. Session sequence is achievable within project timeline\n\n"
        "After sign-off: say 'Proceed with O6-S1' to begin Agent 04 backend development."
    )


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    pdf = PlanPDF()
    make_cover(pdf)
    _ds_page(pdf, 'amber',
        "DATA SOURCE: AMBER -- AI-authored project plan from O3 SRS, O4 architecture, O5 ML outputs.",
        (
            "WHAT IS REAL IN THIS DOCUMENT:\n"
            "  * Technology choices (Next.js, FastAPI, Supabase, Railway, Vercel) confirmed by researcher.\n"
            "  * Design system (Warm Ivory Palette) adopted from Buildwise NG, confirmed by researcher.\n"
            "  * Multi-agent structure from researcher's instruction document.\n"
            "  * File structure derived from O4 architecture decisions.\n"
            "  * API contract derived from O4 SRS + O5 ML output schemas.\n\n"
            "WHAT REQUIRES VALIDATION:\n"
            "  * All file paths and API endpoint definitions must be validated by the research team.\n"
            "  * Acceptance criteria may need adjustment after implementation begins.\n"
            "  * Session timeline is estimated -- adjust as needed during development.\n\n"
            "RULE: No agent may write production code until this plan is reviewed and approved."
        )
    )
    section1(pdf)
    section2(pdf)
    section3(pdf)
    section4(pdf)
    section5(pdf)
    section6(pdf)
    section7(pdf)
    pdf.output(OUT)
    print(f"[OK] O6_00_Agent01_Project_Plan.pdf ({pdf.page} pages) -> {OUT}")


if __name__ == "__main__":
    main()
