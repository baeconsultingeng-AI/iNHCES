"""
iNHCES O4 Step 1 — System Architecture Document Generator
Deliverable: O4_01_System_Architecture.pdf
DATA SOURCE: AMBER — AI-authored conceptual design based on O3 SRS IEEE 830
             and iNHCES Research Advisory Framework. No real deployment data.
             Architecture must be validated by the research team before O6 build.

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
DOC_ID  = "O4-01"
DOC_TITLE = "iNHCES System Architecture Document"
DOC_SUBTITLE = "Conceptual Design — All Seven Layers"


# ── Document PDF class ─────────────────────────────────────────────────────────
class ArchPDF(DocPDF):
    def __init__(self):
        super().__init__(DOC_TITLE, DOC_ID)

    def header(self):
        self.set_fill_color(*DARK_NAVY)
        self.rect(0, 0, 210, 14, 'F')
        self.set_font("Helvetica", "B", 7)
        self.set_text_color(*WHITE)
        self.set_xy(5, 4)
        self.cell(PAGE_W, 6, sanitize(
            "iNHCES  |  TETFund NRF 2025  |  Dept. of Quantity Surveying, ABU Zaria"
            "  |  O4 Step 1 — System Architecture"
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
            f"{DOC_TITLE}  |  ABU Zaria / TETFund NRF 2025  |  Page {self.page_no()}"
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

    def h3(self, text):
        self.ln(1)
        self.set_font("Helvetica", "BI", 9)
        self.set_text_color(*DARK_GREY)
        self.set_x(LEFT)
        self.multi_cell(PAGE_W, 5.2, sanitize(text))
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

    def layer_box(self, layer_name, colour, items):
        """Coloured layer summary box."""
        self.ln(2)
        self.set_fill_color(*colour)
        self.set_draw_color(*GOLD)
        self.set_line_width(0.5)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*WHITE)
        self.set_x(LEFT)
        self.cell(PAGE_W, 7, sanitize(f"  {layer_name}"), border=1, fill=True, ln=True)
        self.set_fill_color(245, 248, 255)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*DARK_GREY)
        for item in items:
            self.set_x(LEFT + 4)
            self.cell(4, 5.2, "-")
            self.set_x(LEFT + 8)
            self.multi_cell(PAGE_W - 8, 5.2, sanitize(item), border="LR", fill=True)
        # Bottom border line
        self.set_x(LEFT)
        self.cell(PAGE_W, 0, "", border="B")
        self.ln(2)
        self.set_text_color(*DARK_GREY)

    def decision_box(self, title, text):
        self.ln(2)
        self.set_fill_color(255, 243, 220)
        self.set_draw_color(180, 100, 0)
        self.set_line_width(0.5)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(120, 60, 0)
        self.set_x(LEFT)
        self.cell(PAGE_W, 6, sanitize(f"  DESIGN DECISION:  {title}"), border=1, fill=True, ln=True)
        self.set_font("Helvetica", "", 9)
        self.set_fill_color(255, 250, 235)
        self.set_x(LEFT)
        self.multi_cell(PAGE_W, 5, sanitize(text), border="LBR", fill=True)
        self.set_text_color(*DARK_GREY)
        self.ln(2)


# ── Cover page ─────────────────────────────────────────────────────────────────
def make_cover(pdf):
    pdf.add_page()
    pdf.set_fill_color(*DARK_NAVY)
    pdf.rect(0, 18, 210, 55, 'F')
    pdf.set_xy(0, 26)
    pdf.set_font("Helvetica", "B", 15)
    pdf.set_text_color(*WHITE)
    pdf.cell(210, 9, sanitize(DOC_TITLE), align="C", ln=True)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(200, 215, 235)
    pdf.cell(210, 7, sanitize(DOC_SUBTITLE), align="C", ln=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*LIGHT_BLUE)
    pdf.cell(210, 6, "Intelligent National Housing Cost Estimating System (iNHCES)", align="C", ln=True)
    pdf.cell(210, 6, "TETFund NRF 2025  |  Department of Quantity Surveying, ABU Zaria", align="C", ln=True)
    pdf.set_draw_color(*GOLD)
    pdf.set_line_width(0.8)
    pdf.line(30, 76, 180, 76)
    pdf.set_xy(LEFT, 84)
    pdf.set_text_color(*DARK_GREY)
    meta = [
        ("Objective:",     "O4 — Develop Conceptual Models for the iNHCES System"),
        ("Step:",          "1 — System Architecture Document"),
        ("Document ID:",   DOC_ID),
        ("Version:",       "1.0 — Initial AI-Assisted Draft"),
        ("Date:",          date.today().strftime("%d %B %Y")),
        ("Grant:",         "TETFund National Research Fund (NRF) 2025"),
        ("Feeds into:",    "P4 (Scientific Data), P7 (Automation in Construction)"),
        ("Next Step:",     "O4 Step 2 — Database Schema (04_schema.sql)"),
    ]
    for label, val in meta:
        pdf.set_x(LEFT)
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*DARK_NAVY)
        pdf.cell(40, 6.5, sanitize(label))
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*DARK_GREY)
        pdf.cell(PAGE_W - 40, 6.5, sanitize(val), ln=True)


# ── Section 1: Overview ────────────────────────────────────────────────────────
def section1(pdf):
    pdf.add_page()
    pdf.h1("1. Architecture Overview")
    pdf.para(
        "The iNHCES system is a web-based AI cost estimation platform for Nigerian "
        "housing construction. It ingests live macroeconomic and material price data, "
        "applies a trained machine learning ensemble model to predict housing "
        "construction cost per square metre (NGN/sqm), and delivers results via "
        "a REST API to a browser-based frontend. The architecture follows a "
        "seven-layer design that separates concerns across User, Presentation, "
        "API, ML, Data, Storage, and Pipeline layers."
    )
    pdf.para(
        "The architecture is derived from: (1) the Delphi consensus requirements "
        "(O3 — 36 consensus items across 7 functional categories); (2) the iNHCES "
        "Research Advisory Framework (Sections 7-8); and (3) standard cloud-native "
        "MLOps design patterns. All hosting decisions prioritise platforms with "
        "free or low-cost tiers suitable for an academic research prototype."
    )

    pdf.h2("1.1 Architecture Summary Table")
    sw = [38, 38, PAGE_W - 76]
    pdf.thead(["Layer", "Technology / Platform", "Primary Responsibility"], sw)
    layers = [
        ("1. User Layer",         "Browser (any)",             "End-user access via HTTPS"),
        ("2. Presentation Layer", "Vanilla HTML/CSS/JS — Vercel CDN", "UI: estimation form, pipeline dashboard"),
        ("3. API Layer",          "FastAPI (Python 3.10+) — Railway", "Business logic, auth, routing, PDF generation"),
        ("4. ML Layer",           "MLflow Model Registry — Railway",  "Champion model serving, experiment tracking, retrain orchestration"),
        ("5. Data Layer",         "Supabase PostgreSQL",        "All persistent data: macro, materials, projects, predictions, models, users"),
        ("6. Storage Layer",      "Cloudflare R2 (S3-compatible)", "PDF reports, model .pkl artifacts, training dataset CSVs"),
        ("7. Pipeline Layer",     "Apache Airflow — Railway",   "9 DAGs for data ingestion, weekly ML retrain, daily drift monitoring"),
    ]
    for i, (layer, tech, resp) in enumerate(layers):
        pdf.mrow([layer, tech, resp], sw, fill=(i % 2 == 1))
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 4.5, sanitize(
        "Table 1: iNHCES seven-layer architecture summary."
    ))
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(2)

    pdf.h2("1.2 Architecture Diagram Reference")
    pdf.info_box(
        "The full system architecture is defined in Mermaid diagram format:\n"
        "  File: 04_conceptual_models/04_Architecture_Diagram.mmd\n"
        "  Render at: mermaid.live  OR  VS Code Mermaid Preview extension\n"
        "  The diagram shows all seven layers, component names, and directed "
        "data flow connections between every component pair."
    )
    pdf.para(
        "The Mermaid diagram is the single authoritative visual representation "
        "of the iNHCES architecture. All narrative descriptions in this document "
        "must remain consistent with it. When the architecture is updated during "
        "O6 implementation, update both this document and "
        "04_Architecture_Diagram.mmd."
    )


# ── Section 2: Layer Descriptions ─────────────────────────────────────────────
def section2(pdf):
    pdf.add_page()
    pdf.h1("2. Layer-by-Layer Description")

    # Layer 1: Users
    pdf.layer_box("LAYER 1 — USER LAYER", DARK_NAVY, [
        "QS Professional: primary end-user; submits cost estimation requests via "
        "the frontend form; downloads PDF cost reports.",
        "Researcher / PI: accesses macro data feeds, project records, and pipeline "
        "monitoring dashboard; reviews model performance metrics.",
        "System Admin: manages user accounts, triggers manual pipeline runs "
        "(e.g., NIQS quarterly upload), promotes challenger models to champion.",
    ])

    # Layer 2: Presentation
    pdf.layer_box("LAYER 2 — PRESENTATION LAYER (Vercel CDN)", (30, 100, 180), [
        "index.html: Cost estimator form — inputs: building type, floor area (sqm), "
        "location (state/zone), construction type, date; outputs: estimated cost, "
        "cost range (±%), SHAP feature importance chart.",
        "dashboard.html: Pipeline monitoring — shows Airflow DAG last run status, "
        "data freshness per source, champion model MAPE, recent predictions log.",
        "app.js: Shared JavaScript — API call handler, form validation, "
        "chart rendering (Chart.js), PDF download trigger.",
        "styles.css: Responsive layout (mobile-first), ABU Zaria brand colours.",
        "vercel.json: Deploy config — redirects /api/* to Railway backend URL, "
        "sets cache headers for static assets.",
        "Deployment: Auto-deploy from GitHub main branch via Vercel GitHub integration. "
        "No server-side rendering — pure static site calling the FastAPI backend.",
    ])

    # Layer 3: API
    pdf.layer_box("LAYER 3 — API LAYER (FastAPI on Railway)", (20, 80, 150), [
        "POST /estimate: Receives building parameters, fetches latest macro/material "
        "features from Supabase, calls champion ML model, returns predicted "
        "cost_per_sqm + confidence interval + SHAP values. Logs prediction to DB.",
        "GET /macro: Returns latest macroeconomic indicators (FX rates, CPI, GDP, "
        "Brent crude) from Supabase macro_* tables. Used by frontend dashboard.",
        "CRUD /projects: Create/read/update/delete project records (building type, "
        "area, location, BQ summary, target cost). RLS-enforced per user.",
        "POST /reports: Generates a PDF cost report for a project using fpdf2, "
        "uploads to Cloudflare R2, returns presigned download URL.",
        "GET /pipeline: Returns Airflow DAG status via Airflow REST API — last run "
        "time, success/failure, next scheduled run.",
        "JWT Auth Middleware: All endpoints protected. Tokens issued by Supabase Auth "
        "(GoTrue). Roles: qsprofessional / researcher / admin.",
        "main.py: FastAPI app entry point. database.py: Supabase async client. "
        "requirements.txt + Dockerfile + railway.toml: deployment config.",
    ])

    # Layer 4: ML
    pdf.add_page()
    pdf.layer_box("LAYER 4 — ML LAYER (MLflow on Railway)", (15, 60, 120), [
        "Champion Model: Stacking Ensemble — XGBoost + LightGBM + Random Forest "
        "base learners with Ridge regression meta-learner. Predicts cost_per_sqm (NGN).",
        "Model Registry: MLflow Model Registry tracks all model versions with "
        "stage labels (Staging / Production / Archived). Champion = Production stage.",
        "Experiment Tracker: Every training run logged with: hyperparameters, "
        "train/val/test MAPE and R2, feature importance, confusion matrix for "
        "cost bracket classification.",
        "Challenger Models: Ridge/Lasso (baseline), Random Forest, XGBoost, "
        "LightGBM, MLP (256->128->64), SVR. All benchmarked in O5.",
        "Champion Promotion: nhces_retrain_weekly DAG retrains challenger and "
        "compares to production MAPE. If challenger MAPE < (production MAPE - 0.5%), "
        "auto-promotes to Staging for human review before Production.",
        "Inference: FastAPI /estimate loads champion model artifact from "
        "Cloudflare R2 (cached in memory), runs predict() with engineered features.",
        "Performance Targets: MAPE <= 15% | R2 >= 0.90 | /estimate response < 3 sec.",
    ])

    # Layer 5: Data
    pdf.layer_box("LAYER 5 — DATA LAYER (Supabase PostgreSQL)", (10, 50, 100), [
        "macro_fx: NGN/USD, NGN/EUR, NGN/GBP exchange rates. Daily frequency. "
        "Source: CBN/FRED API (nhces_daily_fx_oil DAG).",
        "macro_cpi / macro_gdp / macro_interest / macro_oil: CPI inflation, "
        "GDP growth, lending rate, Brent crude. Monthly/annual. "
        "Sources: World Bank API, EIA API, CBN.",
        "material_cement / material_steel / material_pms: Cement price by brand "
        "and region; iron rod price by diameter and region; petrol (PMS) price "
        "by state. Weekly/monthly. Sources: scrapers + NNPC.",
        "unit_rates: NIQS quarterly unit rates by trade, region, and building type. "
        "Quarterly. Source: manual CSV upload.",
        "market_prices: Property listing prices (NGN/sqm) by zone and property type. "
        "Weekly. Source: PropertyPro + Private Property scrapers.",
        "projects: Researcher/professional project records. Columns: project_id, "
        "user_id, building_type, floor_area_sqm, location_state, location_zone, "
        "construction_type, target_cost, created_at.",
        "predictions: Log of every /estimate call. Columns: prediction_id, "
        "project_id, predicted_cost_per_sqm, confidence_lower, confidence_upper, "
        "model_version, shap_values (JSONB), timestamp.",
        "ml_models: Champion/challenger model registry metadata (mirrors MLflow).",
        "users / audit_log: Supabase Auth user records + row-level audit trail.",
        "Row Level Security (RLS): All tables enforce user-scoped access. "
        "Defined in 04_rls_policies.sql (O4 Step 2).",
    ])

    # Layer 6: Storage
    pdf.layer_box("LAYER 6 — STORAGE LAYER (Cloudflare R2)", (8, 40, 80), [
        "PDF Reports: One PDF per project per estimation run. "
        "Path pattern: reports/{user_id}/{project_id}/{timestamp}.pdf. "
        "Served via presigned R2 URL (24-hour expiry).",
        "Model Artifacts: Champion and challenger .pkl files (scikit-learn pipeline "
        "objects). Path: models/{mlflow_run_id}/model.pkl. "
        "FastAPI loads champion at startup and caches in memory.",
        "Training Datasets: Versioned CSV snapshots of the full feature matrix "
        "used in each weekly retrain. Path: datasets/{date}/train.csv. "
        "Retained for 12 months for reproducibility.",
        "R2 is S3-compatible — accessed via boto3 with Cloudflare R2 endpoint "
        "in nhces-backend/app/services/r2_storage.py.",
    ])

    # Layer 7: Pipeline
    pdf.add_page()
    pdf.layer_box("LAYER 7 — PIPELINE LAYER (Apache Airflow on Railway)", (5, 30, 60), [
        "nhces_daily_fx_oil @ 06:00 WAT: Fetches NGN/USD, NGN/EUR, NGN/GBP "
        "from FRED API and Brent crude from EIA API. Inserts into macro_fx "
        "and macro_oil tables.",
        "nhces_weekly_materials @ Monday: Scrapes cement prices "
        "(BusinessDay, DangoteCement.com) and iron rod prices (Jiji.ng, BuildBay) "
        "by brand and region. Inserts into material_cement and material_steel.",
        "nhces_weekly_property @ Tuesday: Scrapes property listing prices from "
        "PropertyPro.ng and PrivateProperty.com.ng. Inserts into market_prices.",
        "nhces_monthly_macro @ 1st of month: Fetches CPI, GDP growth, lending rate "
        "from CBN Statistics DB and World Bank API. Inserts into macro_cpi, "
        "macro_gdp, macro_interest.",
        "nhces_quarterly_niqs @ manual trigger: Processes manually uploaded NIQS "
        "unit rate CSV. Validates schema, inserts into unit_rates.",
        "nhces_worldbank_annual @ January: Annual World Bank data refresh — "
        "GDP per capita, household income. Inserts into macro_gdp.",
        "nhces_retrain_weekly @ Sunday: Assembles feature matrix from all macro/"
        "material/property tables, trains challenger models, logs to MLflow, "
        "compares to champion MAPE, promotes if threshold met.",
        "nhces_drift_monitor @ 18:00 WAT daily: Calculates Population Stability Index "
        "(PSI) for each feature against training baseline. If PSI > 0.2 for any "
        "key feature, triggers emergency retrain and sends alert.",
        "All DAG code in: 05_ml_models/05_dags/nhces_retrain_weekly.py (O5 Step 4).",
    ])


# ── Section 3: Design Decisions ───────────────────────────────────────────────
def section3(pdf):
    pdf.add_page()
    pdf.h1("3. Key Architecture Design Decisions")

    pdf.decision_box(
        "Vanilla JS Frontend (not React/Vue)",
        "Rationale: iNHCES is an academic research prototype with a limited "
        "number of UI screens (estimation form + pipeline dashboard). "
        "A JavaScript framework would add build tooling complexity and dependency "
        "management overhead with no user-facing benefit at this scale. "
        "Vanilla JS with a single app.js is sufficient, fully auditable by "
        "non-frontend researchers, and deployable to Vercel with zero configuration. "
        "Revisit for production scale-out post-publication."
    )

    pdf.decision_box(
        "FastAPI over Django/Flask",
        "Rationale: FastAPI provides automatic OpenAPI/Swagger documentation "
        "(critical for academic transparency and API testing), native async support "
        "(important for concurrent Supabase + MLflow + R2 calls in /estimate), "
        "and Pydantic-based request/response validation aligned with the typed "
        "feature schema from O4 Step 2. Startup time on Railway cold-start is "
        "<500ms vs Django's ~2 seconds, keeping /estimate < 3 second target feasible."
    )

    pdf.decision_box(
        "Supabase PostgreSQL over MongoDB/Firebase",
        "Rationale: The iNHCES data is fundamentally relational — time-series "
        "macro data with foreign keys to predictions, projects, and model records. "
        "Supabase provides PostgreSQL (full SQL, JOINs, window functions for "
        "time-series analysis) plus built-in Row Level Security, GoTrue Auth "
        "(JWT), and a Python client. This eliminates the need for a separate "
        "auth service. The free tier (500 MB, unlimited API calls) is adequate "
        "for the research prototype phase."
    )

    pdf.decision_box(
        "MLflow over SageMaker/Vertex AI",
        "Rationale: MLflow is open-source, self-hostable on Railway, and "
        "integrates natively with scikit-learn, XGBoost, and LightGBM — the "
        "exact model family used in iNHCES. Cloud ML platforms (SageMaker, "
        "Vertex) are cost-prohibitive for a TETFund academic project and "
        "introduce vendor lock-in. MLflow's Model Registry provides the "
        "champion/challenger promotion workflow required by the O5 retrain DAG."
    )

    pdf.decision_box(
        "Cloudflare R2 over AWS S3",
        "Rationale: R2 has zero egress fees (S3 charges ~$0.09/GB egress). "
        "For a research prototype generating PDF reports and serving model "
        "artifacts, egress cost is the dominant storage cost driver. "
        "R2 is S3-API-compatible, so boto3 code requires only an endpoint URL "
        "change to migrate to S3 if needed post-publication."
    )

    pdf.decision_box(
        "Apache Airflow over Prefect/Dagster",
        "Rationale: Airflow is the industry-standard orchestrator with the "
        "largest community, most mature sensor/operator library, and direct "
        "Railway deployment support. The iNHCES DAG schedule (9 DAGs at "
        "daily/weekly/monthly/annual cadences) maps naturally to Airflow's "
        "cron-based scheduler. The nhces_drift_monitor DAG requires a sensor "
        "that monitors a database condition — Airflow's SqlSensor handles this "
        "natively."
    )


# ── Section 4: Security Architecture ──────────────────────────────────────────
def section4(pdf):
    pdf.add_page()
    pdf.h1("4. Security Architecture")

    pdf.h2("4.1 Authentication and Authorisation")
    pdf.para(
        "iNHCES uses Supabase Auth (GoTrue) for authentication. Users register "
        "and log in via the frontend; Supabase issues a JWT access token (1-hour "
        "expiry) and a refresh token (7-day expiry). The JWT is included in all "
        "API requests as a Bearer token in the Authorization header. FastAPI's "
        "JWT Auth Middleware validates the token signature against the Supabase "
        "JWT secret on every request."
    )
    rw = [35, PAGE_W - 35]
    pdf.thead(["Role", "Permissions"], rw)
    roles = [
        ("qsprofessional",
         "POST /estimate; GET /macro; CRUD own /projects; POST /reports for own projects. "
         "Cannot access other users' data (RLS enforced at DB level)."),
        ("researcher",
         "All qsprofessional permissions + read all projects (anonymised) for "
         "research analysis + GET /pipeline status."),
        ("admin",
         "All researcher permissions + manage users + trigger manual pipeline "
         "runs + promote challenger models to champion."),
    ]
    for i, (role, perms) in enumerate(roles):
        pdf.mrow([role, perms], rw, fill=(i % 2 == 1))
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 4.5, sanitize("Table 2: iNHCES user roles and permissions."))
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(2)

    pdf.h2("4.2 Row Level Security (RLS)")
    pdf.para(
        "Supabase Row Level Security policies are defined in "
        "`04_conceptual_models/04_rls_policies.sql` (O4 Step 2). "
        "Key policies:"
    )
    pdf.bullet([
        "projects: Users can SELECT/INSERT/UPDATE/DELETE only their own rows "
        "(WHERE user_id = auth.uid()).",
        "predictions: Users can SELECT only predictions linked to their own projects.",
        "macro_* and material_* tables: SELECT for all authenticated users; "
        "INSERT/UPDATE only for the service role (Airflow pipeline).",
        "reports: Users can SELECT only their own report records; "
        "service role for INSERT.",
        "ml_models: SELECT for all authenticated; INSERT/UPDATE for admin role only.",
        "audit_log: INSERT for all; SELECT for admin only.",
    ])

    pdf.h2("4.3 Data in Transit and at Rest")
    pdf.bullet([
        "All traffic between browser and Vercel/Railway is HTTPS (TLS 1.2+). "
        "Vercel and Railway enforce HTTPS by default.",
        "Supabase encrypts data at rest (AES-256) and in transit (TLS). "
        "Connection strings stored as Railway environment variables, never in code.",
        "Cloudflare R2 encrypts objects at rest. Presigned URLs expire in 24 hours.",
        "ANTHROPIC_API_KEY, EIA_API_KEY, FRED_API_KEY stored as Railway/Vercel "
        "environment variables. Never committed to Git. .env.example provided "
        "with placeholder values only.",
        "ML model artifacts in R2 are not publicly accessible — only readable "
        "via service-role presigned URLs from the FastAPI backend.",
    ])

    pdf.h2("4.4 API Rate Limiting and Abuse Prevention")
    pdf.bullet([
        "FastAPI rate limiting: 10 /estimate requests per user per minute "
        "(slowapi library). Prevents ML inference abuse.",
        "Supabase enforces its own rate limits on the PostgreSQL connection pool.",
        "Airflow scraper DAGs include polite crawl delays (2-5 seconds between "
        "requests) and respect robots.txt. Scrapers are for academic research "
        "use only.",
    ])


# ── Section 5: Integration and External APIs ───────────────────────────────────
def section5(pdf):
    pdf.add_page()
    pdf.h1("5. External Integration Points")

    ew = [38, 28, PAGE_W - 66]
    pdf.thead(["Data Source", "Access Method", "Notes"], ew)
    integrations = [
        ("World Bank Open Data",
         "HTTP API (wbgapi)\nNo key required",
         "GDP growth (NY.GDP.MKTP.KD.ZG), CPI inflation (FP.CPI.TOTL.ZG), "
         "lending rate (FR.INR.LEND). Annual data. fetch_worldbank.py already "
         "implemented (O2 Step 1). GREEN data."),
        ("EIA API (Brent crude)",
         "HTTP REST API\nEIA_API_KEY env var",
         "Europe Brent Spot Price (PET.RBRTE.A). Annual or monthly. "
         "fetch_eia_oil.py implemented with synthetic fallback (O2 Step 1). "
         "Upgrade to GREEN by setting EIA_API_KEY."),
        ("FRED API (CBN FX rates)",
         "fredapi Python client\nFRED_API_KEY env var",
         "NGN/USD (DEXNAUS), NGN/EUR via cross-rate (DEXUSEU), "
         "NGN/GBP via cross-rate (DEXUSGB). Annual. "
         "fetch_cbn_fx.py implemented with synthetic fallback. "
         "Upgrade to GREEN by setting FRED_API_KEY."),
        ("PropertyPro.ng\nPrivateProperty.com.ng",
         "Web scraper\n(requests + BeautifulSoup)",
         "Property listing prices (NGN/sqm) by zone. Weekly. "
         "nhces_weekly_property DAG. Respect ToS and robots.txt. "
         "IRB not required for publicly listed prices."),
        ("BusinessDay NG\nJiji.ng / BuildBay",
         "Web scraper\n(requests + BeautifulSoup)",
         "Cement prices (50kg bag by brand/region), iron rod prices "
         "(per tonne by diameter). Weekly. nhces_weekly_materials DAG."),
        ("NNPC / NMDPRA",
         "HTTP / scraper\nor manual CSV",
         "PMS (petrol) pump price by state. Monthly. "
         "nhces_monthly_macro DAG or manual upload if no API available."),
        ("NIQS Quarterly Schedule",
         "Manual CSV upload\nvia admin dashboard",
         "Unit rates by trade and building type. Quarterly. "
         "nhces_quarterly_niqs DAG processes uploaded file. "
         "Requires MoU with NIQS for regular data access."),
        ("Airflow REST API",
         "HTTP REST API\nairflow user/pass",
         "FastAPI /pipeline endpoint queries Airflow REST API for DAG "
         "run status. Internal Railway network call only."),
        ("MLflow Tracking Server",
         "mlflow Python client\nMLFLOW_TRACKING_URI env var",
         "FastAPI and Airflow DAGs log experiments to MLflow via the "
         "tracking URI. Model artifacts stored in Cloudflare R2 "
         "(configured as MLflow artifact store)."),
        ("Supabase Auth (GoTrue)",
         "Supabase Python client\nSUPABASE_URL + SERVICE_KEY",
         "JWT token verification on every FastAPI request. "
         "User management via Supabase dashboard or admin API."),
    ]
    for i, (src, method, notes) in enumerate(integrations):
        pdf.mrow([src, method, notes], ew, fill=(i % 2 == 1))
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 4.5, sanitize(
        "Table 3: iNHCES external integration points — data sources, access "
        "methods, and implementation notes."
    ))
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(2)


# ── Section 6: Environment Variables ──────────────────────────────────────────
def section6(pdf):
    pdf.add_page()
    pdf.h1("6. Environment Variables Reference")
    pdf.para(
        "All sensitive credentials are stored as environment variables, never "
        "committed to Git. The .env.example file (created in O6 Step 1) "
        "documents all required variables with placeholder values. "
        "The following table is the definitive reference."
    )
    vw = [48, 18, PAGE_W - 66]
    pdf.thead(["Variable Name", "Service", "Description"], vw)
    env_vars = [
        ("SUPABASE_URL",            "Supabase",    "Project URL from Supabase Settings -> API"),
        ("SUPABASE_ANON_KEY",       "Supabase",    "Public anon key for client-side requests"),
        ("SUPABASE_SERVICE_KEY",    "Supabase",    "Service role key for admin DB operations (Airflow, FastAPI backend)"),
        ("SUPABASE_JWT_SECRET",     "Supabase",    "JWT secret for token verification in FastAPI middleware"),
        ("CLOUDFLARE_R2_ENDPOINT",  "Cloudflare",  "R2 bucket endpoint URL (e.g. https://[account].r2.cloudflarestorage.com)"),
        ("CLOUDFLARE_R2_ACCESS_KEY","Cloudflare",  "R2 access key ID (from Cloudflare R2 API Tokens)"),
        ("CLOUDFLARE_R2_SECRET_KEY","Cloudflare",  "R2 secret access key"),
        ("CLOUDFLARE_R2_BUCKET",    "Cloudflare",  "R2 bucket name (e.g. nhces-storage)"),
        ("MLFLOW_TRACKING_URI",     "MLflow",      "http://[railway-mlflow-service]:5000"),
        ("AIRFLOW_API_URL",         "Airflow",     "http://[railway-airflow-service]:8080/api/v1"),
        ("AIRFLOW_USERNAME",        "Airflow",     "Airflow web UI username"),
        ("AIRFLOW_PASSWORD",        "Airflow",     "Airflow web UI password"),
        ("EIA_API_KEY",             "EIA",         "API key from eia.gov (optional — synthetic fallback if absent)"),
        ("FRED_API_KEY",            "FRED",        "API key from fred.stlouisfed.org (optional — synthetic fallback if absent)"),
        ("ANTHROPIC_API_KEY",       "Anthropic",   "Claude Code API key — development only, not deployed to Railway"),
        ("RAILWAY_ENVIRONMENT",     "Railway",     "Set to 'production' by Railway automatically on deploy"),
        ("SECRET_KEY",              "FastAPI",      "Random 32-byte hex string for session signing"),
    ]
    for i, (var, svc, desc) in enumerate(env_vars):
        pdf.mrow([var, svc, desc], vw, fill=(i % 2 == 1))
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 4.5, sanitize(
        "Table 4: iNHCES environment variables reference. "
        "Set all variables in Railway project settings (backend/Airflow/MLflow) "
        "and Vercel project settings (frontend). "
        "Never commit real values to Git."
    ))
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(2)


# ── Section 7: Deployment Architecture ────────────────────────────────────────
def section7(pdf):
    pdf.add_page()
    pdf.h1("7. Deployment Architecture")

    pdf.h2("7.1 Service Topology")
    pdf.para(
        "The iNHCES system runs as four separately deployed services. "
        "All four are configured to auto-deploy from the same GitHub repository "
        "via their respective CI/CD integrations."
    )
    dw = [30, 32, 28, PAGE_W - 90]
    pdf.thead(["Service", "Platform", "Tier / Cost", "Auto-Deploy Trigger"], dw)
    deployments = [
        ("nhces-frontend",   "Vercel",   "Free (Hobby)",   "Push to main -> Vercel GitHub integration"),
        ("nhces-backend",    "Railway",  "Starter $5/mo",  "Push to main -> .github/workflows/deploy.yml"),
        ("mlflow-server",    "Railway",  "Starter $5/mo",  "Manual deploy (stable — rarely changes)"),
        ("airflow-server",   "Railway",  "Starter $5/mo",  "Manual deploy (DAG files updated via Git sync)"),
    ]
    for i, row in enumerate(deployments):
        pdf.trow(list(row), dw, fill=(i % 2 == 1))
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GREY)
    pdf.set_x(LEFT)
    pdf.multi_cell(PAGE_W, 4.5, sanitize(
        "Table 5: iNHCES service deployment topology and estimated cost."
    ))
    pdf.set_text_color(*DARK_GREY)
    pdf.ln(2)

    pdf.h2("7.2 CI/CD Pipeline")
    pdf.para(
        "Two GitHub Actions workflows are defined in "
        "`.github/workflows/` (implemented in O6 Step 6):"
    )
    pdf.bullet([
        "test.yml: Triggered on every pull request to main. "
        "Runs pytest (nhces-backend/tests/) with a Supabase test database. "
        "PR cannot be merged if tests fail.",
        "deploy.yml: Triggered on push to main (after test.yml passes). "
        "Deploys nhces-backend to Railway using the Railway CLI action. "
        "Vercel auto-deploys nhces-frontend independently via its GitHub integration.",
    ])

    pdf.h2("7.3 Scalability Considerations")
    pdf.para(
        "The current architecture is sized for an academic prototype "
        "(estimated 10-50 concurrent users during research demonstrations). "
        "For production scale-out (post P7 publication), the following "
        "changes are recommended:"
    )
    pdf.bullet([
        "Backend: Add a Railway replica (horizontal scaling) or migrate to "
        "a Kubernetes deployment. FastAPI is stateless and scales horizontally.",
        "ML Inference: Move champion model to a dedicated inference service "
        "(Railway or Hugging Face Inference Endpoints) to decouple ML latency "
        "from the API response time budget.",
        "Database: Upgrade Supabase to Pro tier for connection pooling "
        "(PgBouncer) and higher storage limits as prediction log grows.",
        "Airflow: Migrate from Railway to a managed Airflow service "
        "(Astronomer, MWAA) if DAG count exceeds 20 or task concurrency "
        "causes Railway memory limits to be hit.",
    ])

    pdf.h2("7.4 Validation Required Before O6 Build")
    pdf.info_box(
        "DATA SOURCE: AMBER -- This architecture is AI-designed from O3 requirements "
        "and the iNHCES Research Advisory Framework. The research team must validate "
        "the following before O6 implementation begins:\n\n"
        "  1. Confirm Railway free/starter tier limits are sufficient for the "
        "prototype phase (CPU, RAM, sleep policy).\n"
        "  2. Confirm Supabase free tier row limits are sufficient for expected "
        "data volume (macro_fx has ~8,760 rows/year at hourly; ~365 at daily).\n"
        "  3. Confirm Cloudflare R2 free tier (10 GB storage, 1M requests/month) "
        "covers expected PDF report and model artifact volume.\n"
        "  4. Confirm NIQS is willing to provide quarterly unit rate data "
        "(MoU may be required).\n"
        "  5. Confirm PropertyPro and BusinessDay ToS permit academic web scraping.\n"
        "  6. Validate the Delphi consensus items (O3) are fully reflected in "
        "this architecture before proceeding to schema design (O4 Step 2)."
    )


# ── Mermaid Diagram Code Page ─────────────────────────────────────────────────
def mermaid_page(pdf):
    pdf.add_page()
    pdf.h1("Appendix A: Architecture Diagram (Mermaid Source)")
    pdf.para(
        "The following Mermaid diagram source defines the iNHCES system architecture. "
        "This is also saved as `04_conceptual_models/04_Architecture_Diagram.mmd`. "
        "To render: paste into mermaid.live OR install the Mermaid Preview extension "
        "in VS Code and open the .mmd file."
    )

    mmd_source = (
        "graph TD\n\n"
        "    subgraph USERS[\"USER LAYER\"]\n"
        "        U1[QS Professional]\n"
        "        U2[Researcher / PI]\n"
        "        U3[System Admin]\n"
        "    end\n\n"
        "    subgraph FRONTEND[\"PRESENTATION LAYER - Vercel CDN\"]\n"
        "        FE1[\"index.html - Cost Estimator\"]\n"
        "        FE2[\"dashboard.html - Pipeline Monitor\"]\n"
        "        FE3[\"app.js / styles.css\"]\n"
        "    end\n\n"
        "    subgraph BACKEND[\"API LAYER - FastAPI on Railway\"]\n"
        "        AUTH[JWT Auth Middleware]\n"
        "        API1[\"POST /estimate\"]\n"
        "        API2[\"GET /macro\"]\n"
        "        API3[\"CRUD /projects\"]\n"
        "        API4[\"POST /reports\"]\n"
        "        API5[\"GET /pipeline\"]\n"
        "        AUTH --> API1 & API2 & API3 & API4 & API5\n"
        "    end\n\n"
        "    subgraph MLAYER[\"ML LAYER - MLflow on Railway\"]\n"
        "        ML1[\"Champion: Stacking Ensemble\"]\n"
        "        ML2[Model Registry]\n"
        "        ML3[Experiment Tracker]\n"
        "        ML4[Challenger Models]\n"
        "    end\n\n"
        "    subgraph DATABASE[\"DATA LAYER - Supabase PostgreSQL\"]\n"
        "        DB1[(macro_fx/cpi/gdp/oil)]\n"
        "        DB2[(materials/unit_rates)]\n"
        "        DB3[(projects/predictions)]\n"
        "        DB4[(ml_models/users)]\n"
        "    end\n\n"
        "    subgraph STORAGE[\"STORAGE LAYER - Cloudflare R2\"]\n"
        "        S1[PDF Reports]\n"
        "        S2[Model Artifacts]\n"
        "        S3[Training Datasets]\n"
        "    end\n\n"
        "    subgraph PIPELINE[\"PIPELINE LAYER - Airflow on Railway\"]\n"
        "        P1[nhces_daily_fx_oil]\n"
        "        P2[nhces_weekly_materials]\n"
        "        P3[nhces_weekly_property]\n"
        "        P4[nhces_monthly_macro]\n"
        "        P7[nhces_retrain_weekly]\n"
        "        P8[nhces_drift_monitor]\n"
        "    end\n\n"
        "    subgraph EXTERNAL[\"EXTERNAL DATA SOURCES\"]\n"
        "        E1[World Bank API]\n"
        "        E2[EIA API]\n"
        "        E3[FRED/CBN API]\n"
        "        E4[PropertyPro Scraper]\n"
        "        E5[BusinessDay Scraper]\n"
        "        E7[NIQS Manual Upload]\n"
        "    end\n\n"
        "    USERS -->|HTTPS| FRONTEND\n"
        "    FRONTEND -->|REST API| BACKEND\n"
        "    API1 -->|predict| ML1\n"
        "    API1 & API2 & API3 & API4 & API5 -->|SQL| DATABASE\n"
        "    API4 -->|upload PDF| STORAGE\n"
        "    ML2 --> S2\n"
        "    ML3 --> S3\n"
        "    PIPELINE -->|INSERT| DATABASE\n"
        "    P7 & P8 -->|retrain| MLAYER\n"
        "    E1 -->|API| P4\n"
        "    E2 & E3 -->|API| P1\n"
        "    E4 & E5 -->|scraper| P2 & P3\n"
        "    E7 -->|CSV| P4\n"
    )
    pdf.code_box(mmd_source)


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    out = os.path.join(OUT_DIR, 'O4_01_System_Architecture.pdf')
    pdf = ArchPDF()

    make_cover(pdf)

    _ds_page(pdf, 'amber',
        "DATA SOURCE: AMBER -- AI-AUTHORED CONCEPTUAL DESIGN",
        (
            "WHAT IS REAL IN THIS DOCUMENT:\n"
            "  * Architecture layers and component choices are derived from the O3 "
            "Delphi consensus (36 items across 7 categories), the iNHCES Research "
            "Advisory Framework (Sections 7-8), and standard cloud-native MLOps "
            "design patterns. These are real design decisions.\n"
            "  * Technology stack choices (FastAPI, Supabase, MLflow, Airflow, "
            "Cloudflare R2, Vercel, Railway) are real platforms selected for "
            "the iNHCES research prototype.\n"
            "  * Environment variable names, API endpoint paths, and table names "
            "are real specifications that will be implemented in O6.\n\n"
            "WHAT IS AI-GENERATED / UNVALIDATED:\n"
            "  * Full narrative descriptions, design decision rationales, and "
            "integration notes were drafted by Claude Code. "
            "The research team must review and validate before O6 build begins.\n"
            "  * Hosting tier cost estimates are indicative. Verify current "
            "Railway / Supabase / Cloudflare R2 pricing before deployment.\n"
            "  * External data source access details (API keys, scraper legality, "
            "NIQS MoU) require real-world confirmation.\n\n"
            "REQUIRED BEFORE O6 BUILD:\n"
            "  1. Research team review and sign-off on all 7 architecture layers\n"
            "  2. Validate Delphi consensus items (O3) are fully reflected here\n"
            "  3. Confirm platform tier limits and costs\n"
            "  4. Obtain any required access agreements (NIQS, PropertyPro ToS)\n"
            "  5. Proceed to O4 Step 2: Database Schema (04_schema.sql)"
        )
    )

    section1(pdf)
    section2(pdf)
    section3(pdf)
    section4(pdf)
    section5(pdf)
    section6(pdf)
    section7(pdf)
    mermaid_page(pdf)

    pdf.output(out)
    print(f"[OK]  O4_01_System_Architecture.pdf  saved -> {out}")
    print(f"      Pages: {pdf.page}")
    print("      DATA SOURCE: AMBER")
    print("      Next: O4 Step 2 -- 04_schema.sql, 04_rls_policies.sql, 04_seed_data.sql")


if __name__ == "__main__":
    main()
