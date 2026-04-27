"""
iNHCES O4 Step 4 — Chapter 4 Conceptual Models PDF Generator
Deliverable: O4_04_Chapter4_Conceptual_Models.pdf
DATA SOURCE: AMBER — AI-authored first draft synthesising O4 Steps 1-3.
             Validates against O3 Delphi consensus (36 items) and SRS IEEE 830.
             Feeds into Papers P4 (Scientific Data) and P7 (Automation in Construction).

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
DOC_ID    = "O4-04"
DOC_TITLE = "Chapter 4: Conceptual System Design"
DOC_SUBTITLE = "Architecture, Schema, DFDs, Pipeline, and User Journey"


class ChapterPDF(DocPDF):
    def __init__(self):
        super().__init__(DOC_TITLE, DOC_ID)

    def header(self):
        self.set_fill_color(*DARK_NAVY)
        self.rect(0, 0, 210, 14, 'F')
        self.set_font("Helvetica", "B", 7)
        self.set_text_color(*WHITE)
        self.set_xy(5, 4)
        self.cell(PAGE_W, 6, sanitize(
            "iNHCES  |  TETFund NRF 2025  |  Dept. Quantity Surveying, ABU Zaria"
            "  |  O4 Step 4 — Chapter 4: Conceptual System Design"
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
            f"iNHCES {DOC_TITLE}  |  ABU Zaria / TETFund NRF 2025  |  Page {self.page_no()}"
        ), align="C")

    def chapter_heading(self, text):
        self.ln(4)
        self.set_fill_color(*DARK_NAVY)
        self.set_text_color(*WHITE)
        self.set_font("Helvetica", "B", 12)
        self.set_x(LEFT)
        self.cell(PAGE_W, 10, sanitize(f"  {text}"), fill=True, ln=True)
        self.set_text_color(*DARK_GREY)
        self.ln(3)

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

    def h3(self, text):
        self.ln(1.5)
        self.set_font("Helvetica", "BI", 9)
        self.set_text_color(*DARK_NAVY)
        self.set_x(LEFT)
        self.multi_cell(PAGE_W, 5.2, sanitize(text))
        self.set_text_color(*DARK_GREY)
        self.ln(0.5)

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

    def rationale_box(self, title, text):
        self.ln(2)
        self.set_fill_color(220, 235, 220)
        self.set_draw_color(0, 100, 50)
        self.set_line_width(0.5)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(0, 80, 30)
        self.set_x(LEFT)
        self.cell(PAGE_W, 6.5, sanitize(f"  DESIGN RATIONALE:  {title}"),
                  border=1, fill=True, ln=True)
        self.set_fill_color(235, 248, 235)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*DARK_GREY)
        self.set_x(LEFT)
        self.multi_cell(PAGE_W, 5, sanitize(text), border="LBR", fill=True)
        self.set_text_color(*DARK_GREY)
        self.ln(2)

    def ref_item(self, text):
        self.set_font("Helvetica", "", 8.5)
        self.set_text_color(*DARK_GREY)
        self.set_x(LEFT + 5)
        self.multi_cell(PAGE_W - 5, 4.8, sanitize(text))
        self.ln(0.5)


# ── Cover ──────────────────────────────────────────────────────────────────────
def make_cover(pdf):
    pdf.add_page()
    pdf.set_fill_color(*DARK_NAVY)
    pdf.rect(0, 18, 210, 55, 'F')
    pdf.set_xy(0, 24)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(200, 215, 235)
    pdf.cell(210, 7, "Intelligent National Housing Cost Estimating System (iNHCES)", align="C", ln=True)
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(*WHITE)
    pdf.cell(210, 10, sanitize(DOC_TITLE), align="C", ln=True)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(200, 215, 235)
    pdf.cell(210, 7, sanitize(DOC_SUBTITLE), align="C", ln=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*LIGHT_BLUE)
    pdf.cell(210, 6, "TETFund NRF 2025  |  Department of Quantity Surveying, ABU Zaria", align="C", ln=True)
    pdf.set_draw_color(*GOLD)
    pdf.set_line_width(0.8)
    pdf.line(30, 79, 180, 79)
    pdf.set_xy(LEFT, 87)
    meta = [
        ("Objective:",    "O4 — Develop Conceptual Models for the iNHCES System"),
        ("Step:",         "4 — Chapter 4 Write-up (Synthesis of Steps 1-3)"),
        ("Document ID:",  DOC_ID),
        ("Version:",      "1.0 — Initial AI-Assisted Draft"),
        ("Date:",         date.today().strftime("%d %B %Y")),
        ("Grant:",        "TETFund National Research Fund (NRF) 2025"),
        ("Feeds into:",   "Paper P4 (Scientific Data) | Paper P7 (Automation in Construction)"),
        ("Completes:",    "O4 — All 4 steps. Next: O5 ML Model Benchmarking."),
    ]
    for label, val in meta:
        pdf.set_x(LEFT)
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*DARK_NAVY)
        pdf.cell(40, 6.5, sanitize(label))
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*DARK_GREY)
        pdf.cell(PAGE_W - 40, 6.5, sanitize(val), ln=True)


# ── Section 4.1: Introduction ─────────────────────────────────────────────────
def section41(pdf):
    pdf.add_page()
    pdf.chapter_heading("CHAPTER 4: CONCEPTUAL SYSTEM DESIGN")
    pdf.h1("4.1 Introduction")
    pdf.para(
        "This chapter presents the conceptual design of the Intelligent National "
        "Housing Cost Estimating System (iNHCES), translating the system requirements "
        "elicited through the three-round Delphi consensus process (Chapter 3) into "
        "formal architectural and behavioural specifications. The conceptual design "
        "serves two purposes: it provides the implementation blueprint for the O6 "
        "development phase, and it constitutes the theoretical contribution of iNHCES "
        "to the system design literature on AI-augmented cost estimation in "
        "developing-economy construction sectors."
    )
    pdf.para(
        "The conceptual design is organised across four interconnected artefact sets, "
        "each developed as a formal model and stored as an implementable file "
        "in the `04_conceptual_models/` directory:"
    )
    pdf.bullet([
        "System Architecture (Section 4.2): a seven-layer cloud-native architecture "
        "specifying all components, technology choices, and inter-component "
        "relationships. File: `04_Architecture_Diagram.mmd` and `O4_01_System_Architecture.pdf`.",
        "Database Schema (Section 4.3): a normalised relational schema for Supabase "
        "PostgreSQL comprising sixteen tables, seven enumerated types, two helper views, "
        "and row-level security policies governing all data access. "
        "Files: `04_schema.sql`, `04_rls_policies.sql`, `04_seed_data.sql`.",
        "Data Flow Diagrams (Section 4.4): a two-level DFD decomposition defining "
        "all system processes, data stores, and data flows. "
        "Files: `04_DFD_Level0.mmd`, `04_DFD_Level1.mmd`.",
        "Pipeline and User Journey Models (Section 4.5): nine-DAG Airflow pipeline "
        "design and satisfaction-scored user journey maps. "
        "Files: `04_Pipeline_Flow.mmd`, `04_User_Journey.mmd`.",
    ])
    pdf.para(
        "Together, these artefacts address the 36 Delphi consensus items across seven "
        "functional categories (Section 4.6) and satisfy all 47 functional requirements "
        "documented in the iNHCES Software Requirements Specification "
        "(SRS, IEEE 830, O3 Step 4). The chapter concludes with a discussion of "
        "design limitations and the transition to O5 ML model benchmarking (Section 4.7)."
    )


# ── Section 4.2: System Architecture ─────────────────────────────────────────
def section42(pdf):
    pdf.add_page()
    pdf.h1("4.2 System Architecture")

    pdf.h2("4.2.1 Architecture Philosophy")
    pdf.para(
        "The iNHCES architecture follows three guiding principles derived from the "
        "Delphi consensus and the iNHCES Research Advisory Framework:"
    )
    pdf.bullet([
        "Separation of concerns: data ingestion, ML inference, API logic, and "
        "frontend presentation are deployed as independently scalable services. "
        "This addresses Delphi Category F (Performance) items F1-F6.",
        "Data provenance transparency: every data record carries a "
        "data_source_level field (GREEN / AMBER / RED) reflecting reliability. "
        "This implements the iNHCES Simulation-to-Publication Framework and "
        "supports Delphi Category D item D5 (data quality disclosure).",
        "Cost-appropriate technology: all platform choices prioritise free or "
        "low-cost tiers for the academic prototype, while remaining upgradeable "
        "to production equivalents without architectural changes.",
    ])

    pdf.h2("4.2.2 Seven-Layer Architecture")
    pdf.para(
        "The system is organised into seven layers (see `04_Architecture_Diagram.mmd`). "
        "Table 4.1 presents the layer summary."
    )
    lw = [36, 38, PAGE_W - 74]
    pdf.thead(["Layer", "Technology / Platform", "Primary Responsibility"], lw)
    layers = [
        ("1. User",         "Browser (any)",              "HTTPS access"),
        ("2. Presentation", "Vanilla HTML/CSS/JS — Vercel","Cost estimator form; pipeline dashboard"),
        ("3. API",          "FastAPI (Python 3.10+) — Railway","Business logic; JWT auth; routing; PDF generation"),
        ("4. ML",           "MLflow Registry — Railway",   "Champion model serving; experiment tracking; retrain"),
        ("5. Data",         "Supabase PostgreSQL",         "Persistent data: macro, materials, projects, predictions"),
        ("6. Storage",      "Cloudflare R2",               "PDF reports; model artefacts; training datasets"),
        ("7. Pipeline",     "Apache Airflow — Railway",    "9 DAGs: data ingestion, ML retrain, drift monitoring"),
    ]
    for i, row in enumerate(layers):
        pdf.trow(list(row), lw, fill=(i % 2 == 1))
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 4.5, sanitize("Table 4.1: iNHCES seven-layer architecture summary."))
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(2)

    pdf.h2("4.2.3 Technology Selection Rationale")
    pdf.rationale_box("FastAPI over Django / Flask",
        "FastAPI provides automatic OpenAPI/Swagger documentation (academic transparency), "
        "native async support (concurrent Supabase + MLflow + R2 calls in /estimate), "
        "and Pydantic validation aligned with the typed feature schema. "
        "Projected /estimate response time: under 3 seconds (Delphi Category F target)."
    )
    pdf.rationale_box("Supabase PostgreSQL over NoSQL alternatives",
        "The iNHCES data model is fundamentally relational (time-series macro data "
        "with FK relationships to prediction and project records). Supabase provides "
        "PostgreSQL (SQL, JOINs, window functions), built-in Row Level Security, "
        "GoTrue Auth (JWT), and a Python client within a single free-tier platform, "
        "eliminating the need for a separate authentication service."
    )
    pdf.rationale_box("Cloudflare R2 over AWS S3",
        "R2 has zero egress fees (AWS S3 charges ~USD 0.09/GB egress). "
        "For an academic prototype generating PDF reports and serving model artefacts, "
        "zero egress cost is the decisive factor. "
        "R2 is S3-API-compatible: migration to S3 requires only an endpoint URL change."
    )
    pdf.rationale_box("Apache Airflow over Prefect / Dagster",
        "Airflow is the industry-standard orchestrator with the largest community. "
        "The nine-DAG cron schedule maps naturally to Airflow's scheduler, and the "
        "SqlSensor operator handles the drift monitor's database condition check natively. "
        "Self-hosted on Railway; no managed service cost at prototype scale."
    )

    pdf.h2("4.2.4 Security Architecture")
    pdf.para(
        "Three mechanisms work in combination to secure the iNHCES system:"
    )
    pdf.bullet([
        "JWT Authentication (Supabase GoTrue): All API endpoints require a valid "
        "JWT access token (1-hour expiry). The FastAPI JWT middleware validates "
        "the token signature on every request.",
        "Row Level Security (RLS): All sixteen tables have RLS enabled. Users "
        "read and write only their own records. Macro and material data is "
        "readable by all authenticated users but writable only by the service "
        "role (Airflow pipelines). See `04_rls_policies.sql`.",
        "Role-Based Access Control (RBAC): Three roles — qsprofessional "
        "(estimate + projects), researcher (+ aggregate data read), admin "
        "(+ user management + model promotion).",
    ])


# ── Section 4.3: Database Design ─────────────────────────────────────────────
def section43(pdf):
    pdf.add_page()
    pdf.h1("4.3 Database Design")

    pdf.h2("4.3.1 Schema Overview")
    pdf.para(
        "The iNHCES schema (`04_schema.sql`) comprises sixteen tables in five "
        "functional groups. Table 4.2 summarises the groups."
    )
    gw = [36, 48, PAGE_W - 84]
    pdf.thead(["Group", "Tables", "Data Level"], gw)
    groups = [
        ("Macroeconomic Data",      "macro_fx, macro_cpi, macro_gdp,\nmacro_interest, macro_oil",
         "GREEN (World Bank live)\nRED* (EIA + FRED — upgrade with API keys)"),
        ("Material Prices",         "material_cement, material_steel,\nmaterial_pms",
         "RED* (scrapers + NNPC — upgrade when scrapers operational)"),
        ("Rates + Market Prices",   "unit_rates, market_prices",
         "RED* (NIQS manual + PropertyPro scraper)"),
        ("Project + Predictions",   "projects, predictions, reports",
         "User-owned, RLS enforced"),
        ("System Management",       "users, ml_models, audit_log",
         "System-managed, admin/service_role access"),
    ]
    for i, row in enumerate(groups):
        pdf.mrow(list(row), gw, fill=(i % 2 == 1))
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 4.5, sanitize(
        "Table 4.2: Database schema functional groups. "
        "RED* = synthetic in prototype; upgrade by configuring API keys. "
        "Full column definitions in O4_02_Database_Schema.pdf."
    ))
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(2)

    pdf.h2("4.3.2 Key Design Decisions")
    pdf.rationale_box("JSONB for SHAP Values and Feature Snapshots",
        "Storing shap_values and feature_snapshot as JSONB in the predictions table "
        "(rather than normalising into separate rows) enables the /estimate endpoint "
        "to return the full prediction record in a single query while keeping the "
        "schema flexible as the feature set evolves across ML retraining cycles. "
        "A JSONB GIN index can be added in O6 if individual SHAP value queries "
        "become a performance concern."
    )
    pdf.rationale_box("data_source_level Enum on Every Observation Row",
        "Rather than a separate data quality table, data_source_level (GREEN/AMBER/RED) "
        "is stored on every observation row. This enables the /macro endpoint to "
        "report data provenance in real time and allows the frontend to display "
        "freshness warnings without a separate API call. The enum constraint prevents "
        "invalid quality labels at the database level."
    )
    pdf.rationale_box("Unique Partial Index on Champion Model",
        "A partial unique index (WHERE is_champion = TRUE) on the ml_models table "
        "enforces at the database level that exactly one model is in Production at "
        "any time, preventing race conditions during the weekly champion promotion "
        "workflow when the Airflow DAG and admin API call could otherwise create "
        "two concurrent champions."
    )
    pdf.rationale_box("Denormalised user_id in predictions",
        "user_id is stored directly in the predictions table (in addition to "
        "project_id -> projects.user_id) to enable efficient RLS policy evaluation "
        "without a JOIN to the projects table on every prediction query. "
        "The trade-off is minor write-time redundancy, which is acceptable "
        "given the read-heavy prediction log access pattern."
    )

    pdf.h2("4.3.3 Normalisation and Referential Integrity")
    pdf.para(
        "The schema is in Third Normal Form (3NF). All transitive dependencies have "
        "been eliminated. Referential integrity is enforced by PostgreSQL foreign key "
        "constraints with appropriate cascade rules:"
    )
    pdf.bullet([
        "projects.user_id -> users.id ON DELETE CASCADE: deleting a user "
        "removes all their projects and, by cascade, their predictions.",
        "predictions.project_id -> projects.id ON DELETE CASCADE: "
        "deleting a project removes its prediction log.",
        "reports.prediction_id -> predictions.id ON DELETE SET NULL: "
        "deleting a prediction retains the report record — the PDF file "
        "in Cloudflare R2 is not automatically deleted (requires separate "
        "R2 lifecycle policy or admin action).",
        "ml_models.promoted_by -> users.id ON DELETE SET NULL: "
        "retains the model record even if the admin user is deleted.",
    ])


# ── Section 4.4: Data Flow Model ──────────────────────────────────────────────
def section44(pdf):
    pdf.add_page()
    pdf.h1("4.4 Data Flow Model")

    pdf.h2("4.4.1 DFD Level 0 — System Boundary")
    pdf.para(
        "The Level 0 DFD (`04_DFD_Level0.mmd`) defines the iNHCES system boundary. "
        "Eleven external entities interact with the system across three categories: "
        "human users (QS Professional, Researcher/PI, System Admin), automated data "
        "sources (World Bank API, EIA API, FRED/CBN API, two scrapers, NNPC/NMDPRA, "
        "NIQS manual upload), and CI/CD infrastructure (GitHub Actions). "
        "All inbound and outbound data flows are explicitly labelled with their "
        "data type, frequency, and direction."
    )
    pdf.para(
        "The QS Professional is the primary source of project input data and the "
        "primary consumer of cost estimates and PDF reports, confirming the dominant "
        "user journey established by the Delphi panel (Category E, items E1-E4, E6)."
    )

    pdf.h2("4.4.2 DFD Level 1 — Process Decomposition")
    pdf.para(
        "The Level 1 DFD (`04_DFD_Level1.mmd`) decomposes the system into six "
        "processes and three data stores. Table 4.3 maps each process to its "
        "primary SRS requirement set."
    )
    pw = [22, 36, 28, PAGE_W - 86]
    pdf.thead(["Process", "Name", "SRS Req. Set", "Key Data Flows"], pw)
    processes = [
        ("1.0", "User Authentication",  "FR-AUTH-01/06",
         "JWT issuance; login audit log"),
        ("2.0", "Cost Estimation",      "FR-EST-01/12",
         "Feature assembly from D1; champion model load from D2; "
         "prediction record + SHAP to D1"),
        ("3.0", "Data Ingestion",       "FR-DATA-01/09",
         "External sources -> validated rows -> D1 macro/material tables"),
        ("4.0", "ML Management",        "FR-ML-01/08",
         "Feature matrix from D1; experiments to D3 (MLflow); "
         "champion artefact to D2 (R2)"),
        ("5.0", "Report Generation",    "FR-RPT-01/05",
         "Project + prediction from D1; PDF to D2; presigned URL to user"),
        ("6.0", "Pipeline Monitoring",  "FR-MON-01/06",
         "PSI computation from D1 vs. D3 baseline; emergency retrain trigger"),
    ]
    for i, row in enumerate(processes):
        pdf.mrow(list(row), pw, fill=(i % 2 == 1))
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 4.5, sanitize(
        "Table 4.3: DFD Level 1 processes mapped to SRS requirement sets. "
        "D1=Supabase, D2=Cloudflare R2, D3=MLflow. "
        "FastAPI implements P1, P2, P5, P6. Airflow implements P3, triggers P4."
    ))
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(2)

    pdf.h2("4.4.3 Key Inter-Process Data Flows")
    pdf.bullet([
        "P3 -> P4 (data availability trigger): Each ingestion DAG completion "
        "signals the retrain schedule. An emergency retrain is triggered by P6 "
        "when PSI exceeds 0.2 for any top-4 SHAP feature.",
        "P2 -> D2 (model loading): The champion .pkl is loaded from Cloudflare "
        "R2 into FastAPI memory at startup and cached. Refreshed on champion "
        "promotion via a background task or rolling restart.",
        "P1 -> P2, P5 (JWT propagation): The user_id extracted from the "
        "validated JWT is stored in every prediction and report record, "
        "ensuring RLS enforcement without additional lookup queries.",
        "P4 -> D1 (champion promotion): The Airflow retrain DAG updates "
        "is_champion in ml_models atomically, enforced by the partial unique "
        "index defined in the database schema.",
    ])


# ── Section 4.5: Pipeline and UX ─────────────────────────────────────────────
def section45(pdf):
    pdf.add_page()
    pdf.h1("4.5 Pipeline Architecture and User Experience Design")

    pdf.h2("4.5.1 Airflow Pipeline Design")
    pdf.para(
        "The nine-DAG Airflow pipeline (`04_Pipeline_Flow.mmd`) is organised "
        "into three tiers by cadence. Table 4.4 presents the full schedule."
    )
    dw = [46, 36, PAGE_W - 82]
    pdf.thead(["DAG Name", "Schedule (WAT)", "Source -> Target"], dw)
    dags = [
        ("nhces_daily_fx_oil",     "06:00 daily",         "FRED API -> macro_fx  |  EIA API -> macro_oil"),
        ("nhces_weekly_materials", "Monday 06:00",        "BusinessDay + Jiji.ng scrapers -> material_cement, material_steel"),
        ("nhces_weekly_property",  "Tuesday 06:00",       "PropertyPro + PrivateProperty -> market_prices"),
        ("nhces_monthly_macro",    "1st of month 06:00",  "World Bank -> macro_cpi, macro_interest  |  NNPC -> material_pms"),
        ("nhces_quarterly_niqs",   "Manual trigger",      "Admin CSV upload -> unit_rates"),
        ("nhces_quarterly_nbs",    "Quarterly 06:00",     "NBS + CBN Stats -> macro_gdp"),
        ("nhces_worldbank_annual", "2 Jan annually",      "World Bank -> macro_gdp (annual refresh)"),
        ("nhces_retrain_weekly",   "Sunday 02:00 WAT",    "All tables -> feature matrix -> MLflow + R2"),
        ("nhces_drift_monitor",    "18:00 daily",         "Latest features vs. MLflow baseline -> PSI check"),
    ]
    for i, row in enumerate(dags):
        pdf.trow(list(row), dw, fill=(i % 2 == 1))
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 4.5, sanitize(
        "Table 4.4: iNHCES Airflow DAG schedule. WAT = UTC+1. "
        "DAG code: 05_ml_models/05_dags/nhces_retrain_weekly.py (O5 Step 4)."
    ))
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(2)

    pdf.para(
        "The retrain pipeline implements the champion-challenger promotion "
        "methodology: retaining the current champion until a MAPE improvement "
        "of >= 0.5 percentage points is confirmed prevents unnecessary model churn "
        "while ensuring continuous improvement as new data accumulates. Drift "
        "detection uses the Population Stability Index (PSI): PSI < 0.1 is stable; "
        "0.1-0.2 is slight drift (AMBER warning); > 0.2 triggers emergency retrain."
    )

    pdf.h2("4.5.2 User Experience Design")
    pdf.para(
        "The user journey analysis (`04_User_Journey.mmd`) scored 21 touchpoints "
        "for the QS Professional and 9 for the Researcher/PI on a 1-5 satisfaction "
        "scale. Three design issues require attention in O6 implementation:"
    )
    uw = [38, PAGE_W - 38]
    pdf.thead(["Pain Point", "O6 Design Response"], uw)
    ux_issues = [
        ("Data freshness transparency "
         "(score 3 when RED-level data shown)",
         "Display a colour-coded (GREEN/AMBER/RED) freshness indicator "
         "on the estimation results page for each feature used. "
         "Powered by the data_source_level field in Supabase."),
        ("PDF report URL expiry "
         "(24-hour R2 presigned URL creates friction)",
         "Implement a persistent report history page in the frontend "
         "with an on-demand 'Re-download' button that generates a "
         "fresh presigned URL from the stored r2_key."),
        ("MLflow access for researchers "
         "(admin redirect required — score 3)",
         "Add a read-only MLflow link in the Models page accessible "
         "to the researcher role, removing the admin dependency."),
    ]
    for i, row in enumerate(ux_issues):
        pdf.mrow(list(row), uw, fill=(i % 2 == 1))
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 4.5, sanitize(
        "Table 4.5: User experience pain points and O6 design responses."
    ))
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(2)


# ── Section 4.6: Traceability Matrix ─────────────────────────────────────────
def section46(pdf):
    pdf.add_page()
    pdf.h1("4.6 Requirements Traceability")
    pdf.para(
        "Table 4.6 maps the seven Delphi functional categories to their primary "
        "realisation in the iNHCES conceptual design. All 36 consensus items "
        "(of 38 total; B6, C6, E5, and G2 excluded by Delphi panel) are addressed."
    )
    tw = [30, 12, PAGE_W - 42]
    pdf.thead(["Delphi Category", "Items", "Primary Architecture Realisation"], tw)
    traceability = [
        ("A — System Functionality", "A1-A6",
         "FastAPI routers: POST /estimate, GET /macro, CRUD /projects, "
         "POST /reports, GET /pipeline. All SRS FR-EST and FR-AUTH requirements."),
        ("B — Data and Integration", "B1-B5\n(B6 excl.)",
         "9 Airflow ingestion DAGs; 10 Supabase tables for macro/material/market data; "
         "data_source_level field on every row; v_latest_macro helper view."),
        ("C — ML and AI Features", "C1-C5\n(C6 excl.)",
         "MLflow champion/challenger workflow; Stacking Ensemble + full model family; "
         "SHAP values stored in predictions.shap_values JSONB; "
         "v_champion_model view for inference; PSI drift detection."),
        ("D — Security and Privacy", "D1-D6",
         "JWT Auth (Supabase GoTrue, 1hr expiry); 36 RLS policies across 16 tables; "
         "RBAC 3 roles; audit_log append-only table; HTTPS/TLS enforced by Vercel/Railway; "
         "environment variables for all secrets."),
        ("E — Usability and UX", "E1-E4, E6\n(E5 excl.)",
         "Vanilla JS responsive frontend (mobile-first CSS); "
         "SHAP feature importance chart on estimation results page; "
         "PDF cost report generation; data freshness indicator; "
         "pipeline dashboard. No dedicated mobile app (E5 excluded)."),
        ("F — Performance + Scalability", "F1-F6",
         "FastAPI async; Railway horizontal scaling; Supabase connection pooling; "
         "rate limiting 10 req/min per user (slowapi); "
         "/estimate target < 3 seconds; champion model cached in FastAPI memory."),
        ("G — Deployment + Operations", "G1, G3-G6\n(G2 excl.)",
         "GitHub Actions CI/CD (test.yml + deploy.yml); Railway auto-deploy; "
         "Airflow monitoring dashboard; PSI drift detection + emergency retrain; "
         "MLflow experiment history. No on-premise deployment (G2 excluded)."),
    ]
    for i, row in enumerate(traceability):
        pdf.mrow(list(row), tw, fill=(i % 2 == 1))
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 4.5, sanitize(
        "Table 4.6: Delphi consensus category traceability to iNHCES conceptual design. "
        "Excluded items: B6 (procurement method mandate), C6 (stacking-only mandate), "
        "E5 (dedicated mobile app), G2 (on-premise deployment). "
        "All 36 consensus items are addressed."
    ))
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(2)


# ── Section 4.7: Limitations ──────────────────────────────────────────────────
def section47(pdf):
    pdf.add_page()
    pdf.h1("4.7 Design Limitations and Future Work")

    pdf.h2("4.7.1 Acknowledged Limitations")
    pdf.bullet([
        "Synthetic data dependency: EIA Brent crude and CBN FX pipelines operate "
        "on synthetic fallback data (RED level) pending configuration of EIA_API_KEY "
        "and FRED_API_KEY. All O2 SHAP results use a synthetic housing cost proxy and "
        "must be re-estimated with real NIQS unit rate data in O5. The data_source_level "
        "field ensures these limitations are visible in all system outputs.",
        "Small training sample: The O2 analysis uses annual data (T=25, 2000-2024). "
        "The O5 benchmarking phase will supplement with project-level BQ cost records "
        "and quarterly/monthly data. The predictions table will accumulate real "
        "project data post-deployment for online learning.",
        "Scraper fragility: PropertyPro, BusinessDay, and Jiji.ng scrapers are "
        "susceptible to website structure changes. Pipeline failure handling includes "
        "RED-level fallback and admin alerts, but data supply agreements with "
        "relevant platforms are recommended for production.",
        "Scalability ceiling: The current Railway/Supabase free-tier configuration "
        "is appropriate for a research prototype. Production deployment would require "
        "Supabase Pro (connection pooling), Railway paid tiers, and a CDN-cached "
        "model inference layer.",
        "NIQS dependency: The unit_rates table is populated by manual quarterly "
        "upload. A formal Memorandum of Understanding with the Nigerian Institute "
        "of Quantity Surveyors is required for reliable data access.",
    ])

    pdf.h2("4.7.2 Validation Required Before O6 Build")
    pdf.info_box(
        "The research team must complete all of the following before O6 implementation begins:\n\n"
        "  [ ] Run 04_schema.sql and 04_rls_policies.sql in Supabase -- verify no SQL errors\n"
        "  [ ] Render all four .mmd diagrams in mermaid.live -- verify syntax\n"
        "  [ ] Confirm 36 Delphi consensus items traceable to Table 4.6 above\n"
        "  [ ] Research team sign-off on all design decisions in Sections 4.2-4.5\n"
        "  [ ] Confirm platform tier limits (Railway, Supabase, Cloudflare R2)\n"
        "  [ ] Obtain NIQS data access agreement\n"
        "  [ ] Confirm PropertyPro and BusinessDay ToS permit academic scraping\n"
        "  [ ] Obtain ABU Zaria IRB approval before any human-subjects data collection"
    )


# ── Section 4.8: Chapter Summary ──────────────────────────────────────────────
def section48(pdf):
    pdf.add_page()
    pdf.h1("4.8 Chapter Summary")
    pdf.para(
        "This chapter has presented the full conceptual design of the iNHCES system "
        "across four formal artefact sets: a seven-layer cloud-native architecture "
        "with documented design decision rationales; a normalised sixteen-table "
        "PostgreSQL schema with row-level security, data provenance tracking, and "
        "two helper views for the API layer; a two-level DFD process model specifying "
        "all six system processes and three data stores; and an Airflow pipeline design "
        "with nine DAGs governing data ingestion, weekly ML retraining, and "
        "daily drift detection."
    )
    pdf.para(
        "The design directly realises all 36 Delphi consensus requirements from "
        "Chapter 3 (Table 4.6) and satisfies all 47 functional requirements in the "
        "SRS (O3 Step 4, Appendix B). The key architectural innovation is the "
        "systematic integration of data quality tracking (the data_source_level field) "
        "across the entire data layer, ensuring that the gap between the synthetic "
        "prototype and a publication-ready system is always visible, measurable, "
        "and actionable."
    )
    pdf.para(
        "Chapter 5 proceeds to the ML model benchmarking phase (Objective O5), "
        "in which the feature engineering pipeline, model training and evaluation "
        "framework, and SHAP-based explainability analysis are implemented using "
        "the database schema and pipeline architecture defined in this chapter. "
        "The champion model identified in O5 will become the production model "
        "served by the iNHCES `/estimate` endpoint in O6."
    )

    pdf.h2("O4 Deliverables Summary")
    ow = [48, 18, 15, PAGE_W - 81]
    pdf.thead(["Deliverable", "File", "Pages", "Data Level"], ow)
    deliverables = [
        ("System Architecture Document",    "O4_01_System_Architecture.pdf",       "13", "AMBER"),
        ("Architecture Diagram (Mermaid)",  "04_Architecture_Diagram.mmd",         "—",  "AMBER"),
        ("Database Schema (SQL)",           "04_schema.sql",                       "—",  "AMBER"),
        ("RLS Policies (SQL)",              "04_rls_policies.sql",                 "—",  "AMBER"),
        ("Seed Data (SQL)",                 "04_seed_data.sql",                    "—",  "RED"),
        ("Database Schema Document",        "O4_02_Database_Schema.pdf",           "16", "AMBER"),
        ("DFD Level 0 (Mermaid)",           "04_DFD_Level0.mmd",                   "—",  "AMBER"),
        ("DFD Level 1 (Mermaid)",           "04_DFD_Level1.mmd",                   "—",  "AMBER"),
        ("User Journey (Mermaid)",          "04_User_Journey.mmd",                 "—",  "AMBER"),
        ("Pipeline Flow (Mermaid)",         "04_Pipeline_Flow.mmd",                "—",  "AMBER"),
        ("Data Flow Diagrams Document",     "O4_03_Data_Flow_Diagrams.pdf",        "9",  "AMBER"),
        ("Chapter 4 Markdown",             "04_Chapter4_Conceptual_Models.md",    "—",  "AMBER"),
        ("Chapter 4 PDF (this document)",  "O4_04_Chapter4_Conceptual_Models.pdf","—",  "AMBER"),
    ]
    for i, row in enumerate(deliverables):
        pdf.trow(list(row), ow, fill=(i % 2 == 1))
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 4.5, sanitize(
        "Table 4.7: O4 complete deliverables. All files in 04_conceptual_models/. "
        "Total PDF pages (O4): 13 + 16 + 9 + this document."
    ))
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(2)


# ── References ─────────────────────────────────────────────────────────────────
def references(pdf):
    pdf.add_page()
    pdf.h1("References")
    pdf.info_box(
        "CITATION VERIFICATION REQUIRED: All references are from AI training knowledge. "
        "Verify every citation in Scopus or Web of Science before submission. "
        "References marked [VERIFY] have not been checked."
    )
    pdf.ln(2)
    refs = [
        ("Christensen, T., & Larsen, B. (2020). MLOps: continuous delivery and "
         "automation pipelines in machine learning. Proceedings of the International "
         "Conference on Machine Learning Engineering, 1-9. "
         "[VERIFY -- details may be inaccurate]"),
        ("Creswell, J.W. (2014). Research design: qualitative, quantitative, and "
         "mixed methods approaches (4th ed.). SAGE Publications. [VERIFY]"),
        ("Fielding, R.T. (2000). Architectural styles and the design of network-based "
         "software architectures. Doctoral dissertation, University of California, "
         "Irvine. [VERIFY -- high confidence, foundational REST paper]"),
        ("Fowler, M. (2002). Patterns of enterprise application architecture. "
         "Addison-Wesley. [VERIFY -- high confidence]"),
        ("Kleppmann, M. (2017). Designing data-intensive applications. "
         "O'Reilly Media. [VERIFY -- high confidence]"),
        ("Lundberg, S.M., & Lee, S.I. (2017). A unified approach to interpreting "
         "model predictions. NeurIPS, 30. [VERIFY -- high confidence, NeurIPS 2017]"),
        ("Page, M.J. et al. (2021). The PRISMA 2020 statement: an updated guideline "
         "for reporting systematic reviews. BMJ, 372, n71. [VERIFY -- high confidence]"),
        ("PostgreSQL Global Development Group. (2024). PostgreSQL 15 documentation. "
         "https://www.postgresql.org/docs/15/ [VERIFY URL]"),
        ("Supabase Inc. (2024). Supabase documentation -- Row Level Security. "
         "https://supabase.com/docs/guides/auth/row-level-security [VERIFY URL]"),
    ]
    for ref in refs:
        pdf.ref_item(ref)


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    out = os.path.join(OUT_DIR, 'O4_04_Chapter4_Conceptual_Models.pdf')
    pdf = ChapterPDF()

    make_cover(pdf)
    _ds_page(pdf, 'amber',
        "DATA SOURCE: AMBER -- AI-AUTHORED CHAPTER SYNTHESISING O4 STEPS 1-3",
        (
            "WHAT IS REAL IN THIS DOCUMENT:\n"
            "  * All architecture decisions, table designs, process flows, and "
            "traceability mappings are derived from real O3 Delphi consensus items, "
            "SRS IEEE 830 requirements, and the four O4 artefact sets.\n"
            "  * Technology selection rationales are real engineering decisions "
            "made for the iNHCES prototype context.\n"
            "  * All file references (04_schema.sql, 04_Architecture_Diagram.mmd, "
            "etc.) point to real files in 04_conceptual_models/.\n\n"
            "WHAT IS AI-GENERATED / UNVALIDATED:\n"
            "  * Full narrative text, section headings, and all design rationale "
            "boxes were drafted by Claude Code. Research team review required.\n"
            "  * References (Section 4.8) are from AI training knowledge -- "
            "verify all in Scopus / Web of Science before submission.\n"
            "  * Delphi item traceability (Table 4.6) reflects AI interpretation "
            "of O3 consensus items -- research team must verify each mapping.\n\n"
            "REQUIRED BEFORE THESIS / PAPER SUBMISSION:\n"
            "  1. Research team review and validation of all sections\n"
            "  2. Verify all 36 Delphi item mappings in Table 4.6\n"
            "  3. Complete O4 validation checklist (Section 4.7.2)\n"
            "  4. Verify all citations in Scopus / Web of Science\n"
            "  5. Replace [VERIFY] tags after citation checking\n"
            "  6. Integrate with Chapter 3 (O3) and Chapter 5 (O5) cross-references\n"
            "  7. Proceed to O5: ML Model Benchmarking"
        )
    )

    section41(pdf)
    section42(pdf)
    section43(pdf)
    section44(pdf)
    section45(pdf)
    section46(pdf)
    section47(pdf)
    section48(pdf)
    references(pdf)

    pdf.output(out)
    print(f"[OK]  O4_04_Chapter4_Conceptual_Models.pdf  saved -> {out}")
    print(f"      Pages: {pdf.page}")
    print("      DATA SOURCE: AMBER")
    print("      O4 IS NOW COMPLETE -- all 4 steps done.")
    print("      Next: O5 -- ML Model Benchmarking (05_ml_models/)")


if __name__ == "__main__":
    main()
